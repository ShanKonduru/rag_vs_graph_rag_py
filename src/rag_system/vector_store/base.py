from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from dataclasses import dataclass

from ..ingestion.models import DocumentChunk


@dataclass
class SearchResult:
    """Represents a search result from vector store"""
    chunk: DocumentChunk
    score: float
    distance: float


class VectorStore(ABC):
    """Abstract base class for vector stores"""
    
    @abstractmethod
    def add_chunks(self, chunks: List[DocumentChunk], embeddings: np.ndarray) -> None:
        """Add document chunks with their embeddings to the store"""
        pass
    
    @abstractmethod
    def search(
        self, 
        query_embedding: np.ndarray, 
        top_k: int = 5,
        score_threshold: Optional[float] = None
    ) -> List[SearchResult]:
        """Search for similar chunks"""
        pass
    
    @abstractmethod
    def get_chunk(self, chunk_id: str) -> Optional[DocumentChunk]:
        """Get a specific chunk by ID"""
        pass
    
    @abstractmethod
    def delete_chunk(self, chunk_id: str) -> bool:
        """Delete a chunk by ID"""
        pass
    
    @abstractmethod
    def get_all_chunks(self) -> List[DocumentChunk]:
        """Get all chunks in the store"""
        pass
    
    @abstractmethod
    def save(self, path: str) -> None:
        """Save the vector store to disk"""
        pass
    
    @abstractmethod
    def load(self, path: str) -> None:
        """Load the vector store from disk"""
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Clear all data from the store"""
        pass
    
    @abstractmethod
    def size(self) -> int:
        """Get the number of chunks in the store"""
        pass
    
    @abstractmethod
    def get_embedding_dimension(self) -> int:
        """Get the embedding dimension"""
        pass


class EmbeddingModel(ABC):
    """Abstract base class for embedding models"""
    
    @abstractmethod
    def encode(self, texts: List[str]) -> np.ndarray:
        """Encode texts into embeddings"""
        pass
    
    @abstractmethod
    def get_dimension(self) -> int:
        """Get embedding dimension"""
        pass
    
    @abstractmethod
    def get_max_sequence_length(self) -> int:
        """Get maximum sequence length"""
        pass