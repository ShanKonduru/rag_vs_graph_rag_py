from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class EntityType(Enum):
    """Types of entities"""
    PERSON = "PERSON"
    ORGANIZATION = "ORG"
    LOCATION = "LOCATION"
    CONCEPT = "CONCEPT"
    DATE = "DATE"
    EVENT = "EVENT"
    OTHER = "OTHER"


@dataclass
class Entity:
    """Represents an entity in the knowledge graph"""
    id: str
    text: str
    type: EntityType
    properties: Dict[str, Any]
    source_chunk_id: str
    confidence: float = 1.0
    
    def __post_init__(self):
        if not self.id:
            import hashlib
            entity_data = f"{self.text}_{self.type.value}_{self.source_chunk_id}"
            self.id = hashlib.md5(entity_data.encode()).hexdigest()


@dataclass 
class Relation:
    """Represents a relationship between entities"""
    id: str
    subject_id: str
    predicate: str
    object_id: str
    properties: Dict[str, Any]
    source_chunk_id: str
    confidence: float = 1.0
    
    def __post_init__(self):
        if not self.id:
            import hashlib
            relation_data = f"{self.subject_id}_{self.predicate}_{self.object_id}_{self.source_chunk_id}"
            self.id = hashlib.md5(relation_data.encode()).hexdigest()


@dataclass
class GraphNode:
    """Represents a node in the knowledge graph"""
    id: str
    label: str
    properties: Dict[str, Any]
    entity_type: EntityType


@dataclass
class GraphEdge:
    """Represents an edge in the knowledge graph"""
    id: str
    source_id: str
    target_id: str
    relationship: str
    properties: Dict[str, Any]


@dataclass
class GraphPath:
    """Represents a path in the knowledge graph"""
    nodes: List[GraphNode]
    edges: List[GraphEdge]
    total_weight: float = 0.0


@dataclass
class GraphQueryResult:
    """Result of a graph query"""
    nodes: List[GraphNode]
    edges: List[GraphEdge]
    paths: List[GraphPath]
    metadata: Dict[str, Any]


class EntityExtractor(ABC):
    """Abstract base class for entity extraction"""
    
    @abstractmethod
    def extract_entities(self, text: str, chunk_id: str) -> List[Entity]:
        """Extract entities from text"""
        pass


class RelationExtractor(ABC):
    """Abstract base class for relation extraction"""
    
    @abstractmethod
    def extract_relations(
        self, 
        text: str, 
        entities: List[Entity], 
        chunk_id: str
    ) -> List[Relation]:
        """Extract relations between entities from text"""
        pass


class KnowledgeGraph(ABC):
    """Abstract base class for knowledge graph storage and querying"""
    
    @abstractmethod
    def add_entities(self, entities: List[Entity]) -> None:
        """Add entities to the knowledge graph"""
        pass
    
    @abstractmethod
    def add_relations(self, relations: List[Relation]) -> None:
        """Add relations to the knowledge graph"""
        pass
    
    @abstractmethod
    def get_entity(self, entity_id: str) -> Optional[Entity]:
        """Get an entity by ID"""
        pass
    
    @abstractmethod
    def get_entities_by_text(self, text: str) -> List[Entity]:
        """Get entities by their text representation"""
        pass
    
    @abstractmethod
    def get_relations_for_entity(self, entity_id: str) -> List[Relation]:
        """Get all relations involving an entity"""
        pass
    
    @abstractmethod
    def find_path(
        self, 
        start_entity_id: str, 
        end_entity_id: str, 
        max_depth: int = 3
    ) -> List[GraphPath]:
        """Find paths between two entities"""
        pass
    
    @abstractmethod
    def get_subgraph(
        self, 
        entity_ids: List[str], 
        depth: int = 1
    ) -> GraphQueryResult:
        """Get subgraph around specified entities"""
        pass
    
    @abstractmethod
    def query(self, query: str) -> GraphQueryResult:
        """Execute a query (e.g., Cypher for Neo4j)"""
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Clear all data from the knowledge graph"""
        pass
    
    @abstractmethod
    def get_statistics(self) -> Dict[str, Any]:
        """Get graph statistics"""
        pass