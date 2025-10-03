from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass

from ..ingestion.models import DocumentChunk
from ..vector_store.base import SearchResult
from ..knowledge_graph.base import GraphQueryResult


@dataclass
class RetrievalContext:
    """Context information from retrieval"""
    text_chunks: List[DocumentChunk]
    vector_scores: List[float]
    graph_data: Optional[GraphQueryResult] = None
    metadata: Dict[str, Any] = None
    
    def get_combined_text(self) -> str:
        """Get all text chunks combined"""
        return "\n\n".join([chunk.content for chunk in self.text_chunks])
    
    def get_graph_summary(self) -> str:
        """Get a summary of graph information"""
        if not self.graph_data:
            return ""
        
        summaries = []
        
        # Add node information
        if self.graph_data.nodes:
            node_info = []
            for node in self.graph_data.nodes:
                node_info.append(f"- {node.label} ({node.entity_type.value})")
            summaries.append("Entities: " + "; ".join(node_info))
        
        # Add relationship information
        if self.graph_data.edges:
            rel_info = []
            for edge in self.graph_data.edges:
                source_label = next((n.label for n in self.graph_data.nodes if n.id == edge.source_id), edge.source_id)
                target_label = next((n.label for n in self.graph_data.nodes if n.id == edge.target_id), edge.target_id)
                rel_info.append(f"{source_label} {edge.relationship} {target_label}")
            summaries.append("Relationships: " + "; ".join(rel_info))
        
        return "\n".join(summaries)


class Retriever(ABC):
    """Abstract base class for retrievers"""
    
    @abstractmethod
    def retrieve(self, query: str, top_k: int = 5) -> RetrievalContext:
        """Retrieve relevant information for a query"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get retriever name"""
        pass