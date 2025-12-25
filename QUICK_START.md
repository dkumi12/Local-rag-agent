# Quick Start Guide - DocuScope AI

Get DocuScope AI running in 5 minutes. This guide walks you through installation and your first document analysis.

## ⚡ 5-Minute Setup

### Step 1: Install Ollama (2 minutes)

Ollama provides the local AI models that power DocuScope AI.

**macOS/Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
Download from [ollama.ai](https://ollama.ai)

### Step 2: Pull Required Models (2 minutes)

Open a terminal and run:

```bash
# Large language model (for understanding & answering)
ollama pull llama3.2:3b

# Embedding model (for document understanding)
ollama pull mxbai-embed-large
```

⏱️ **This downloads ~3GB total** (one-time setup)

### Step 3: Install & Run DocuScope AI (1 minute)

```bash
# Clone the repository
git clone https://github.com/dkumi12/Local-rag-agent.git
cd Local-rag-agent

# Install Python dependencies
pip install -r requirements.txt
```

**Option A: Web Interface (Recommended)**
```bash
streamlit run app.py
```
Opens at `http://localhost:8501`

**Option B: Command Line**
```bash
python main.py your_document.csv
# or
python main.py your_document.pdf
```

---

## 🎯 Your First Analysis (1-2 minutes)

### Using the Web Interface

1. Launch with `streamlit run app.py`
2. Click **"Upload a CSV or PDF"**
3. Select your document
4. Type a question in the text box:
   - "What's the main topic?"
   - "Summarize the key points"
   - "Give me the top 5 items by value"
5. Click **"Ask"**

### Using Command Line

```bash
python main.py examples/sample.csv

# You'll see:
# 🤖 DocuScope AI - Interactive Session
# 💬 Your question: What's the average value?
```

---

## 🔧 Troubleshooting

### ❌ "Ollama not found"
Make sure Ollama is running in the background:
```bash
# macOS/Linux
ollama serve

# Windows
ollama serve  # Or use the Ollama app from taskbar
```

### ❌ "Model not found"
Pull the required models:
```bash
ollama pull llama3.2:3b
ollama pull mxbai-embed-large
```

### ❌ "File not found"
Make sure you use the full path to your file:
```bash
# ✅ Correct
python main.py /Users/name/Documents/myfile.pdf

# ❌ Wrong
python main.py myfile.pdf
```

### ❌ "Permission denied"
On macOS/Linux:
```bash
chmod +x main.py
python main.py document.pdf
```

---

## 📂 Next Steps

- **Explore Examples:** Check `/examples` folder for sample documents
- **Learn the API:** Read [docs/API.md](docs/API.md) to use in your own code
- **Configure Models:** See [docs/CONFIGURATION.md](docs/CONFIGURATION.md) for advanced setup
- **Understand Architecture:** Read [ARCHITECTURE.md](ARCHITECTURE.md) for technical details

---

## 💡 Common Questions

**Q: Can I use different models?**
A: Yes! See [docs/CONFIGURATION.md](docs/CONFIGURATION.md) for other models like Llama 2, Mistral, etc.

**Q: How large can my documents be?**
A: DocuScope AI can handle documents from a few pages to hundreds of pages. Processing time depends on document size and your computer's RAM.

**Q: Is my data private?**
A: Completely. Everything runs locally on your computer. No data leaves your device.

**Q: Can I use this in production?**
A: Yes! See [docs/API.md](docs/API.md) for integration examples.

---

## 🚀 You're Ready!

You now have a fully functional local AI system for document analysis. Happy analyzing! 🎉

For detailed information, check out the full [README.md](README.md).
