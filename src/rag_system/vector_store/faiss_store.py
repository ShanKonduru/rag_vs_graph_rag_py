import faiss
import numpy as np
import pickle
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import logging

from .base import VectorStore, SearchResult
from ..ingestion.models import DocumentChunk


logger = logging.getLogger(__name__)


class FAISSVectorStore(VectorStore):
    """FAISS-based vector store implementation"""
    
    def __init__(
        self, 
        dimension: int,
        index_type: str = "flat",
        distance_metric: str = "cosine"
    ):
        self.dimension = dimension
        self.index_type = index_type
        self.distance_metric = distance_metric
        
        # Create FAISS index
        self.index = self._create_index()
        
        # Store chunks metadata
        self.chunks: Dict[int, DocumentChunk] = {}
        self.id_to_index: Dict[str, int] = {}
        self.index_to_id: Dict[int, str] = {}
        self._next_index = 0
    
    def _create_index(self) -> faiss.Index:
        """Create FAISS index based on configuration"""
        if self.index_type.lower() == "flat":
            if self.distance_metric.lower() == "cosine":
                # Normalize vectors for cosine similarity
                index = faiss.IndexFlatIP(self.dimension)
            elif self.distance_metric.lower() == "l2":
                index = faiss.IndexFlatL2(self.dimension)
            else:
                raise ValueError(f"Unsupported distance metric: {self.distance_metric}")
        
        elif self.index_type.lower() == "hnsw":
            # HNSW index for approximate search
            if self.distance_metric.lower() == "cosine":
                index = faiss.IndexHNSWFlat(self.dimension, 32, faiss.METRIC_INNER_PRODUCT)
            elif self.distance_metric.lower() == "l2":
                index = faiss.IndexHNSWFlat(self.dimension, 32, faiss.METRIC_L2)
            else:
                raise ValueError(f"Unsupported distance metric: {self.distance_metric}")
        
        else:
            raise ValueError(f"Unsupported index type: {self.index_type}")
        
        return index
    
    def add_chunks(self, chunks: List[DocumentChunk], embeddings: np.ndarray) -> None:
        """Add document chunks with their embeddings to the store"""
        if len(chunks) != embeddings.shape[0]:
            raise ValueError("Number of chunks must match number of embeddings")
        
        if embeddings.shape[1] != self.dimension:
            raise ValueError(f"Embedding dimension {embeddings.shape[1]} doesn't match index dimension {self.dimension}")
        
        # Normalize embeddings for cosine similarity
        if self.distance_metric.lower() == "cosine":
            embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        
        # Add embeddings to index
        start_index = self._next_index
        self.index.add(embeddings.astype(np.float32))
        
        # Store chunk metadata
        for i, chunk in enumerate(chunks):
            idx = start_index + i
            self.chunks[idx] = chunk
            self.id_to_index[chunk.id] = idx
            self.index_to_id[idx] = chunk.id
        
        self._next_index += len(chunks)
        logger.info(f"Added {len(chunks)} chunks to FAISS index")
    
    def search(
        self, 
        query_embedding: np.ndarray, 
        top_k: int = 5,
        score_threshold: Optional[float] = None
    ) -> List[SearchResult]:
        """Search for similar chunks"""
        if self.index.ntotal == 0:
            return []
        
        # Ensure query embedding is 2D
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
        
        # Normalize for cosine similarity
        if self.distance_metric.lower() == "cosine":
            query_embedding = query_embedding / np.linalg.norm(query_embedding, axis=1, keepdims=True)
        
        # Search
        distances, indices = self.index.search(query_embedding.astype(np.float32), top_k)
        
        results = []
        for distance, idx in zip(distances[0], indices[0]):
            if idx == -1:  # No more results
                break
            
            chunk = self.chunks.get(idx)
            if chunk is None:
                continue
            
            # Convert distance to score
            if self.distance_metric.lower() == "cosine":
                score = float(distance)  # Inner product (higher is better)
            else:
                score = 1.0 / (1.0 + float(distance))  # Convert L2 distance to score
            
            # Apply score threshold
            if score_threshold is not None and score < score_threshold:
                continue
            
            results.append(SearchResult(
                chunk=chunk,
                score=score,
                distance=float(distance)
            ))
        
        return results
    
    def get_chunk(self, chunk_id: str) -> Optional[DocumentChunk]:
        """Get a specific chunk by ID"""
        idx = self.id_to_index.get(chunk_id)
        if idx is not None:
            return self.chunks.get(idx)
        return None
    
    def delete_chunk(self, chunk_id: str) -> bool:
        """Delete a chunk by ID (not supported in FAISS)"""
        logger.warning("Delete operation not supported in FAISS. Consider rebuilding the index.")
        return False
    
    def get_all_chunks(self) -> List[DocumentChunk]:
        """Get all chunks in the store"""
        return list(self.chunks.values())
    
    def save(self, path: str) -> None:
        """Save the vector store to disk"""
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        
        # Save FAISS index
        faiss.write_index(self.index, str(path / "index.faiss"))
        
        # Save metadata
        metadata = {
            "dimension": self.dimension,
            "index_type": self.index_type,
            "distance_metric": self.distance_metric,
            "_next_index": self._next_index,
            "id_to_index": self.id_to_index,
            "index_to_id": self.index_to_id
        }
        
        with open(path / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
        
        # Save chunks
        with open(path / "chunks.pkl", "wb") as f:
            pickle.dump(self.chunks, f)
        
        logger.info(f"Saved FAISS vector store to {path}")
    
    def load(self, path: str) -> None:
        """Load the vector store from disk"""
        path = Path(path)
        
        if not path.exists():
            raise FileNotFoundError(f"Vector store path not found: {path}")
        
        # Load FAISS index
        index_path = path / "index.faiss"
        if index_path.exists():
            self.index = faiss.read_index(str(index_path))
        else:
            raise FileNotFoundError(f"FAISS index not found: {index_path}")
        
        # Load metadata
        metadata_path = path / "metadata.json"
        if metadata_path.exists():
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
            
            self.dimension = metadata["dimension"]
            self.index_type = metadata["index_type"]
            self.distance_metric = metadata["distance_metric"]
            self._next_index = metadata["_next_index"]
            self.id_to_index = metadata["id_to_index"]
            self.index_to_id = {int(k): v for k, v in metadata["index_to_id"].items()}
        
        # Load chunks
        chunks_path = path / "chunks.pkl"
        if chunks_path.exists():
            with open(chunks_path, "rb") as f:
                self.chunks = pickle.load(f)
        
        logger.info(f"Loaded FAISS vector store from {path}")
    
    def clear(self) -> None:
        """Clear all data from the store"""
        self.index = self._create_index()
        self.chunks.clear()
        self.id_to_index.clear()
        self.index_to_id.clear()
        self._next_index = 0
        logger.info("Cleared FAISS vector store")
    
    def size(self) -> int:
        """Get the number of chunks in the store"""
        return self.index.ntotal
    
    def get_embedding_dimension(self) -> int:
        """Get the embedding dimension"""
        return self.dimension