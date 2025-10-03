@echo off
REM Launch Enhanced RAG Comparison Dashboard

echo Starting Enhanced RAG vs Graph RAG Comparison Dashboard...
echo.

cd /d "%~dp0\.."

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call "venv\Scripts\activate.bat"
)

echo.
echo Enhanced Dashboard will be available at: http://localhost:8509
echo This version attempts to load real systems with fallback to demo mode
echo Press Ctrl+C to stop the dashboard
echo.

python -m streamlit run enhanced_dashboard.py --server.port 8509

pause