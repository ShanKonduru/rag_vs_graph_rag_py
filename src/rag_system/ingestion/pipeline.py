import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from concurrent.futures import ThreadPoolExecutor, as_completed

from ..config import SystemConfig
from .models import Document, DocumentChunk, TextChunker
from .processors import ProcessorRegistry


logger = logging.getLogger(__name__)


class IngestionPipeline:
    """Main ingestion pipeline for processing documents"""
    
    def __init__(self, config: SystemConfig):
        self.config = config
        self.processor_registry = ProcessorRegistry()
        self.chunker = TextChunker(
            chunk_size=config.ingestion.chunk_size,
            chunk_overlap=config.ingestion.chunk_overlap,
            min_chunk_length=config.ingestion.min_chunk_length
        )
    
    def ingest_file(self, file_path: Union[str, Path]) -> List[DocumentChunk]:
        """Ingest a single file and return chunks"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not file_path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")
        
        # Check if file format is supported
        if file_path.suffix.lower().replace('.', '') not in self.config.ingestion.supported_formats:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
        
        try:
            logger.info(f"Processing file: {file_path}")
            
            # Get appropriate processor
            processor = self.processor_registry.get_processor(file_path)
            
            # Process document
            document = processor.process(file_path)
            
            # Chunk document
            chunks = self.chunker.chunk_document(document)
            
            logger.info(f"Processed {file_path.name}: {len(chunks)} chunks created")
            return chunks
            
        except Exception as e:
            logger.error(f"Error ingesting file {file_path}: {e}")
            raise
    
    def ingest_directory(
        self, 
        directory_path: Union[str, Path], 
        recursive: bool = True,
        max_workers: int = 4
    ) -> List[DocumentChunk]:
        """Ingest all supported files in a directory"""
        directory_path = Path(directory_path)
        
        if not directory_path.exists():
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        
        if not directory_path.is_dir():
            raise ValueError(f"Path is not a directory: {directory_path}")
        
        # Find all supported files
        files_to_process = self._find_supported_files(directory_path, recursive)
        
        if not files_to_process:
            logger.warning(f"No supported files found in {directory_path}")
            return []
        
        logger.info(f"Found {len(files_to_process)} files to process in {directory_path}")
        
        all_chunks = []
        
        # Process files in parallel
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all files for processing
            future_to_file = {
                executor.submit(self.ingest_file, file_path): file_path 
                for file_path in files_to_process
            }
            
            # Collect results
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    chunks = future.result()
                    all_chunks.extend(chunks)
                except Exception as e:
                    logger.error(f"Error processing {file_path}: {e}")
        
        logger.info(f"Processed {len(files_to_process)} files, created {len(all_chunks)} chunks")
        return all_chunks
    
    def ingest_multiple_files(
        self, 
        file_paths: List[Union[str, Path]], 
        max_workers: int = 4
    ) -> List[DocumentChunk]:
        """Ingest multiple specific files"""
        all_chunks = []
        
        # Process files in parallel
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all files for processing
            future_to_file = {
                executor.submit(self.ingest_file, file_path): file_path 
                for file_path in file_paths
            }
            
            # Collect results
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    chunks = future.result()
                    all_chunks.extend(chunks)
                except Exception as e:
                    logger.error(f"Error processing {file_path}: {e}")
        
        logger.info(f"Processed {len(file_paths)} files, created {len(all_chunks)} chunks")
        return all_chunks
    
    def _find_supported_files(self, directory_path: Path, recursive: bool) -> List[Path]:
        """Find all supported files in directory"""
        supported_extensions = {f".{fmt}" for fmt in self.config.ingestion.supported_formats}
        files = []
        
        if recursive:
            for file_path in directory_path.rglob("*"):
                if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                    files.append(file_path)
        else:
            for file_path in directory_path.iterdir():
                if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                    files.append(file_path)
        
        return files
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported file formats"""
        return self.config.ingestion.supported_formats
    
    def update_chunker_config(
        self, 
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None,
        min_chunk_length: Optional[int] = None
    ) -> None:
        """Update chunker configuration"""
        if chunk_size is not None:
            self.config.ingestion.chunk_size = chunk_size
        if chunk_overlap is not None:
            self.config.ingestion.chunk_overlap = chunk_overlap
        if min_chunk_length is not None:
            self.config.ingestion.min_chunk_length = min_chunk_length
        
        # Recreate chunker with new configuration
        self.chunker = TextChunker(
            chunk_size=self.config.ingestion.chunk_size,
            chunk_overlap=self.config.ingestion.chunk_overlap,
            min_chunk_length=self.config.ingestion.min_chunk_length
        )