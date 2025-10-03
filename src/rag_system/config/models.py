from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from pathlib import Path


class EmbeddingConfig(BaseModel):
    """Configuration for embedding models"""
    model_name: str = Field(default="all-MiniLM-L6-v2", description="Embedding model name")
    max_seq_length: int = Field(default=512, description="Maximum sequence length")
    device: str = Field(default="cpu", description="Device to run embedding model")
    batch_size: int = Field(default=32, description="Batch size for embedding")


class VectorStoreConfig(BaseModel):
    """Configuration for vector store"""
    backend: str = Field(default="faiss", description="Vector store backend (faiss, sqlite)")
    index_type: str = Field(default="flat", description="Index type (flat, hnsw)")
    distance_metric: str = Field(default="cosine", description="Distance metric")
    dimension: int = Field(default=384, description="Embedding dimension")
    storage_path: Path = Field(default="./data/vector_store", description="Storage path")


class Neo4jConfig(BaseModel):
    """Configuration for Neo4j database"""
    uri: str = Field(default="bolt://localhost:7687", description="Neo4j URI")
    username: str = Field(default="neo4j", description="Neo4j username")
    password: str = Field(default="password", description="Neo4j password")
    database: str = Field(default="neo4j", description="Neo4j database name")


class OllamaConfig(BaseModel):
    """Configuration for Ollama LLM"""
    base_url: str = Field(default="http://localhost:11434", description="Ollama base URL")
    model_name: str = Field(default="llama2", description="Ollama model name")
    temperature: float = Field(default=0.7, description="Generation temperature")
    max_tokens: int = Field(default=512, description="Maximum tokens to generate")
    timeout: int = Field(default=60, description="Request timeout in seconds")


class IngestionConfig(BaseModel):
    """Configuration for document ingestion"""
    chunk_size: int = Field(default=512, description="Text chunk size")
    chunk_overlap: int = Field(default=50, description="Chunk overlap")
    supported_formats: List[str] = Field(
        default=["pdf", "txt", "html", "md", "docx"], 
        description="Supported file formats"
    )
    min_chunk_length: int = Field(default=50, description="Minimum chunk length")


class RetrievalConfig(BaseModel):
    """Configuration for retrieval methods"""
    top_k: int = Field(default=5, description="Number of top documents to retrieve")
    similarity_threshold: float = Field(default=0.7, description="Similarity threshold")
    graph_traversal_depth: int = Field(default=2, description="Graph traversal depth for Graph RAG")
    max_graph_nodes: int = Field(default=20, description="Maximum nodes to retrieve from graph")


class EvaluationConfig(BaseModel):
    """Configuration for evaluation"""
    metrics: List[str] = Field(
        default=["exact_match", "f1", "rouge_l", "bleu"], 
        description="Evaluation metrics"
    )
    test_dataset_path: Optional[Path] = Field(default=None, description="Test dataset path")
    output_dir: Path = Field(default="./experiments/results", description="Results output directory")


class ExperimentConfig(BaseModel):
    """Configuration for experiments"""
    name: str = Field(default="default_experiment", description="Experiment name")
    methods: List[str] = Field(
        default=["rag", "graph_rag", "kg_only"], 
        description="Methods to compare"
    )
    grid_search_params: Dict[str, List[Any]] = Field(
        default_factory=dict, 
        description="Parameters for grid search"
    )
    num_runs: int = Field(default=1, description="Number of runs per configuration")
    save_intermediate: bool = Field(default=True, description="Save intermediate results")


class SystemConfig(BaseModel):
    """Main system configuration"""
    embedding: EmbeddingConfig = Field(default_factory=EmbeddingConfig)
    vector_store: VectorStoreConfig = Field(default_factory=VectorStoreConfig)
    neo4j: Neo4jConfig = Field(default_factory=Neo4jConfig)
    ollama: OllamaConfig = Field(default_factory=OllamaConfig)
    ingestion: IngestionConfig = Field(default_factory=IngestionConfig)
    retrieval: RetrievalConfig = Field(default_factory=RetrievalConfig)
    evaluation: EvaluationConfig = Field(default_factory=EvaluationConfig)
    experiment: ExperimentConfig = Field(default_factory=ExperimentConfig)
    
    # Global settings
    log_level: str = Field(default="INFO", description="Logging level")
    random_seed: int = Field(default=42, description="Random seed for reproducibility")
    data_dir: Path = Field(default="./data", description="Data directory")
    output_dir: Path = Field(default="./experiments", description="Output directory")