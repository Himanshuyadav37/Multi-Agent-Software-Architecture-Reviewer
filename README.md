# 🧠 Multi-Agent Software Architecture Reviewer

An intelligent AI-powered system that analyzes software repositories using multiple specialized agents to provide comprehensive architecture, security, and compliance reviews.

## 🚀 Features

- **Multi-Agent Architecture**: Uses specialized agents for different analysis aspects
- **Repository Analysis**: Supports GitHub repository cloning and local file analysis
- **Security Assessment**: Identifies security vulnerabilities and coding risks
- **Architecture Review**: Analyzes code complexity and design patterns
- **Tech Stack Detection**: Automatically identifies technologies used
- **RAG-Powered Q&A**: Ask questions about code using vector search
- **Web Interface**: Beautiful Streamlit-based UI for easy interaction
- **LangGraph Workflow**: Orchestrates multiple agents efficiently

## 🏗️ Architecture Overview

### LangGraph Workflow Design
````
START
  │
  ▼
Repository Loader
  │
  ▼
Supervisor
  │
  ├── Security Agent
  ├── Design Agent
  ├── Compliance Agent
  └── Test Agent
          │
          ▼
   Merge Results Node
          │
          ▼
   Final Report Node
          │
          ▼
         END
```

### Project Structure
````
├── app/
│   ├── agents/                 # AI agents for different analysis types
│   │   ├── architecture_agent.py    # Code complexity and design analysis
│   │   ├── security_agent.py        # Security vulnerability detection
│   │   └── router_agent.py          # Tech stack classification
│   ├── graph/                  # LangGraph workflow definitions
│   │   └── workflow.py             # Main workflow orchestration
│   ├── parsers/                # Code parsing and analysis
│   │   ├── ast_parser.py          # Abstract syntax tree analysis
│   │   └── repo_parser.py          # Repository file parsing
│   ├── prompts/                # Agent prompts
│   │   ├── compliance_prompt.py
│   │   ├── design_prompt.py
│   │   └── security_prompt.py
│   ├── rag/                    # Retrieval-Augmented Generation
│   │   ├── chunker.py             # Document chunking
│   │   ├── embeddings.py          # Text embeddings
│   │   ├── retriever.py           # Vector search retrieval
│   │   └── vector_store.py        # Vector database operations
│   ├── tools/                  # Utility tools
│   └── utils/                  # General utilities
│       └── github_loader.py       # GitHub repository cloning
├── streamlit_app.py           # Main web application
├── main.py                   # CLI interface
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
└── packages.txt             # System dependencies for deployment
```

## 🛠️ Tech Stack

- **Frontend**: Streamlit (Web UI)
- **Backend**: Python 3.8+
- **AI Framework**: LangChain, LangGraph
- **LLM**: Groq (Llama 3.3 70B)
- **Vector Database**: ChromaDB, FAISS
- **Code Analysis**: Radon, Bandit, Tree-sitter
- **Embeddings**: Sentence Transformers
- **Version Control**: GitPython

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Git
- Groq API key

### Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/Multi-Agent-Software-Architecture-Reviewer.git
cd Multi-Agent-Software-Architecture-Reviewer
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your Groq API key
```

5. **Run the application**
```bash
# Web interface
streamlit run streamlit_app.py

# Or CLI interface
python main.py
```

## 🌐 Deployment

### Streamlit Cloud Deployment

1. **Push to GitHub**
   - Ensure your code is pushed to a GitHub repository

2. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Configure environment variables:
     - `GROQ_API_KEY`: Your Groq API key
     - Optional: `HUGGINGFACE_API_KEY`: Hugging Face API key

3. **Deploy**
   - Streamlit Cloud will automatically detect `requirements.txt` and `packages.txt`
   - The app will be live at your chosen URL

### Manual Server Deployment

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install git python3-pip

# Clone and setup
git clone <repository-url>
cd Multi-Agent-Software-Architecture-Reviewer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set environment variables
export GROQ_API_KEY="your_api_key_here"

# Run with systemd or process manager
streamlit run streamlit_app.py --server.port 8501
```

## 🎯 Usage

### Web Interface

1. **Upload Repository**
   - Enter GitHub repository URL
   - Or upload local repository files

2. **Analysis Options**
   - Choose analysis types (Security, Architecture, Compliance)
   - Configure analysis parameters

3. **View Results**
   - Comprehensive reports with findings
   - Interactive code analysis
   - Q&A chat interface

### CLI Interface

```bash
python main.py
```

Follow the prompts to:
1. Enter GitHub repository URL
2. Select analysis options
3. View generated reports

## 🔧 Configuration

### Environment Variables

Create a `.env` file with:

```env
# Required
GROQ_API_KEY=your_groq_api_key_here

# Optional
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
```

### Supported File Types

- **Python**: `.py`
- **JavaScript/TypeScript**: `.js`, `.jsx`, `.ts`, `.tsx`
- **Configuration**: `Dockerfile`, `docker-compose.yml`
- **Documentation**: `.md`, `.txt`
- **Web**: `.html`, `.css`

## 📊 Analysis Types

### 🔒 Security Analysis
- Identifies potential security vulnerabilities
- Analyzes dangerous coding patterns
- Provides severity classification (LOW, MEDIUM, HIGH, CRITICAL)
- Suggests security improvements

### 🏗️ Architecture Analysis
- Code complexity metrics (Cyclomatic complexity)
- Design pattern recognition
- Architecture quality assessment
- Maintainability analysis

### 📋 Compliance Analysis
- Coding standards compliance
- Best practices verification
- Documentation completeness
- License compatibility

## 🤖 Agent System

### Router Agent
- Classifies repository tech stack
- Determines which agents to activate
- Optimizes analysis workflow

### Security Agent
- Performs security-focused code review
- Identifies vulnerabilities and risks
- Generates security reports

### Architecture Agent
- Analyzes code structure and design
- Calculates complexity metrics
- Provides architecture recommendations

## 🔍 RAG System

The system uses Retrieval-Augmented Generation for intelligent code Q&A:

1. **Document Chunking**: Code is split into manageable chunks
2. **Embedding Generation**: Text embeddings created for semantic search
3. **Vector Storage**: Chunks stored in vector database
4. **Intelligent Retrieval**: Relevant code retrieved based on queries
5. **Context-Aware Responses**: AI answers with code context

## 🛡️ Security Features

- **Static Analysis**: Uses Bandit for security scanning
- **AST Parsing**: Tree-sitter for code structure analysis
- **Vulnerability Detection**: Identifies common security issues
- **Risk Assessment**: Provides severity classifications

## 📈 Performance

- **Parallel Processing**: Multiple agents work concurrently
- **Caching**: Vector database for fast retrieval
- **Optimized Embeddings**: Efficient text processing
- **Scalable Architecture**: Handles large repositories

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   ```
   ModuleNotFoundError: No module named 'radon'
   ```
   **Solution**: Run `pip install -r requirements.txt`

2. **API Key Errors**
   ```
   Error: Invalid Groq API key
   ```
   **Solution**: Check `.env` file and ensure `GROQ_API_KEY` is set

3. **Git Clone Errors**
   ```
   Error: Repository not found
   ```
   **Solution**: Ensure repository URL is correct and public

4. **Memory Issues**
   ```
   MemoryError during analysis
   ```
   **Solution**: For large repositories, consider increasing system memory or analyzing specific directories

### Deployment Issues

1. **Streamlit Cloud Build Failures**
   - Check all dependencies are in `requirements.txt`
   - Verify `.env.example` exists
   - Ensure `packages.txt` includes system dependencies

2. **Environment Variable Issues**
   - Add all required variables in Streamlit Cloud settings
   - Use exact variable names as in `.env.example`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **LangChain** for the AI framework
- **Groq** for high-performance LLM inference
- **Streamlit** for the web interface
- **ChromaDB** for vector storage
- **Radon** for code complexity analysis

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the documentation

---