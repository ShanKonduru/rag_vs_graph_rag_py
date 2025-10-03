# 🕸️ Graph Visualizer Guide

## 📊 Knowledge Graph & Graph RAG Visualization

This interactive tool provides comprehensive visualization for exploring the complexity of knowledge graphs and Graph RAG structures in your RAG system.

## 🚀 **Quick Start**

### **Launch Graph Visualizer**
```bash
# Windows
.\run_graph_visualizer.bat

# Unix/Linux
./run_graph_visualizer.sh
```

**Visualizer URL**: [http://localhost:8502](http://localhost:8502)

## 🎯 **What You Can Visualize**

### **1. 🧠 AI Knowledge Graph**
- **Core AI concepts** and their relationships
- **Technology dependencies** (ML → DL → Neural Networks)
- **Application domains** (Healthcare, Autonomous Vehicles, etc.)
- **Company/Organization connections**

**Complexity Features**:
- 17 nodes with strategic relationships
- Hierarchical concept organization
- Multi-domain applications
- Real-world technology mappings

### **2. 📄 Document Relationship Graph**
- **Document similarity networks** based on content
- **Shared topic relationships** between documents
- **Content clustering** visualization
- **Topic distribution** analysis

**Complexity Features**:
- 24+ documents with topic connections
- 12 different AI/ML topics
- Cross-document similarity links
- Dynamic relationship strength

### **3. 👥 Entity Relationship Graph**
- **Complex entity networks** (People, Organizations, Technologies)
- **Multi-type relationships** (works_with, develops, collaborates)
- **Influence mapping** and connection strength
- **Network analysis** of entity clusters

**Complexity Features**:
- 50+ entities across 5 categories
- 80+ strategic relationships
- Multi-layered connection types
- Realistic organizational structures

### **4. 🕸️ Neo4j Integration**
- **Live Neo4j connection** (when Docker services are running)
- **Real knowledge graph exploration**
- **Cypher query examples**
- **Production graph analysis**

## 📈 **Graph Complexity Analysis**

### **Metrics Displayed**
- **Nodes & Edges**: Basic graph size
- **Density**: How interconnected the graph is (0-1 scale)
- **Average Clustering**: Local connectivity patterns
- **Connected Components**: Number of separate graph parts
- **Average Degree**: Average connections per node
- **Diameter**: Longest shortest path in the graph
- **Average Path Length**: Typical distance between nodes

### **Complexity Scoring (1-10 Scale)**
- **1-3**: 🟢 Simple graphs (easy to understand)
- **4-6**: 🟡 Moderate complexity (balanced structure)
- **7-10**: 🔴 High complexity (dense, interconnected networks)

**Scoring Factors**:
- Node count (more nodes = higher complexity)
- Graph density (more connections = higher complexity)
- Average degree (highly connected nodes = higher complexity)
- Clustering coefficient (local connectivity patterns)
- Component connectivity (single vs. multiple components)

## 🔍 **Interactive Features**

### **Graph Visualization**
- **Drag and zoom** for detailed exploration
- **Node hover** for detailed information
- **Color coding** by node type
- **Size scaling** based on connection count
- **Relationship visualization** with edge labels

### **Node Explorer**
- **Select any node** to see detailed information
- **View all connections** and relationship types
- **Explore neighbor networks**
- **Analyze node properties** and metadata

### **Statistical Analysis**
- **Degree distribution** histograms
- **Node type** distribution pie charts
- **Complexity assessment** with explanations
- **Network health** indicators

## 🕸️ **Neo4j Integration**

### **When Neo4j is Available**
If you have Neo4j running (via Docker services), you can:

1. **Explore live knowledge graphs** created by your RAG system
2. **Run Cypher queries** to analyze graph structure
3. **View real entity relationships** from your documents
4. **Analyze actual Graph RAG** construction patterns

### **Sample Cypher Queries**
```cypher
// Show all nodes
MATCH (n) RETURN n LIMIT 25

// Count nodes by type  
MATCH (n) RETURN labels(n) as type, count(n) as count

// Find highly connected nodes
MATCH (n) RETURN n, size((n)--()) as degree ORDER BY degree DESC LIMIT 10

// Show relationship types
MATCH (a)-[r]->(b) RETURN type(r) as relationship, count(r) as count ORDER BY count DESC

// Find paths between entities
MATCH p=(a)-[*1..3]-(b) WHERE a.name CONTAINS 'AI' AND b.name CONTAINS 'ML' RETURN p LIMIT 5
```

### **Starting Neo4j Services**
```bash
# Start Docker services
.\docker_services.bat start

# Check status
.\docker_services.bat status

# Access Neo4j Browser
# URL: http://localhost:7474
# Username: neo4j
# Password: password (check docker-compose.yml)
```

## 🎨 **Understanding Graph Complexity**

### **Simple Graphs (Score 1-3)**
- **Few nodes** (< 20)
- **Low density** (< 0.1)
- **Linear or tree-like** structures
- **Easy to understand** relationships

**Example**: Basic concept hierarchies, simple workflows

### **Moderate Complexity (Score 4-6)**
- **Medium nodes** (20-50)
- **Moderate density** (0.1-0.3)
- **Some clustering** and cross-connections
- **Balanced structure** with clear patterns

**Example**: Department organizational charts, technology stacks

### **High Complexity (Score 7-10)**
- **Many nodes** (50+)
- **High density** (> 0.3)
- **Dense clustering** and multiple connection types
- **Complex patterns** requiring careful analysis

**Example**: Enterprise knowledge graphs, social networks, complex research domains

## 🔧 **Technical Implementation**

### **Graph Generation**
- **NetworkX** for graph data structures
- **Plotly** for interactive visualizations
- **Streamlit** for web interface
- **Strategic node placement** using spring-force algorithms

### **Visualization Features**
- **Node sizing** based on degree centrality
- **Color coding** by semantic type
- **Interactive positioning** with physics simulation
- **Hover tooltips** with detailed metadata

### **Analysis Algorithms**
- **Centrality measures** (degree, betweenness, closeness)
- **Community detection** for clustering analysis
- **Path finding** for relationship exploration
- **Network statistics** for complexity assessment

## 💡 **Use Cases**

### **🔬 Research & Analysis**
- **Understand knowledge structure** in your domain
- **Identify key concepts** and their relationships
- **Analyze information density** and connectivity patterns
- **Plan knowledge graph** expansion strategies

### **🏢 Enterprise Applications**
- **Visualize organizational knowledge**
- **Map technology dependencies**
- **Understand information flow**
- **Plan knowledge management** initiatives

### **🎓 Educational Purposes**
- **Learn graph theory** concepts interactively
- **Understand network analysis** principles
- **Explore real-world** graph structures
- **Compare different** graph types and complexities

## 🚨 **Troubleshooting**

### **Graph Visualizer Won't Start**
```bash
Error: ModuleNotFoundError: No module named 'networkx'
```
**Solution**:
```bash
pip install networkx plotly pandas numpy
```

### **Neo4j Connection Issues**
```bash
⚠️ Neo4j Not Available
```
**Solutions**:
1. **Start Docker Desktop**
2. **Run**: `.\docker_services.bat start`
3. **Wait** for services to start (1-2 minutes)
4. **Refresh** the visualizer page

### **Performance Issues with Large Graphs**
- **Reduce node count** in sample graphs
- **Use simpler layouts** for better performance
- **Filter nodes** by type or importance
- **Use Neo4j Browser** for very large graphs

## 🌟 **Key Benefits**

### **📊 Visual Understanding**
- **See graph complexity** at a glance
- **Identify connection patterns** visually
- **Understand network structures** intuitively
- **Compare different** graph types

### **🔍 Interactive Exploration**
- **Drill down** into specific nodes
- **Explore neighborhoods** around entities
- **Analyze connection** strength and types
- **Navigate large graphs** efficiently

### **📈 Complexity Assessment**
- **Quantify graph complexity** with metrics
- **Compare different** network structures
- **Plan system scalability**
- **Optimize graph design**

---

**🎯 Ready to explore your knowledge graphs?** 

**Quick Start**: `.\run_graph_visualizer.bat` and open [http://localhost:8502](http://localhost:8502)

**Pro Tip**: Start with the AI Knowledge Graph to understand basic patterns, then explore the Document and Entity graphs to see increasing complexity levels!