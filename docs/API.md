# 🔧 API Documentation

## What is the API?

The **API (Application Programming Interface)** allows you to use DocuScope AI **programmatically** in your own Python scripts, web applications, or data pipelines - instead of just using the web interface or command line.

## 🚀 Why Use the API?

**Instead of manually uploading files and asking questions**, you can:
- **Automate document analysis** for hundreds of files
- **Integrate with web applications** (Flask, Django, FastAPI)
- **Build custom workflows** and data pipelines
- **Create batch processing scripts** for business reports
- **Embed AI analysis** in existing Python applications

## 💻 Basic API Usage

```python
from main import DocuScopeAI

# 1. Create instance
app = DocuScopeAI()

# 2. Initialize AI models (do this once)
app.initialize_models()

# 3. Load a document
app.load_document("my_data.csv")

# 4. Ask questions programmatically
result = app.ask_question("What are the sales trends?")
print(result["result"])  # AI answer
print(result["source_documents"])  # Source citations
```

## 🔧 Available Methods

### `DocuScopeAI()` 
Create a new instance of the document analyzer.

### `initialize_models()`
Load the AI models (Ollama). Do this once per application.
- **Returns**: `True` if successful, `False` if failed
- **Note**: Requires Ollama to be running with models installed

### `validate_file(file_path)`
Check if a file exists and is supported (CSV or PDF).
- **Parameters**: `file_path` (string) - path to file
- **Returns**: `True` if valid, `False` if not

### `load_document(file_path)`
Process a document for analysis.
- **Parameters**: `file_path` (string) - path to CSV or PDF file
- **Returns**: `True` if successful, `False` if failed
- **Note**: Must call this before asking questions

### `ask_question(query)`
Ask a question about the loaded document.
- **Parameters**: `query` (string) - your question in natural language
- **Returns**: Dictionary with `result` and `source_documents`, or `None` if failed

## 📊 Practical Examples

### Example 1: Analyze Business Reports
```python
from main import DocuScopeAI

def analyze_monthly_reports():
    app = DocuScopeAI()
    app.initialize_models()
    
    reports = ["jan_sales.csv", "feb_sales.csv", "mar_sales.csv"]
    
    for report in reports:
        app.load_document(report)
        
        # Ask standard business questions
        revenue = app.ask_question("What's the total revenue?")
        trends = app.ask_question("What are the key trends?")
        
        print(f"\n{report}:")
        print(f"Revenue: {revenue['result']}")
        print(f"Trends: {trends['result']}")
```

### Example 2: Web Application Integration
```python
# Flask web app example
from flask import Flask, request, jsonify
from main import DocuScopeAI

app_flask = Flask(__name__)
docuscope = DocuScopeAI()
docuscope.initialize_models()  # Initialize once when app starts

@app_flask.route('/analyze', methods=['POST'])
def analyze_document():
    file_path = request.json['file_path']
    question = request.json['question']
    
    if docuscope.load_document(file_path):
        result = docuscope.ask_question(question)
        return jsonify({
            "answer": result["result"],
            "sources_count": len(result["source_documents"])
        })
    
    return jsonify({"error": "Failed to process document"})
```

### Example 3: Batch Processing
```python
def batch_analyze_documents(file_list, questions):
    """Analyze multiple documents with the same questions."""
    
    app = DocuScopeAI()
    app.initialize_models()
    
    results = {}
    
    for file_path in file_list:
        print(f"Processing {file_path}...")
        
        if app.load_document(file_path):
            file_results = {}
            
            for question in questions:
                answer = app.ask_question(question)
                if answer:
                    file_results[question] = answer["result"]
            
            results[file_path] = file_results
    
    return results

# Usage
files = ["data1.csv", "data2.pdf", "report.pdf"]
questions = [
    "What are the main findings?",
    "Any risks mentioned?",
    "What are the recommendations?"
]

analysis_results = batch_analyze_documents(files, questions)
```

## 🔄 Response Format

When you call `ask_question()`, you get back a dictionary:

```python
{
    "result": "The AI's answer to your question",
    "source_documents": [
        {
            "page_content": "Relevant text from the document",
            "metadata": {"source": "file.pdf", "page": 1}
        }
    ]
}
```

## ⚠️ Error Handling

Always check return values:

```python
app = DocuScopeAI()

# Check if models loaded
if not app.initialize_models():
    print("Error: Could not load AI models")
    exit()

# Check if document loaded
if not app.load_document("myfile.pdf"):
    print("Error: Could not load document")
    exit()

# Check if question was answered
result = app.ask_question("What is this about?")
if result is None:
    print("Error: Could not get answer")
else:
    print(f"Answer: {result['result']}")
```

## 🎯 Real-World Use Cases

1. **Business Intelligence**: Automatically analyze sales reports, customer feedback
2. **Research**: Process academic papers, extract key findings
3. **Compliance**: Analyze contracts, policies for specific clauses
4. **Content Management**: Categorize and summarize documents
5. **Data Pipeline**: Integrate AI analysis into ETL workflows

The API makes DocuScope AI a **powerful tool for automation** rather than just a manual document viewer!

---

## 👨‍💻 Author

**David Osei Kumi**  
LinkedIn: [linkedin.com/in/david-osei-kumi](https://www.linkedin.com/in/david-osei-kumi)  
GitHub: [@dkumi12](https://github.com/dkumi12)
