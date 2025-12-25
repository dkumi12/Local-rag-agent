# Configuration Guide - DocuScope AI

Advanced configuration options for DocuScope AI.

## 🎛️ Overview

DocuScope AI can be customized in several ways:

1. **Model Selection** - Choose different AI models
2. **Retrieval Parameters** - Tune document retrieval
3. **LLM Parameters** - Control generation behavior
4. **System Settings** - Environment configuration

---

## 🤖 Model Selection

### Embedding Models

Embedding models convert text to vectors for similarity search.

#### Available Models (via Ollama)

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| `mxbai-embed-large` | 1.3GB | Medium | High | Default, general-purpose |
| `nomic-embed-text` | 272MB | Fast | Good | Small documents, speed |
| `bge-large-en` | 1.3GB | Medium | Very High | Dense retrieval |
| `bge-small-en` | 33MB | Very Fast | Good | Resource-constrained |

#### Installation & Usage

```bash
# Install new embedding model
ollama pull nomic-embed-text
```

```python
from main import DocuScopeAI
from langchain_community.embeddings import OllamaEmbeddings

app = DocuScopeAI()
app.initialize_models()

# Override embedding model
app.embedding = OllamaEmbeddings(model="nomic-embed-text")

# Continue as normal
app.load_document("document.pdf")
```

#### Comparison

**mxbai-embed-large (Default)**
```python
# Pros: Good balance, general-purpose
# Cons: Larger download, slower than small models
app.embedding = OllamaEmbeddings(model="mxbai-embed-large")
```

**nomic-embed-text (Fast)**
```python
# Pros: Small download (272MB), very fast
# Cons: Slightly lower quality
app.embedding = OllamaEmbeddings(model="nomic-embed-text")
```

**bge-large-en (Best Quality)**
```python
# Pros: Highest quality embeddings
# Cons: Larger, slower
app.embedding = OllamaEmbeddings(model="bge-large-en")
```

### Language Models

Language models generate answers based on context.

#### Available Models (via Ollama)

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| `llama3.2:3b` | 2.0GB | Fast | Good | Default, balanced |
| `llama3.2:1b` | 0.8GB | Very Fast | Fair | Low-resource |
| `mistral` | 4.1GB | Medium | Excellent | High-quality answers |
| `neural-chat` | 4.1GB | Medium | Very Good | Conversational |
| `orca-mini` | 1.3GB | Fast | Good | Reasoning tasks |

#### Installation & Usage

```bash
# Install new language model
ollama pull mistral
```

```python
from main import DocuScopeAI
from langchain_community.llms.ollama import Ollama

app = DocuScopeAI()
app.initialize_models()

# Override language model
app.llm = Ollama(model="mistral")

# Continue as normal
result = app.ask_question("Summarize this document")
```

#### Model Comparison

**llama3.2:3b (Default)**
```python
# Pros: Fast, balanced, low memory
# Cons: Lower quality than larger models
app.llm = Ollama(model="llama3.2:3b")
```

**llama3.2:1b (Lightweight)**
```python
# Pros: Smallest size, fastest
# Cons: Lower reasoning ability
app.llm = Ollama(model="llama3.2:1b")
```

**mistral (Best Quality)**
```python
# Pros: Excellent reasoning, detailed answers
# Cons: Slower, more memory
app.llm = Ollama(model="mistral")
```

**neural-chat (Conversational)**
```python
# Pros: Natural conversation, good UX
# Cons: May be less factual
app.llm = Ollama(model="neural-chat")
```

---

## 🔍 Retrieval Parameters

### Number of Sources (k)

Controls how many document chunks are retrieved for each question.

```python
# Default: 4 sources
app.qa_chain.retriever.search_kwargs = {"k": 4}

# More sources (better recall, slower)
app.qa_chain.retriever.search_kwargs = {"k": 8}

# Fewer sources (faster, may miss context)
app.qa_chain.retriever.search_kwargs = {"k": 2}
```

**When to adjust:**
- **k=2-3**: Fast, concise answers, small documents
- **k=4**: Default, balanced
- **k=6-8**: Complex questions, large documents
- **k=10+**: Exhaustive search, quality over speed

### Similarity Threshold

Minimum similarity score to retrieve a document.

```python
from langchain_community.vectorstores import Chroma

# Modify retriever to use threshold
app.qa_chain.retriever = vectordb.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={
        "k": 4,
        "score_threshold": 0.5  # 0.0 to 1.0
    }
)
```

**Threshold Values:**
- **0.3-0.5**: Liberal (may retrieve irrelevant docs)
- **0.5-0.7**: Balanced (default behavior)
- **0.7-0.9**: Strict (only highly similar docs)

---

## 🧠 Language Model Parameters

### Temperature

Controls randomness/creativity in responses. Higher = more creative, lower = more deterministic.

```python
app.llm = Ollama(
    model="llama3.2:3b",
    temperature=0.7  # Default: 0.7
)
```

**Values:**
- **0.0**: Deterministic, same answer every time
- **0.3-0.5**: Focused, consistent
- **0.7**: Balanced (default)
- **0.9-1.0**: Creative, varied responses

**When to use:**
- **Low (0-0.3)**: Factual QA, data analysis
- **Medium (0.3-0.7)**: General purpose
- **High (0.7-1.0)**: Creative tasks

### Top P

Controls diversity of responses.

```python
app.llm = Ollama(
    model="llama3.2:3b",
    top_p=0.9  # Default: 0.9
)
```

**Values:**
- **0.5**: Only top 50% probable tokens
- **0.9**: More diverse (default)
- **1.0**: All tokens possible

### Max Tokens

Maximum length of generated response.

```python
# Not directly configurable in Ollama wrapper
# But can be adjusted in prompt engineering
```

---

## 🔧 System Configuration

### Ollama Server

By default, DocuScope AI connects to Ollama at `localhost:11434`.

#### Custom Ollama Host

```bash
# Connect to remote Ollama server
export OLLAMA_HOST="http://remote.server:11434"
```

```python
from langchain_community.llms.ollama import Ollama

app.llm = Ollama(
    model="llama3.2:3b",
    base_url="http://remote.server:11434"
)
```

#### Docker Setup

```bash
# Run Ollama in Docker
docker run -d \
  -p 11434:11434 \
  -v ollama:/root/.ollama \
  --name ollama \
  ollama/ollama

# Pull models
docker exec ollama ollama pull llama3.2:3b
docker exec ollama ollama pull mxbai-embed-large
```

### GPU Acceleration

By default, Ollama uses CPU. Enable GPU for faster inference.

#### NVIDIA GPU (CUDA)

```bash
# Install NVIDIA Docker
# https://github.com/NVIDIA/nvidia-docker

docker run -d \
  --gpus all \
  -p 11434:11434 \
  ollama/ollama
```

#### Apple Metal GPU

```bash
# Automatic on Apple Silicon Macs
# Ollama automatically uses Metal acceleration
```

#### AMD GPU (ROCm)

```bash
docker run -d \
  --device /dev/kfd \
  --device /dev/dri \
  -p 11434:11434 \
  ollama/ollama:rocm
```

---

## 📊 Performance Tuning

### For Speed

If latency is critical:

```python
from main import DocuScopeAI
from langchain_community.llms.ollama import Ollama
from langchain_community.embeddings import OllamaEmbeddings

app = DocuScopeAI()

# Small, fast models
app.embedding = OllamaEmbeddings(model="bge-small-en")
app.llm = Ollama(model="llama3.2:1b", temperature=0.0)

# Fewer retrieved documents
app.qa_chain.retriever.search_kwargs = {"k": 2}
```

**Expected latency:** 2-5 seconds per query

### For Quality

If accuracy is critical:

```python
app.embedding = OllamaEmbeddings(model="bge-large-en")
app.llm = Ollama(model="mistral", temperature=0.3)

# More retrieved documents
app.qa_chain.retriever.search_kwargs = {"k": 8}
```

**Expected latency:** 15-45 seconds per query

### For Memory Usage

If running on limited RAM:

```python
# Use smaller models
app.embedding = OllamaEmbeddings(model="bge-small-en")
app.llm = Ollama(model="llama3.2:1b")
```

**Expected memory:** 4-6GB total

---

## 🎯 Preset Configurations

### Lightweight (Minimal Resources)

```python
def setup_lightweight():
    from main import DocuScopeAI
    from langchain_community.llms.ollama import Ollama
    from langchain_community.embeddings import OllamaEmbeddings
    
    app = DocuScopeAI()
    app.initialize_models()
    
    app.embedding = OllamaEmbeddings(model="bge-small-en")
    app.llm = Ollama(model="llama3.2:1b", temperature=0.0)
    app.qa_chain.retriever.search_kwargs = {"k": 2}
    
    return app

# Usage
app = setup_lightweight()
```

### Balanced (Default)

```python
def setup_balanced():
    from main import DocuScopeAI
    
    app = DocuScopeAI()
    app.initialize_models()
    
    # Use defaults (mxbai-embed-large, llama3.2:3b)
    
    return app

# Usage
app = setup_balanced()
```

### High Quality

```python
def setup_high_quality():
    from main import DocuScopeAI
    from langchain_community.llms.ollama import Ollama
    from langchain_community.embeddings import OllamaEmbeddings
    
    app = DocuScopeAI()
    app.initialize_models()
    
    app.embedding = OllamaEmbeddings(model="bge-large-en")
    app.llm = Ollama(model="mistral", temperature=0.3)
    app.qa_chain.retriever.search_kwargs = {"k": 8}
    
    return app

# Usage
app = setup_high_quality()
```

---

## 📈 Benchmarks

### Speed Comparison (per query)

```
Model Setup          | Latency      | Memory  | Quality
─────────────────────────────────────────────────────────
Lightweight          | 2-5 sec      | 4-6GB   | Fair
Balanced (default)   | 5-15 sec     | 7-12GB  | Good
High Quality         | 15-45 sec    | 12-16GB | Excellent
```

### Quality Comparison (subjective)

```
Model Setup    | Factuality | Relevance | Completeness
────────────────────────────────────────────────────
Lightweight    | Good       | Good      | Fair
Balanced       | Good       | Excellent | Good
High Quality   | Excellent  | Excellent | Excellent
```

---

## 🐛 Troubleshooting Configuration

### Slow Performance

**Check:**
1. Model size (larger = slower)
2. Retrieval k value (higher = slower)
3. CPU/GPU utilization

**Solution:**
```python
# Use faster models
app.llm = Ollama(model="llama3.2:1b")
app.qa_chain.retriever.search_kwargs = {"k": 3}
```

### Poor Quality Answers

**Check:**
1. Embedding model quality
2. LLM quality
3. Retrieval k value

**Solution:**
```python
# Use better models
app.embedding = OllamaEmbeddings(model="bge-large-en")
app.llm = Ollama(model="mistral")
app.qa_chain.retriever.search_kwargs = {"k": 8}
```

### High Memory Usage

**Check:**
1. Model size
2. Document size
3. Chunk count

**Solution:**
```python
# Use smaller models
app.embedding = OllamaEmbeddings(model="bge-small-en")
app.llm = Ollama(model="llama3.2:1b")
```

### Connection Issues

**Check:**
```bash
# Verify Ollama is running
curl http://localhost:11434/api/tags

# Check available models
ollama list
```

**Solution:**
```bash
# Start Ollama server
ollama serve
```

---

## 📚 Related Documentation

- [QUICK_START.md](../QUICK_START.md) - Setup guide
- [ARCHITECTURE.md](../ARCHITECTURE.md) - System design
- [docs/API.md](../docs/API.md) - API reference
- [README.md](../README.md) - Project overview

