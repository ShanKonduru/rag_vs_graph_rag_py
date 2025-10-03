@echo off
REM =====================================================
REM  RAG System - Full Pipeline Execution (Windows)
REM =====================================================
REM  This script runs the complete RAG vs Graph RAG pipeline
REM  Usage: run_full_pipeline.bat
REM =====================================================

echo.
echo ========================================
echo  RAG vs Graph RAG - Full Pipeline
echo ========================================
echo.

REM Check if virtual environment is activated
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please activate virtual environment first.
    echo Run: 002_activate.bat
    pause
    exit /b 1
)

REM Check if required packages are installed
python -c "import sentence_transformers" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Required packages not installed. Please run setup first.
    echo Run: 003_setup.bat
    pause
    exit /b 1
)

echo [1/6] Document Ingestion...
echo =====================================
python main.py ingest -i data/documents -r
if errorlevel 1 (
    echo ERROR: Document ingestion failed!
    pause
    exit /b 1
)
echo SUCCESS: Documents ingested
echo.

echo [2/6] Building Vector Store...
echo =====================================
python main.py build-vector-store -i data/documents --backend faiss
if errorlevel 1 (
    echo ERROR: Vector store building failed!
    pause
    exit /b 1
)
echo SUCCESS: Vector store built
echo.

echo [3/6] Building Knowledge Graph...
echo =====================================
python main.py build-knowledge-graph -i data/documents
if errorlevel 1 (
    echo WARNING: Knowledge graph building failed (Neo4j may not be running)
    echo This is optional - continuing with available methods...
)
echo.

echo [4/6] Testing Standard RAG Query...
echo =====================================
python main.py query "What is artificial intelligence?" --method rag
if errorlevel 1 (
    echo ERROR: RAG query failed!
    pause
    exit /b 1
)
echo.

echo [5/6] Testing Graph RAG Query...
echo =====================================
python main.py query "What are the types of machine learning?" --method graph_rag
if errorlevel 1 (
    echo WARNING: Graph RAG query failed (services may not be running)
)
echo.

echo [6/6] Running Evaluation Experiment...
echo =====================================
python main.py experiment --config configs/default.yaml --output experiments/results/
if errorlevel 1 (
    echo WARNING: Full experiment failed (some services may not be running)
    echo Check experiments/results/ for partial results
)
echo.

echo ========================================
echo  Pipeline Complete!
echo ========================================
echo.
echo Results available in:
echo - data/chunks/           : Processed document chunks
echo - data/vector_store/     : FAISS vector database
echo - experiments/results/   : Evaluation results
echo.
echo Next steps:
echo 1. Start Docker services: docker-compose up -d
echo 2. Re-run for full Graph RAG and KG functionality
echo 3. Check README.md for detailed usage instructions
echo.
pause