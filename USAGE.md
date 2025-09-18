# Usage Guide

## Quick Start

### Web Interface (Recommended)

1. **Launch the application**
   ```bash
   streamlit run app.py
   ```

2. **Upload a document**
   - Drag and drop or click to browse
   - Supported formats: CSV, PDF

3. **Ask questions**
   - Type natural language questions
   - Click "Ask" to get AI-powered answers

### Command Line Interface

1. **Run the CLI version**
   ```bash
   python main.py
   ```

2. **Enter document path**
   ```
   Enter path to your CSV or PDF file: /path/to/your/document.pdf
   ```

3. **Interactive questioning**
   ```
   💬 Your question: What are the main findings?
   📌 Answer: [AI generated response]
   ```

## Example Use Cases

### 📊 CSV Data Analysis

**Sample Questions:**
- "What are the top 10 items by value?"
- "Show me the trends over time"
- "What's the average price in the dataset?"
- "Which category has the highest sales?"
- "Are there any outliers in the data?"

### 📄 PDF Document Analysis

**Sample Questions:**
- "Summarize the main points of this document"
- "What are the key recommendations?"
- "Find all mentions of [specific term]"
- "What methodology was used in this research?"
- "List the conclusions from this report"

### 🔍 Advanced Queries

**Complex Analysis:**
- "Compare the performance metrics across different quarters"
- "What patterns do you notice in customer behavior?"
- "Identify potential risks mentioned in the document"
- "Extract all numerical data and their meanings"

## Best Practices

### 📝 Crafting Good Questions

**✅ Good Questions:**
- Specific and clear
- "What are the top 5 products by revenue in 2024?"
- "Summarize the methodology section"

**❌ Avoid:**
- Vague questions: "Tell me about this"
- Questions requiring data not in the document

### 📊 CSV File Tips

**Optimal CSV Structure:**
- Include headers in the first row
- Use consistent data formats
- Avoid special characters in column names
- Keep file size reasonable (< 100MB for best performance)

### 📄 PDF File Tips

**Best Results With:**
- Text-based PDFs (not scanned images)
- Well-structured documents
- Clear headings and sections
- Reasonable file size (< 50MB)

## Features Deep Dive

### 🎯 Source Citations

DocuScope AI provides source references for all answers:
- **Source Documents**: Shows relevant excerpts
- **Transparency**: See exactly where answers come from
- **Verification**: Cross-reference AI responses

### 🔒 Privacy Features

- **Local Processing**: No data sent to external servers
- **Temporary Storage**: Files processed in memory only
- **No Logging**: Queries and responses not stored permanently

### ⚡ Performance Optimization

**Speed Tips:**
- Use SSD storage for better model loading
- Close unnecessary applications
- Smaller documents process faster
- Restart Ollama if responses slow down

## Customization

### 🎨 UI Theming

The app uses a professional color scheme:
- **Background**: Geyser Grey (#C6C5C0)
- **Accent**: Navy (#0A2342) and Copper (#B87333)
- **Typography**: Lora serif font

### 🤖 Model Configuration

**Change Models in Code:**

```python
# Different LLM model
llm = Ollama(model="llama3.2:1b")  # Smaller, faster

# Different embedding model
embedding = OllamaEmbeddings(model="nomic-embed-text")
```

**Available Models:**
- `llama3.2:1b` - Faster, less capable
- `llama3.2:3b` - Balanced (default)
- `llama3.2:8b` - More capable, slower

## Troubleshooting

### Common Issues

**1. Slow Responses**
- Check if Ollama models are loaded: `ollama list`
- Restart Ollama service
- Try smaller models

**2. Upload Errors**
- Verify file format (CSV or PDF)
- Check file size (< 100MB recommended)
- Ensure file is not corrupted

**3. Memory Issues**
- Close other applications
- Use smaller models
- Process smaller documents

**4. No Relevant Answers**
- Check if question relates to document content
- Try rephrasing questions
- Verify document was processed correctly

### Getting Help

If you encounter issues:
1. Check the console output for error messages
2. Verify all dependencies are installed
3. Ensure Ollama models are downloaded
4. Try with a simple test document first

## Next Steps

- Explore the [API Documentation](docs/API.md)
- Check out [Example Scripts](examples/)
- Contribute to the project on GitHub
