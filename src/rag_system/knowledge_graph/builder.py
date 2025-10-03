import logging
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from ..config import SystemConfig
from ..ingestion.models import DocumentChunk
from ..llm import LLMClient
from .base import Entity, Relation, KnowledgeGraph
from .extractors import (
    SpacyEntityExtractor, LLMEntityExtractor,
    SpacyRelationExtractor, LLMRelationExtractor
)
from .neo4j_graph import Neo4jKnowledgeGraph


logger = logging.getLogger(__name__)


class KnowledgeGraphBuilder:
    """Main class for building knowledge graphs from document chunks"""
    
    def __init__(self, config: SystemConfig, llm_client: Optional[LLMClient] = None):
        self.config = config
        self.llm_client = llm_client
        
        # Initialize extractors
        self._init_extractors()
        
        # Initialize knowledge graph
        self.knowledge_graph = Neo4jKnowledgeGraph(
            uri=config.neo4j.uri,
            username=config.neo4j.username,
            password=config.neo4j.password,
            database=config.neo4j.database
        )
    
    def _init_extractors(self):
        """Initialize entity and relation extractors"""
        # Try to use spaCy extractors first, fallback to LLM if not available
        try:
            self.entity_extractor = SpacyEntityExtractor()
            self.relation_extractor = SpacyRelationExtractor()
            logger.info("Using spaCy extractors")
        except Exception as e:
            if self.llm_client:
                logger.warning(f"spaCy not available ({e}), using LLM extractors")
                self.entity_extractor = LLMEntityExtractor(self.llm_client)
                self.relation_extractor = LLMRelationExtractor(self.llm_client)
            else:
                logger.error("Neither spaCy nor LLM available for extraction")
                raise ValueError("No extraction method available")
    
    def build_from_chunks(
        self, 
        chunks: List[DocumentChunk], 
        max_workers: int = 4,
        batch_size: int = 10
    ) -> Dict[str, Any]:
        """Build knowledge graph from document chunks"""
        
        logger.info(f"Building knowledge graph from {len(chunks)} chunks")
        
        all_entities = []
        all_relations = []
        
        # Process chunks in batches
        for i in range(0, len(chunks), batch_size):
            batch_chunks = chunks[i:i + batch_size]
            
            # Extract entities and relations in parallel
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Submit entity extraction tasks
                entity_futures = {
                    executor.submit(self._extract_entities_from_chunk, chunk): chunk
                    for chunk in batch_chunks
                }
                
                # Collect entity results
                batch_entities = []
                for future in as_completed(entity_futures):
                    chunk = entity_futures[future]
                    try:
                        entities = future.result()
                        batch_entities.extend(entities)
                        logger.debug(f"Extracted {len(entities)} entities from chunk {chunk.id}")
                    except Exception as e:
                        logger.error(f"Error extracting entities from chunk {chunk.id}: {e}")
                
                # Add entities to graph
                if batch_entities:
                    self.knowledge_graph.add_entities(batch_entities)
                    all_entities.extend(batch_entities)
                
                # Submit relation extraction tasks
                relation_futures = {
                    executor.submit(self._extract_relations_from_chunk, chunk, batch_entities): chunk
                    for chunk in batch_chunks
                }
                
                # Collect relation results
                batch_relations = []
                for future in as_completed(relation_futures):
                    chunk = relation_futures[future]
                    try:
                        relations = future.result()
                        batch_relations.extend(relations)
                        logger.debug(f"Extracted {len(relations)} relations from chunk {chunk.id}")
                    except Exception as e:
                        logger.error(f"Error extracting relations from chunk {chunk.id}: {e}")
                
                # Add relations to graph
                if batch_relations:
                    self.knowledge_graph.add_relations(batch_relations)
                    all_relations.extend(batch_relations)
            
            logger.info(f"Processed batch {i//batch_size + 1}/{(len(chunks) + batch_size - 1)//batch_size}")
        
        # Build statistics
        stats = {
            "total_chunks": len(chunks),
            "total_entities": len(all_entities),
            "total_relations": len(all_relations),
            "entity_types": self._count_entity_types(all_entities),
            "graph_stats": self.knowledge_graph.get_statistics()
        }
        
        logger.info(f"Knowledge graph built: {stats}")
        return stats
    
    def _extract_entities_from_chunk(self, chunk: DocumentChunk) -> List[Entity]:
        """Extract entities from a single chunk"""
        try:
            return self.entity_extractor.extract_entities(chunk.content, chunk.id)
        except Exception as e:
            logger.error(f"Error extracting entities from chunk {chunk.id}: {e}")
            return []
    
    def _extract_relations_from_chunk(
        self, 
        chunk: DocumentChunk, 
        chunk_entities: List[Entity]
    ) -> List[Relation]:
        """Extract relations from a single chunk"""
        try:
            # Filter entities that belong to this chunk
            relevant_entities = [
                entity for entity in chunk_entities 
                if entity.source_chunk_id == chunk.id
            ]
            
            if len(relevant_entities) < 2:
                return []
            
            return self.relation_extractor.extract_relations(
                chunk.content, relevant_entities, chunk.id
            )
        except Exception as e:
            logger.error(f"Error extracting relations from chunk {chunk.id}: {e}")
            return []
    
    def _count_entity_types(self, entities: List[Entity]) -> Dict[str, int]:
        """Count entities by type"""
        type_counts = {}
        for entity in entities:
            entity_type = entity.type.value
            type_counts[entity_type] = type_counts.get(entity_type, 0) + 1
        return type_counts
    
    def get_knowledge_graph(self) -> KnowledgeGraph:
        """Get the knowledge graph instance"""
        return self.knowledge_graph
    
    def clear_knowledge_graph(self) -> None:
        """Clear the knowledge graph"""
        self.knowledge_graph.clear()
        logger.info("Knowledge graph cleared")
    
    def get_entities_for_text(self, text: str) -> List[Entity]:
        """Get entities related to a text query"""
        return self.knowledge_graph.get_entities_by_text(text)
    
    def get_subgraph_for_entities(
        self, 
        entity_ids: List[str], 
        depth: int = 1
    ) -> Dict[str, Any]:
        """Get subgraph around entities"""
        result = self.knowledge_graph.get_subgraph(entity_ids, depth)
        
        return {
            "nodes": [
                {
                    "id": node.id,
                    "label": node.label,
                    "type": node.entity_type.value,
                    "properties": node.properties
                }
                for node in result.nodes
            ],
            "edges": [
                {
                    "id": edge.id,
                    "source": edge.source_id,
                    "target": edge.target_id,
                    "relationship": edge.relationship,
                    "properties": edge.properties
                }
                for edge in result.edges
            ],
            "metadata": result.metadata
        }
    
    def close(self):
        """Close knowledge graph connection"""
        if hasattr(self.knowledge_graph, 'close'):
            self.knowledge_graph.close()