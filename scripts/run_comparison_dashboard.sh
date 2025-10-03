#!/bin/bash
# RAG Comparison Dashboard Launcher
# Launches the comprehensive RAG systems comparison dashboard

echo ""
echo "===================================="
echo "   🔍 RAG Comparison Dashboard"
echo "===================================="
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating virtual environment..."
    source ./scripts/002_activate.sh
fi

# Check if Ollama is running
echo "Checking Ollama service..."
if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo "⚠️  Warning: Ollama service not detected at localhost:11434"
    echo "    Please ensure Ollama is running for full functionality"
    echo ""
    read -p "Press Enter to continue..."
fi

# Launch comparison dashboard
echo "🚀 Starting RAG Comparison Dashboard..."
echo ""
echo "Dashboard will be available at: http://localhost:8502"
echo ""
echo "Features:"
echo "  • Query multiple RAG systems simultaneously"
echo "  • Real-time performance metrics comparison"
echo "  • Response quality analysis"
echo "  • Interactive visualization"
echo ""

streamlit run comparison_dashboard.py --server.port 8502 --server.headless false

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Error: Failed to start comparison dashboard"
    echo ""
    echo "Troubleshooting:"
    echo "  1. Ensure virtual environment is activated"
    echo "  2. Install required packages: pip install streamlit plotly"
    echo "  3. Check if port 8502 is available"
    echo ""
    read -p "Press Enter to continue..."
else
    echo ""
    echo "✅ Comparison dashboard launched successfully!"
    echo ""
fi