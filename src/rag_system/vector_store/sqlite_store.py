import sqlite3
import numpy as np
import json
import pickle
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import logging

from .base import VectorStore, SearchResult
from ..ingestion.models import DocumentChunk


logger = logging.getLogger(__name__)


class SQLiteVectorStore(VectorStore):
    """SQLite-based vector store implementation with basic vector search"""
    
    def __init__(self, db_path: str, dimension: int):
        self.db_path = Path(db_path)
        self.dimension = dimension
        
        # Create database and tables
        self._init_database()
    
    def _init_database(self) -> None:
        """Initialize SQLite database and tables"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS chunks (
                    id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    metadata TEXT NOT NULL,
                    document_id TEXT NOT NULL,
                    chunk_index INTEGER NOT NULL,
                    start_offset INTEGER NOT NULL,
                    end_offset INTEGER NOT NULL,
                    embedding BLOB NOT NULL
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_document_id ON chunks(document_id)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_chunk_index ON chunks(chunk_index)
            """)
            
            conn.commit()
    
    def add_chunks(self, chunks: List[DocumentChunk], embeddings: np.ndarray) -> None:
        """Add document chunks with their embeddings to the store"""
        if len(chunks) != embeddings.shape[0]:
            raise ValueError("Number of chunks must match number of embeddings")
        
        if embeddings.shape[1] != self.dimension:
            raise ValueError(f"Embedding dimension {embeddings.shape[1]} doesn't match expected dimension {self.dimension}")
        
        with sqlite3.connect(str(self.db_path)) as conn:
            for chunk, embedding in zip(chunks, embeddings):
                # Serialize metadata and embedding
                metadata_json = json.dumps(chunk.metadata)
                embedding_blob = pickle.dumps(embedding.astype(np.float32))
                
                conn.execute("""
                    INSERT OR REPLACE INTO chunks 
                    (id, content, metadata, document_id, chunk_index, start_offset, end_offset, embedding)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    chunk.id,
                    chunk.content,
                    metadata_json,
                    chunk.document_id,
                    chunk.chunk_index,
                    chunk.start_offset,
                    chunk.end_offset,
                    embedding_blob
                ))
            
            conn.commit()
        
        logger.info(f"Added {len(chunks)} chunks to SQLite vector store")
    
    def search(
        self, 
        query_embedding: np.ndarray, 
        top_k: int = 5,
        score_threshold: Optional[float] = None
    ) -> List[SearchResult]:
        """Search for similar chunks using cosine similarity"""
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
        
        query_norm = np.linalg.norm(query_embedding)
        if query_norm == 0:
            return []
        
        results = []
        
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.execute("SELECT * FROM chunks")
            
            for row in cursor:
                chunk_id, content, metadata_json, document_id, chunk_index, start_offset, end_offset, embedding_blob = row
                
                # Deserialize data
                metadata = json.loads(metadata_json)
                embedding = pickle.loads(embedding_blob)
                
                # Calculate cosine similarity
                embedding_norm = np.linalg.norm(embedding)
                if embedding_norm == 0:
                    continue
                
                cosine_sim = np.dot(query_embedding[0], embedding) / (query_norm * embedding_norm)
                
                # Apply score threshold
                if score_threshold is not None and cosine_sim < score_threshold:
                    continue
                
                # Create chunk object
                chunk = DocumentChunk(
                    id=chunk_id,
                    content=content,
                    metadata=metadata,
                    document_id=document_id,
                    chunk_index=chunk_index,
                    start_offset=start_offset,
                    end_offset=end_offset
                )
                
                results.append(SearchResult(
                    chunk=chunk,
                    score=float(cosine_sim),
                    distance=1.0 - float(cosine_sim)  # Convert similarity to distance
                ))
        
        # Sort by score (descending) and return top_k
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]
    
    def get_chunk(self, chunk_id: str) -> Optional[DocumentChunk]:
        """Get a specific chunk by ID"""
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.execute("SELECT * FROM chunks WHERE id = ?", (chunk_id,))
            row = cursor.fetchone()
            
            if row is None:
                return None
            
            chunk_id, content, metadata_json, document_id, chunk_index, start_offset, end_offset, embedding_blob = row
            metadata = json.loads(metadata_json)
            
            return DocumentChunk(
                id=chunk_id,
                content=content,
                metadata=metadata,
                document_id=document_id,
                chunk_index=chunk_index,
                start_offset=start_offset,
                end_offset=end_offset
            )
    
    def delete_chunk(self, chunk_id: str) -> bool:
        """Delete a chunk by ID"""
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.execute("DELETE FROM chunks WHERE id = ?", (chunk_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def get_all_chunks(self) -> List[DocumentChunk]:
        """Get all chunks in the store"""
        chunks = []
        
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.execute("SELECT * FROM chunks")
            
            for row in cursor:
                chunk_id, content, metadata_json, document_id, chunk_index, start_offset, end_offset, embedding_blob = row
                metadata = json.loads(metadata_json)
                
                chunk = DocumentChunk(
                    id=chunk_id,
                    content=content,
                    metadata=metadata,
                    document_id=document_id,
                    chunk_index=chunk_index,
                    start_offset=start_offset,
                    end_offset=end_offset
                )
                chunks.append(chunk)
        
        return chunks
    
    def save(self, path: str) -> None:
        """Save the vector store to a different location"""
        import shutil
        target_path = Path(path)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(self.db_path), str(target_path))
        logger.info(f"Saved SQLite vector store to {target_path}")
    
    def load(self, path: str) -> None:
        """Load the vector store from a different location"""
        source_path = Path(path)
        if not source_path.exists():
            raise FileNotFoundError(f"Vector store database not found: {source_path}")
        
        import shutil
        shutil.copy2(str(source_path), str(self.db_path))
        logger.info(f"Loaded SQLite vector store from {source_path}")
    
    def clear(self) -> None:
        """Clear all data from the store"""
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute("DELETE FROM chunks")
            conn.commit()
        logger.info("Cleared SQLite vector store")
    
    def size(self) -> int:
        """Get the number of chunks in the store"""
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM chunks")
            return cursor.fetchone()[0]
    
    def get_embedding_dimension(self) -> int:
        """Get the embedding dimension"""
        return self.dimension