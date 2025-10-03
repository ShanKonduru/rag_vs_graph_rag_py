#!/bin/bash
# =====================================================
#  RAG System - Full Pipeline Execution (Unix/Linux)
# =====================================================
#  This script runs the complete RAG vs Graph RAG pipeline
#  Usage: ./run_full_pipeline.sh
# =====================================================

set -e  # Exit on any error

echo ""
echo "========================================"
echo "  RAG vs Graph RAG - Full Pipeline"
echo "========================================"
echo ""

# Function to check command success
check_success() {
    if [ $? -eq 0 ]; then
        echo "SUCCESS: $1"
    else
        echo "ERROR: $1 failed!"
        exit 1
    fi
}

# Function to check optional command
check_optional() {
    if [ $? -eq 0 ]; then
        echo "SUCCESS: $1"
    else
        echo "WARNING: $1 failed (services may not be running)"
        echo "This is optional - continuing..."
    fi
}

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "ERROR: Python not found. Please activate virtual environment first."
    echo "Run: source venv/bin/activate"
    exit 1
fi

# Check if required packages are installed
python -c "import sentence_transformers" 2>/dev/null || {
    echo "ERROR: Required packages not installed. Please run setup first."
    echo "Run: pip install -r requirements.txt"
    exit 1
}

echo "[1/6] Document Ingestion..."
echo "====================================="
python main.py ingest -i data/documents -r
check_success "Documents ingested"
echo ""

echo "[2/6] Building Vector Store..."
echo "====================================="
python main.py build-vector-store -i data/documents --backend faiss
check_success "Vector store built"
echo ""

echo "[3/6] Building Knowledge Graph..."
echo "====================================="
python main.py build-knowledge-graph -i data/documents
check_optional "Knowledge graph building"
echo ""

echo "[4/6] Testing Standard RAG Query..."
echo "====================================="
python main.py query "What is artificial intelligence?" --method rag
check_success "RAG query"
echo ""

echo "[5/6] Testing Graph RAG Query..."
echo "====================================="
python main.py query "What are the types of machine learning?" --method graph_rag
check_optional "Graph RAG query"
echo ""

echo "[6/6] Running Evaluation Experiment..."
echo "====================================="
python main.py experiment --config configs/default.yaml --output experiments/results/
check_optional "Full experiment"
echo ""

echo "========================================"
echo "  Pipeline Complete!"
echo "========================================"
echo ""
echo "Results available in:"
echo "- data/chunks/           : Processed document chunks"
echo "- data/vector_store/     : FAISS vector database"
echo "- experiments/results/   : Evaluation results"
echo ""
echo "Next steps:"
echo "1. Start Docker services: docker-compose up -d"
echo "2. Re-run for full Graph RAG and KG functionality"
echo "3. Check README.md for detailed usage instructions"
echo ""