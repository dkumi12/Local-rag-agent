# DocuScope AI Examples

This directory contains example files and usage scenarios for DocuScope AI.

## 📄 Example Files

### Pizza Reviews Dataset (pizza_reviews.csv)
A sample CSV dataset containing pizza restaurant reviews with ratings and locations.

**Sample Questions:**
- "What's the average rating across all reviews?"
- "Which restaurant has the highest rating?"
- "Show me reviews from New York"
- "What are the most common words in negative reviews?"

### SmartPDF Document (smartpdf.pdf)
An example PDF document for testing PDF analysis capabilities.

**Sample Questions:**
- "Summarize the main points of this document"
- "What are the key recommendations?"
- "List any important dates or numbers mentioned"

## 🚀 Quick Start Examples

### Web Interface
```bash
# Launch the web app
streamlit run app.py

# Upload pizza_reviews.csv
# Try: "What are the top-rated pizza places?"
```

### Command Line
```bash
# Interactive session
python main.py examples/pizza_reviews.csv

# Example questions:
💬 Your question: What's the average rating?
💬 Your question: Which city has the most reviews?
💬 Your question: Show me 5-star rated places
```

## 📊 CSV Analysis Examples

### Business Intelligence Queries
```
"What are the sales trends over time?"
"Which products have the highest profit margin?"
"Show me customer demographics breakdown"
"What's the correlation between price and sales?"
```

### Data Exploration
```
"How many rows are in this dataset?"
"What are the column names and their data types?"
"Are there any missing values?"
"What's the distribution of values in column X?"
```

## 📄 PDF Analysis Examples

### Research Papers
```
"What is the methodology used in this study?"
"What are the main findings and conclusions?"
"List all the references cited"
"What limitations are mentioned?"
```

### Reports & Documents
```
"Create an executive summary"
"What are the key performance indicators?"
"List all recommendations made"
"What risks are identified?"
```

## 💡 Pro Tips

1. **Be Specific**: Instead of "Tell me about this data", ask "What are the top 5 products by sales volume?"

2. **Use Context**: Reference column names or sections when asking about CSV or PDF content

3. **Iterate**: Ask follow-up questions to dive deeper into insights

4. **Verify**: Use the source citations to verify AI responses

## 🔧 Custom Integration

### Python Script Integration
```python
from main import DocuScopeAI

# Initialize
app = DocuScopeAI()
app.initialize_models()

# Load document
app.load_document("data.csv")

# Ask questions programmatically
result = app.ask_question("What's the total revenue?")
print(result["result"])
```

### Batch Processing
```python
import os

files = ["data1.csv", "data2.pdf", "report.pdf"]
for file in files:
    app.load_document(file)
    result = app.ask_question("Summarize key insights")
    # Process results...
```
