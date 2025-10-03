@echo off
REM =====================================================
REM  RAG System - Quick Test Commands (Windows)
REM =====================================================
REM  This script runs individual test commands
REM  Usage: run_quick_tests.bat
REM =====================================================

echo.
echo ========================================
echo  RAG System - Quick Tests
echo ========================================
echo.

if "%1"=="help" (
    echo Available commands:
    echo   run_quick_tests.bat ingest       - Ingest documents only
    echo   run_quick_tests.bat vector       - Build vector store only
    echo   run_quick_tests.bat graph        - Build knowledge graph only
    echo   run_quick_tests.bat query        - Run sample queries
    echo   run_quick_tests.bat experiment   - Run evaluation experiment
    echo   run_quick_tests.bat docker       - Start Docker services
    echo   run_quick_tests.bat all          - Run all tests
    goto :eof
)

if "%1"=="ingest" (
    echo Running document ingestion...
    python main.py ingest -i data/documents -r
    goto :eof
)

if "%1"=="vector" (
    echo Building vector store...
    python main.py build-vector-store -i data/documents --backend faiss
    goto :eof
)

if "%1"=="graph" (
    echo Building knowledge graph...
    python main.py build-knowledge-graph -i data/documents
    goto :eof
)

if "%1"=="query" (
    echo Testing RAG queries...
    echo.
    echo Query 1: What is artificial intelligence?
    python main.py query "What is artificial intelligence?" --method rag
    echo.
    echo Query 2: What are the types of machine learning?
    python main.py query "What are the types of machine learning?" --method rag
    echo.
    echo Query 3: What is generative AI?
    python main.py query "What is generative AI?" --method rag
    goto :eof
)

if "%1"=="experiment" (
    echo Running evaluation experiment...
    python main.py experiment --config configs/default.yaml --output experiments/results/
    goto :eof
)

if "%1"=="docker" (
    echo Starting Docker services...
    cd docker
    docker-compose up -d
    cd ..
    echo Docker services started. Check with: docker ps
    goto :eof
)

if "%1"=="all" (
    echo Running all tests...
    call run_quick_tests.bat ingest
    call run_quick_tests.bat vector
    call run_quick_tests.bat graph
    call run_quick_tests.bat query
    call run_quick_tests.bat experiment
    goto :eof
)

echo Usage: run_quick_tests.bat [command]
echo Run 'run_quick_tests.bat help' for available commands
echo.
echo Quick commands:
echo   ingest    - Process documents
echo   vector    - Build vector store
echo   query     - Test sample queries
echo   all       - Run complete pipeline