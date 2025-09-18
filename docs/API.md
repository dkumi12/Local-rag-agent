# 🔧 API Documentation

## Python API

Use DocuScope AI programmatically for batch processing or integration.

### Quick Start

```python
from main import DocuScopeAI

# Initialize
app = DocuScopeAI()
app.initialize_models()

# Load document
app.load_document("document.pdf")

# Ask questions
result = app.ask_question("What are the main points?")
print(result["result"])
```

### Class Reference

#### DocuScopeAI Methods

- `initialize_models()` - Load AI models
- `load_document(path)` - Process a document  
- `ask_question(query)` - Query the document

### Response Format

```python
{
    "result": "AI generated answer",
    "source_documents": [...]  # Source citations
}
```

### Batch Processing

```python
files = ["doc1.pdf", "data.csv"] 
for file in files:
    app.load_document(file)
    result = app.ask_question("Summarize this")
    print(f"{file}: {result['result']}")
```

### Configuration

Customize models in the source code:

```python
# Use different models
llm = Ollama(model="llama3.2:1b")         # Smaller/faster
embedding = OllamaEmbeddings(model="...")  # Different embedding
```

## Error Handling

Always check return values:

```python
if app.initialize_models():
    if app.load_document(path):
        result = app.ask_question(query)
        if result:
            print(result["result"])
```
