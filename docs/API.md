# API Documentation - DocuScope AI

Complete API reference for using DocuScope AI as a Python library.

## 📚 Overview

DocuScope AI provides three interfaces:

1. **Web Interface** (`app.py`) - Streamlit web application
2. **Command Line** (`main.py`) - Interactive CLI
3. **Python API** (`main.py + api_examples.py`) - Programmatic access

This document covers the **Python API** for programmatic usage.

---

## 🔧 Basic API Usage

### Initialization

```python
from main import DocuScopeAI

# Create instance
app = DocuScopeAI()

# Initialize models (downloads if not present)
if not app.initialize_models():
    print("Failed to initialize models")
    exit(1)
```

### Loading a Document

```python
# Load a CSV file
app.load_document("path/to/data.csv")

# Or load a PDF file
app.load_document("path/to/document.pdf")

# Check if loading succeeded
if not app.load_document("document.pdf"):
    print("Failed to load document")
```

### Asking Questions

```python
# Simple question
result = app.ask_question("What are the main insights?")

if result:
    print(result["result"])
    print(result["source_documents"])
```

---

## 📖 Class Reference

### DocuScopeAI

Main class for document analysis.

#### Methods

##### `__init__()`

Initialize the DocuScopeAI instance.

```python
app = DocuScopeAI()
```

**Returns:** `None`

---

##### `initialize_models() -> bool`

Initialize AI models (embedding and language models).

**Must be called before loading documents.**

```python
success = app.initialize_models()
if not success:
    print("Failed to initialize")
```

**Returns:** `bool` - `True` if successful, `False` if models unavailable

**Raises:** `ImportError` if dependencies missing

**Side Effects:**
- Downloads models if not present locally (~3GB)
- Initializes `self.embedding` and `self.llm`

---

##### `validate_file(file_path: str) -> bool`

Validate file before processing.

```python
if app.validate_file("document.pdf"):
    app.load_document("document.pdf")
```

**Parameters:**
- `file_path` (str) - Path to file

**Returns:** `bool` - `True` if valid, `False` if invalid

**Validation Checks:**
- File exists
- File is readable
- File extension is `.csv` or `.pdf`

---

##### `load_document(file_path: str) -> bool`

Load and process a document.

```python
success = app.load_document("data.csv")
if success:
    print("Document loaded successfully")
```

**Parameters:**
- `file_path` (str) - Path to CSV or PDF file

**Returns:** `bool` - `True` if successful, `False` otherwise

**Raises:** Exception on file read errors

**Side Effects:**
- Creates embeddings for all document chunks
- Initializes vector database (ChromaDB)
- Creates RAG chain

**Time Complexity:**
- Small documents (<10 pages): 5-10 seconds
- Medium documents (10-100 pages): 15-60 seconds
- Large documents (>100 pages): 1-5 minutes

---

##### `ask_question(query: str) -> Optional[dict]`

Ask a question about the loaded document.

```python
result = app.ask_question("Summarize the main points")

if result:
    answer = result["result"]
    sources = result["source_documents"]
    
    print(f"Answer: {answer}")
    print(f"Used {len(sources)} sources")
```

**Parameters:**
- `query` (str) - Natural language question

**Returns:** `dict` with keys:
- `"result"` (str) - Generated answer
- `"source_documents"` (list) - Document chunks used

Returns `None` if no document loaded or error occurs.

**Time Complexity:** 5-30 seconds depending on model

**Example Response:**
```python
{
    "result": "The main products by sales are...",
    "source_documents": [
        Document(page_content="Sales data Q1...", metadata={}),
        Document(page_content="Product rankings...", metadata={}),
        Document(page_content="Top 10 products...", metadata={})
    ]
}
```

---

##### `interactive_session()`

Start interactive Q&A session (CLI).

```python
app.load_document("document.pdf")
app.interactive_session()  # Starts interactive loop
```

**Parameters:** None

**Returns:** `None`

**Behavior:**
- Loops until user types 'exit', 'quit', 'q', or 'bye'
- Accepts KeyboardInterrupt (Ctrl+C)
- Accepts EOFError (Ctrl+D)
- Displays answers with source documents

---

## 📝 Complete Example

```python
from main import DocuScopeAI

# Initialize
app = DocuScopeAI()

# Setup
if not app.initialize_models():
    print("❌ Models failed to initialize")
    exit(1)

# Load document
document_path = "sales_report.csv"
if not app.load_document(document_path):
    print(f"❌ Failed to load {document_path}")
    exit(1)

# Ask questions
questions = [
    "What was the total revenue?",
    "Which product had the highest sales?",
    "What's the average order value?"
]

for question in questions:
    print(f"\n📝 Question: {question}")
    
    result = app.ask_question(question)
    
    if result:
        print(f"📌 Answer: {result['result']}")
        print(f"📑 Sources used: {len(result['source_documents'])}")
    else:
        print("❌ Failed to get answer")
```

---

## 🔄 Batch Processing

Process multiple documents with the same questions:

```python
from main import DocuScopeAI

app = DocuScopeAI()
app.initialize_models()

documents = [
    "report_2023.csv",
    "report_2024.csv",
    "summary.pdf"
]

analysis_questions = [
    "What's the total value?",
    "List the top 5 items",
    "Summarize in one sentence"
]

results = {}

for doc in documents:
    if app.load_document(doc):
        results[doc] = {}
        
        for question in analysis_questions:
            result = app.ask_question(question)
            results[doc][question] = result["result"] if result else None
        
        print(f"✅ Analyzed {doc}")
    else:
        print(f"❌ Failed to load {doc}")

# Save or process results
import json
with open("analysis_results.json", "w") as f:
    json.dump(results, f, indent=2)
```

---

## 🌐 Web Integration

Use DocuScope AI in a web application:

```python
from flask import Flask, request, jsonify
from main import DocuScopeAI
import os
from werkzeug.utils import secure_filename

app_flask = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize once at startup
doc_ai = DocuScopeAI()
doc_ai.initialize_models()

@app_flask.route("/analyze", methods=["POST"])
def analyze_document():
    """Analyze uploaded document and answer question."""
    
    # Get file and question
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files["file"]
    question = request.form.get("question", "Summarize this document")
    
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    
    # Save file
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    try:
        # Load and analyze
        if not doc_ai.load_document(filepath):
            return jsonify({"error": "Failed to process file"}), 400
        
        result = doc_ai.ask_question(question)
        
        if not result:
            return jsonify({"error": "Failed to get answer"}), 400
        
        return jsonify({
            "success": True,
            "answer": result["result"],
            "num_sources": len(result["source_documents"])
        })
    
    finally:
        # Cleanup
        if os.path.exists(filepath):
            os.remove(filepath)

if __name__ == "__main__":
    app_flask.run(debug=True)
```

---

## 🔍 Advanced Usage

### Custom Model Selection

```python
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms.ollama import Ollama
from main import DocuScopeAI

app = DocuScopeAI()

# Override default models
app.embedding = OllamaEmbeddings(model="nomic-embed-text")
app.llm = Ollama(model="mistral")

# Continue as normal
app.load_document("document.pdf")
result = app.ask_question("What's the summary?")
```

### Error Handling

```python
from main import DocuScopeAI
import logging

logger = logging.getLogger(__name__)

app = DocuScopeAI()

try:
    if not app.initialize_models():
        logger.error("Failed to initialize models")
        raise RuntimeError("Model initialization failed")
    
    if not app.load_document("document.pdf"):
        logger.error("Failed to load document")
        raise RuntimeError("Document loading failed")
    
    result = app.ask_question("What's the main topic?")
    
    if not result:
        logger.error("Failed to get answer")
        raise RuntimeError("Question answering failed")
    
    print(f"Success: {result['result']}")

except RuntimeError as e:
    logger.error(f"Error: {e}")
    # Handle error appropriately
except Exception as e:
    logger.error(f"Unexpected error: {e}")
```

### Streaming Results (Future)

Currently, results are returned when ready. Future versions may support streaming.

```python
# Planned for future versions
# for partial_result in app.ask_question_stream("Question"):
#     print(partial_result)
```

---

## 📊 Return Value Details

### `ask_question()` Return Format

```python
{
    "result": str,                    # Generated answer
    "source_documents": [             # Documents used
        {
            "page_content": str,      # Document text
            "metadata": dict          # Document metadata
        },
        ...
    ]
}
```

**Example:**
```python
{
    "result": "Based on the sales data, the top 3 products are...",
    "source_documents": [
        {
            "page_content": "Product A: $100K sales, Product B: $95K sales...",
            "metadata": {}
        }
    ]
}
```

---

## 🛠️ Configuration

### Environment Variables

```bash
# Model configuration (set before importing)
export OLLAMA_MODEL_EMBEDDING="mxbai-embed-large"
export OLLAMA_MODEL_LLM="llama3.2:3b"

# Ollama server (if not localhost:11434)
export OLLAMA_HOST="http://localhost:11434"
```

### Code Configuration

```python
from langchain_community.llms.ollama import Ollama

app = DocuScopeAI()
app.initialize_models()

# Adjust retrieval parameters
app.qa_chain.retriever.search_kwargs = {"k": 8}  # Get more sources

# Change generation parameters
app.llm.temperature = 0.7  # Creativity (0-1)
app.llm.top_p = 0.95       # Diversity
```

---

## ⚠️ Error Handling

### Common Errors

**"Ollama not found"**
```python
# Make sure Ollama is running
# Run: ollama serve
```

**"Model not found"**
```python
# Pull required models
# Run: ollama pull llama3.2:3b
#      ollama pull mxbai-embed-large
```

**"No document loaded"**
```python
# Load a document first
app.load_document("file.pdf")

# Then ask questions
app.ask_question("Question?")
```

### Robust Error Handling

```python
def safe_analyze(file_path, question):
    """Safe document analysis with error handling."""
    
    try:
        app = DocuScopeAI()
        
        if not app.initialize_models():
            return {"error": "Models unavailable"}
        
        if not app.validate_file(file_path):
            return {"error": "Invalid file"}
        
        if not app.load_document(file_path):
            return {"error": "Failed to load document"}
        
        result = app.ask_question(question)
        
        if not result:
            return {"error": "Failed to generate answer"}
        
        return {
            "success": True,
            "answer": result["result"],
            "sources": len(result["source_documents"])
        }
    
    except ImportError as e:
        return {"error": f"Missing dependency: {e}"}
    except FileNotFoundError as e:
        return {"error": f"File not found: {e}"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}
```

---

## 📞 Support

For issues or questions:
1. Check [QUICK_START.md](../QUICK_START.md) for setup help
2. Review [ARCHITECTURE.md](../ARCHITECTURE.md) for design details
3. Check [api_examples.py](../api_examples.py) for working examples
4. Open an issue on GitHub

---

## 🔗 Related Documentation

- [README.md](../README.md) - Project overview
- [QUICK_START.md](../QUICK_START.md) - Setup guide
- [ARCHITECTURE.md](../ARCHITECTURE.md) - System design
- [api_examples.py](../api_examples.py) - Working code examples

