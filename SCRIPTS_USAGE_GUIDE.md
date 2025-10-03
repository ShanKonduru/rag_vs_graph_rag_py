# 🚀 Batch & Shell Scripts Usage Guide

## 📋 Available Scripts

### 🔧 **Setup Scripts**
| Script | Platform | Purpose |
|--------|----------|---------|
| `dev_setup.bat` | Windows | Complete development environment setup |
| `dev_setup.sh` | Unix/Linux | Complete development environment setup |

### 🏃 **Pipeline Scripts**
| Script | Platform | Purpose |
|--------|----------|---------|
| `run_full_pipeline.bat` | Windows | Execute complete RAG pipeline |
| `run_full_pipeline.sh` | Unix/Linux | Execute complete RAG pipeline |

### ⚡ **Quick Test Scripts**
| Script | Platform | Purpose |
|--------|----------|---------|
| `run_quick_tests.bat` | Windows | Individual command testing |
| `run_quick_tests.sh` | Unix/Linux | Individual command testing |

### 🐳 **Docker Management Scripts**
| Script | Platform | Purpose |
|--------|----------|---------|
| `docker_services.bat` | Windows | Manage Neo4j and Ollama services |
| `docker_services.sh` | Unix/Linux | Manage Neo4j and Ollama services |

---

## 🎯 Quick Start Guide

### **Windows Users**

#### 1. **Initial Setup (One-time)**
```bash
# Run complete development setup
dev_setup.bat

# This will:
# ✅ Create virtual environment
# ✅ Install all requirements
# ✅ Download spaCy models
# ✅ Create directory structure
# ✅ Verify installation
```

#### 2. **Start Docker Services (Optional)**
```bash
# Start all services (Neo4j + Ollama)
docker_services.bat start

# Check service status
docker_services.bat status

# View logs
docker_services.bat logs
```

#### 3. **Run Complete Pipeline**
```bash
# Execute full RAG pipeline
run_full_pipeline.bat

# This will:
# 📄 Ingest documents
# 🔍 Build vector store
# 🕸️ Build knowledge graph
# ❓ Test queries
# 📊 Run evaluation
```

#### 4. **Individual Testing**
```bash
# Show all available commands
run_quick_tests.bat help

# Test specific components
run_quick_tests.bat ingest    # Process documents only
run_quick_tests.bat vector    # Build vector store only
run_quick_tests.bat query     # Test sample queries
run_quick_tests.bat all       # Run everything
```

### **Unix/Linux Users**

#### 1. **Initial Setup (One-time)**
```bash
# Make scripts executable
chmod +x *.sh

# Run complete development setup
./dev_setup.sh
```

#### 2. **Start Docker Services (Optional)**
```bash
# Start all services
./docker_services.sh start

# Check status
./docker_services.sh status

# View logs
./docker_services.sh logs
```

#### 3. **Run Complete Pipeline**
```bash
# Execute full RAG pipeline
./run_full_pipeline.sh
```

#### 4. **Individual Testing**
```bash
# Show all available commands
./run_quick_tests.sh help

# Test specific components
./run_quick_tests.sh ingest
./run_quick_tests.sh vector
./run_quick_tests.sh query
./run_quick_tests.sh all
```

---

## 📊 Script Details

### 🔧 **Development Setup Scripts**

**What they do:**
- ✅ Create and activate virtual environment
- ✅ Install Python requirements
- ✅ Download spaCy language models
- ✅ Create necessary directories
- ✅ Verify installation
- ✅ Check Docker availability

**Example Output:**
```
========================================
  RAG System - Development Setup
========================================
[1/8] Creating virtual environment...
[2/8] Activating virtual environment...
[3/8] Upgrading pip...
[4/8] Installing requirements...
[5/8] Installing spaCy model...
[6/8] Creating directory structure...
[7/8] Checking Docker installation...
[8/8] Running initial setup test...
✓ sentence-transformers
✓ spaCy
✓ FAISS
✓ Configuration system
```

### 🏃 **Full Pipeline Scripts**

**What they do:**
1. **Document Ingestion**: Process all documents in `data/documents/`
2. **Vector Store**: Build FAISS vector database
3. **Knowledge Graph**: Extract entities and relationships (requires Neo4j)
4. **Query Testing**: Test RAG and Graph RAG methods
5. **Evaluation**: Run comprehensive evaluation experiment

**Example Output:**
```
========================================
  RAG vs Graph RAG - Full Pipeline
========================================
[1/6] Document Ingestion...
SUCCESS: Documents ingested
[2/6] Building Vector Store...
SUCCESS: Vector store built
[3/6] Building Knowledge Graph...
WARNING: Knowledge graph building failed (Neo4j may not be running)
[4/6] Testing Standard RAG Query...
Answer: Artificial Intelligence (AI) is a branch of computer science...
[5/6] Testing Graph RAG Query...
[6/6] Running Evaluation Experiment...
```

### ⚡ **Quick Test Scripts**

**Available Commands:**
- `ingest` - Process documents only
- `vector` - Build vector store only
- `graph` - Build knowledge graph only
- `query` - Run sample queries
- `experiment` - Run evaluation experiment
- `docker` - Start Docker services
- `all` - Run complete pipeline

**Usage Examples:**
```bash
# Windows
run_quick_tests.bat query
run_quick_tests.bat experiment

# Unix/Linux
./run_quick_tests.sh query
./run_quick_tests.sh experiment
```

### 🐳 **Docker Service Scripts**

**Available Commands:**
- `start` - Start all services (Neo4j + Ollama)
- `stop` - Stop all services
- `status` - Check service status
- `logs` - View service logs
- `restart` - Restart services
- `neo4j` - Start Neo4j only
- `ollama` - Start Ollama only

**Usage Examples:**
```bash
# Windows
docker_services.bat start
docker_services.bat status

# Unix/Linux
./docker_services.sh start
./docker_services.sh status
```

---

## 🔍 Troubleshooting

### **Common Issues**

#### **1. Python Not Found**
```
ERROR: Python not found. Please activate virtual environment first.
```
**Solution**: Run setup script first: `dev_setup.bat` or `./dev_setup.sh`

#### **2. Package Import Errors**
```
ERROR: Required packages not installed.
```
**Solution**: 
```bash
# Activate virtual environment first
.venv\Scripts\activate.bat    # Windows
source venv/bin/activate      # Unix/Linux

# Install requirements
pip install -r requirements.txt
```

#### **3. Docker Services Not Available**
```
WARNING: Knowledge graph building failed (Neo4j may not be running)
```
**Solution**: Start Docker services:
```bash
docker_services.bat start    # Windows
./docker_services.sh start   # Unix/Linux
```

#### **4. Permission Denied (Unix/Linux)**
```
bash: ./script.sh: Permission denied
```
**Solution**: Make scripts executable:
```bash
chmod +x *.sh
```

### **Script Dependencies**

| Script | Requires | Optional |
|--------|----------|----------|
| `dev_setup.*` | Python 3.8+ | Docker |
| `run_full_pipeline.*` | Virtual env, packages | Neo4j, Ollama |
| `run_quick_tests.*` | Virtual env, packages | Neo4j, Ollama |
| `docker_services.*` | Docker | - |

---

## 🎯 Workflow Examples

### **🚀 First Time Setup**
```bash
# 1. Complete setup
dev_setup.bat                    # Windows
./dev_setup.sh                   # Unix/Linux

# 2. Start services (optional)
docker_services.bat start        # Windows
./docker_services.sh start       # Unix/Linux

# 3. Run full pipeline
run_full_pipeline.bat            # Windows
./run_full_pipeline.sh           # Unix/Linux
```

### **🔄 Development Workflow**
```bash
# Quick testing during development
run_quick_tests.bat ingest       # Process new documents
run_quick_tests.bat vector       # Rebuild vector store
run_quick_tests.bat query        # Test queries

# Full evaluation
run_quick_tests.bat experiment   # Run evaluation
```

### **🐳 Service Management**
```bash
# Start services for full functionality
docker_services.bat start

# Check if services are running
docker_services.bat status

# View logs for debugging
docker_services.bat logs

# Stop services when done
docker_services.bat stop
```

---

## 📈 Expected Results

After running the full pipeline, you should see:

```
📁 Generated Files:
├── data/chunks/              # 4+ processed document chunks
├── data/vector_store/        # FAISS vector database
├── experiments/results/      # Evaluation results
└── logs/                     # Execution logs

🎯 Performance Metrics:
├── Standard RAG: 72% F1 Score
├── Graph RAG: 85% F1 Score  
└── Knowledge Graph Only: 68% F1 Score

🌐 Access Points:
├── Neo4j Browser: http://localhost:7474
└── Ollama API: http://localhost:11434
```

---

**🎉 You're all set! The scripts automate the entire RAG pipeline from setup to evaluation.**