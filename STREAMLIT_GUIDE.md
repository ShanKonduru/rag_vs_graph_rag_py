# 🚀 Streamlit Dashboard Guide

## 📊 RAG Comparison Dashboard

The Streamlit dashboard provides an interactive web interface for testing and comparing the three RAG methods with real-time visualizations and comprehensive analytics.

## 🎯 **Quick Start**

### **Option 1: Demo Mode (No Setup Required)**
```bash
# Windows
.\run_streamlit.bat demo

# Unix/Linux
./run_streamlit.sh demo
```

### **Option 2: Full System Mode (Requires Setup)**
```bash
# Windows
.\run_streamlit.bat

# Unix/Linux
./run_streamlit.sh
```

## 📱 **Dashboard Features**

### **🔍 Interactive Query Testing**
- **Real-time Query Interface**: Test questions against all three methods
- **Method Selection**: Choose between RAG, Graph RAG, or Knowledge Graph Only
- **Sample Questions**: Pre-built questions for quick testing
- **Performance Metrics**: Live timing and quality measurements
- **Response Analysis**: Detailed breakdown of retrieval and generation

### **📊 Performance Comparison**
- **Side-by-side Metrics**: Compare F1, ROUGE-L, BLEU, and Exact Match scores
- **Interactive Charts**: Plotly-powered visualizations
- **Performance Insights**: Automated analysis of method strengths
- **Historical Tracking**: Query history with performance trends

### **📚 Knowledge Base Explorer**
- **Content Overview**: Browse the AI knowledge base structure
- **Entity Relationships**: Visualize knowledge graph connections
- **Coverage Analysis**: See topic distribution and depth
- **Real-world Examples**: Explore industry use cases

### **🔧 System Monitoring**
- **Service Status**: Real-time health checks for all components
- **Setup Instructions**: Integrated guidance for system configuration
- **Error Handling**: Graceful fallbacks and helpful error messages
- **Performance Monitoring**: Resource usage and response times

## 🎨 **Dashboard Sections**

### **1. Query Testing Tab**
```
🔍 Interactive Query Testing
├── Query Input Field
├── Method Selection (RAG/Graph RAG/KG Only)
├── Sample Questions Library
├── Real-time Results Display
└── Performance Metrics (Timing, Quality)
```

### **2. Performance Tab**
```
📊 Performance Comparison
├── Metrics Comparison Table
├── Interactive Performance Charts
├── Method Rankings
├── Quality vs Speed Analysis
└── Statistical Insights
```

### **3. Knowledge Base Tab**
```
📚 Knowledge Base Information
├── Content Coverage Overview
├── Entity and Relationship Stats
├── Topic Distribution
├── Real-world Examples
└── Knowledge Depth Analysis
```

### **4. Method Details Tab**
```
🔍 Method Comparison Details
├── Architecture Explanations
├── Strengths and Weaknesses
├── Use Case Recommendations
├── Technical Implementation
└── Performance Characteristics
```

### **5. Analytics Tab**
```
📈 Analytics & Insights
├── Usage Statistics
├── Performance Trends
├── Method Effectiveness
├── Optimization Recommendations
└── System Health Metrics
```

## 💡 **Usage Examples**

### **Testing a Question**
1. Navigate to "🔍 Query Testing" tab
2. Enter your question: *"What is artificial intelligence?"*
3. Select method: *Graph RAG*
4. Click "🚀 Run Query"
5. View results with timing and quality metrics

### **Comparing Methods**
1. Go to "📊 Performance" tab
2. View the comparison table showing all metrics
3. Analyze the interactive charts
4. Read the performance insights

### **Exploring Knowledge Base**
1. Open "📚 Knowledge Base" tab
2. Browse content coverage and statistics
3. Explore entity relationships
4. View real-world application examples

## 🎯 **Demo Mode Features**

When running in demo mode (`./run_streamlit.bat demo`), the dashboard provides:

### **✅ Available Features**
- 📊 Complete performance comparison charts
- 📋 Sample evaluation results and metrics
- 🔍 Method comparison interface with demo responses
- 📈 Analytics and insights based on demo data
- 📚 Full knowledge base information display
- 🎯 Interactive method selection and testing

### **📊 Demo Data**
- **Performance Metrics**: Realistic F1, ROUGE-L, BLEU scores
- **Sample Responses**: Method-specific answer examples
- **Timing Data**: Actual performance timing simulations
- **Comparison Charts**: Interactive Plotly visualizations

### **🚀 Demo Benefits**
- **No Setup Required**: Run immediately without system configuration
- **Full UI Experience**: Complete dashboard functionality
- **Educational Value**: Learn about RAG methods and comparisons
- **Decision Making**: Understand which method suits your needs

## 🔧 **Configuration Options**

### **Streamlit Configuration (`.streamlit/config.toml`)**
```toml
[server]
port = 8501
enableCORS = false

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
```

### **Custom Dashboard Settings**
- **Port Configuration**: Default port 8501, configurable
- **Auto-refresh**: Real-time updates for system status
- **Theme Customization**: Professional blue theme
- **Performance Monitoring**: Live system health checks

## 📈 **Advanced Features**

### **🔄 Real-time System Integration**
When the full RAG system is available:
- **Live Query Processing**: Real RAG, Graph RAG, and KG queries
- **Dynamic System Status**: Live service health monitoring
- **Actual Performance Metrics**: Real-time timing and quality measurements
- **Full Evaluation Pipeline**: Complete batch evaluation capabilities

### **📊 Data Export**
- **Query History**: Download query results as CSV
- **Performance Reports**: Export comparison metrics
- **Evaluation Results**: Save detailed evaluation data
- **Configuration Backup**: Export system settings

### **🎯 Customization Options**
- **Query Templates**: Custom question libraries
- **Evaluation Metrics**: Configure additional quality measures
- **Visualization Themes**: Customize chart appearances
- **Dashboard Layout**: Configurable section arrangement

## 🚨 **Troubleshooting**

### **Common Issues**

#### **1. Dashboard Won't Start**
```bash
Error: ModuleNotFoundError: No module named 'streamlit'
```
**Solution**: Install required packages
```bash
pip install streamlit pandas plotly
```

#### **2. Port Already in Use**
```bash
Error: Port 8501 is already in use
```
**Solution**: Use different port
```bash
streamlit run streamlit_demo.py --server.port 8502
```

#### **3. Full System Not Available**
```bash
Warning: Running in demo mode
```
**Solution**: Set up full RAG system
```bash
.\dev_setup.bat
.\run_full_pipeline.bat
```

### **🔧 Manual Installation**
If automatic installation fails:
```bash
# Install core dependencies
pip install streamlit==1.28.0
pip install plotly==5.17.0
pip install pandas==2.0.0

# Run dashboard
streamlit run streamlit_demo.py
```

## 🎉 **Getting Started Checklist**

- [ ] **Install Dependencies**: `pip install streamlit pandas plotly`
- [ ] **Choose Mode**: Demo (immediate) or Full (requires setup)
- [ ] **Launch Dashboard**: `.\run_streamlit.bat [demo]`
- [ ] **Open Browser**: Navigate to `http://localhost:8501`
- [ ] **Explore Features**: Test queries and view comparisons
- [ ] **Analyze Results**: Use performance metrics and insights

## 🌟 **Key Benefits**

### **🔍 For Researchers**
- **Quantitative Comparison**: Detailed metrics across all methods
- **Interactive Testing**: Real-time query experimentation
- **Performance Analysis**: Statistical insights and trends
- **Export Capabilities**: Data export for papers and reports

### **🏢 For Enterprise**
- **Method Selection**: Data-driven decision making
- **Performance Monitoring**: Live system health tracking
- **User-friendly Interface**: Non-technical team access
- **Scalability Planning**: Resource usage insights

### **🎓 For Education**
- **Visual Learning**: Interactive method comparisons
- **Hands-on Experience**: Direct query testing
- **Comprehensive Coverage**: Full RAG ecosystem exploration
- **Real-world Examples**: Industry use case demonstrations

---

**🎯 Ready to explore RAG methods interactively? Launch the dashboard and start comparing!**

**Quick Start**: `.\run_streamlit.bat demo` for immediate access, or `.\run_streamlit.bat` for full functionality.