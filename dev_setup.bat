@echo off
REM =====================================================
REM  RAG System - Development Setup (Windows)
REM =====================================================
REM  Complete development environment setup
REM  Usage: dev_setup.bat
REM =====================================================

echo.
echo ========================================
echo  RAG System - Development Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8+ first.
    echo Download from: https://python.org/downloads/
    pause
    exit /b 1
)

echo [1/8] Creating virtual environment...
echo =====================================
if not exist .venv (
    python -m venv .venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)

echo [2/8] Activating virtual environment...
echo =====================================
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo [3/8] Upgrading pip...
echo =====================================
python -m pip install --upgrade pip

echo [4/8] Installing requirements...
echo =====================================
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install requirements
    pause
    exit /b 1
)

echo [5/8] Installing spaCy model...
echo =====================================
python -m spacy download en_core_web_sm
if errorlevel 1 (
    echo WARNING: Failed to install spaCy model
    echo This may affect entity extraction
)

echo [6/8] Creating directory structure...
echo =====================================
if not exist data\chunks mkdir data\chunks
if not exist data\vector_store mkdir data\vector_store
if not exist experiments\results mkdir experiments\results
if not exist logs mkdir logs

echo [7/8] Checking Docker installation...
echo =====================================
docker --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Docker not found. Neo4j and Ollama services will not be available.
    echo Install Docker Desktop from: https://docker.com/products/docker-desktop
) else (
    echo Docker found - services can be started with: docker-compose up -d
)

echo [8/8] Running initial setup test...
echo =====================================
python -c "import sentence_transformers; print('✓ sentence-transformers')"
python -c "import spacy; print('✓ spaCy')"
python -c "import faiss; print('✓ FAISS')"
python -c "from src.rag_system.config import ConfigManager; print('✓ Configuration system')"

echo.
echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Start Docker services (optional): docker-compose up -d
echo 2. Run full pipeline: run_full_pipeline.bat
echo 3. Or run individual tests: run_quick_tests.bat help
echo.
echo Virtual environment is now active.
echo To deactivate later, run: deactivate
echo.
pause