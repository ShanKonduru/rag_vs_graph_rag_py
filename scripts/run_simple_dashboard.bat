@echo off
REM Launch Simple RAG Comparison Dashboard

echo Starting Simple RAG vs Graph RAG Comparison Dashboard...
echo.

cd /d "%~dp0\.."

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call "venv\Scripts\activate.bat"
)

echo.
echo Dashboard will be available at: http://localhost:8508
echo Press Ctrl+C to stop the dashboard
echo.

python -m streamlit run simple_dashboard.py --server.port 8508

pause