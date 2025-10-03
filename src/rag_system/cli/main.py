import click
import logging
from pathlib import Path

from ..config import config_manager, SystemConfig


# Setup logging
def setup_logging(log_level: str):
    """Setup logging configuration"""
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {log_level}')
    
    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


@click.group()
@click.option('--config', '-c', type=click.Path(exists=True), help='Configuration file path')
@click.option('--log-level', default='INFO', type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR']), help='Logging level')
@click.pass_context
def cli(ctx, config, log_level):
    """RAG vs Graph RAG vs Knowledge Graph Comparison System"""
    
    # Setup logging
    setup_logging(log_level)
    
    # Load configuration
    if config:
        system_config = config_manager.load_from_file(Path(config))
    else:
        system_config = config_manager.load_default()
    
    # Store in context
    ctx.ensure_object(dict)
    ctx.obj['config'] = system_config
    
    click.echo("RAG vs Graph RAG vs Knowledge Graph System")
    click.echo(f"Configuration loaded, log level: {log_level}")


@cli.command()
@click.option('--input-dir', '-i', required=True, type=click.Path(exists=True), help='Input directory with documents')
@click.option('--recursive', '-r', is_flag=True, help='Process directories recursively')
@click.option('--max-workers', default=4, help='Maximum number of worker threads')
@click.pass_context
def ingest(ctx, input_dir, recursive, max_workers):
    """Ingest documents and create chunks"""
    from ..ingestion import IngestionPipeline
    
    config = ctx.obj['config']
    
    try:
        # Create ingestion pipeline
        pipeline = IngestionPipeline(config)
        
        click.echo(f"Ingesting documents from: {input_dir}")
        click.echo(f"Recursive: {recursive}, Workers: {max_workers}")
        
        # Ingest documents
        chunks = pipeline.ingest_directory(
            directory_path=input_dir,
            recursive=recursive,
            max_workers=max_workers
        )
        
        click.echo(f"Successfully ingested {len(chunks)} chunks")
        
        # Save chunks metadata if needed
        output_dir = Path(config.data_dir) / "chunks"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        import json
        chunks_metadata = []
        for chunk in chunks:
            chunks_metadata.append({
                'id': chunk.id,
                'content_length': len(chunk.content),
                'document_id': chunk.document_id,
                'chunk_index': chunk.chunk_index,
                'source': chunk.metadata.get('source', ''),
                'file_type': chunk.metadata.get('file_type', '')
            })
        
        with open(output_dir / "chunks_metadata.json", 'w') as f:
            json.dump(chunks_metadata, f, indent=2)
        
        click.echo(f"Chunks metadata saved to: {output_dir / 'chunks_metadata.json'}")
        
    except Exception as e:
        click.echo(f"Error during ingestion: {e}", err=True)
        raise click.ClickException(str(e))


@cli.command()
@click.option('--input-dir', '-i', required=True, type=click.Path(exists=True), help='Input directory with documents')
@click.option('--recursive', '-r', is_flag=True, help='Process directories recursively')
@click.option('--backend', default='faiss', type=click.Choice(['faiss', 'sqlite']), help='Vector store backend')
@click.option('--rebuild', is_flag=True, help='Rebuild vector store from scratch')
@click.pass_context
def build_vector_store(ctx, input_dir, recursive, backend, rebuild):
    """Build vector store from documents"""
    from ..ingestion import IngestionPipeline
    from ..vector_store import create_embedding_model, FAISSVectorStore, SQLiteVectorStore
    
    config = ctx.obj['config']
    
    try:
        # Update vector store backend in config
        config.vector_store.backend = backend
        
        # Create ingestion pipeline
        pipeline = IngestionPipeline(config)
        
        # Create embedding model
        embedding_model = create_embedding_model(
            model_name=config.embedding.model_name,
            device=config.embedding.device,
            batch_size=config.embedding.batch_size
        )
        
        # Create vector store
        if backend == 'faiss':
            vector_store = FAISSVectorStore(
                dimension=embedding_model.get_dimension(),
                index_type=config.vector_store.index_type,
                distance_metric=config.vector_store.distance_metric
            )
        else:  # sqlite
            db_path = Path(config.vector_store.storage_path) / "vector_store.db"
            vector_store = SQLiteVectorStore(
                db_path=str(db_path),
                dimension=embedding_model.get_dimension()
            )
        
        click.echo(f"Building {backend} vector store from: {input_dir}")
        
        # Check if vector store exists and rebuild flag
        store_path = Path(config.vector_store.storage_path)
        if store_path.exists() and not rebuild:
            click.echo(f"Vector store exists at {store_path}. Use --rebuild to recreate.")
            return
        
        # Ingest documents
        chunks = pipeline.ingest_directory(
            directory_path=input_dir,
            recursive=recursive
        )
        
        if not chunks:
            click.echo("No chunks found to index")
            return
        
        click.echo(f"Creating embeddings for {len(chunks)} chunks...")
        
        # Create embeddings
        chunk_texts = [chunk.content for chunk in chunks]
        embeddings = embedding_model.encode(chunk_texts)
        
        # Add to vector store
        vector_store.add_chunks(chunks, embeddings)
        
        # Save vector store
        vector_store.save(str(store_path))
        
        click.echo(f"Vector store built successfully: {len(chunks)} chunks indexed")
        click.echo(f"Vector store saved to: {store_path}")
        
    except Exception as e:
        click.echo(f"Error building vector store: {e}", err=True)
        raise click.ClickException(str(e))


@cli.command()
@click.option('--input-dir', '-i', required=True, type=click.Path(exists=True), help='Input directory with documents')
@click.option('--recursive', '-r', is_flag=True, help='Process directories recursively')
@click.option('--use-llm', is_flag=True, help='Use LLM for entity/relation extraction')
@click.option('--rebuild', is_flag=True, help='Rebuild knowledge graph from scratch')
@click.pass_context
def build_knowledge_graph(ctx, input_dir, recursive, use_llm, rebuild):
    """Build knowledge graph from documents"""
    from ..ingestion import IngestionPipeline
    from ..knowledge_graph import KnowledgeGraphBuilder
    from ..llm import OllamaClient
    
    config = ctx.obj['config']
    
    try:
        # Create LLM client if needed
        llm_client = None
        if use_llm:
            llm_client = OllamaClient(
                base_url=config.ollama.base_url,
                model_name=config.ollama.model_name,
                timeout=config.ollama.timeout
            )
            
            if not llm_client.is_available():
                click.echo("Warning: Ollama server not available, falling back to spaCy", err=True)
                llm_client = None
        
        # Create knowledge graph builder
        kg_builder = KnowledgeGraphBuilder(config, llm_client)
        
        # Check if we should rebuild
        if rebuild:
            click.echo("Clearing existing knowledge graph...")
            kg_builder.clear_knowledge_graph()
        
        # Create ingestion pipeline
        pipeline = IngestionPipeline(config)
        
        click.echo(f"Building knowledge graph from: {input_dir}")
        click.echo(f"Using LLM extraction: {use_llm and llm_client is not None}")
        
        # Ingest documents
        chunks = pipeline.ingest_directory(
            directory_path=input_dir,
            recursive=recursive
        )
        
        if not chunks:
            click.echo("No chunks found to process")
            return
        
        # Build knowledge graph
        stats = kg_builder.build_from_chunks(chunks)
        
        click.echo("Knowledge graph built successfully!")
        click.echo(f"Total chunks processed: {stats['total_chunks']}")
        click.echo(f"Total entities extracted: {stats['total_entities']}")
        click.echo(f"Total relations extracted: {stats['total_relations']}")
        click.echo(f"Entity types: {stats['entity_types']}")
        
        # Close connections
        kg_builder.close()
        
    except Exception as e:
        click.echo(f"Error building knowledge graph: {e}", err=True)
        raise click.ClickException(str(e))


@cli.command()
@click.option('--query', '-q', required=True, help='Query to search for')
@click.option('--method', '-m', default='graph_rag', 
              type=click.Choice(['rag', 'graph_rag', 'kg_only']), 
              help='Retrieval method to use')
@click.option('--top-k', default=5, help='Number of results to retrieve')
@click.pass_context
def query(ctx, query, method, top_k):
    """Query the system using different methods"""
    from ..vector_store import create_embedding_model, FAISSVectorStore, SQLiteVectorStore
    from ..knowledge_graph import KnowledgeGraphBuilder
    from ..retrieval import RAGRetriever, GraphRAGRetriever, KnowledgeGraphRetriever
    from ..llm import OllamaClient, RAG_SYSTEM_PROMPT, RAG_ANSWER_PROMPT, GRAPH_RAG_SYSTEM_PROMPT, GRAPH_RAG_ANSWER_PROMPT, KG_SYSTEM_PROMPT, KG_ANSWER_PROMPT, create_messages
    import time
    
    config = ctx.obj['config']
    
    try:
        click.echo(f"Query: {query}")
        click.echo(f"Method: {method}")
        click.echo(f"Top-k: {top_k}")
        click.echo("-" * 50)
        
        start_time = time.time()
        
        # Create LLM client
        llm_client = OllamaClient(
            base_url=config.ollama.base_url,
            model_name=config.ollama.model_name,
            timeout=config.ollama.timeout
        )
        
        if not llm_client.is_available():
            raise click.ClickException("Ollama server not available")
        
        # Setup retriever based on method
        if method in ['rag', 'graph_rag']:
            # Load vector store
            embedding_model = create_embedding_model(
                model_name=config.embedding.model_name,
                device=config.embedding.device
            )
            
            store_path = Path(config.vector_store.storage_path)
            if not store_path.exists():
                raise click.ClickException(f"Vector store not found at {store_path}. Run 'build-vector-store' first.")
            
            if config.vector_store.backend == 'faiss':
                vector_store = FAISSVectorStore(
                    dimension=embedding_model.get_dimension(),
                    index_type=config.vector_store.index_type,
                    distance_metric=config.vector_store.distance_metric
                )
            else:
                db_path = store_path / "vector_store.db"
                vector_store = SQLiteVectorStore(
                    db_path=str(db_path),
                    dimension=embedding_model.get_dimension()
                )
            
            vector_store.load(str(store_path))
        
        if method in ['graph_rag', 'kg_only']:
            # Create knowledge graph builder to access the graph
            kg_builder = KnowledgeGraphBuilder(config)
            knowledge_graph = kg_builder.get_knowledge_graph()
        
        # Create appropriate retriever
        if method == 'rag':
            retriever = RAGRetriever(vector_store, embedding_model, config)
            system_prompt = RAG_SYSTEM_PROMPT.format()
            answer_template = RAG_ANSWER_PROMPT
        elif method == 'graph_rag':
            retriever = GraphRAGRetriever(vector_store, embedding_model, knowledge_graph, config)
            system_prompt = GRAPH_RAG_SYSTEM_PROMPT.format()
            answer_template = GRAPH_RAG_ANSWER_PROMPT
        else:  # kg_only
            retriever = KnowledgeGraphRetriever(knowledge_graph, config)
            system_prompt = KG_SYSTEM_PROMPT.format()
            answer_template = KG_ANSWER_PROMPT
        
        # Retrieve context
        retrieval_start = time.time()
        context = retriever.retrieve(query, top_k)
        retrieval_time = time.time() - retrieval_start
        
        click.echo(f"Retrieval completed in {retrieval_time:.2f}s")
        
        # Display retrieval results
        if context.text_chunks:
            click.echo(f"\nRetrieved {len(context.text_chunks)} text chunks:")
            for i, chunk in enumerate(context.text_chunks):
                score = context.vector_scores[i] if i < len(context.vector_scores) else 0.0
                click.echo(f"  {i+1}. Score: {score:.3f}, Length: {len(chunk.content)} chars")
                click.echo(f"     Preview: {chunk.content[:100]}...")
        
        if context.graph_data:
            click.echo(f"\nGraph data: {len(context.graph_data.nodes)} nodes, {len(context.graph_data.edges)} edges")
        
        # Prepare prompt
        if method == 'rag':
            prompt = answer_template.format(
                context=context.get_combined_text(),
                question=query
            )
        elif method == 'graph_rag':
            prompt = answer_template.format(
                text_context=context.get_combined_text(),
                graph_context=context.get_graph_summary(),
                question=query
            )
        else:  # kg_only
            prompt = answer_template.format(
                graph_data=context.get_graph_summary(),
                question=query
            )
        
        # Generate answer
        generation_start = time.time()
        messages = create_messages(system_prompt, prompt)
        answer = llm_client.chat(
            messages=messages,
            temperature=config.ollama.temperature,
            max_tokens=config.ollama.max_tokens
        )
        generation_time = time.time() - generation_start
        
        total_time = time.time() - start_time
        
        # Display results
        click.echo("\n" + "="*50)
        click.echo("ANSWER:")
        click.echo("="*50)
        click.echo(answer)
        click.echo("\n" + "="*50)
        click.echo("TIMING:")
        click.echo(f"Retrieval: {retrieval_time:.2f}s")
        click.echo(f"Generation: {generation_time:.2f}s")
        click.echo(f"Total: {total_time:.2f}s")
        
        # Close connections
        if method in ['graph_rag', 'kg_only']:
            kg_builder.close()
        
    except Exception as e:
        click.echo(f"Error during query: {e}", err=True)
        raise click.ClickException(str(e))


if __name__ == '__main__':
    cli()