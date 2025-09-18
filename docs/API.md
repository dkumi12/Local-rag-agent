# API Documentation

## DocuScope AI Python API

### Overview

DocuScope AI provides a simple Python API for programmatic document analysis. This is useful for batch processing, integration with other applications, or building custom workflows.

### Quick Start

```python
from main import DocuScopeAI

# Initialize the system
app = DocuScopeAI()

# Load AI models
if app.initialize_models():
    # Load a document
    if app.load_document("path/to/your/document.pdf"):
        # Ask questions
        result = app.ask_question("What are the main points?")
        print(result["result"])
```

### Class Reference

#### `DocuScopeAI`

The main class for document analysis operations.

**Methods:**

##### `__init__()`
Initialize a new DocuScope AI instance.

##### `initialize_models() -> bool`
Initialize the AI models (embedding and language models).

**Returns:** `True` if successful, `False` otherwise.

**Example:**
```python
app = DocuScopeAI()
success = app.initialize_models()
if not success:
    print("Failed to initialize models")
```

##### `validate_file(file_path: str) -> bool`
Validate that a file exists and is supported.

**Parameters:**
- `file_path` (str): Path to the file to validate

**Returns:** `True` if valid, `False` otherwise.

##### `load_document(file_path: str) -> bool`
Load and process a document for analysis.

**Parameters:**
- `file_path` (str): Path to CSV or PDF file

**Returns:** `True` if successful, `False` otherwise.

**Example:**
```python
success = app.load_document("data.csv")
if success:
    print("Document loaded successfully")
```

##### `ask_question(query: str) -> Optional[dict]`
Ask a question about the loaded document.

**Parameters:**
- `query` (str): Natural language question

**Returns:** Dictionary with results or `None` if error.

**Response Format:**
```python
{
    "result": "AI generated answer",
    "source_documents": [
        {
            "page_content": "Source text snippet",
            "metadata": {...}
        }
    ]
}
```

### Batch Processing Example

```python
import os
from pathlib import Path

def process_documents(directory: str, questions: list):
    """Process all documents in a directory."""
    app = DocuScopeAI()
    
    if not app.initialize_models():
        return
    
    results = {}
    
    for file_path in Path(directory).glob("*.{csv,pdf}"):
        print(f"Processing {file_path}")
        
        if app.load_document(str(file_path)):
            file_results = {}
            
            for question in questions:
                result = app.ask_question(question)
                if result:
                    file_results[question] = result["result"]
            
            results[str(file_path)] = file_results
    
    return results

# Usage
questions = [
    "What are the main findings?",
    "Summarize the key points",
    "What trends are visible?"
]

results = process_documents("./data", questions)
```

### Integration Examples

#### Flask Web API

```python
from flask import Flask, request, jsonify
from main import DocuScopeAI

app = Flask(__name__)
docuscope = DocuScopeAI()
docuscope.initialize_models()

@app.route('/analyze', methods=['POST'])
def analyze_document():
    file_path = request.json.get('file_path')
    question = request.json.get('question')
    
    if docuscope.load_document(file_path):
        result = docuscope.ask_question(question)
        return jsonify(result)
    
    return jsonify({"error": "Failed to load document"})

if __name__ == '__main__':
    app.run()
```

#### Jupyter Notebook Integration

```python
# Cell 1: Setup
from main import DocuScopeAI
import pandas as pd

app = DocuScopeAI()
app.initialize_models()

# Cell 2: Load Data
app.load_document("sales_data.csv")

# Cell 3: Analysis
questions = [
    "What's the total revenue?",
    "Which product sells the most?",
    "What are the seasonal trends?"
]

for q in questions:
    result = app.ask_question(q)
    print(f"Q: {q}")
    print(f"A: {result['result']}\n")
```

### Error Handling

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.INFO)

try:
    app = DocuScopeAI()
    
    if not app.initialize_models():
        raise Exception("Model initialization failed")
    
    if not app.load_document("document.pdf"):
        raise Exception("Document loading failed")
    
    result = app.ask_question("Summarize this")
    if result is None:
        raise Exception("Question processing failed")
        
except Exception as e:
    print(f"Error: {e}")
```

### Configuration

See `config.toml` for configuration options:

```python
# Custom model configuration
app = DocuScopeAI()
app.embedding = OllamaEmbeddings(model="custom-embed-model")
app.llm = Ollama(model="custom-llm-model")
```

### Performance Tips

1. **Model Initialization**: Initialize models once and reuse the instance
2. **Document Caching**: Keep the QA chain in memory for multiple questions
3. **Batch Processing**: Process multiple documents in sequence without reinitializing
4. **Memory Management**: Clear vector stores between documents if processing many files

### Troubleshooting

**Common Issues:**

1. **Models not found**: Ensure Ollama models are installed
2. **Memory errors**: Use smaller chunk sizes or models
3. **Slow responses**: Check system resources and model size
4. **Import errors**: Verify all dependencies are installed

**Debug Mode:**

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Now you'll see detailed logs
app = DocuScopeAI()
app.initialize_models()
```
