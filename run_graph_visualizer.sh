#!/bin/bash
# =====================================================
#  Graph Visualizer Launcher (Unix/Linux)
# =====================================================
#  Launch the interactive graph visualization tool
# =====================================================

echo ""
echo "========================================"
echo "  🕸️ Graph Visualizer for RAG System"
echo "========================================"
echo ""

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "ERROR: Python not found. Please activate virtual environment first."
    echo "Run: source venv/bin/activate"
    exit 1
fi

# Check if required packages are installed
echo "Checking required packages..."
python -c "import streamlit, networkx, plotly" 2>/dev/null || {
    echo "Installing required packages..."
    pip install streamlit networkx plotly pandas numpy
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install required packages"
        exit 1
    fi
}

echo "Starting Graph Visualizer..."
echo ""
echo "========================================"
echo "  Graph Visualizer will open in browser"
echo "  URL: http://localhost:8502"
echo "========================================"
echo ""
echo "Features:"
echo "  - 🧠 AI Knowledge Graph visualization"
echo "  - 📄 Document relationship networks"
echo "  - 👥 Entity relationship graphs"
echo "  - 🕸️ Neo4j integration (when available)"
echo ""
echo "Press Ctrl+C to stop the visualizer"
echo ""

streamlit run graph_visualizer.py --server.port 8502 --server.headless false

echo ""
echo "Graph Visualizer stopped."