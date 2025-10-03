#!/usr/bin/env python3
"""
RAG Systems Comparison Dashboard Verification
Checks if all systems are ready for comparison
"""

import sys
import os
from pathlib import Path
import json
import time

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def check_ollama_connection():
    """Check if Ollama is running and accessible"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ Ollama is running with {len(models)} models available")
            for model in models[:3]:  # Show first 3 models
                print(f"   • {model.get('name', 'Unknown')}")
            return True
        else:
            print("❌ Ollama is running but returned error")
            return False
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        return False

def check_existing_data():
    """Check if existing RAG data is available"""
    data_path = Path("data")
    checks = {
        "Vector Store": data_path / "vector_store" / "index.faiss",
        "Chunks Data": data_path / "chunks",
        "Sample Questions": data_path / "sample_questions.json",
        "Knowledge Base": data_path / "knowledge_base"
    }
    
    all_good = True
    for name, path in checks.items():
        if path.exists():
            print(f"✅ {name}: Found at {path}")
        else:
            print(f"❌ {name}: Missing at {path}")
            all_good = False
    
    return all_good

def check_rag_system():
    """Check if RAG system modules are importable"""
    try:
        from src.rag_system.config import ConfigManager
        from src.rag_system.retrieval import RAGRetriever, GraphRAGRetriever, KnowledgeGraphRetriever
        from src.rag_system.llm import OllamaClient
        from src.rag_system.evaluation import ExactMatchMetric
        print("✅ RAG system modules are importable")
        
        # Try to initialize config
        config_manager = ConfigManager()
        print("✅ Configuration manager initialized")
        
        return True
    except Exception as e:
        print(f"❌ RAG system check failed: {e}")
        return False

def check_streamlit_dependencies():
    """Check if Streamlit and visualization dependencies are available"""
    dependencies = [
        ("streamlit", "Streamlit web framework"),
        ("plotly", "Interactive plotting"),
        ("pandas", "Data manipulation"),
        ("numpy", "Numerical operations")
    ]
    
    all_good = True
    for module, description in dependencies:
        try:
            __import__(module)
            print(f"✅ {description}: {module} is available")
        except ImportError:
            print(f"❌ {description}: {module} is missing")
            all_good = False
    
    return all_good

def estimate_comparison_capabilities():
    """Estimate what comparison capabilities are available"""
    print("\n🔍 Comparison Capabilities Assessment:")
    
    # Check vector store size
    vector_metadata_path = Path("data/vector_store/metadata.json")
    if vector_metadata_path.exists():
        try:
            with open(vector_metadata_path) as f:
                metadata = json.load(f)
                chunk_count = metadata.get('_next_index', 0)
                print(f"   • Vector Store: ~{chunk_count} chunks available")
        except:
            print("   • Vector Store: Available but size unknown")
    
    # Check sample questions
    questions_path = Path("data/sample_questions.json")
    if questions_path.exists():
        try:
            with open(questions_path) as f:
                questions = json.load(f)
                print(f"   • Sample Questions: {len(questions)} questions available")
        except:
            print("   • Sample Questions: Available but count unknown")
    
    # Check document sources
    docs_path = Path("data/documents")
    if docs_path.exists():
        doc_files = list(docs_path.glob("*"))
        print(f"   • Source Documents: {len(doc_files)} files")

def main():
    """Main verification function"""
    print("🔍 RAG Comparison Dashboard Verification")
    print("=" * 50)
    
    checks = [
        ("Ollama LLM Service", check_ollama_connection),
        ("Existing Data", check_existing_data),
        ("RAG System Modules", check_rag_system),
        ("Streamlit Dependencies", check_streamlit_dependencies)
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        print(f"\n📋 Checking {check_name}...")
        if not check_func():
            all_passed = False
    
    estimate_comparison_capabilities()
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All systems ready! You can now run the comparison dashboard:")
        print("   scripts\\run_comparison_dashboard.bat")
        print("\n💡 The dashboard will allow you to:")
        print("   • Select from existing RAG, Graph RAG, and Knowledge Graph systems")
        print("   • Query all systems simultaneously with your questions")
        print("   • Compare response times, quality, and other metrics")
        print("   • Visualize the advantages of Graph RAG over standard RAG")
    else:
        print("⚠️  Some issues found. Please address them before running the dashboard.")
        print("\n🔧 Potential solutions:")
        print("   • Run: scripts\\dev_setup.bat")
        print("   • Ensure Ollama is running with a model loaded")
        print("   • Check that existing RAG data is properly set up")
    
    return all_passed

if __name__ == "__main__":
    main()