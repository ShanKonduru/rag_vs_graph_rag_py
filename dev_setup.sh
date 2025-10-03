#!/bin/bash
# =====================================================
#  RAG System - Development Setup (Unix/Linux)
# =====================================================
#  Complete development environment setup
#  Usage: ./dev_setup.sh
# =====================================================

set -e

echo ""
echo "========================================"
echo "  RAG System - Development Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 not found. Please install Python 3.8+ first."
    exit 1
fi

echo "[1/8] Creating virtual environment..."
echo "====================================="
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created"
else
    echo "Virtual environment already exists"
fi

echo "[2/8] Activating virtual environment..."
echo "====================================="
source venv/bin/activate

echo "[3/8] Upgrading pip..."
echo "====================================="
python -m pip install --upgrade pip

echo "[4/8] Installing requirements..."
echo "====================================="
pip install -r requirements.txt

echo "[5/8] Installing spaCy model..."
echo "====================================="
python -m spacy download en_core_web_sm || {
    echo "WARNING: Failed to install spaCy model"
    echo "This may affect entity extraction"
}

echo "[6/8] Creating directory structure..."
echo "====================================="
mkdir -p data/chunks
mkdir -p data/vector_store
mkdir -p experiments/results
mkdir -p logs

echo "[7/8] Checking Docker installation..."
echo "====================================="
if command -v docker &> /dev/null; then
    echo "Docker found - services can be started with: docker-compose up -d"
else
    echo "WARNING: Docker not found. Neo4j and Ollama services will not be available."
    echo "Install Docker from: https://docker.com/products/docker-desktop"
fi

echo "[8/8] Running initial setup test..."
echo "====================================="
python -c "import sentence_transformers; print('✓ sentence-transformers')"
python -c "import spacy; print('✓ spaCy')"
python -c "import faiss; print('✓ FAISS')"
python -c "from src.rag_system.config import ConfigManager; print('✓ Configuration system')"

echo ""
echo "========================================"
echo "  Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Start Docker services (optional): docker-compose up -d"
echo "2. Run full pipeline: ./run_full_pipeline.sh"
echo "3. Or run individual tests: ./run_quick_tests.sh help"
echo ""
echo "Virtual environment is now active."
echo "To deactivate later, run: deactivate"
echo ""