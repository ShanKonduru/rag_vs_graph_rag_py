#!/usr/bin/env python3
"""Build knowledge graph with correct config"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from rag_system.config import ConfigManager
from rag_system.knowledge_graph.builder import KnowledgeGraphBuilder
from rag_system.vector_store import FAISSVectorStore, create_embedding_model

def build_knowledge_graph():
    """Build knowledge graph using the correct config"""
    try:
        # Load config
        config_manager = ConfigManager()
        config_path = Path("configs/default.yaml")
        config = config_manager.load_from_file(config_path)
        
        print(f"Using Neo4j config: {config.neo4j.uri}, {config.neo4j.username}, database: {config.neo4j.database}")
        
        # Load existing vector store to get document chunks
        embedding_model = create_embedding_model(config.embedding.model_name)
        vector_store = FAISSVectorStore(
            dimension=embedding_model.get_dimension(),
            index_type=config.vector_store.index_type,
            distance_metric=config.vector_store.distance_metric,
        )
        
        # Load existing vector store
        vector_store_path = Path(config.vector_store.storage_path)
        if vector_store_path.exists():
            vector_store.load(str(vector_store_path))
            print(f"Loaded vector store with {len(vector_store.chunks)} chunks")
        else:
            print("No vector store found!")
            return
        
        # Build knowledge graph from the chunks
        builder = KnowledgeGraphBuilder(config)
        builder.build_from_chunks(vector_store.chunks)
        
        print("Knowledge graph built successfully!")
        
    except Exception as e:
        print(f"Error building knowledge graph: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    build_knowledge_graph()