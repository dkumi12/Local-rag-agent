# Examples - DocuScope AI

Working code examples for common use cases.

## 📚 Examples Overview

All examples are in the `/examples` directory and ready to run.

| Example | File | Use Case |
|---------|------|----------|
| Basic Usage | `01_basic_usage.py` | Simple document analysis |
| Batch Processing | `02_batch_processing.py` | Multiple documents with same questions |
| Custom Configuration | `03_custom_configuration.py` | Speed/quality optimization |

---

## 🚀 Example 1: Basic Usage

**File:** `examples/01_basic_usage.py`

**What it does:** Loads a single document and asks multiple questions.

**When to use:** Getting started, simple analysis.

### Quick Run

```bash
python examples/01_basic_usage.py
```

### Code Example

```python
from main import DocuScopeAI

# Initialize
app = DocuScopeAI()
app.initialize_models()

# Load document
app.load_document("path/to/document.csv")

# Ask questions
result = app.ask_question("What's the main topic?")
print(result["result"])
```

### What You'll Learn

- How to initialize DocuScope AI
- How to load a document
- How to ask questions and get answers
- How to handle results

### Next Steps

- Change the document path to analyze your own files
- Modify the questions list to ask different questions
- Check error handling for robustness

---

## 📊 Example 2: Batch Processing

**File:** `examples/02_batch_processing.py`

**What it does:** Analyzes multiple documents with the same set of questions, outputs results to JSON.

**When to use:** Generating reports, comparing documents, automated analysis.

### Quick Run

```bash
python examples/02_batch_processing.py
```

### Code Example

```python
from main import DocuScopeAI

app = DocuScopeAI()
app.initialize_models()

documents = [
    "report_2023.csv",
    "report_2024.csv",
    "summary.pdf"
]

questions = [
    "What's the total value?",
    "What are the top items?",
    "Summarize in one sentence"
]

results = {}
for doc in documents:
    app.load_document(doc)
    results[doc] = {}
    for question in questions:
        result = app.ask_question(question)
        results[doc][question] = result["result"]
```

### What You'll Learn

- How to process multiple documents
- How to ask the same questions across documents
- How to save and organize results
- Batch processing best practices

### Use Cases

- Generate quarterly reports
- Compare document versions
- Create analysis summaries
- Automated compliance checking

---

## 🎛️ Example 3: Custom Configuration

**File:** `examples/03_custom_configuration.py`

**What it does:** Shows how to optimize DocuScope AI for different scenarios.

**When to use:** Performance tuning, resource constraints, accuracy requirements.

### Quick Run

```bash
python examples/03_custom_configuration.py
```

### Configuration Presets

#### Speed Optimized
```python
app.embedding = OllamaEmbeddings(model="bge-small-en")
app.llm = Ollama(model="llama3.2:1b")
app.qa_chain.retriever.search_kwargs = {"k": 2}
```
- **Speed:** 2-5 seconds per query
- **Memory:** 4-6GB
- **Quality:** Fair
- **Best for:** Quick analysis, low-resource systems

#### Balanced (Default)
```python
# Uses default models
# k=4 by default
```
- **Speed:** 5-15 seconds per query
- **Memory:** 7-12GB
- **Quality:** Good
- **Best for:** General purpose analysis

#### Quality Optimized
```python
app.embedding = OllamaEmbeddings(model="bge-large-en")
app.llm = Ollama(model="mistral")
app.qa_chain.retriever.search_kwargs = {"k": 8}
```
- **Speed:** 15-45 seconds per query
- **Memory:** 12-16GB
- **Quality:** Excellent
- **Best for:** High-accuracy requirements

### What You'll Learn

- How to customize embedding models
- How to customize language models
- How to tune retrieval parameters
- Performance trade-offs
- How to measure and compare configurations

### Common Customizations

**Lower latency:**
```python
app.embedding = OllamaEmbeddings(model="nomic-embed-text")
app.llm = Ollama(model="llama3.2:1b")
```

**Lower memory usage:**
```python
app.embedding = OllamaEmbeddings(model="bge-small-en")
app.llm = Ollama(model="llama3.2:1b")
```

**Higher accuracy:**
```python
app.embedding = OllamaEmbeddings(model="bge-large-en")
app.llm = Ollama(model="mistral")
```

---

## 🔧 Running Examples

### Setup

All examples require DocuScope AI to be set up first:

```bash
# Install dependencies
pip install -r requirements.txt

# Ensure Ollama is running
ollama serve  # In another terminal

# Pull required models (first time only)
ollama pull llama3.2:3b
ollama pull mxbai-embed-large
```

### Running an Example

```bash
# From repo root
python examples/01_basic_usage.py

# Or with Python3
python3 examples/01_basic_usage.py
```

### Modifying Examples

Each example is designed to be modified:

1. **Change the document path:**
   ```python
   document_path = "path/to/your/document.csv"
   ```

2. **Change the questions:**
   ```python
   questions = [
       "Your question 1?",
       "Your question 2?",
   ]
   ```

3. **Modify the configuration:**
   ```python
   app.embedding = OllamaEmbeddings(model="nomic-embed-text")
   ```

---

## 📝 Creating Your Own Example

Here's a template for creating new examples:

```python
"""
Example Title

Brief description of what this example does.
"""

from main import DocuScopeAI

def main():
    """Main function."""
    
    # Setup
    app = DocuScopeAI()
    if not app.initialize_models():
        print("Failed to initialize")
        return
    
    # Load document
    if not app.load_document("path/to/document.pdf"):
        print("Failed to load document")
        return
    
    # Your custom logic here
    result = app.ask_question("Your question?")
    
    if result:
        print(f"Answer: {result['result']}")
    else:
        print("Failed to get answer")

if __name__ == "__main__":
    main()
```

---

## 🐛 Troubleshooting Examples

### "Ollama not found"
```bash
# Make sure Ollama server is running
ollama serve
```

### "Model not found"
```bash
ollama pull llama3.2:3b
ollama pull mxbai-embed-large
```

### "File not found"
Update the file paths in the example to match your files:
```python
document_path = "/absolute/path/to/file.csv"
```

### "Out of memory"
Use a lighter configuration:
```python
app.embedding = OllamaEmbeddings(model="bge-small-en")
app.llm = Ollama(model="llama3.2:1b")
```

---

## 📚 Learning Path

**Beginner:**
1. Start with `01_basic_usage.py`
2. Understand the three main steps: init, load, ask
3. Modify questions to analyze different aspects

**Intermediate:**
1. Try `02_batch_processing.py`
2. Learn how to handle multiple documents
3. Understand how to organize and save results

**Advanced:**
1. Study `03_custom_configuration.py`
2. Experiment with different model combinations
3. Optimize for your specific use case

---

## 🔗 Related Documentation

- [QUICK_START.md](../QUICK_START.md) - Setup guide
- [docs/API.md](../docs/API.md) - API reference
- [ARCHITECTURE.md](../ARCHITECTURE.md) - System design
- [docs/CONFIGURATION.md](../docs/CONFIGURATION.md) - Advanced configuration

---

## 💡 Tips & Tricks

### Measuring Performance

```python
import time

start = time.time()
result = app.ask_question("Question?")
elapsed = time.time() - start

print(f"Query took {elapsed:.2f} seconds")
```

### Error Handling

```python
try:
    if not app.load_document(path):
        print(f"Failed to load {path}")
        return
except FileNotFoundError:
    print("File not found")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Progress Tracking

```python
for i, doc in enumerate(documents):
    print(f"Progress: {i+1}/{len(documents)}")
    if app.load_document(doc):
        result = app.ask_question("Question?")
```

---

## 🎓 Example Usage in Real Applications

### Web Application (Flask)

```python
from flask import Flask, request, jsonify
from main import DocuScopeAI

app_flask = Flask(__name__)
doc_ai = DocuScopeAI()
doc_ai.initialize_models()

@app_flask.route("/analyze", methods=["POST"])
def analyze():
    file = request.files["document"]
    file.save("temp.pdf")
    
    doc_ai.load_document("temp.pdf")
    result = doc_ai.ask_question(request.form["question"])
    
    return jsonify({"answer": result["result"]})
```

### CLI Tool

```python
import argparse
from main import DocuScopeAI

parser = argparse.ArgumentParser()
parser.add_argument("document")
parser.add_argument("--question", default="Summarize this")
args = parser.parse_args()

app = DocuScopeAI()
app.initialize_models()
app.load_document(args.document)
result = app.ask_question(args.question)
print(result["result"])
```

### Jupyter Notebook

```python
from main import DocuScopeAI

app = DocuScopeAI()
app.initialize_models()
app.load_document("data.csv")

# Explore interactively
for question in questions_to_explore:
    result = app.ask_question(question)
    print(f"Q: {question}\nA: {result['result']}\n")
```

---

**Happy analyzing!** 🎉

For more information, see the [main README](../README.md).

