import spacy
import json
import re
from typing import List, Dict, Any, Optional
import logging

from .base import Entity, EntityType, Relation, EntityExtractor, RelationExtractor
from ..llm import LLMClient, get_prompt_template, create_messages


logger = logging.getLogger(__name__)


class SpacyEntityExtractor(EntityExtractor):
    """Entity extraction using spaCy NLP"""
    
    def __init__(self, model_name: str = "en_core_web_sm"):
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            logger.error(f"spaCy model {model_name} not found. Install with: python -m spacy download {model_name}")
            raise
        
        # Entity type mappings
        self.entity_type_mapping = {
            "PERSON": EntityType.PERSON,
            "ORG": EntityType.ORGANIZATION,
            "GPE": EntityType.LOCATION,  # Geopolitical entity
            "LOC": EntityType.LOCATION,
            "DATE": EntityType.DATE,
            "TIME": EntityType.DATE,
            "EVENT": EntityType.EVENT,
            "FAC": EntityType.LOCATION,  # Facility
            "MONEY": EntityType.OTHER,
            "PERCENT": EntityType.OTHER,
            "CARDINAL": EntityType.OTHER,
            "ORDINAL": EntityType.OTHER
        }
    
    def extract_entities(self, text: str, chunk_id: str) -> List[Entity]:
        """Extract entities using spaCy NER"""
        doc = self.nlp(text)
        entities = []
        
        for ent in doc.ents:
            # Map spaCy entity type to our EntityType
            entity_type = self.entity_type_mapping.get(ent.label_, EntityType.OTHER)
            
            # Create entity
            entity = Entity(
                id="",  # Will be auto-generated
                text=ent.text.strip(),
                type=entity_type,
                properties={
                    "spacy_label": ent.label_,
                    "start_char": ent.start_char,
                    "end_char": ent.end_char,
                    "lemma": ent.lemma_
                },
                source_chunk_id=chunk_id,
                confidence=1.0  # spaCy doesn't provide confidence scores by default
            )
            entities.append(entity)
        
        # Also extract noun phrases as potential concepts
        for noun_phrase in doc.noun_chunks:
            # Skip if already extracted as named entity
            if any(ent.start <= noun_phrase.start < ent.end for ent in doc.ents):
                continue
            
            # Filter out very short or common phrases
            if len(noun_phrase.text.strip()) < 3:
                continue
            
            # Check if it's a meaningful concept (contains no pronouns)
            if any(token.pos_ == "PRON" for token in noun_phrase):
                continue
            
            entity = Entity(
                id="",  # Will be auto-generated
                text=noun_phrase.text.strip(),
                type=EntityType.CONCEPT,
                properties={
                    "spacy_label": "CONCEPT",
                    "start_char": noun_phrase.start_char,
                    "end_char": noun_phrase.end_char,
                    "root": noun_phrase.root.text
                },
                source_chunk_id=chunk_id,
                confidence=0.7  # Lower confidence for concepts
            )
            entities.append(entity)
        
        return entities


class LLMEntityExtractor(EntityExtractor):
    """Entity extraction using LLM"""
    
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        self.entity_prompt = get_prompt_template("entity_extraction")
    
    def extract_entities(self, text: str, chunk_id: str) -> List[Entity]:
        """Extract entities using LLM"""
        
        # Create prompt
        prompt = self.entity_prompt.format(text=text)
        
        try:
            # Get LLM response
            response = self.llm_client.chat([
                {"role": "user", "content": prompt}
            ], temperature=0.1)
            
            # Parse JSON response
            entities_data = self._parse_llm_response(response)
            
            # Convert to Entity objects
            entities = []
            for entity_data in entities_data:
                entity_type = EntityType.OTHER
                try:
                    entity_type = EntityType(entity_data.get("label", "OTHER"))
                except ValueError:
                    # Map common variations
                    label = entity_data.get("label", "").upper()
                    if "PERSON" in label:
                        entity_type = EntityType.PERSON
                    elif "ORG" in label:
                        entity_type = EntityType.ORGANIZATION
                    elif "LOC" in label:
                        entity_type = EntityType.LOCATION
                    elif "CONCEPT" in label:
                        entity_type = EntityType.CONCEPT
                    elif "DATE" in label:
                        entity_type = EntityType.DATE
                
                entity = Entity(
                    id="",  # Will be auto-generated
                    text=entity_data.get("text", "").strip(),
                    type=entity_type,
                    properties={
                        "llm_label": entity_data.get("label", ""),
                        "start_pos": entity_data.get("start_pos", 0)
                    },
                    source_chunk_id=chunk_id,
                    confidence=0.8  # Default confidence for LLM extraction
                )
                
                if entity.text:  # Only add non-empty entities
                    entities.append(entity)
            
            return entities
            
        except Exception as e:
            logger.error(f"Error in LLM entity extraction: {e}")
            return []
    
    def _parse_llm_response(self, response: str) -> List[Dict[str, Any]]:
        """Parse LLM response to extract entities"""
        try:
            # Try to find JSON in the response
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            
            # Fallback: try to parse the entire response as JSON
            return json.loads(response)
            
        except json.JSONDecodeError:
            # Fallback: simple pattern matching
            logger.warning("Could not parse LLM response as JSON, using pattern matching")
            entities = []
            
            # Look for entity patterns in the response
            lines = response.split('\n')
            for line in lines:
                if ':' in line and any(keyword in line.upper() for keyword in ['PERSON', 'ORG', 'LOC', 'CONCEPT', 'DATE']):
                    try:
                        parts = line.split(':')
                        if len(parts) >= 2:
                            entity_text = parts[1].strip()
                            entity_type = parts[0].strip().upper()
                            
                            entities.append({
                                "text": entity_text,
                                "label": entity_type,
                                "start_pos": 0
                            })
                    except:
                        continue
            
            return entities


class SpacyRelationExtractor(RelationExtractor):
    """Simple relation extraction using spaCy dependency parsing"""
    
    def __init__(self, model_name: str = "en_core_web_sm"):
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            logger.error(f"spaCy model {model_name} not found. Install with: python -m spacy download {model_name}")
            raise
    
    def extract_relations(
        self, 
        text: str, 
        entities: List[Entity], 
        chunk_id: str
    ) -> List[Relation]:
        """Extract relations using dependency parsing"""
        doc = self.nlp(text)
        relations = []
        
        # Create entity lookup by text
        entity_lookup = {ent.text.lower(): ent for ent in entities}
        
        # Extract subject-verb-object patterns
        for token in doc:
            if token.pos_ == "VERB":
                # Find subject
                subject = None
                for child in token.children:
                    if child.dep_ in ["nsubj", "nsubjpass"]:
                        subject = child
                        break
                
                # Find object
                obj = None
                for child in token.children:
                    if child.dep_ in ["dobj", "pobj", "attr"]:
                        obj = child
                        break
                
                if subject and obj:
                    # Check if subject and object are entities
                    subject_text = subject.text.lower()
                    obj_text = obj.text.lower()
                    
                    subject_entity = entity_lookup.get(subject_text)
                    obj_entity = entity_lookup.get(obj_text)
                    
                    if subject_entity and obj_entity and subject_entity.id != obj_entity.id:
                        relation = Relation(
                            id="",  # Will be auto-generated
                            subject_id=subject_entity.id,
                            predicate=token.lemma_,
                            object_id=obj_entity.id,
                            properties={
                                "verb": token.text,
                                "dependency": token.dep_,
                                "pos": token.pos_
                            },
                            source_chunk_id=chunk_id,
                            confidence=0.6
                        )
                        relations.append(relation)
        
        return relations


class LLMRelationExtractor(RelationExtractor):
    """Relation extraction using LLM"""
    
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        self.relation_prompt = get_prompt_template("relation_extraction")
    
    def extract_relations(
        self, 
        text: str, 
        entities: List[Entity], 
        chunk_id: str
    ) -> List[Relation]:
        """Extract relations using LLM"""
        
        if len(entities) < 2:
            return []
        
        # Prepare entities for prompt
        entities_str = ", ".join([f"{ent.text} ({ent.type.value})" for ent in entities])
        
        # Create prompt
        prompt = self.relation_prompt.format(text=text, entities=entities_str)
        
        try:
            # Get LLM response
            response = self.llm_client.chat([
                {"role": "user", "content": prompt}
            ], temperature=0.1)
            
            # Parse JSON response
            relations_data = self._parse_llm_response(response)
            
            # Convert to Relation objects
            relations = []
            entity_lookup = {ent.text.lower(): ent for ent in entities}
            
            for relation_data in relations_data:
                subject_text = relation_data.get("subject", "").lower()
                object_text = relation_data.get("object", "").lower()
                predicate = relation_data.get("predicate", "")
                
                subject_entity = entity_lookup.get(subject_text)
                object_entity = entity_lookup.get(object_text)
                
                if subject_entity and object_entity and subject_entity.id != object_entity.id:
                    relation = Relation(
                        id="",  # Will be auto-generated
                        subject_id=subject_entity.id,
                        predicate=predicate,
                        object_id=object_entity.id,
                        properties={
                            "llm_extracted": True
                        },
                        source_chunk_id=chunk_id,
                        confidence=0.7
                    )
                    relations.append(relation)
            
            return relations
            
        except Exception as e:
            logger.error(f"Error in LLM relation extraction: {e}")
            return []
    
    def _parse_llm_response(self, response: str) -> List[Dict[str, Any]]:
        """Parse LLM response to extract relations"""
        try:
            # Try to find JSON in the response
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            
            # Fallback: try to parse the entire response as JSON
            return json.loads(response)
            
        except json.JSONDecodeError:
            logger.warning("Could not parse LLM response as JSON")
            return []