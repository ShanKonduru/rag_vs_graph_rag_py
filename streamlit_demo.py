import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
from pathlib import Path
import time

# Simple demo data for when the full system isn't available
DEMO_DATA = {
    'evaluation_results': {
        'rag': [
            {'exact_match': 0.65, 'f1_score': 0.72, 'rouge_l': 0.68, 'bleu_score': 0.45},
            {'exact_match': 0.70, 'f1_score': 0.75, 'rouge_l': 0.72, 'bleu_score': 0.48},
            {'exact_match': 0.60, 'f1_score': 0.70, 'rouge_l': 0.65, 'bleu_score': 0.42}
        ],
        'graph_rag': [
            {'exact_match': 0.78, 'f1_score': 0.85, 'rouge_l': 0.82, 'bleu_score': 0.58},
            {'exact_match': 0.82, 'f1_score': 0.88, 'rouge_l': 0.85, 'bleu_score': 0.62},
            {'exact_match': 0.75, 'f1_score': 0.83, 'rouge_l': 0.80, 'bleu_score': 0.55}
        ],
        'kg_only': [
            {'exact_match': 0.58, 'f1_score': 0.68, 'rouge_l': 0.65, 'bleu_score': 0.42},
            {'exact_match': 0.62, 'f1_score': 0.70, 'rouge_l': 0.68, 'bleu_score': 0.45},
            {'exact_match': 0.55, 'f1_score': 0.66, 'rouge_l': 0.62, 'bleu_score': 0.40}
        ]
    },
    'sample_answers': {
        'rag': "Artificial Intelligence (AI) is a branch of computer science that aims to create machines capable of intelligent behavior. AI systems can perform tasks that typically require human intelligence, such as learning, reasoning, problem-solving, perception, and language understanding.",
        'graph_rag': "Artificial Intelligence (AI) is a branch of computer science focused on creating intelligent machines. It encompasses various subfields including Machine Learning, Natural Language Processing, and Computer Vision. AI systems demonstrate human-like cognitive abilities and are applied across healthcare, transportation, finance, and entertainment industries.",
        'kg_only': "Artificial Intelligence (AI) is a computer science field. It relates to Machine Learning as a parent concept. AI is used in healthcare applications and transportation systems."
    }
}

# Page configuration
st.set_page_config(
    page_title="🧠 RAG Comparison Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.metric-card {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
}
.success-card {
    border-left: 5px solid #28a745;
    background-color: #d4edda;
    padding: 1rem;
    margin: 1rem 0;
}
.info-card {
    border-left: 5px solid #17a2b8;
    background-color: #d1ecf1;
    padding: 1rem;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

def check_full_system():
    """Check if the full RAG system is available"""
    try:
        import sys
        sys.path.append("src")
        from src.rag_system.config import ConfigManager
        return True
    except:
        return False

def render_header():
    """Render the main header"""
    st.markdown('<h1 class="main-header">🧠 RAG vs Graph RAG vs Knowledge Graph Dashboard</h1>', 
               unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <p style="font-size: 1.2rem; color: #666;">
            Interactive comparison of three knowledge-driven QA approaches
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_system_status():
    """Render system status"""
    st.sidebar.markdown("## 🔧 System Status")
    
    full_system = check_full_system()
    
    if full_system:
        st.sidebar.success("✅ Full RAG system available")
        
        # Check actual system components
        status_items = [
            ("📄 Documents", Path("data/documents").exists(), "Documents loaded"),
            ("🔍 Vector Store", Path("data/vector_store").exists(), "FAISS index ready"),
            ("🕸️ Neo4j", False, "Knowledge graph ready"),  # Simplified check
            ("🤖 Ollama", False, "LLM service ready")  # Simplified check
        ]
        
        for name, is_ready, description in status_items:
            color = "🟢" if is_ready else "🔴"
            st.sidebar.markdown(f"{color} **{name}**: {description if is_ready else 'Not available'}")
    else:
        st.sidebar.info("ℹ️ Running in demo mode")
        st.sidebar.markdown("""
        **Demo Features:**
        - 📊 Performance comparison charts
        - 📋 Sample evaluation results
        - 🔍 Method comparison interface
        - 📈 Analytics and insights
        """)
    
    with st.sidebar.expander("🚀 Setup Instructions"):
        st.markdown("""
        **To enable full functionality:**
        
        **Windows:**
        ```bash
        .\\dev_setup.bat
        .\\docker_services.bat start
        .\\run_full_pipeline.bat
        ```
        
        **Unix/Linux:**
        ```bash
        ./dev_setup.sh
        ./docker_services.sh start
        ./run_full_pipeline.sh
        ```
        """)

def render_demo_query_interface():
    """Render demo query interface"""
    st.markdown("## 🔍 Interactive Query Testing")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_input(
            "Enter your question:",
            placeholder="e.g., What is artificial intelligence?",
            help="Ask questions about AI (demo responses)"
        )
    
    with col2:
        method = st.selectbox(
            "Method:",
            options=['rag', 'graph_rag', 'kg_only'],
            format_func=lambda x: {
                'rag': '🔍 Standard RAG',
                'graph_rag': '🕸️ Graph RAG',
                'kg_only': '📊 Knowledge Graph Only'
            }[x]
        )
    
    if st.button("🚀 Run Query (Demo)", type="primary", use_container_width=True):
        if query.strip():
            render_demo_query_result(query, method)
        else:
            st.warning("Please enter a question first!")
    
    # Sample questions
    with st.expander("💡 Sample Questions"):
        sample_questions = [
            "What is artificial intelligence?",
            "How does machine learning work?",
            "What are the types of machine learning?",
            "What is generative AI?",
            "What are AI agents?",
        ]
        
        cols = st.columns(2)
        for i, question in enumerate(sample_questions):
            with cols[i % 2]:
                if st.button(f"📝 {question}", key=f"sample_{i}"):
                    render_demo_query_result(question, method)

def render_demo_query_result(query, method):
    """Render demo query result"""
    method_names = {
        'rag': '🔍 Standard RAG',
        'graph_rag': '🕸️ Graph RAG',
        'kg_only': '📊 Knowledge Graph Only'
    }
    
    st.markdown(f"### Results from {method_names[method]}")
    
    # Simulate processing time
    with st.spinner("Processing query..."):
        time.sleep(1)  # Simulate processing
    
    # Demo response
    answer = DEMO_DATA['sample_answers'][method]
    
    with st.container():
        st.markdown('<div class="success-card">', unsafe_allow_html=True)
        st.markdown(f"**Query:** {query}")
        st.markdown(f"**Answer:** {answer}")
        
        # Demo metrics
        col1, col2, col3 = st.columns(3)
        
        timing_data = {
            'rag': {'total': 8.55, 'retrieval': 0.045, 'generation': 8.5},
            'graph_rag': {'total': 9.32, 'retrieval': 0.12, 'generation': 9.2},
            'kg_only': {'total': 7.88, 'retrieval': 0.08, 'generation': 7.8}
        }
        
        timing = timing_data[method]
        
        with col1:
            st.metric("Total Time", f"{timing['total']:.2f}s")
        
        with col2:
            st.metric("Retrieval Time", f"{timing['retrieval']:.3f}s")
        
        with col3:
            st.metric("Generation Time", f"{timing['generation']:.2f}s")
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_comparison_metrics():
    """Render comparison metrics"""
    st.markdown("## 📊 Performance Comparison")
    
    # Calculate averages from demo data
    comparison_data = []
    
    for method, results in DEMO_DATA['evaluation_results'].items():
        avg_metrics = {}
        for metric in ['exact_match', 'f1_score', 'rouge_l', 'bleu_score']:
            avg_metrics[metric] = sum(r[metric] for r in results) / len(results)
        
        comparison_data.append({
            'Method': method.replace('_', ' ').title(),
            'Exact Match': f"{avg_metrics['exact_match']:.3f}",
            'F1 Score': f"{avg_metrics['f1_score']:.3f}",
            'ROUGE-L': f"{avg_metrics['rouge_l']:.3f}",
            'BLEU Score': f"{avg_metrics['bleu_score']:.3f}"
        })
    
    # Display comparison table
    df = pd.DataFrame(comparison_data)
    st.dataframe(df, use_container_width=True)
    
    # Performance insights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🏆 Best Overall")
        st.markdown("**Graph RAG** leads with 85% F1 score")
        st.progress(0.85)
    
    with col2:
        st.markdown("### ⚡ Fastest")
        st.markdown("**Knowledge Graph Only** at 7.88s")
        st.progress(0.88)
    
    with col3:
        st.markdown("### 🎯 Most Accurate")
        st.markdown("**Graph RAG** with 78% exact match")
        st.progress(0.78)

def render_knowledge_base_info():
    """Render knowledge base information"""
    st.markdown("## 📚 Knowledge Base Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📖 Content Coverage")
        st.markdown("""
        - **🤖 Core AI Concepts**: Traditional AI, Machine Learning, Deep Learning
        - **🔥 Modern AI Topics**: Generative AI, Large Language Models
        - **🚀 Agentic AI**: AI Agents, Agentic Swarms, Multi-agent Systems
        - **🎯 Applications**: Healthcare, Finance, Transportation, Entertainment
        - **📊 Technical Details**: Neural Networks, NLP, Computer Vision
        """)
    
    with col2:
        st.markdown("### 📈 Knowledge Base Stats")
        
        stats = [
            ("Documents", "1 comprehensive guide", "2,500+ words"),
            ("Entities", "50+ AI concepts", "Companies & technologies"),
            ("Relationships", "Complex hierarchies", "AI → ML → Deep Learning"),
            ("Examples", "Real-world cases", "Tesla, Netflix, OpenAI")
        ]
        
        for label, value, detail in stats:
            st.metric(label, value, detail)

def render_method_comparison():
    """Render detailed method comparison"""
    st.markdown("## 🔍 Method Comparison Details")
    
    methods = {
        '🔍 Standard RAG': {
            'description': 'Traditional vector-based retrieval with LLM generation',
            'strengths': ['Fast retrieval', 'Good semantic matching', 'Simple architecture'],
            'weaknesses': ['Limited relationship understanding', 'Context fragmentation'],
            'best_for': 'Large-scale factual Q&A with speed requirements'
        },
        '🕸️ Graph RAG': {
            'description': 'Hybrid approach combining vector similarity and knowledge graphs',
            'strengths': ['Rich contextual information', 'Entity relationship awareness', 'Better multi-hop reasoning'],
            'weaknesses': ['Higher complexity', 'Slower than pure RAG', 'Requires graph construction'],
            'best_for': 'Complex knowledge domains requiring relationship understanding'
        },
        '📊 Knowledge Graph Only': {
            'description': 'Pure graph-based retrieval without vector similarity',
            'strengths': ['Excellent relationship understanding', 'Explainable reasoning', 'Perfect for structured queries'],
            'weaknesses': ['Limited semantic similarity', 'Requires high-quality extraction', 'Graph completeness dependent'],
            'best_for': 'Structured queries with explainable reasoning paths'
        }
    }
    
    for method_name, details in methods.items():
        with st.expander(method_name):
            st.markdown(f"**Description:** {details['description']}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**✅ Strengths:**")
                for strength in details['strengths']:
                    st.markdown(f"• {strength}")
            
            with col2:
                st.markdown("**⚠️ Limitations:**")
                for weakness in details['weaknesses']:
                    st.markdown(f"• {weakness}")
            
            st.markdown(f"**🎯 Best For:** {details['best_for']}")

def render_analytics():
    """Render analytics and insights"""
    st.markdown("## 📈 Analytics & Insights")
    
    # Key insights
    insights = [
        {
            'title': '🏆 Graph RAG Leadership',
            'description': 'Graph RAG consistently outperforms other methods with 85% F1 score, combining the best of vector similarity and graph relationships.',
            'impact': 'High'
        },
        {
            'title': '⚡ Speed vs Quality Trade-off',
            'description': 'Knowledge Graph Only is fastest (7.88s) but Graph RAG provides better quality despite 15% slower performance.',
            'impact': 'Medium'
        },
        {
            'title': '🎯 Use Case Optimization',
            'description': 'Each method excels in specific scenarios: RAG for speed, Graph RAG for complex reasoning, KG for structured queries.',
            'impact': 'High'
        }
    ]
    
    for insight in insights:
        color = "success" if insight['impact'] == 'High' else "info"
        st.markdown(f'<div class="{color}-card">', unsafe_allow_html=True)
        st.markdown(f"**{insight['title']}**")
        st.markdown(insight['description'])
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Main application"""
    render_header()
    render_system_status()
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔍 Query Testing",
        "📊 Performance",
        "📚 Knowledge Base",
        "🔍 Method Details",
        "📈 Analytics"
    ])
    
    with tab1:
        render_demo_query_interface()
    
    with tab2:
        render_comparison_metrics()
    
    with tab3:
        render_knowledge_base_info()
    
    with tab4:
        render_method_comparison()
    
    with tab5:
        render_analytics()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 2rem;">
        <p>🧠 RAG Comparison Dashboard | Built with Streamlit</p>
        <p>For full functionality, set up the complete RAG system using the automation scripts.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()