# 🤖 DocuScope AI

> **Privacy-first document analysis with local AI processing**  
> *Built by [David Osei Kumi](https://www.linkedin.com/in/david-osei-kumi)*

DocuScope AI is a powerful document analysis tool that uses **Retrieval-Augmented Generation (RAG)** to provide intelligent insights from your CSV and PDF files. Built with privacy-first principles, it runs completely offline using local Ollama models.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.29.0-red.svg)
![LangChain](https://img.shields.io/badge/langchain-0.1.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

---

## 🎬 Live Demo

![DocuScope AI Demo](assets/demo.gif)

*DocuScope AI in action - Upload a document, ask questions, get instant insights*

---

## ✨ Features

- 🔒 **100% Offline Processing** - Your data never leaves your device
- 📊 **Multi-Format Support** - Analyze CSV and PDF documents
- 🤖 **Local AI Models** - Powered by Ollama (Llama 3.2:3b)
- 🎨 **Beautiful UI** - Clean, responsive Streamlit interface
- ⚡ **Fast Vector Search** - ChromaDB for efficient document retrieval
- 🔍 **Intelligent Q&A** - Ask natural language questions about your documents
- 💻 **Dual Interface** - Web app and command-line interface

---

## 🚀 Quick Start

**New here?** Start with [QUICK_START.md](QUICK_START.md) for a 5-minute setup guide.

### Prerequisites

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull required models
ollama pull llama3.2:3b
ollama pull mxbai-embed-large
```

### Installation

```bash
# Clone repository
git clone https://github.com/dkumi12/Local-rag-agent.git
cd Local-rag-agent

# Install dependencies
pip install -r requirements.txt

# Run web app
streamlit run app.py

# Or run CLI version
python main.py
```

---

## 📚 Documentation

Choose your next step based on what you need:

### Getting Started
- **[QUICK_START.md](QUICK_START.md)** - 5-minute setup guide
  - Installation steps
  - Running your first analysis
  - Troubleshooting

### Understanding the System
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - How DocuScope AI works
  - System architecture
  - Data flow diagrams
  - Component explanations
  - Privacy & security

### Using the API
- **[docs/API.md](docs/API.md)** - Complete API reference
  - Class methods
  - Usage examples
  - Integration patterns
  - Error handling

### Configuration & Optimization
- **[docs/CONFIGURATION.md](docs/CONFIGURATION.md)** - Advanced setup
  - Model selection
  - Performance tuning
  - Custom presets (speed/quality/balance)
  - System configuration

### Learning by Example
- **[docs/EXAMPLES.md](docs/EXAMPLES.md)** - Working code examples
  - Basic usage example
  - Batch processing
  - Custom configurations
  - Real-world applications

---

## 💡 Quick Usage Examples

### Web Interface

1. Launch with `streamlit run app.py`
2. Upload your CSV or PDF file
3. Ask questions like:
   - *"What are the top 5 products by sales?"*
   - *"Summarize the main findings"*
   - *"Show me trends in the data"*

### Command Line

```bash
python main.py path/to/your/document.pdf
```

Then ask questions interactively!

### Python API

```python
from main import DocuScopeAI

# Initialize
app = DocuScopeAI()
app.initialize_models()

# Load document
app.load_document("data.csv")

# Ask questions
result = app.ask_question("What are the main insights?")
print(result["result"])
```

For more examples, see [docs/EXAMPLES.md](docs/EXAMPLES.md).

---

## 🏗️ Architecture Overview

```
Document Upload → LangChain Loader → Text Chunking → 
Ollama Embeddings → ChromaDB Storage → Vector Search → 
Ollama LLM → AI Response + Sources
```

**Tech Stack:**
- **Backend**: Python, LangChain, ChromaDB
- **AI**: Ollama (Llama 3.2:3b, mxbai-embed-large)  
- **Frontend**: Streamlit with custom CSS
- **Processing**: PyPDF, CSV Loader

For detailed architecture information, see [ARCHITECTURE.md](ARCHITECTURE.md).

---

## 📊 Sample Questions

**For CSV Data:**
- "What's the average revenue by quarter?"
- "Which customer segment is most profitable?"
- "Show me sales trends over time"

**For PDF Documents:**
- "What are the key recommendations?"
- "Summarize the methodology section"
- "Find mentions of risk factors"

---

## ⚙️ Configuration

### Default Setup (Balanced)
- Model: `llama3.2:3b` (3B parameters)
- Embeddings: `mxbai-embed-large`
- Speed: 5-15 seconds per query
- Memory: 7-12GB

### Want to Optimize?

**For Speed:**
```python
app.embedding = OllamaEmbeddings(model="bge-small-en")
app.llm = Ollama(model="llama3.2:1b")
# 2-5 seconds per query, 4-6GB memory
```

**For Quality:**
```python
app.embedding = OllamaEmbeddings(model="bge-large-en")
app.llm = Ollama(model="mistral")
# 15-45 seconds per query, 12-16GB memory
```

See [docs/CONFIGURATION.md](docs/CONFIGURATION.md) for all options.

---

## 🔒 Privacy & Security

- ✅ All processing happens locally on your machine
- ✅ No data sent to external APIs or cloud services
- ✅ Documents processed in memory only
- ✅ Complete control over sensitive information

DocuScope AI never:
- ❌ Sends documents to external servers
- ❌ Logs queries or results
- ❌ Stores user data
- ❌ Requires internet connection

---

## 🎯 Use Cases

- **Document Analysis** - Extract insights from reports, papers, articles
- **Data Exploration** - Ask questions about CSV files and datasets
- **Report Generation** - Automated analysis and summary creation
- **Research** - Analyze academic papers and research documents
- **Compliance** - Review documents for specific requirements
- **Knowledge Extraction** - Build question-answer datasets

---

## 🔧 Development

### API Reference

```python
from main import DocuScopeAI

app = DocuScopeAI()
app.initialize_models()       # Setup AI models
app.validate_file(path)       # Check if file is valid
app.load_document(path)       # Load CSV or PDF
app.ask_question(query)       # Get answer about document
app.interactive_session()     # Start CLI question loop
```

Full documentation: [docs/API.md](docs/API.md)

### Batch Processing

```python
# Process multiple documents
documents = ["report1.csv", "report2.csv", "report3.pdf"]
for doc in documents:
    app.load_document(doc)
    result = app.ask_question("What's the summary?")
```

Example: [examples/02_batch_processing.py](examples/02_batch_processing.py)

### Web Integration

```python
from flask import Flask, request
from main import DocuScopeAI

app_flask = Flask(__name__)
doc_ai = DocuScopeAI()
doc_ai.initialize_models()

@app_flask.route("/analyze", methods=["POST"])
def analyze():
    file = request.files["document"]
    question = request.form["question"]
    # Process and return
```

See [docs/API.md](docs/API.md) for complete integration examples.

---

## 📈 Performance

### Typical Performance Metrics

```
Document Size      | Load Time | Query Time | Memory
────────────────────────────────────────────────────
Small (5-10p)      | 2-5s      | 5-10s      | 7-12GB
Medium (50p)       | 10-30s    | 10-20s     | 7-12GB
Large (500p)       | 1-5min    | 20-60s     | 8-15GB
```

### Tips for Better Performance

1. **Use smaller models for speed**
   ```python
   app.llm = Ollama(model="llama3.2:1b")
   ```

2. **Retrieve fewer documents**
   ```python
   app.qa_chain.retriever.search_kwargs = {"k": 2}
   ```

3. **Ask specific questions**
   - ✅ "What are the top 3 risks?"
   - ❌ "Tell me everything"

---

## 🐛 Troubleshooting

### Common Issues

**"Ollama not found"**
```bash
# Make sure Ollama is running
ollama serve
```

**"Model not found"**
```bash
ollama pull llama3.2:3b
ollama pull mxbai-embed-large
```

**"Out of memory"**
Use smaller models or limit document size.

For more help, see [QUICK_START.md](QUICK_START.md).

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**David Osei Kumi**
- LinkedIn: [linkedin.com/in/david-osei-kumi](https://www.linkedin.com/in/david-osei-kumi)
- GitHub: [@dkumi12](https://github.com/dkumi12)

---

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) for excellent local AI models
- [LangChain](https://langchain.com/) for the RAG framework
- [Streamlit](https://streamlit.io/) for the beautiful web interface
- [ChromaDB](https://www.trychroma.com/) for vector storage

---

## 📞 Support & Documentation

- **Getting Started:** [QUICK_START.md](QUICK_START.md)
- **Technical Details:** [ARCHITECTURE.md](ARCHITECTURE.md)
- **API Reference:** [docs/API.md](docs/API.md)
- **Configuration:** [docs/CONFIGURATION.md](docs/CONFIGURATION.md)
- **Examples:** [docs/EXAMPLES.md](docs/EXAMPLES.md)

---

**Built with ❤️ by David Osei Kumi**

*Privacy-first, offline document analysis powered by local AI*
