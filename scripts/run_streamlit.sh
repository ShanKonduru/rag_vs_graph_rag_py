#!/bin/bash
# =====================================================
#  RAG System - Streamlit Dashboard Launcher (Unix/Linux)
# =====================================================
#  Launch the interactive Streamlit dashboard
#  Usage: ./run_streamlit.sh [demo]
# =====================================================

echo ""
echo "========================================"
echo "  RAG System - Streamlit Dashboard"
echo "========================================"
echo ""

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "ERROR: Python not found. Please activate virtual environment first."
    echo "Run: source venv/bin/activate"
    exit 1
fi

# Determine which app to run
APP_FILE="streamlit_app.py"
if [ "$1" == "demo" ]; then
    APP_FILE="streamlit_demo.py"
    echo "Running in DEMO mode..."
else
    echo "Running FULL system mode..."
fi

# Check if streamlit is installed
python -c "import streamlit" 2>/dev/null || {
    echo "Installing Streamlit and required packages..."
    pip install streamlit plotly pandas
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install Streamlit"
        exit 1
    fi
}

echo "Starting Streamlit dashboard..."
echo ""
echo "========================================"
echo "  Dashboard will open in your browser"
echo "  URL: http://localhost:8501"
echo "========================================"
echo ""
echo "Available modes:"
echo "  ./run_streamlit.sh      - Full system (requires setup)"
echo "  ./run_streamlit.sh demo - Demo mode (no setup required)"
echo ""
echo "Press Ctrl+C to stop the dashboard"
echo ""

streamlit run $APP_FILE --server.port 8501 --server.headless false

echo ""
echo "Dashboard stopped."