#!/bin/bash
# =====================================================
#  RAG System - Quick Test Commands (Unix/Linux)
# =====================================================
#  This script runs individual test commands
#  Usage: ./run_quick_tests.sh [command]
# =====================================================

show_help() {
    echo "Available commands:"
    echo "  ./run_quick_tests.sh ingest       - Ingest documents only"
    echo "  ./run_quick_tests.sh vector       - Build vector store only"
    echo "  ./run_quick_tests.sh graph        - Build knowledge graph only"
    echo "  ./run_quick_tests.sh query        - Run sample queries"
    echo "  ./run_quick_tests.sh experiment   - Run evaluation experiment"
    echo "  ./run_quick_tests.sh docker       - Start Docker services"
    echo "  ./run_quick_tests.sh all          - Run all tests"
}

echo ""
echo "========================================"
echo "  RAG System - Quick Tests"
echo "========================================"
echo ""

case "$1" in
    "help")
        show_help
        ;;
    "ingest")
        echo "Running document ingestion..."
        python main.py ingest -i data/documents -r
        ;;
    "vector")
        echo "Building vector store..."
        python main.py build-vector-store -i data/documents --backend faiss
        ;;
    "graph")
        echo "Building knowledge graph..."
        python main.py build-knowledge-graph -i data/documents
        ;;
    "query")
        echo "Testing RAG queries..."
        echo ""
        echo "Query 1: What is artificial intelligence?"
        python main.py query "What is artificial intelligence?" --method rag
        echo ""
        echo "Query 2: What are the types of machine learning?"
        python main.py query "What are the types of machine learning?" --method rag
        echo ""
        echo "Query 3: What is generative AI?"
        python main.py query "What is generative AI?" --method rag
        ;;
    "experiment")
        echo "Running evaluation experiment..."
        python main.py experiment --config configs/default.yaml --output experiments/results/
        ;;
    "docker")
        echo "Starting Docker services..."
        cd docker
        docker-compose up -d
        cd ..
        echo "Docker services started. Check with: docker ps"
        ;;
    "all")
        echo "Running all tests..."
        ./run_quick_tests.sh ingest
        ./run_quick_tests.sh vector
        ./run_quick_tests.sh graph
        ./run_quick_tests.sh query
        ./run_quick_tests.sh experiment
        ;;
    *)
        echo "Usage: ./run_quick_tests.sh [command]"
        echo "Run './run_quick_tests.sh help' for available commands"
        echo ""
        echo "Quick commands:"
        echo "  ingest    - Process documents"
        echo "  vector    - Build vector store"
        echo "  query     - Test sample queries"
        echo "  all       - Run complete pipeline"
        ;;
esac