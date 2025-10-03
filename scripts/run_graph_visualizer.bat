@echo off
REM =====================================================
REM  Graph Visualizer Launcher (Windows)
REM =====================================================
REM  Launch the interactive graph visualization tool
REM =====================================================

echo.
echo ========================================
echo  🕸️ Graph Visualizer for RAG System
echo ========================================
echo.

REM Check if virtual environment is activated
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please activate virtual environment first.
    echo Run: .venv\Scripts\activate.bat
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking required packages...
python -c "import streamlit, networkx, plotly" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install streamlit networkx plotly pandas numpy
    if errorlevel 1 (
        echo ERROR: Failed to install required packages
        pause
        exit /b 1
    )
)

echo Starting Graph Visualizer...
echo.
echo ========================================
echo  Graph Visualizer will open in browser
echo  URL: http://localhost:8502
echo ========================================
echo.
echo Features:
echo  - 🧠 AI Knowledge Graph visualization
echo  - 📄 Document relationship networks
echo  - 👥 Entity relationship graphs
echo  - 🕸️ Neo4j integration (when available)
echo.
echo Press Ctrl+C to stop the visualizer
echo.

streamlit run graph_visualizer.py --server.port 8502 --server.headless false

echo.
echo Graph Visualizer stopped.
pause