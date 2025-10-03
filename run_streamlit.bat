@echo off
REM =====================================================
REM  RAG System - Streamlit Dashboard Launcher (Windows)
REM =====================================================
REM  Launch the interactive Streamlit dashboard
REM  Usage: run_streamlit.bat [demo]
REM =====================================================

echo.
echo ========================================
echo  RAG System - Streamlit Dashboard
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

REM Determine which app to run
set APP_FILE=streamlit_app.py
if "%1"=="demo" (
    set APP_FILE=streamlit_demo.py
    echo Running in DEMO mode...
) else (
    echo Running FULL system mode...
)

REM Check if streamlit is installed
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo Installing Streamlit and required packages...
    pip install streamlit plotly pandas
    if errorlevel 1 (
        echo ERROR: Failed to install Streamlit
        pause
        exit /b 1
    )
)

echo Starting Streamlit dashboard...
echo.
echo ========================================
echo  Dashboard will open in your browser
echo  URL: http://localhost:8501
echo ========================================
echo.
echo Available modes:
echo   run_streamlit.bat      - Full system (requires setup)
echo   run_streamlit.bat demo - Demo mode (no setup required)
echo.
echo Press Ctrl+C to stop the dashboard
echo.

streamlit run %APP_FILE% --server.port 8501 --server.headless false

echo.
echo Dashboard stopped.
pause