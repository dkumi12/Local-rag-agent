# Installation & Setup Guide

## System Requirements

- **Python**: 3.8 or higher
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Storage**: 2GB free space for models
- **OS**: Windows, macOS, or Linux

## Step-by-Step Installation

### 1. Install Ollama

**Windows/macOS:**
- Download from [ollama.ai](https://ollama.ai/)
- Run the installer

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. Download Required AI Models

```bash
# Large language model for question answering
ollama pull llama3.2:3b

# Embedding model for document vectorization  
ollama pull mxbai-embed-large
```

### 3. Clone and Setup the Project

```bash
# Clone repository
git clone https://github.com/yourusername/docuscope-ai.git
cd docuscope-ai

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
# Test Ollama models
ollama list

# Should show:
# llama3.2:3b
# mxbai-embed-large
```

### 5. Run the Application

```bash
# Web interface
streamlit run app.py

# Command line interface
python main.py
```

## Troubleshooting

### Common Issues

**"Model not found" error:**
```bash
ollama pull llama3.2:3b
ollama pull mxbai-embed-large
```

**Streamlit not opening:**
- Check if port 8501 is available
- Try: `streamlit run app.py --server.port 8502`

**Memory issues:**
- Close other applications
- Consider using smaller models if available

**Import errors:**
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Model Alternatives

If you have limited resources, try these smaller models:

```bash
# Smaller LLM (faster but less capable)
ollama pull llama3.2:1b

# Update main.py and app.py to use:
llm = Ollama(model="llama3.2:1b")
```

## Performance Tips

- **SSD Storage**: Store models on SSD for faster loading
- **RAM**: More RAM allows processing larger documents
- **CPU**: Multi-core processors improve response time

## Next Steps

Once installed, check out:
- [Usage Guide](USAGE.md)
- [API Documentation](docs/API.md)
- [Examples](examples/)
