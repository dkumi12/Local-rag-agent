# 📄 DocuScope AI

> **Your private AI agent for documents — classic, clear, offline insights.**

DocuScope AI is a powerful document analysis tool that leverages **Retrieval-Augmented Generation (RAG)** to provide intelligent insights from your CSV and PDF files. Built with privacy-first principles, it runs completely offline using local Ollama models.

## ✨ Features

- 🔒 **100% Offline Processing** - Your data never leaves your device
- 📊 **Multi-Format Support** - Analyze CSV and PDF documents
- 🤖 **Local AI Models** - Powered by Ollama (Llama 3.2:3b)
- 🎨 **Beautiful UI** - Clean, responsive Streamlit interface
- ⚡ **Fast Vector Search** - ChromaDB for efficient document retrieval
- 🔍 **Intelligent Q&A** - Ask natural language questions about your documents

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai/) installed locally
- Required Ollama models:
  ```bash
  ollama pull llama3.2:3b
  ollama pull mxbai-embed-large
  ```

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/local-ag-csv.git
   cd local-ag-csv
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   # Streamlit Web App
   streamlit run app.py
   
   # Or CLI version
   python main.py
   ```

## 💡 Usage

### Web Interface
1. Launch the app with `streamlit run app.py`
2. Upload your CSV or PDF file
3. Ask questions about your document
4. Get AI-powered insights with source citations

### Command Line
1. Run `python main.py`
2. Enter the path to your document
3. Start asking questions interactively

## 🏗️ Architecture

```
DocuScope AI
├── Document Upload (CSV/PDF)
├── Document Processing (LangChain Loaders)
├── Text Embedding (Ollama mxbai-embed-large)
├── Vector Storage (ChromaDB)
├── LLM Query (Ollama Llama 3.2:3b)
└── Response with Sources
```

## 🛠️ Tech Stack

- **Backend**: Python, LangChain, ChromaDB
- **AI Models**: Ollama (Llama 3.2:3b, mxbai-embed-large)
- **Frontend**: Streamlit
- **Document Processing**: PyPDF, CSV Loader
- **Vector Database**: Chroma

## 📊 Example Use Cases

- **Business Analytics**: Query sales data, financial reports
- **Research**: Analyze research papers, extract key insights  
- **Data Exploration**: Ask questions about CSV datasets
- **Document Review**: Get summaries and insights from PDFs

## 🔒 Privacy & Security

- All processing happens locally on your machine
- No data is sent to external APIs or cloud services
- Documents are processed in memory only
- Complete control over your sensitive information

## 📝 Sample Questions

**For CSV files:**
- "What are the top 5 products by sales?"
- "Show me trends in the data"
- "What's the average value in column X?"

**For PDF files:**
- "Summarize the main points of this document"
- "What are the key recommendations?"
- "Find information about [specific topic]"

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**David Osei Kumi**

- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) for providing excellent local AI models
- [LangChain](https://langchain.com/) for the powerful RAG framework
- [Streamlit](https://streamlit.io/) for the beautiful web interface

---

*Built with ❤️ for privacy-conscious document analysis*
