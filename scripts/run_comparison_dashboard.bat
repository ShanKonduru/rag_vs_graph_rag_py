@echo off
REM RAG Comparison Dashboard Launcher
REM Launches the comprehensive RAG systems comparison dashboard

echo.
echo ====================================
echo   🔍 RAG Comparison Dashboard
echo ====================================
echo.

REM Check if virtual environment is activated
if not defined VIRTUAL_ENV (
    echo Activating virtual environment...
    if exist ".venv\Scripts\activate.bat" (
        call .venv\Scripts\activate.bat
    ) else (
        echo ⚠️  Virtual environment not found. Please run scripts\dev_setup.bat first
        pause
        exit /b 1
    )
)

REM Check if Ollama is running
echo Checking Ollama service...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Warning: Ollama service not detected at localhost:11434
    echo    Please ensure Ollama is running for full functionality
    echo.
    pause
)

REM Launch comparison dashboard
echo 🚀 Starting RAG Comparison Dashboard...
echo.
echo Dashboard will be available at: http://localhost:8506
echo.
echo Features:
echo   • Query multiple RAG systems simultaneously
echo   • Real-time performance metrics comparison
echo   • Response quality analysis
echo   • Interactive visualization
echo.

streamlit run comparison_dashboard.py --server.port 8506 --server.headless false

if %errorlevel% neq 0 (
    echo.
    echo ❌ Error: Failed to start comparison dashboard
    echo.
    echo Troubleshooting:
    echo   1. Ensure virtual environment is activated
    echo   2. Install required packages: pip install streamlit plotly
    echo   3. Check if port 8502 is available
    echo.
    pause
) else (
    echo.
    echo ✅ Comparison dashboard launched successfully!
    echo.
)

pause