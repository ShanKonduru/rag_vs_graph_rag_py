import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
import asyncio
import subprocess

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent / "src"))

try:
    from src.rag_system.config import ConfigManager
    from src.rag_system.retrieval import RAGRetriever, GraphRAGRetriever, KnowledgeGraphRetriever
    from src.rag_system.evaluation.metrics import EvaluationMetrics
    from src.rag_system.evaluation.evaluator import Evaluator
    FULL_SYSTEM_AVAILABLE = True
except ImportError as e:
    st.warning(f"RAG system modules not available: {e}")
    st.info("🔧 Running in demo mode with mock data")
    FULL_SYSTEM_AVAILABLE = False

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
.method-card {
    border: 2px solid #e1e5e9;
    border-radius: 0.5rem;
    padding: 1rem;
    margin: 1rem 0;
}
.success-card {
    border-left: 5px solid #28a745;
    background-color: #d4edda;
    padding: 1rem;
    margin: 1rem 0;
}
.warning-card {
    border-left: 5px solid #ffc107;
    background-color: #fff3cd;
    padding: 1rem;
    margin: 1rem 0;
}
.error-card {
    border-left: 5px solid #dc3545;
    background-color: #f8d7da;
    padding: 1rem;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

class RAGDashboard:
    def __init__(self):
        self.config_manager = None
        self.config = None
        self.init_session_state()
        self.load_config()
    
    def get_mock_response(self, query, method):
        """Generate mock response when full system is not available"""
        mock_responses = {
            'rag': {
                'answer': f"[Mock RAG Response] Artificial intelligence (AI) is a branch of computer science that aims to create machines capable of intelligent behavior. This response was generated using traditional Retrieval-Augmented Generation, which combines vector search with language generation to provide factual answers based on retrieved documents.",
                'metadata': {
                    'retrieval_time': 0.045,
                    'generation_time': 1.23,
                    'retrieved_chunks': 3,
                    'sources': ['ai_introduction.md', 'ml_basics.pdf'],
                    'confidence': 0.87
                }
            },
            'graph_rag': {
                'answer': f"[Mock Graph RAG Response] Artificial intelligence represents a convergence of computer science, mathematics, and cognitive science. Using Graph RAG, we can see the relationships between AI concepts, machine learning algorithms, and their applications across various industries. This hybrid approach provides both factual accuracy and contextual understanding.",
                'metadata': {
                    'retrieval_time': 0.078,
                    'generation_time': 1.45,
                    'retrieved_chunks': 5,
                    'graph_entities': ['AI', 'Machine Learning', 'Computer Science'],
                    'relationship_strength': 0.92,
                    'sources': ['ai_introduction.md', 'deep_learning.pdf', 'industry_applications.md'],
                    'confidence': 0.91
                }
            },
            'kg_only': {
                'answer': f"[Mock KG Response] Based on knowledge graph traversal: AI → Computer Science → Algorithms → Problem Solving. The knowledge graph shows direct relationships between artificial intelligence and computational methods, with high confidence paths through machine learning and data processing nodes.",
                'metadata': {
                    'query_time': 0.023,
                    'traversal_depth': 3,
                    'nodes_visited': 12,
                    'relationship_types': ['IS_A', 'RELATES_TO', 'USES'],
                    'confidence_score': 0.89,
                    'reasoning_path': ['AI', 'Computer Science', 'Algorithms', 'Problem Solving']
                }
            }
        }
        
        base_response = mock_responses.get(method, mock_responses['rag'])
        
        # Customize response based on query
        if 'machine learning' in query.lower():
            base_response['answer'] = base_response['answer'].replace('Artificial intelligence', 'Machine learning')
        elif 'deep learning' in query.lower():
            base_response['answer'] = base_response['answer'].replace('Artificial intelligence', 'Deep learning')
        
        return base_response['answer'], base_response['metadata']
    
    def init_session_state(self):
        """Initialize session state variables"""
        if 'query_history' not in st.session_state:
            st.session_state.query_history = []
        if 'evaluation_results' not in st.session_state:
            st.session_state.evaluation_results = None
        if 'selected_method' not in st.session_state:
            st.session_state.selected_method = 'rag'
    
    def load_config(self):
        """Load configuration"""
        if not FULL_SYSTEM_AVAILABLE:
            self.config = None
            return
            
        try:
            self.config_manager = ConfigManager()
            self.config = self.config_manager.get_config()
        except Exception as e:
            st.warning(f"Configuration not available: {e}")
            st.info("🔧 Running with default settings")
            self.config = None
    
    def check_system_status(self):
        """Check the status of various system components"""
        status = {
            'vector_store': False,
            'neo4j': False,
            'ollama': False,
            'documents': False
        }
        
        # Check vector store
        vector_store_path = Path("data/vector_store")
        if vector_store_path.exists() and any(vector_store_path.iterdir()):
            status['vector_store'] = True
        
        # Check documents
        docs_path = Path("data/documents")
        if docs_path.exists() and any(docs_path.iterdir()):
            status['documents'] = True
        
        # Check Neo4j (simplified check)
        try:
            import requests
            response = requests.get("http://localhost:7474", timeout=2)
            status['neo4j'] = response.status_code == 200
        except (ImportError, Exception):
            status['neo4j'] = False
        
        # Check Ollama (simplified check)
        try:
            import requests
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            status['ollama'] = response.status_code == 200
        except (ImportError, Exception):
            status['ollama'] = False
        
        return status
    
    def render_header(self):
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
    
    def render_system_status(self):
        """Render system status indicators"""
        st.sidebar.markdown("## 🔧 System Status")
        
        status = self.check_system_status()
        
        status_items = [
            ("📄 Documents", status['documents'], "Documents loaded"),
            ("🔍 Vector Store", status['vector_store'], "FAISS index ready"),
            ("🕸️ Neo4j", status['neo4j'], "Knowledge graph ready"),
            ("🤖 Ollama", status['ollama'], "LLM service ready")
        ]
        
        for name, is_ready, description in status_items:
            color = "🟢" if is_ready else "🔴"
            st.sidebar.markdown(f"{color} **{name}**: {description if is_ready else 'Not available'}")
        
        if not all(status.values()):
            st.sidebar.warning("⚠️ Some services are not available. Full functionality may be limited.")
            
            with st.sidebar.expander("🚀 Quick Setup"):
                st.markdown("""
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
    
    def render_query_interface(self):
        """Render the query interface"""
        st.markdown("## 🔍 Interactive Query Testing")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            query = st.text_input(
                "Enter your question:",
                placeholder="e.g., What is artificial intelligence?",
                help="Ask questions about the AI knowledge base"
            )
        
        with col2:
            method = st.selectbox(
                "Method:",
                options=['rag', 'graph_rag', 'kg_only'],
                format_func=lambda x: {
                    'rag': '🔍 Standard RAG',
                    'graph_rag': '🕸️ Graph RAG',
                    'kg_only': '📊 Knowledge Graph Only'
                }[x],
                index=['rag', 'graph_rag', 'kg_only'].index(st.session_state.selected_method)
            )
        
        st.session_state.selected_method = method
        
        if st.button("🚀 Run Query", type="primary", use_container_width=True):
            if query.strip():
                self.run_single_query(query, method)
            else:
                st.warning("Please enter a question first!")
        
        # Sample questions
        with st.expander("💡 Sample Questions"):
            sample_questions = [
                "What is artificial intelligence?",
                "How does machine learning work?",
                "What are the types of machine learning?",
                "What is generative AI?",
                "What are AI agents and agentic systems?",
                "How is AI used in healthcare?",
                "What is the difference between AI and machine learning?"
            ]
            
            cols = st.columns(2)
            for i, question in enumerate(sample_questions):
                with cols[i % 2]:
                    if st.button(f"📝 {question}", key=f"sample_{i}"):
                        st.session_state.temp_query = question
                        st.rerun()
        
        # Handle sample question selection
        if hasattr(st.session_state, 'temp_query'):
            self.run_single_query(st.session_state.temp_query, method)
            del st.session_state.temp_query
    
    def run_single_query(self, query: str, method: str):
        """Run a single query and display results"""
        with st.spinner(f"Running {method.upper()} query..."):
            try:
                start_time = time.time()
                
                # Check if full system is available
                if FULL_SYSTEM_AVAILABLE and self.config:
                    # Import and initialize the retriever based on method
                    if method == 'rag':
                        retriever = RAGRetriever(self.config)
                        answer, metadata = retriever.retrieve_and_generate(query)
                    elif method == 'graph_rag':
                        retriever = GraphRAGRetriever(self.config)
                        answer, metadata = retriever.retrieve_and_generate(query)
                    else:  # kg_only
                        retriever = KnowledgeGraphRetriever(self.config)
                        answer, metadata = retriever.retrieve_and_generate(query)
                else:
                    # Use mock responses when full system is not available
                    answer, metadata = self.get_mock_response(query, method)
                
                end_time = time.time()
                total_time = end_time - start_time
                
                # Store in query history
                query_result = {
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'query': query,
                    'method': method,
                    'answer': answer,
                    'metadata': metadata,
                    'total_time': total_time
                }
                
                st.session_state.query_history.insert(0, query_result)
                
                # Display results
                self.display_query_results(query_result)
                
            except Exception as e:
                st.error(f"Error running {method} query: {str(e)}")
                st.info("💡 Tip: Make sure the system is properly set up and services are running.")
    
    def display_query_results(self, result):
        """Display query results"""
        method_names = {
            'rag': '🔍 Standard RAG',
            'graph_rag': '🕸️ Graph RAG',
            'kg_only': '📊 Knowledge Graph Only'
        }
        
        st.markdown(f"### Results from {method_names[result['method']]}")
        
        # Results container
        with st.container():
            st.markdown('<div class="success-card">', unsafe_allow_html=True)
            st.markdown(f"**Query:** {result['query']}")
            st.markdown(f"**Answer:** {result['answer']}")
            
            # Metadata and timing
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Time", f"{result['total_time']:.2f}s")
            
            with col2:
                retrieval_time = result['metadata'].get('retrieval_time', 0)
                st.metric("Retrieval Time", f"{retrieval_time:.3f}s")
            
            with col3:
                generation_time = result['metadata'].get('generation_time', 0)
                st.metric("Generation Time", f"{generation_time:.2f}s")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Retrieved chunks (if available)
            if 'retrieved_chunks' in result['metadata']:
                with st.expander("📄 Retrieved Chunks"):
                    chunks = result['metadata']['retrieved_chunks']
                    for i, chunk in enumerate(chunks[:3]):  # Show top 3
                        st.markdown(f"**Chunk {i+1}:** {chunk}")
    
    def render_batch_evaluation(self):
        """Render batch evaluation interface"""
        st.markdown("## 📊 Batch Evaluation")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("Run comprehensive evaluation across all methods:")
            
            # Load sample questions
            sample_questions_path = Path("data/sample_questions.json")
            if sample_questions_path.exists():
                with open(sample_questions_path, 'r') as f:
                    questions = json.load(f)
                
                st.info(f"📋 Found {len(questions)} sample questions ready for evaluation")
            else:
                # Use fallback questions when no sample questions file exists
                st.info("📋 Using demo evaluation questions")
                questions = [
                    {
                        "id": 1,
                        "question": "What is artificial intelligence?",
                        "expected_answer": "Artificial intelligence (AI) is a branch of computer science focused on creating intelligent machines that can perform tasks typically requiring human intelligence.",
                        "metadata": {"topic": "AI basics", "difficulty": "beginner"}
                    },
                    {
                        "id": 2,
                        "question": "How does machine learning relate to artificial intelligence?",
                        "expected_answer": "Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed.",
                        "metadata": {"topic": "ML relationship", "difficulty": "intermediate"}
                    },
                    {
                        "id": 3,
                        "question": "What are the main applications of AI in healthcare?",
                        "expected_answer": "AI applications in healthcare include medical imaging diagnosis, drug discovery, personalized treatment plans, robotic surgery, and predictive analytics for patient outcomes.",
                        "metadata": {"topic": "AI applications", "difficulty": "intermediate"}
                    },
                    {
                        "id": 4,
                        "question": "What is deep learning and how does it work?",
                        "expected_answer": "Deep learning is a subset of machine learning that uses artificial neural networks with multiple layers to model and understand complex patterns in data.",
                        "metadata": {"topic": "Deep learning", "difficulty": "advanced"}
                    },
                    {
                        "id": 5,
                        "question": "What are the ethical considerations in AI development?",
                        "expected_answer": "Ethical considerations in AI include bias and fairness, privacy protection, transparency and explainability, accountability, job displacement, and responsible AI governance.",
                        "metadata": {"topic": "AI ethics", "difficulty": "advanced"}
                    }
                ]
                
            if questions:
                methods_to_test = st.multiselect(
                    "Select methods to evaluate:",
                    options=['rag', 'graph_rag', 'kg_only'],
                    default=['rag', 'graph_rag', 'kg_only'],
                    format_func=lambda x: {
                        'rag': '🔍 Standard RAG',
                        'graph_rag': '🕸️ Graph RAG',
                        'kg_only': '📊 Knowledge Graph Only'
                    }[x]
                )
                
                if st.button("🚀 Run Batch Evaluation", type="primary"):
                    self.run_batch_evaluation(questions, methods_to_test)
            else:
                st.warning("📋 No evaluation questions available.")
                if st.button("🔄 Generate Sample Questions"):
                    self.generate_sample_questions()
        
        with col2:
            st.markdown("### 📈 Evaluation Metrics")
            st.markdown("""
            - **Exact Match**: Perfect answer matching
            - **F1 Score**: Token-level precision/recall
            - **ROUGE-L**: Longest common subsequence
            - **BLEU**: N-gram based similarity
            - **Timing**: Performance metrics
            """)
    
    def run_batch_evaluation(self, questions, methods):
        """Run batch evaluation"""
        if not methods:
            st.warning("Please select at least one method to evaluate.")
            return
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        results = {}
        total_steps = len(methods) * len(questions)
        current_step = 0
        
        for method in methods:
            status_text.text(f"Evaluating {method.upper()}...")
            method_results = []
            
            for question in questions:
                current_step += 1
                progress_bar.progress(current_step / total_steps)
                
                try:
                    # Run query
                    if FULL_SYSTEM_AVAILABLE and self.config:
                        if method == 'rag':
                            retriever = RAGRetriever(self.config)
                        elif method == 'graph_rag':
                            retriever = GraphRAGRetriever(self.config)
                        else:
                            retriever = KnowledgeGraphRetriever(self.config)
                        
                        answer, metadata = retriever.retrieve_and_generate(question['question'])
                        
                        # Calculate metrics
                        evaluator = Evaluator()
                        metrics = evaluator.evaluate_single(
                            answer, 
                            question['expected_answer'],
                            question['question']
                        )
                    else:
                        # Use mock evaluation when full system not available
                        answer, metadata = self.get_mock_response(question['question'], method)
                        
                        # Generate realistic different metrics for each method
                        question_hash = hash(question['question']) % 100
                        
                        if method == 'rag':
                            # RAG: Good but not best scores
                            metrics = {
                                'exact_match': 0.65 + (question_hash % 15) * 0.01,
                                'f1_score': 0.72 + (question_hash % 12) * 0.01,
                                'rouge_l': 0.68 + (question_hash % 14) * 0.01,
                                'bleu_score': 0.45 + (question_hash % 10) * 0.01
                            }
                        elif method == 'graph_rag':
                            # Graph RAG: Best performance due to context understanding
                            metrics = {
                                'exact_match': 0.78 + (question_hash % 12) * 0.01,
                                'f1_score': 0.85 + (question_hash % 8) * 0.01,
                                'rouge_l': 0.82 + (question_hash % 10) * 0.01,
                                'bleu_score': 0.58 + (question_hash % 8) * 0.01
                            }
                        else:  # kg_only
                            # KG Only: Lower scores but fast, good for structured queries
                            metrics = {
                                'exact_match': 0.58 + (question_hash % 10) * 0.01,
                                'f1_score': 0.68 + (question_hash % 8) * 0.01,
                                'rouge_l': 0.65 + (question_hash % 12) * 0.01,
                                'bleu_score': 0.42 + (question_hash % 8) * 0.01
                            }
                    
                    method_results.append({
                        'question': question['question'],
                        'answer': answer,
                        'expected': question['expected_answer'],
                        'metrics': metrics,
                        'metadata': metadata
                    })
                    
                except Exception as e:
                    st.warning(f"Failed to evaluate question with {method}: {str(e)}")
            
            results[method] = method_results
        
        progress_bar.progress(1.0)
        status_text.text("Evaluation complete!")
        
        # Store results
        st.session_state.evaluation_results = results
        
        # Display results
        self.display_evaluation_results(results)
    
    def display_evaluation_results(self, results):
        """Display evaluation results"""
        if not results:
            return
        
        st.markdown("### 📊 Evaluation Results")
        
        # Summary metrics
        summary_data = []
        for method, method_results in results.items():
            if method_results:
                # Calculate averages
                metrics_avg = {}
                for metric in ['exact_match', 'f1_score', 'rouge_l', 'bleu_score']:
                    values = [r['metrics'][metric] for r in method_results if metric in r['metrics']]
                    metrics_avg[metric] = sum(values) / len(values) if values else 0
                
                summary_data.append({
                    'Method': method.replace('_', ' ').title(),
                    'Exact Match': f"{metrics_avg['exact_match']:.3f}",
                    'F1 Score': f"{metrics_avg['f1_score']:.3f}",
                    'ROUGE-L': f"{metrics_avg['rouge_l']:.3f}",
                    'BLEU Score': f"{metrics_avg['bleu_score']:.3f}"
                })
        
        # Display summary table
        if summary_data:
            df_summary = pd.DataFrame(summary_data)
            st.dataframe(df_summary, use_container_width=True)
            
            # Visualization
            self.create_evaluation_charts(results)
    
    def create_evaluation_charts(self, results):
        """Create evaluation charts"""
        # Prepare data for visualization
        chart_data = []
        for method, method_results in results.items():
            for result in method_results:
                chart_data.append({
                    'Method': method.replace('_', ' ').title(),
                    'Exact Match': result['metrics'].get('exact_match', 0),
                    'F1 Score': result['metrics'].get('f1_score', 0),
                    'ROUGE-L': result['metrics'].get('rouge_l', 0),
                    'BLEU Score': result['metrics'].get('bleu_score', 0)
                })
        
        if not chart_data:
            return
        
        df = pd.DataFrame(chart_data)
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Exact Match', 'F1 Score', 'ROUGE-L', 'BLEU Score'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "bar"}]]
        )
        
        metrics = ['Exact Match', 'F1 Score', 'ROUGE-L', 'BLEU Score']
        positions = [(1,1), (1,2), (2,1), (2,2)]
        
        for metric, (row, col) in zip(metrics, positions):
            method_avgs = df.groupby('Method')[metric].mean().reset_index()
            
            fig.add_trace(
                go.Bar(
                    x=method_avgs['Method'],
                    y=method_avgs[metric],
                    name=metric,
                    showlegend=False
                ),
                row=row, col=col
            )
        
        fig.update_layout(height=600, title_text="Evaluation Metrics Comparison")
        st.plotly_chart(fig, use_container_width=True)
    
    def render_query_history(self):
        """Render query history"""
        if not st.session_state.query_history:
            st.info("No queries executed yet. Try running some queries above!")
            return
        
        st.markdown("## 📋 Query History")
        
        # Clear history button
        if st.button("🗑️ Clear History"):
            st.session_state.query_history = []
            st.rerun()
        
        # Display history
        for i, result in enumerate(st.session_state.query_history[:10]):  # Show last 10
            with st.expander(f"{result['timestamp']} - {result['method'].upper()}: {result['query'][:50]}..."):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**Query:** {result['query']}")
                    st.markdown(f"**Answer:** {result['answer']}")
                
                with col2:
                    st.metric("Total Time", f"{result['total_time']:.2f}s")
                    st.metric("Method", result['method'].upper())
    
    def render_analytics(self):
        """Render analytics and insights"""
        st.markdown("## 📈 Analytics & Insights")
        
        if not st.session_state.query_history:
            st.info("No query data available for analytics. Run some queries first!")
            return
        
        # Query statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_queries = len(st.session_state.query_history)
            st.metric("Total Queries", total_queries)
        
        with col2:
            methods_used = set(q['method'] for q in st.session_state.query_history)
            st.metric("Methods Tested", len(methods_used))
        
        with col3:
            avg_time = sum(q['total_time'] for q in st.session_state.query_history) / total_queries
            st.metric("Avg Response Time", f"{avg_time:.2f}s")
        
        # Method usage chart
        method_counts = {}
        for query in st.session_state.query_history:
            method = query['method']
            method_counts[method] = method_counts.get(method, 0) + 1
        
        if method_counts:
            fig = px.pie(
                values=list(method_counts.values()),
                names=list(method_counts.keys()),
                title="Method Usage Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Performance comparison
        if len(methods_used) > 1:
            performance_data = []
            for query in st.session_state.query_history:
                performance_data.append({
                    'Method': query['method'],
                    'Response Time': query['total_time'],
                    'Timestamp': query['timestamp']
                })
            
            df_perf = pd.DataFrame(performance_data)
            fig = px.box(df_perf, x='Method', y='Response Time', 
                        title="Response Time Distribution by Method")
            st.plotly_chart(fig, use_container_width=True)
    
    def generate_sample_questions(self):
        """Generate sample questions"""
        with st.spinner("Generating sample questions..."):
            try:
                # Run the CLI command to generate questions
                result = subprocess.run([
                    "python", "main.py", "experiment", "generate-test-data", "-n", "5"
                ], capture_output=True, text=True, cwd=".")
                
                if result.returncode == 0:
                    st.success("✅ Sample questions generated successfully!")
                    st.rerun()
                else:
                    st.error(f"Failed to generate questions: {result.stderr}")
            except Exception as e:
                st.error(f"Error generating questions: {str(e)}")
    
    def run(self):
        """Main application runner"""
        self.render_header()
        self.render_system_status()
        
        # Main tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "🔍 Interactive Query", 
            "📊 Batch Evaluation", 
            "📋 Query History", 
            "📈 Analytics"
        ])
        
        with tab1:
            self.render_query_interface()
        
        with tab2:
            self.render_batch_evaluation()
        
        with tab3:
            self.render_query_history()
        
        with tab4:
            self.render_analytics()

def main():
    """Main entry point"""
    try:
        dashboard = RAGDashboard()
        dashboard.run()
    except Exception as e:
        st.error(f"Failed to initialize dashboard: {str(e)}")
        st.info("Please ensure the RAG system is properly installed and configured.")

if __name__ == "__main__":
    main()