import click
import json
import csv
import time
from pathlib import Path
from typing import List, Dict, Any

from ..config import config_manager
from ..evaluation import Question, Answer, StandardEvaluator


@click.group()
def experiment():
    """Run experiments and evaluations"""
    pass


@experiment.command()
@click.option('--test-data', '-t', required=True, type=click.Path(exists=True), help='Test dataset file (JSON)')
@click.option('--methods', '-m', multiple=True, default=['rag', 'graph_rag', 'kg_only'], 
              help='Methods to test')
@click.option('--output-dir', '-o', default='./experiments/results', help='Output directory')
@click.option('--config', '-c', type=click.Path(exists=True), help='Configuration file')
@click.option('--runs', default=1, help='Number of runs per configuration')
@click.pass_context
def run_evaluation(ctx, test_data, methods, output_dir, config, runs):
    """Run evaluation experiment comparing different methods"""
    from ..vector_store import create_embedding_model, FAISSVectorStore, SQLiteVectorStore
    from ..knowledge_graph import KnowledgeGraphBuilder
    from ..retrieval import RAGRetriever, GraphRAGRetriever, KnowledgeGraphRetriever
    from ..llm import OllamaClient, RAG_SYSTEM_PROMPT, RAG_ANSWER_PROMPT, GRAPH_RAG_SYSTEM_PROMPT, GRAPH_RAG_ANSWER_PROMPT, KG_SYSTEM_PROMPT, KG_ANSWER_PROMPT, create_messages
    
    # Load configuration
    if config:
        system_config = config_manager.load_from_file(Path(config))
    else:
        system_config = config_manager.load_default()
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Load test data
    with open(test_data, 'r') as f:
        test_questions_data = json.load(f)
    
    questions = [
        Question(
            id=str(q.get('id', i)),
            question=q['question'],
            expected_answer=q['expected_answer'],
            context=q.get('context'),
            metadata=q.get('metadata', {})
        )
        for i, q in enumerate(test_questions_data)
    ]
    
    click.echo(f"Loaded {len(questions)} test questions")
    
    # Initialize evaluator
    evaluator = StandardEvaluator()
    
    # Setup common components
    llm_client = OllamaClient(
        base_url=system_config.ollama.base_url,
        model_name=system_config.ollama.model_name,
        timeout=system_config.ollama.timeout
    )
    
    if not llm_client.is_available():
        raise click.ClickException("Ollama server not available")
    
    # Setup vector store and knowledge graph if needed
    vector_store = None
    knowledge_graph = None
    embedding_model = None
    
    if any(method in ['rag', 'graph_rag'] for method in methods):
        # Load vector store
        embedding_model = create_embedding_model(
            model_name=system_config.embedding.model_name,
            device=system_config.embedding.device
        )
        
        store_path = system_config.vector_store.storage_path
        if not store_path.exists():
            raise click.ClickException(f"Vector store not found at {store_path}")
        
        if system_config.vector_store.backend == 'faiss':
            vector_store = FAISSVectorStore(
                dimension=embedding_model.get_dimension(),
                index_type=system_config.vector_store.index_type,
                distance_metric=system_config.vector_store.distance_metric
            )
        else:
            db_path = store_path / "vector_store.db"
            vector_store = SQLiteVectorStore(
                db_path=str(db_path),
                dimension=embedding_model.get_dimension()
            )
        
        vector_store.load(str(store_path))
    
    if any(method in ['graph_rag', 'kg_only'] for method in methods):
        # Create knowledge graph
        kg_builder = KnowledgeGraphBuilder(system_config)
        knowledge_graph = kg_builder.get_knowledge_graph()
    
    # Run experiments for each method
    all_results = []
    all_answers = []
    
    for method in methods:
        click.echo(f"\nRunning experiments for method: {method}")
        
        # Create retriever
        if method == 'rag':
            retriever = RAGRetriever(vector_store, embedding_model, system_config)
            system_prompt = RAG_SYSTEM_PROMPT.format()
            answer_template = RAG_ANSWER_PROMPT
        elif method == 'graph_rag':
            retriever = GraphRAGRetriever(vector_store, embedding_model, knowledge_graph, system_config)
            system_prompt = GRAPH_RAG_SYSTEM_PROMPT.format()
            answer_template = GRAPH_RAG_ANSWER_PROMPT
        else:  # kg_only
            retriever = KnowledgeGraphRetriever(knowledge_graph, system_config)
            system_prompt = KG_SYSTEM_PROMPT.format()
            answer_template = KG_ANSWER_PROMPT
        
        # Process each question
        method_answers = []
        for question in questions:
            for run in range(runs):
                start_time = time.time()
                
                # Retrieve context
                context = retriever.retrieve(
                    query=question.question,
                    top_k=system_config.retrieval.top_k
                )
                
                # Prepare prompt
                if method == 'rag':
                    prompt = answer_template.format(
                        context=context.get_combined_text(),
                        question=question.question
                    )
                elif method == 'graph_rag':
                    prompt = answer_template.format(
                        text_context=context.get_combined_text(),
                        graph_context=context.get_graph_summary(),
                        question=question.question
                    )
                else:  # kg_only
                    prompt = answer_template.format(
                        graph_data=context.get_graph_summary(),
                        question=question.question
                    )
                
                # Generate answer
                messages = create_messages(system_prompt, prompt)
                answer_text = llm_client.chat(
                    messages=messages,
                    temperature=system_config.ollama.temperature,
                    max_tokens=system_config.ollama.max_tokens
                )
                
                response_time = time.time() - start_time
                
                # Create answer object
                answer = Answer(
                    question_id=question.id,
                    answer=answer_text,
                    retrieval_context=context.get_combined_text() + "\n" + context.get_graph_summary(),
                    method=method,
                    response_time=response_time,
                    metadata={
                        'run': run,
                        'num_text_chunks': len(context.text_chunks),
                        'has_graph_data': context.graph_data is not None
                    }
                )
                
                method_answers.append(answer)
                all_answers.append(answer)
        
        # Evaluate method results
        method_results = evaluator.evaluate_batch(questions, method_answers)
        all_results.extend(method_results)
        
        click.echo(f"Completed {len(method_answers)} evaluations for {method}")
    
    # Generate summary
    comparison = evaluator.compare_methods(all_results)
    
    # Save results
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    
    # Save detailed results
    results_file = output_path / f"evaluation_results_{timestamp}.json"
    with open(results_file, 'w') as f:
        json.dump({
            'config': system_config.model_dump(),
            'questions': [q.__dict__ for q in questions],
            'answers': [a.__dict__ for a in all_answers],
            'results': [r.__dict__ for r in all_results],
            'comparison': comparison
        }, f, indent=2, default=str)
    
    # Save CSV summary
    csv_file = output_path / f"evaluation_summary_{timestamp}.csv"
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Method', 'Num Questions', 'Exact Match', 'F1 Score', 
            'ROUGE-L', 'BLEU Score', 'Retrieval Recall', 
            'Avg Response Time', 'Std Response Time'
        ])
        
        for method, summary in comparison['method_summaries'].items():
            writer.writerow([
                method,
                summary.num_questions,
                f"{summary.avg_exact_match:.4f}",
                f"{summary.avg_f1_score:.4f}",
                f"{summary.avg_rouge_l:.4f}",
                f"{summary.avg_bleu_score:.4f}",
                f"{summary.avg_retrieval_recall:.4f}",
                f"{summary.avg_response_time:.4f}",
                f"{summary.std_response_time:.4f}"
            ])
    
    # Display results
    click.echo("\n" + "="*60)
    click.echo("EVALUATION RESULTS")
    click.echo("="*60)
    
    for method, summary in comparison['method_summaries'].items():
        click.echo(f"\n{method.upper()}:")
        click.echo(f"  Questions: {summary.num_questions}")
        click.echo(f"  Exact Match: {summary.avg_exact_match:.4f}")
        click.echo(f"  F1 Score: {summary.avg_f1_score:.4f}")
        click.echo(f"  ROUGE-L: {summary.avg_rouge_l:.4f}")
        click.echo(f"  BLEU Score: {summary.avg_bleu_score:.4f}")
        click.echo(f"  Retrieval Recall: {summary.avg_retrieval_recall:.4f}")
        click.echo(f"  Avg Response Time: {summary.avg_response_time:.4f}s")
    
    click.echo(f"\nBest performing methods:")
    for metric, (best_method, best_score) in comparison['best_methods'].items():
        click.echo(f"  {metric}: {best_method} ({best_score:.4f})")
    
    click.echo(f"\nResults saved to:")
    click.echo(f"  Detailed: {results_file}")
    click.echo(f"  Summary: {csv_file}")
    
    # Close connections
    if knowledge_graph:
        kg_builder.close()


@experiment.command()
@click.option('--output-file', '-o', default='./data/sample_questions.json', help='Output file for sample questions')
@click.option('--num-questions', '-n', default=20, help='Number of questions to generate')
def generate_test_data(output_file, num_questions):
    """Generate sample test questions"""
    
    # Sample questions for testing the system
    sample_questions = [
        {
            "id": 1,
            "question": "What is artificial intelligence?",
            "expected_answer": "Artificial intelligence (AI) is a branch of computer science that aims to create machines and systems capable of performing tasks that typically require human intelligence, such as learning, reasoning, problem-solving, perception, and language understanding.",
            "metadata": {"topic": "AI basics"}
        },
        {
            "id": 2,
            "question": "How does machine learning work?",
            "expected_answer": "Machine learning is a subset of AI that enables computers to learn and improve from experience without being explicitly programmed. It works by using algorithms to identify patterns in data, build mathematical models based on training data, and make predictions or decisions on new data.",
            "metadata": {"topic": "Machine Learning"}
        },
        {
            "id": 3,
            "question": "What are the main types of machine learning?",
            "expected_answer": "The main types of machine learning are: 1) Supervised learning, where models learn from labeled training data; 2) Unsupervised learning, where models find patterns in unlabeled data; and 3) Reinforcement learning, where models learn through interaction with an environment and feedback.",
            "metadata": {"topic": "ML Types"}
        },
        {
            "id": 4,
            "question": "What is deep learning?",
            "expected_answer": "Deep learning is a subset of machine learning that uses artificial neural networks with multiple layers (deep networks) to model and understand complex patterns in data. It's particularly effective for tasks like image recognition, natural language processing, and speech recognition.",
            "metadata": {"topic": "Deep Learning"}
        },
        {
            "id": 5,
            "question": "What is natural language processing?",
            "expected_answer": "Natural Language Processing (NLP) is a field of AI that focuses on enabling computers to understand, interpret, and generate human language. It combines computational linguistics with machine learning to process and analyze large amounts of natural language data.",
            "metadata": {"topic": "NLP"}
        }
    ]
    
    # Extend with more questions if needed
    questions = sample_questions[:num_questions]
    
    # Create output directory
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save questions
    with open(output_path, 'w') as f:
        json.dump(questions, f, indent=2)
    
    click.echo(f"Generated {len(questions)} sample questions")
    click.echo(f"Saved to: {output_path}")


if __name__ == '__main__':
    experiment()