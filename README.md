# 🤖 DocuScope AI

> **Privacy-first document analysis with local AI processing**

DocuScope AI is a powerful document analysis tool that uses **Retrieval-Augmented Generation (RAG)** to provide intelligent insights from your CSV and PDF files. Built with privacy-first principles, it runs completely offline using local Ollama models.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.29.0-red.svg)
![LangChain](https://img.shields.io/badge/langchain-0.1.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

- 🔒 **100% Offline Processing** - Your data never leaves your device
- 📊 **Multi-Format Support** - Analyze CSV and PDF documents
- 🤖 **Local AI Models** - Powered by Ollama (Llama 3.2:3b)
- 🎨 **Beautiful UI** - Clean, responsive Streamlit interface
- ⚡ **Fast Vector Search** - ChromaDB for efficient document retrieval
- 🔍 **Intelligent Q&A** - Ask natural language questions about your documents
- 💻 **Dual Interface** - Web app and command-line interface

## 🚀 Quick Start

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

## 💡 Usage Examples

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

## 🏗️ Architecture

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

## 📊 Sample Questions

**For CSV Data:**
- "What's the average revenue by quarter?"
- "Which customer segment is most profitable?"
- "Show me sales trends over time"

**For PDF Documents:**
- "What are the key recommendations?"
- "Summarize the methodology section"
- "Find mentions of risk factors"

## 🔒 Privacy & Security

- All processing happens locally on your machine
- No data sent to external APIs or cloud services
- Documents processed in memory only
- Complete control over sensitive information

## 🛠️ Development

### API Usage

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

### Configuration

Models and settings can be customized in the source code:

```python
# Different models
llm = Ollama(model="llama3.2:1b")  # Faster, smaller
embedding = OllamaEmbeddings(model="nomic-embed-text")
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) for excellent local AI models
- [LangChain](https://langchain.com/) for the RAG framework
- [Streamlit](https://streamlit.io/) for the beautiful web interface

---

**Built with ❤️ for privacy-conscious document analysis**
