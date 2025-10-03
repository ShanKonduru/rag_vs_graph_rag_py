"""
Simple RAG vs Graph RAG Comparison Dashboard
This is a simplified version focused on core functionality without complex threading.
"""
import streamlit as st
import sys
import os
import time
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

# Simple imports - avoid complex dependencies initially
try:
    from src.rag_system.config import ConfigManager
    IMPORTS_AVAILABLE = True
except ImportError as e:
    IMPORTS_AVAILABLE = False
    print(f"Import error: {e}")

class SimpleRAGComparator:
    """Simple RAG comparison with minimal dependencies"""
    
    def __init__(self):
        self.demo_mode = True
        self.systems = {}
        
    def load_demo_systems(self):
        """Load demo systems for testing"""
        self.systems = {
            'RAG': {'status': 'demo', 'description': 'Standard vector-based RAG'},
            'Graph RAG': {'status': 'demo', 'description': 'Enhanced RAG with knowledge graphs'},
            'Knowledge Graph': {'status': 'demo', 'description': 'Pure graph-based retrieval'}
        }
        return len(self.systems)
    
    def query_system(self, system_name: str, query: str):
        """Simulate system querying"""
        start_time = time.time()
        
        # Simulate different response patterns
        responses = {
            'RAG': f"RAG Response: Based on vector similarity search for '{query}', I found relevant documents. However, I cannot make connections between related concepts that aren't explicitly mentioned together.",
            'Graph RAG': f"Graph RAG Response: For '{query}', I can trace relationships and dependencies. The graph structure reveals hidden connections and provides more comprehensive context by linking related entities and concepts.",
            'Knowledge Graph': f"Knowledge Graph Response: Using graph traversal for '{query}', I can explore multi-hop relationships and uncover implicit knowledge through entity connections and semantic relationships."
        }
        
        # Simulate different response times
        delays = {'RAG': 0.5, 'Graph RAG': 0.8, 'Knowledge Graph': 0.3}
        time.sleep(delays.get(system_name, 0.5))
        
        end_time = time.time()
        response_time = end_time - start_time
        
        return {
            'response': responses.get(system_name, f"Demo response for {system_name}"),
            'response_time': response_time,
            'timestamp': datetime.now().isoformat(),
            'source_count': len(query.split()) * 2,  # Simulate source diversity
            'confidence': 0.85 if 'Graph' in system_name else 0.75
        }

def load_challenge_questions():
    """Load challenge questions from JSON file"""
    questions_file = project_root / "graph_rag_challenge_questions.json"
    try:
        with open(questions_file, 'r') as f:
            data = json.load(f)
            return data.get('questions', [])
    except FileNotFoundError:
        return [
            {
                "question": "What are the prerequisites for learning machine learning?",
                "category": "learning_pathway",
                "difficulty": "intermediate"
            },
            {
                "question": "How do microservices architecture patterns relate to database design principles?",
                "category": "cross_domain",
                "difficulty": "advanced"
            }
        ]

def main():
    st.set_page_config(
        page_title="RAG vs Graph RAG Comparison",
        page_icon="🔬",
        layout="wide"
    )
    
    st.title("🔬 RAG vs Graph RAG Comparison Dashboard")
    st.markdown("*Compare different retrieval approaches and see Graph RAG advantages*")
    
    # Initialize comparator
    if 'comparator' not in st.session_state:
        st.session_state.comparator = SimpleRAGComparator()
        
    # Sidebar - System Status
    with st.sidebar:
        st.header("🛠️ System Status")
        
        if st.button("🔄 Initialize Systems"):
            with st.spinner("Loading systems..."):
                count = st.session_state.comparator.load_demo_systems()
                st.success(f"✅ {count} systems loaded (demo mode)")
        
        # Show system status
        if hasattr(st.session_state.comparator, 'systems'):
            for name, info in st.session_state.comparator.systems.items():
                status_icon = "🟢" if info['status'] == 'demo' else "🔴"
                st.write(f"{status_icon} **{name}**: {info['description']}")
        
        st.markdown("---")
        st.markdown("**Import Status:**")
        status_icon = "✅" if IMPORTS_AVAILABLE else "⚠️"
        st.markdown(f"{status_icon} Core imports: {'Available' if IMPORTS_AVAILABLE else 'Demo mode'}")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Query Interface")
        
        # Question selection
        questions = load_challenge_questions()
        question_options = ["Custom question..."] + [q['question'] for q in questions]
        
        selected_question = st.selectbox(
            "Select a challenge question:",
            question_options,
            help="These questions are designed to showcase Graph RAG advantages"
        )
        
        if selected_question == "Custom question...":
            query = st.text_area(
                "Enter your question:",
                placeholder="Ask something that requires connecting different concepts...",
                height=100
            )
        else:
            query = selected_question
            # Show question details
            question_data = next((q for q in questions if q['question'] == selected_question), None)
            if question_data:
                st.info(f"**Category**: {question_data.get('category', 'N/A')} | **Difficulty**: {question_data.get('difficulty', 'N/A')}")
        
        # Query button
        if st.button("🚀 Compare Systems", disabled=not query.strip()):
            if hasattr(st.session_state.comparator, 'systems') and query.strip():
                st.header("📊 Comparison Results")
                
                results = {}
                cols = st.columns(len(st.session_state.comparator.systems))
                
                for idx, (system_name, system_info) in enumerate(st.session_state.comparator.systems.items()):
                    with cols[idx]:
                        st.subheader(f"🤖 {system_name}")
                        
                        with st.spinner(f"Querying {system_name}..."):
                            result = st.session_state.comparator.query_system(system_name, query)
                            results[system_name] = result
                        
                        # Display response
                        st.write("**Response:**")
                        st.write(result['response'])
                        
                        # Display metrics
                        st.metric("⏱️ Response Time", f"{result['response_time']:.2f}s")
                        st.metric("📚 Sources", result['source_count'])
                        st.metric("🎯 Confidence", f"{result['confidence']:.1%}")
                
                # Comparison summary
                st.header("📈 Performance Summary")
                
                summary_col1, summary_col2 = st.columns(2)
                
                with summary_col1:
                    st.subheader("Response Times")
                    time_data = {name: result['response_time'] for name, result in results.items()}
                    st.bar_chart(time_data)
                
                with summary_col2:
                    st.subheader("Key Insights")
                    st.markdown("**Graph RAG Advantages:**")
                    st.markdown("- 🔗 Better relationship understanding")
                    st.markdown("- 🧠 More comprehensive context")
                    st.markdown("- 🎯 Higher-quality responses for complex queries")
                    
                    st.markdown("**Standard RAG Advantages:**")
                    st.markdown("- ⚡ Faster response times")
                    st.markdown("- 💾 Lower computational overhead")
                    st.markdown("- 🔍 Good for direct factual queries")
            else:
                st.warning("Please initialize systems and enter a question first.")
    
    with col2:
        st.header("💡 Tips")
        st.markdown("""
        **Best questions for Graph RAG:**
        - Multi-step reasoning
        - Relationship queries
        - Prerequisites/dependencies
        - Cross-domain connections
        - Learning pathways
        
        **Example:**
        *"What skills do I need before learning React, and how do they relate to each other?"*
        """)
        
        if questions:
            st.header("🎯 Challenge Categories")
            categories = list(set(q.get('category', 'general') for q in questions))
            for category in categories:
                count = len([q for q in questions if q.get('category') == category])
                st.write(f"**{category.replace('_', ' ').title()}**: {count} questions")

if __name__ == "__main__":
    main()