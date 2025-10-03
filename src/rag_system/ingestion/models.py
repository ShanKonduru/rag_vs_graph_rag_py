from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path
import hashlib


@dataclass
class Document:
    """Represents a processed document"""
    id: str
    content: str
    metadata: Dict[str, Any]
    source: str
    
    def __post_init__(self):
        if not self.id:
            # Generate ID from content hash if not provided
            self.id = hashlib.md5(self.content.encode()).hexdigest()


@dataclass
class DocumentChunk:
    """Represents a chunk of a document"""
    id: str
    content: str
    metadata: Dict[str, Any]
    document_id: str
    chunk_index: int
    start_offset: int
    end_offset: int
    
    def __post_init__(self):
        if not self.id:
            # Generate chunk ID from document ID and chunk index
            chunk_data = f"{self.document_id}_{self.chunk_index}_{self.start_offset}_{self.end_offset}"
            self.id = hashlib.md5(chunk_data.encode()).hexdigest()


class DocumentProcessor:
    """Base class for document processors"""
    
    def can_process(self, file_path: Path) -> bool:
        """Check if this processor can handle the given file"""
        raise NotImplementedError
    
    def process(self, file_path: Path) -> Document:
        """Process a file and return a Document"""
        raise NotImplementedError


class TextChunker:
    """Text chunking utility"""
    
    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50, min_chunk_length: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_length = min_chunk_length
    
    def chunk_text(self, text: str, document_id: str, metadata: Optional[Dict[str, Any]] = None) -> List[DocumentChunk]:
        """Split text into overlapping chunks"""
        if metadata is None:
            metadata = {}
        
        chunks = []
        start = 0
        chunk_index = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            # If this is not the last chunk, try to break at word boundary
            if end < len(text):
                # Look for the last space within the last 50 characters
                last_space = text.rfind(' ', end - 50, end)
                if last_space > start:
                    end = last_space
            
            chunk_text = text[start:end].strip()
            
            # Skip chunks that are too short
            if len(chunk_text) >= self.min_chunk_length:
                chunk_metadata = {
                    **metadata,
                    "chunk_index": chunk_index,
                    "start_offset": start,
                    "end_offset": end,
                    "chunk_length": len(chunk_text)
                }
                
                chunk = DocumentChunk(
                    id="",  # Will be auto-generated
                    content=chunk_text,
                    metadata=chunk_metadata,
                    document_id=document_id,
                    chunk_index=chunk_index,
                    start_offset=start,
                    end_offset=end
                )
                chunks.append(chunk)
                chunk_index += 1
            
            # Move start position with overlap
            start = end - self.chunk_overlap
            
            # Ensure we don't go backwards
            if start <= 0:
                start = end
            
            # Break if we're not making progress
            if start >= len(text):
                break
        
        return chunks
    
    def chunk_document(self, document: Document) -> List[DocumentChunk]:
        """Chunk a document into smaller pieces"""
        return self.chunk_text(
            text=document.content,
            document_id=document.id,
            metadata={
                **document.metadata,
                "source": document.source
            }
        )