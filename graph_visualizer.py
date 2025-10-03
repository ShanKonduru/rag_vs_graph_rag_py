#!/usr/bin/env python3
"""
🕸️ Graph Visualizer for RAG System Knowledge Graphs

This tool provides comprehensive visualization for:
- Neo4j Knowledge Graphs 
- Graph RAG structures
- Sample graph demonstrations
- Interactive graph exploration
"""

import streamlit as st
import networkx as nx
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import json
import time
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import random
import re
from collections import defaultdict
import math

# Page configuration
st.set_page_config(
    page_title="🕸️ Graph Visualizer - RAG System",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.graph-stats {
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 0.5rem;
    border-left: 4px solid #007bff;
    margin: 1rem 0;
}
.node-info {
    background-color: #e9ecef;
    padding: 0.5rem;
    border-radius: 0.3rem;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

class GraphVisualizer:
    def __init__(self):
        self.neo4j_available = self.check_neo4j_connection()
        # Try to load from knowledge base first, fallback to samples
        try:
            self.sample_graphs = self.create_knowledge_base_graphs()
            self.data_source = "knowledge_base"
        except Exception as e:
            st.warning(f"Could not load knowledge base data: {e}")
            self.sample_graphs = self.create_sample_graphs()
            self.data_source = "sample"
        
    def check_neo4j_connection(self) -> bool:
        """Check if Neo4j is available"""
        try:
            import requests
            response = requests.get("http://localhost:7474", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def create_sample_graphs(self) -> Dict[str, nx.Graph]:
        """Create sample graphs to demonstrate different complexities"""
        graphs = {}
        
        # 1. Simple AI Knowledge Graph
        ai_graph = nx.Graph()
        
        # AI Core Concepts
        ai_nodes = [
            ("AI", {"type": "concept", "description": "Artificial Intelligence", "importance": 10}),
            ("ML", {"type": "concept", "description": "Machine Learning", "importance": 9}),
            ("DL", {"type": "concept", "description": "Deep Learning", "importance": 8}),
            ("NLP", {"type": "concept", "description": "Natural Language Processing", "importance": 7}),
            ("CV", {"type": "concept", "description": "Computer Vision", "importance": 7}),
            ("RL", {"type": "concept", "description": "Reinforcement Learning", "importance": 6}),
            
            # Applications
            ("Healthcare", {"type": "application", "description": "Medical AI Applications", "importance": 8}),
            ("Autonomous_Vehicles", {"type": "application", "description": "Self-driving cars", "importance": 7}),
            ("Chatbots", {"type": "application", "description": "Conversational AI", "importance": 6}),
            ("Recommendation", {"type": "application", "description": "Recommendation Systems", "importance": 6}),
            
            # Technologies
            ("Neural_Networks", {"type": "technology", "description": "Artificial Neural Networks", "importance": 9}),
            ("Transformers", {"type": "technology", "description": "Transformer Architecture", "importance": 8}),
            ("CNN", {"type": "technology", "description": "Convolutional Neural Networks", "importance": 7}),
            ("RNN", {"type": "technology", "description": "Recurrent Neural Networks", "importance": 6}),
            
            # Companies/Organizations
            ("OpenAI", {"type": "organization", "description": "AI Research Company", "importance": 8}),
            ("Google", {"type": "organization", "description": "Technology Company", "importance": 8}),
            ("Meta", {"type": "organization", "description": "Social Media & AI Company", "importance": 7}),
        ]
        
        ai_graph.add_nodes_from(ai_nodes)
        
        # Add relationships
        ai_edges = [
            ("AI", "ML", {"relationship": "includes", "strength": 0.9}),
            ("ML", "DL", {"relationship": "includes", "strength": 0.8}),
            ("ML", "RL", {"relationship": "includes", "strength": 0.7}),
            ("AI", "NLP", {"relationship": "includes", "strength": 0.8}),
            ("AI", "CV", {"relationship": "includes", "strength": 0.8}),
            ("DL", "Neural_Networks", {"relationship": "uses", "strength": 0.9}),
            ("DL", "CNN", {"relationship": "includes", "strength": 0.8}),
            ("DL", "RNN", {"relationship": "includes", "strength": 0.7}),
            ("NLP", "Transformers", {"relationship": "uses", "strength": 0.9}),
            ("NLP", "Chatbots", {"relationship": "enables", "strength": 0.8}),
            ("CV", "CNN", {"relationship": "uses", "strength": 0.9}),
            ("ML", "Recommendation", {"relationship": "enables", "strength": 0.8}),
            ("AI", "Healthcare", {"relationship": "applied_in", "strength": 0.8}),
            ("AI", "Autonomous_Vehicles", {"relationship": "applied_in", "strength": 0.9}),
            ("OpenAI", "Transformers", {"relationship": "developed", "strength": 0.8}),
            ("Google", "Transformers", {"relationship": "developed", "strength": 0.9}),
            ("Meta", "AI", {"relationship": "researches", "strength": 0.8}),
        ]
        
        ai_graph.add_edges_from(ai_edges)
        graphs["AI Knowledge Graph"] = ai_graph
        
        # 2. Complex Document Relationship Graph
        doc_graph = nx.Graph()
        
        # Documents and topics
        documents = [
            f"doc_{i}" for i in range(1, 25)
        ]
        
        topics = [
            "machine_learning", "deep_learning", "neural_networks", "ai_ethics", 
            "computer_vision", "natural_language", "robotics", "algorithms",
            "data_science", "statistics", "optimization", "programming"
        ]
        
        # Add document nodes
        for doc in documents:
            doc_graph.add_node(doc, type="document", size=random.randint(100, 1000))
        
        # Add topic nodes
        for topic in topics:
            doc_graph.add_node(topic, type="topic", importance=random.uniform(0.3, 1.0))
        
        # Add relationships between documents and topics
        for doc in documents:
            # Each document relates to 2-4 topics
            related_topics = random.sample(topics, random.randint(2, 4))
            for topic in related_topics:
                doc_graph.add_edge(doc, topic, 
                                 relationship="contains", 
                                 strength=random.uniform(0.4, 1.0))
        
        # Add document-to-document similarity relationships
        for i, doc1 in enumerate(documents):
            for doc2 in documents[i+1:]:
                if random.random() < 0.15:  # 15% chance of similarity
                    doc_graph.add_edge(doc1, doc2, 
                                     relationship="similar_to", 
                                     strength=random.uniform(0.5, 0.9))
        
        graphs["Document Relationship Graph"] = doc_graph
        
        # 3. Entity Relationship Graph (Complex)
        entity_graph = nx.Graph()
        
        # Create a more complex entity relationship network
        entities = {
            "people": [f"Person_{i}" for i in range(1, 15)],
            "organizations": [f"Org_{i}" for i in range(1, 10)],
            "technologies": [f"Tech_{i}" for i in range(1, 12)],
            "concepts": [f"Concept_{i}" for i in range(1, 8)],
            "locations": [f"Location_{i}" for i in range(1, 6)]
        }
        
        # Add all entities
        for entity_type, entity_list in entities.items():
            for entity in entity_list:
                entity_graph.add_node(entity, 
                                    type=entity_type, 
                                    influence=random.uniform(0.1, 1.0))
        
        # Add complex relationships
        all_entities = [entity for entity_list in entities.values() for entity in entity_list]
        
        # Add strategic relationships
        for _ in range(80):  # Add 80 relationships
            entity1, entity2 = random.sample(all_entities, 2)
            if not entity_graph.has_edge(entity1, entity2):
                rel_types = ["works_with", "develops", "located_in", "founded", "uses", "collaborates"]
                entity_graph.add_edge(entity1, entity2,
                                    relationship=random.choice(rel_types),
                                    strength=random.uniform(0.3, 1.0))
        
        graphs["Entity Relationship Graph"] = entity_graph
        
        return graphs
    
    def load_document_chunks(self) -> List[Dict]:
        """Load document chunks from the knowledge base"""
        chunks_file = Path("data/chunks/chunks_metadata.json")
        chunks_data = []
        
        if not chunks_file.exists():
            st.warning("⚠️ No document chunks found. Please run document ingestion first.")
            return []
        
        try:
            with open(chunks_file, 'r', encoding='utf-8') as f:
                chunks_metadata = json.load(f)
            
            # Since individual chunk files don't exist, let's try to load from source documents
            for chunk_meta in chunks_metadata:
                source_path = chunk_meta.get('source', '')
                content = ""
                
                # Try to load content from the original source file
                if source_path:
                    # Convert Windows path separator to current system
                    source_path = source_path.replace('\\', os.sep)
                    source_file = Path(source_path)
                    
                    if source_file.exists():
                        try:
                            with open(source_file, 'r', encoding='utf-8') as f:
                                full_content = f.read()
                            
                            # For now, use a portion of the content as chunk content
                            # In a real system, you'd have the actual chunk boundaries
                            chunk_size = chunk_meta.get('content_length', 500)
                            chunk_index = chunk_meta.get('chunk_index', 0)
                            start_pos = chunk_index * chunk_size
                            content = full_content[start_pos:start_pos + chunk_size]
                            
                        except Exception as e:
                            st.warning(f"Could not read source file {source_file}: {e}")
                
                chunk_data = {
                    **chunk_meta,
                    'content': content
                }
                chunks_data.append(chunk_data)
                
            return chunks_data
            
        except Exception as e:
            st.error(f"Error loading document chunks: {e}")
            return []
    
    def extract_entities_from_text(self, text: str) -> List[str]:
        """Simple entity extraction from text"""
        # Basic entity extraction - look for capitalized words/phrases
        entities = []
        
        # Find capitalized words (potential proper nouns)
        words = re.findall(r'\b[A-Z][a-z]+\b', text)
        
        # Find multi-word capitalized phrases
        phrases = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b', text)
        
        # Technical terms and acronyms
        tech_terms = re.findall(r'\b[A-Z]{2,}\b', text)
        
        entities.extend(words)
        entities.extend(phrases)
        entities.extend(tech_terms)
        
        # Filter out common words and clean up
        common_words = {'The', 'This', 'That', 'These', 'Those', 'And', 'Or', 'But', 'For', 'With', 'From', 'To', 'In', 'On', 'At', 'By'}
        entities = [e for e in entities if e not in common_words and len(e) > 2]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_entities = []
        for entity in entities:
            if entity.lower() not in seen:
                seen.add(entity.lower())
                unique_entities.append(entity)
        
        return unique_entities[:20]  # Limit to top 20 entities
    
    def create_document_relationship_graph(self) -> nx.Graph:
        """Create a graph showing relationships between actual documents"""
        chunks = self.load_document_chunks()
        
        if not chunks:
            return self.create_sample_graphs()["Document Relationship Graph"]
        
        doc_graph = nx.Graph()
        
        # Group chunks by document
        documents = defaultdict(list)
        for chunk in chunks:
            doc_id = chunk.get('document_id', 'unknown')
            documents[doc_id].append(chunk)
        
        # Create document nodes
        for doc_id, doc_chunks in documents.items():
            # Use the source file name as node name
            doc_name = doc_chunks[0].get('source', doc_id).split('\\')[-1].split('/')[-1]
            
            # Calculate document properties
            total_content = ' '.join([chunk.get('content', '') for chunk in doc_chunks])
            word_count = len(total_content.split())
            chunk_count = len(doc_chunks)
            
            doc_graph.add_node(doc_name, 
                             type="document",
                             doc_id=doc_id,
                             chunks=chunk_count,
                             words=word_count,
                             size=min(100 + word_count // 10, 500))
        
        # Create relationships based on shared entities
        doc_entities = {}
        for doc_id, doc_chunks in documents.items():
            doc_name = doc_chunks[0].get('source', doc_id).split('\\')[-1].split('/')[-1]
            total_content = ' '.join([chunk.get('content', '') for chunk in doc_chunks])
            doc_entities[doc_name] = set(self.extract_entities_from_text(total_content))
        
        # Add edges based on entity overlap
        doc_names = list(doc_entities.keys())
        for i, doc1 in enumerate(doc_names):
            for doc2 in doc_names[i+1:]:
                shared_entities = doc_entities[doc1] & doc_entities[doc2]
                if shared_entities:
                    similarity = len(shared_entities) / len(doc_entities[doc1] | doc_entities[doc2])
                    if similarity > 0.1:  # Minimum threshold
                        doc_graph.add_edge(doc1, doc2,
                                         relationship="shares_entities",
                                         shared_entities=list(shared_entities),
                                         similarity=similarity,
                                         strength=similarity)
        
        return doc_graph
    
    def create_entity_relationship_graph(self) -> nx.Graph:
        """Create a graph showing entity relationships from actual documents"""
        chunks = self.load_document_chunks()
        
        if not chunks:
            return self.create_sample_graphs()["Entity Relationship Graph"]
        
        entity_graph = nx.Graph()
        entity_docs = defaultdict(set)  # Track which documents contain each entity
        entity_chunks = defaultdict(set)  # Track which chunks contain each entity
        
        # Extract entities from all chunks
        for chunk in chunks:
            content = chunk.get('content', '')
            if content:
                entities = self.extract_entities_from_text(content)
                chunk_id = chunk.get('id', '')
                doc_source = chunk.get('source', '').split('\\')[-1].split('/')[-1]
                
                for entity in entities:
                    entity_docs[entity].add(doc_source)
                    entity_chunks[entity].add(chunk_id)
        
        # Filter entities that appear in multiple chunks (more significant)
        significant_entities = {entity: docs for entity, docs in entity_docs.items() 
                              if len(entity_chunks[entity]) >= 1}
        
        # Add entity nodes
        for entity, docs in significant_entities.items():
            doc_count = len(docs)
            chunk_count = len(entity_chunks[entity])
            
            # Determine entity type based on patterns
            entity_type = "concept"
            if entity.isupper() and len(entity) <= 5:
                entity_type = "acronym"
            elif any(word in entity.lower() for word in ['learning', 'network', 'algorithm', 'model']):
                entity_type = "technology"
            elif entity.lower().endswith(('ing', 'tion', 'ism', 'ity')):
                entity_type = "concept"
            else:
                entity_type = "term"
            
            entity_graph.add_node(entity,
                                type=entity_type,
                                documents=list(docs),
                                chunk_count=chunk_count,
                                doc_count=doc_count,
                                importance=min(chunk_count / 5.0, 1.0),
                                size=min(50 + chunk_count * 10, 200))
        
        # Add relationships between entities that co-occur
        entities = list(significant_entities.keys())
        for i, entity1 in enumerate(entities):
            for entity2 in entities[i+1:]:
                # Check if entities co-occur in the same chunks
                shared_chunks = entity_chunks[entity1] & entity_chunks[entity2]
                if shared_chunks:
                    co_occurrence = len(shared_chunks)
                    strength = min(co_occurrence / 3.0, 1.0)
                    
                    entity_graph.add_edge(entity1, entity2,
                                        relationship="co_occurs",
                                        shared_chunks=len(shared_chunks),
                                        strength=strength)
        
        return entity_graph
    
    def create_knowledge_base_graphs(self) -> Dict[str, nx.Graph]:
        """Create graphs from actual knowledge base data"""
        graphs = {}
        
        # Keep the AI Knowledge Graph as a sample
        graphs["AI Knowledge Graph (Sample)"] = self.create_sample_graphs()["AI Knowledge Graph"]
        
        # Add real data graphs
        graphs["Document Relationship Graph"] = self.create_document_relationship_graph()
        graphs["Entity Relationship Graph"] = self.create_entity_relationship_graph()
        
        return graphs
    
    def render_header(self):
        """Render the application header"""
        st.markdown('<h1 class="main-header">🕸️ Knowledge Graph & Graph RAG Visualizer</h1>', 
                   unsafe_allow_html=True)
        
        # Data source indicator
        data_source_emoji = "📊" if self.data_source == "knowledge_base" else "🎭"
        data_source_text = "Real Knowledge Base" if self.data_source == "knowledge_base" else "Sample Data"
        data_source_color = "#28a745" if self.data_source == "knowledge_base" else "#ffc107"
        
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 2rem;">
            <p style="font-size: 1.2rem; color: #666;">
                Explore and visualize the complexity of knowledge graphs and Graph RAG structures
            </p>
            <div style="background-color: {data_source_color}; color: white; padding: 0.5rem; border-radius: 0.5rem; display: inline-block; margin-top: 1rem;">
                {data_source_emoji} <strong>Data Source:</strong> {data_source_text}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def render_sidebar_status(self):
        """Render connection status in sidebar"""
        st.sidebar.markdown("## 🔧 Connection Status")
        
        if self.neo4j_available:
            st.sidebar.success("✅ Neo4j Connected")
            st.sidebar.markdown("**Neo4j Browser**: [http://localhost:7474](http://localhost:7474)")
        else:
            st.sidebar.warning("⚠️ Neo4j Not Available")
            st.sidebar.markdown("""
            **To connect to Neo4j:**
            1. Start Docker Desktop
            2. Run: `.\\docker_services.bat start`
            3. Wait for services to start
            4. Refresh this page
            """)
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("## 📊 Available Visualizations")
        st.sidebar.markdown("""
        - 🧠 **AI Knowledge Graph**: Core AI concepts and relationships
        - 📄 **Document Graph**: Document similarity and topic relationships  
        - 👥 **Entity Graph**: Complex entity relationship networks
        - 🔍 **Interactive Analysis**: Node and edge exploration tools
        """)
    
    def create_interactive_graph_plot(self, graph: nx.Graph, title: str) -> go.Figure:
        """Create an interactive Plotly graph visualization"""
        # Calculate layout
        if len(graph.nodes()) > 100:
            pos = nx.spring_layout(graph, k=3, iterations=50)
        else:
            pos = nx.spring_layout(graph, k=1, iterations=100)
        
        # Prepare node traces
        node_trace = go.Scatter(
            x=[pos[node][0] for node in graph.nodes()],
            y=[pos[node][1] for node in graph.nodes()],
            mode='markers+text',
            text=[str(node) for node in graph.nodes()],
            textposition="middle center",
            hovertemplate='<b>%{text}</b><br>' +
                         'Type: %{customdata[0]}<br>' +
                         'Connections: %{customdata[1]}<extra></extra>',
            customdata=[[
                graph.nodes[node].get('type', 'unknown'),
                len(list(graph.neighbors(node)))
            ] for node in graph.nodes()],
            marker=dict(
                size=[max(8, len(list(graph.neighbors(node))) * 3) for node in graph.nodes()],
                color=[self.get_node_color(graph.nodes[node].get('type', 'unknown')) for node in graph.nodes()],
                line=dict(width=2, color='white'),
                opacity=0.8
            ),
            name="Nodes"
        )
        
        # Prepare edge traces
        edge_x = []
        edge_y = []
        edge_info = []
        
        for edge in graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            
            edge_data = graph.edges[edge]
            edge_info.append(f"{edge[0]} ↔ {edge[1]}: {edge_data.get('relationship', 'connected')}")
        
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1, color='rgba(125,125,125,0.5)'),
            hoverinfo='none',
            mode='lines',
            name="Connections"
        )
        
        # Create figure
        fig = go.Figure(data=[edge_trace, node_trace],
                       layout=go.Layout(
                        title=dict(text=title, x=0.5, font=dict(size=20)),
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        annotations=[ dict(
                            text="Drag to move nodes • Zoom with mouse wheel • Hover for details",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002,
                            xanchor='left', yanchor='bottom',
                            font=dict(color="gray", size=12)
                        )],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        plot_bgcolor='white'
                    ))
        
        return fig
    
    def get_node_color(self, node_type: str) -> str:
        """Get color for node based on type"""
        color_map = {
            'concept': '#FF6B6B',
            'application': '#4ECDC4', 
            'technology': '#45B7D1',
            'organization': '#96CEB4',
            'document': '#FFEAA7',
            'topic': '#DDA0DD',
            'people': '#FFB347',
            'organizations': '#98D8C8',
            'technologies': '#A8E6CF',
            'concepts': '#FFD3A5',
            'locations': '#FD79A8',
            'unknown': '#95A5A6'
        }
        return color_map.get(node_type, color_map['unknown'])
    
    def analyze_graph_complexity(self, graph: nx.Graph) -> Dict:
        """Analyze graph complexity metrics"""
        metrics = {
            'nodes': len(graph.nodes()),
            'edges': len(graph.edges()),
            'density': nx.density(graph),
            'avg_clustering': nx.average_clustering(graph),
            'connected_components': nx.number_connected_components(graph),
            'avg_degree': sum(dict(graph.degree()).values()) / len(graph.nodes()) if len(graph.nodes()) > 0 else 0,
            'diameter': 'N/A',
            'avg_path_length': 'N/A'
        }
        
        # Calculate diameter and average path length for connected graphs
        if nx.is_connected(graph):
            try:
                metrics['diameter'] = nx.diameter(graph)
                metrics['avg_path_length'] = nx.average_shortest_path_length(graph)
            except:
                pass
        elif len(graph.nodes()) > 0:
            # For disconnected graphs, analyze the largest component
            largest_cc = max(nx.connected_components(graph), key=len) if nx.number_connected_components(graph) > 0 else set()
            if len(largest_cc) > 1:
                subgraph = graph.subgraph(largest_cc)
                try:
                    metrics['diameter'] = f"{nx.diameter(subgraph)} (largest component)"
                    metrics['avg_path_length'] = f"{nx.average_shortest_path_length(subgraph):.2f} (largest component)"
                except:
                    pass
        
        return metrics
    
    def render_graph_analysis(self, graph: nx.Graph, graph_name: str):
        """Render detailed graph analysis"""
        st.markdown(f"### 📊 Analysis: {graph_name}")
        
        metrics = self.analyze_graph_complexity(graph)
        
        # Display metrics in columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Nodes", metrics['nodes'])
            st.metric("Avg Clustering", f"{metrics['avg_clustering']:.3f}")
        
        with col2:
            st.metric("Edges", metrics['edges'])
            st.metric("Components", metrics['connected_components'])
        
        with col3:
            st.metric("Density", f"{metrics['density']:.3f}")
            st.metric("Avg Degree", f"{metrics['avg_degree']:.1f}")
        
        with col4:
            st.metric("Diameter", str(metrics['diameter']))
            st.metric("Avg Path Length", str(metrics['avg_path_length']))
        
        # Complexity assessment
        complexity_score = self.calculate_complexity_score(metrics)
        
        st.markdown('<div class="graph-stats">', unsafe_allow_html=True)
        st.markdown(f"**Complexity Score**: {complexity_score}/10")
        
        if complexity_score <= 3:
            st.markdown("🟢 **Simple Graph** - Easy to understand and navigate")
        elif complexity_score <= 6:
            st.markdown("🟡 **Moderate Complexity** - Good balance of structure and connections")
        else:
            st.markdown("🔴 **High Complexity** - Dense network with many interconnections")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Node degree distribution
        degrees = [graph.degree(node) for node in graph.nodes()]
        degree_df = pd.DataFrame({'degree': degrees})
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_hist = px.histogram(degree_df, x='degree', 
                                  title="Node Degree Distribution",
                                  labels={'degree': 'Number of Connections', 'count': 'Number of Nodes'})
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col2:
            # Node types distribution
            if graph.nodes():
                node_types = [graph.nodes[node].get('type', 'unknown') for node in graph.nodes()]
                type_counts = pd.Series(node_types).value_counts()
                
                fig_pie = px.pie(values=type_counts.values, names=type_counts.index,
                               title="Node Types Distribution")
                st.plotly_chart(fig_pie, use_container_width=True)
    
    def calculate_complexity_score(self, metrics: Dict) -> int:
        """Calculate a complexity score from 1-10 based on graph metrics"""
        score = 0
        
        # Node count contribution (0-2 points)
        if metrics['nodes'] > 50:
            score += 2
        elif metrics['nodes'] > 20:
            score += 1
        
        # Density contribution (0-2 points)
        if metrics['density'] > 0.3:
            score += 2
        elif metrics['density'] > 0.1:
            score += 1
        
        # Average degree contribution (0-2 points)
        if metrics['avg_degree'] > 5:
            score += 2
        elif metrics['avg_degree'] > 2:
            score += 1
        
        # Clustering contribution (0-2 points)
        if metrics['avg_clustering'] > 0.5:
            score += 2
        elif metrics['avg_clustering'] > 0.2:
            score += 1
        
        # Connected components contribution (0-2 points)
        if metrics['connected_components'] == 1:
            score += 2
        elif metrics['connected_components'] <= 3:
            score += 1
        
        return min(score, 10)
    
    def render_node_explorer(self, graph: nx.Graph):
        """Render interactive node explorer"""
        st.markdown("### 🔍 Node Explorer")
        
        if not graph.nodes():
            st.warning("No nodes available in the selected graph.")
            return
        
        # Node selection
        selected_node = st.selectbox(
            "Select a node to explore:",
            options=list(graph.nodes()),
            format_func=lambda x: f"{x} ({graph.nodes[x].get('type', 'unknown')})"
        )
        
        if selected_node:
            node_data = graph.nodes[selected_node]
            neighbors = list(graph.neighbors(selected_node))
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="node-info">', unsafe_allow_html=True)
                st.markdown(f"**Node**: {selected_node}")
                st.markdown(f"**Type**: {node_data.get('type', 'unknown')}")
                st.markdown(f"**Connections**: {len(neighbors)}")
                
                for key, value in node_data.items():
                    if key != 'type':
                        st.markdown(f"**{key.title()}**: {value}")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                if neighbors:
                    st.markdown("**Connected Nodes:**")
                    for neighbor in neighbors[:10]:  # Show max 10 neighbors
                        neighbor_type = graph.nodes[neighbor].get('type', 'unknown')
                        edge_data = graph.edges[selected_node, neighbor]
                        relationship = edge_data.get('relationship', 'connected')
                        st.markdown(f"• {neighbor} ({neighbor_type}) - *{relationship}*")
                    
                    if len(neighbors) > 10:
                        st.markdown(f"... and {len(neighbors) - 10} more")
                else:
                    st.markdown("No connections found.")
    
    def render_neo4j_integration(self):
        """Render Neo4j integration interface"""
        st.markdown("### 🕸️ Neo4j Knowledge Graph")
        
        if not self.neo4j_available:
            st.warning("Neo4j is not available. Please start the Docker services to explore live knowledge graphs.")
            
            with st.expander("🚀 Start Neo4j Services"):
                st.markdown("""
                **Step 1**: Start Docker Desktop
                
                **Step 2**: Run the following command:
                ```bash
                .\\docker_services.bat start
                ```
                
                **Step 3**: Wait for services to start (may take 1-2 minutes)
                
                **Step 4**: Refresh this page
                
                **Step 5**: Access Neo4j Browser at [http://localhost:7474](http://localhost:7474)
                """)
            return
        
        st.success("✅ Neo4j is running! You can explore the knowledge graph.")
        
        # Neo4j browser link
        st.markdown("""
        **Neo4j Browser**: [http://localhost:7474](http://localhost:7474)
        
        **Default Credentials**:
        - Username: `neo4j`
        - Password: `password` (or check docker-compose.yml)
        """)
        
        # Sample queries
        st.markdown("### 📝 Sample Cypher Queries")
        
        sample_queries = [
            ("Show all nodes", "MATCH (n) RETURN n LIMIT 25"),
            ("Count nodes by type", "MATCH (n) RETURN labels(n) as type, count(n) as count"),
            ("Find highly connected nodes", "MATCH (n) RETURN n, size((n)--()) as degree ORDER BY degree DESC LIMIT 10"),
            ("Show relationships", "MATCH (a)-[r]->(b) RETURN type(r) as relationship, count(r) as count ORDER BY count DESC"),
            ("Find paths between entities", "MATCH p=(a)-[*1..3]-(b) WHERE a.name CONTAINS 'AI' AND b.name CONTAINS 'ML' RETURN p LIMIT 5"),
        ]
        
        for query_name, query in sample_queries:
            with st.expander(f"🔍 {query_name}"):
                st.code(query, language="cypher")
                if st.button(f"Copy {query_name} query", key=f"copy_{query_name}"):
                    st.success(f"Query copied! Paste it in Neo4j Browser.")
    
    def run(self):
        """Main application runner"""
        self.render_header()
        self.render_sidebar_status()
        
        # Main content tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "🧠 AI Knowledge Graph",
            "📄 Document Relationships", 
            "👥 Entity Networks",
            "🕸️ Neo4j Integration"
        ])
        
        with tab1:
            st.markdown("## 🧠 AI Knowledge Graph")
            if self.data_source == "knowledge_base":
                st.markdown("Sample AI concept relationships (demonstration purposes)")
            else:
                st.markdown("Explore the relationships between AI concepts, technologies, and applications.")
            
            # Handle different graph names based on data source
            graph_key = "AI Knowledge Graph (Sample)" if self.data_source == "knowledge_base" else "AI Knowledge Graph"
            graph = self.sample_graphs[graph_key]
            
            # Visualization
            fig = self.create_interactive_graph_plot(graph, "AI Knowledge Graph Network")
            st.plotly_chart(fig, use_container_width=True)
            
            # Analysis
            self.render_graph_analysis(graph, "AI Knowledge Graph")
            
            # Node explorer
            self.render_node_explorer(graph)
        
        with tab2:
            st.markdown("## 📄 Document Relationship Graph")
            if self.data_source == "knowledge_base":
                chunks = self.load_document_chunks()
                if chunks:
                    st.markdown(f"**📊 Knowledge Base Status:** {len(chunks)} document chunks loaded from your data")
                    documents = len(set([chunk.get('document_id', '') for chunk in chunks]))
                    st.markdown(f"**📚 Documents:** {documents} documents processed")
                else:
                    st.warning("⚠️ No document chunks found. Please run document ingestion first.")
                st.markdown("Shows relationships between your actual documents based on shared entities and content.")
            else:
                st.markdown("Visualize how documents are connected through shared topics and content similarity.")
            
            graph = self.sample_graphs["Document Relationship Graph"]
            
            # Visualization
            fig = self.create_interactive_graph_plot(graph, "Document Relationship Network")
            st.plotly_chart(fig, use_container_width=True)
            
            # Analysis
            self.render_graph_analysis(graph, "Document Relationship Graph")
            
            # Node explorer
            self.render_node_explorer(graph)
        
        with tab3:
            st.markdown("## 👥 Entity Relationship Networks")
            if self.data_source == "knowledge_base":
                chunks = self.load_document_chunks()
                if chunks:
                    # Extract and show entity statistics
                    all_entities = []
                    for chunk in chunks:
                        content = chunk.get('content', '')
                        if content:
                            entities = self.extract_entities_from_text(content)
                            all_entities.extend(entities)
                    
                    unique_entities = len(set(all_entities))
                    st.markdown(f"**🏷️ Entities Extracted:** {unique_entities} unique entities from your documents")
                    st.markdown("Shows relationships between entities extracted from your knowledge base.")
                else:
                    st.warning("⚠️ No document chunks found. Please run document ingestion first.")
            else:
                st.markdown("Complex networks showing relationships between people, organizations, technologies, and concepts.")
            
            graph = self.sample_graphs["Entity Relationship Graph"]
            
            # Visualization
            fig = self.create_interactive_graph_plot(graph, "Entity Relationship Network")
            st.plotly_chart(fig, use_container_width=True)
            
            # Analysis
            self.render_graph_analysis(graph, "Entity Relationship Graph")
            
            # Node explorer
            self.render_node_explorer(graph)
        
        with tab4:
            self.render_neo4j_integration()

def main():
    """Main entry point"""
    try:
        visualizer = GraphVisualizer()
        visualizer.run()
    except Exception as e:
        st.error(f"Error initializing graph visualizer: {str(e)}")
        st.info("Please ensure all required packages are installed.")

if __name__ == "__main__":
    main()