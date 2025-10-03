# 🤖 Automation Scripts

This folder contains all the automation scripts for the RAG vs Graph RAG vs Knowledge Graph system.

## 📁 Script Overview

| Script | Platform | Description |
|--------|----------|-------------|
| `dev_setup.bat/.sh` | Windows/Unix | Complete development environment setup |
| `run_full_pipeline.bat/.sh` | Windows/Unix | Execute complete RAG evaluation pipeline |
| `run_quick_tests.bat/.sh` | Windows/Unix | Individual command testing and validation |
| `docker_services.bat/.sh` | Windows/Unix | Docker service management (start/stop/status) |
| `run_streamlit.bat/.sh` | Windows/Unix | Launch interactive Streamlit dashboard |
| `run_graph_visualizer.bat/.sh` | Windows/Unix | Launch graph visualization tool |
| `run_comparison_dashboard.bat/.sh` | Windows/Unix | **NEW:** Real-time RAG systems comparison dashboard |

## 🚀 Quick Start

### **Windows Users:**
```bash
# Complete setup and pipeline execution
scripts\dev_setup.bat                 # One-time setup
scripts\docker_services.bat start     # Start services (optional)
scripts\run_full_pipeline.bat         # Execute full pipeline
```

### **Unix/Linux Users:**
```bash
# Make scripts executable and run setup
chmod +x scripts/*.sh
scripts/dev_setup.sh                # One-time setup
scripts/docker_services.sh start    # Start services (optional)
scripts/run_full_pipeline.sh        # Execute full pipeline
```

## 📖 Detailed Usage

### **Development Setup**
- **Purpose**: Install dependencies, configure Python environment
- **Usage**: `scripts/dev_setup.bat` (Windows) or `scripts/dev_setup.sh` (Unix)
- **What it does**: Installs requirements.txt, downloads spaCy models, validates setup

### **Full Pipeline**
- **Purpose**: Complete RAG system evaluation from start to finish
- **Usage**: `scripts/run_full_pipeline.bat/.sh`
- **What it does**: Document ingestion → Vector store → Knowledge graph → Evaluation

### **Quick Tests**
- **Purpose**: Individual component testing and validation
- **Usage**: `scripts/run_quick_tests.bat/.sh [command]`
- **Available commands**: `ingest`, `vector`, `knowledge-graph`, `query`, `experiment`

### **Docker Services**
- **Purpose**: Manage Neo4j and Ollama Docker containers
- **Usage**: `scripts/docker_services.bat/.sh [action]`
- **Available actions**: `start`, `stop`, `status`, `logs`

### **Interactive Tools**
- **Streamlit Dashboard**: `scripts/run_streamlit.bat/.sh [demo]`
- **Graph Visualizer**: `scripts/run_graph_visualizer.bat/.sh`

## 🔧 Script Customization

All scripts can be customized by editing the variables at the top of each file:

```bash
# Example customization in dev_setup.sh
PYTHON_VERSION="3.8+"
REQUIREMENTS_FILE="requirements.txt"
SPACY_MODEL="en_core_web_sm"
```

## 📚 Documentation

For comprehensive workflow documentation, see:
- **[SCRIPTS_USAGE_GUIDE.md](../SCRIPTS_USAGE_GUIDE.md)** - Complete automation workflow
- **[SCRIPTS_SUMMARY.md](../SCRIPTS_SUMMARY.md)** - Quick reference for all scripts

## ✨ Benefits of Script Organization

- ✅ **Clean Project Root**: Main directory is no longer cluttered
- ✅ **Easy Discovery**: All automation scripts in one place
- ✅ **Cross-Platform**: Both Windows (.bat) and Unix (.sh) versions
- ✅ **Consistent Interface**: Standardized command patterns across all scripts