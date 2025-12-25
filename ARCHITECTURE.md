# Architecture - DocuScope AI

This document explains how DocuScope AI works under the hood.

## 🏗️ System Architecture

DocuScope AI uses a **Retrieval-Augmented Generation (RAG)** architecture to provide intelligent document analysis with local AI models.

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER INTERACTION LAYER                      │
│  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────┐   │
│  │  Streamlit Web  │  │  CLI Interface   │  │  Python API  │   │
│  │   Interface     │  │   (main.py)      │  │ (api_examples)   │
│  └────────┬────────┘  └─────────┬────────┘  └──────┬───────┘   │
└───────────┼──────────────────────┼───────────────────┼──────────┘
            │                      │                   │
            └──────────────────────┼───────────────────┘
                                   │
┌──────────────────────────────────┴────────────────────────────────┐
│                    DOCUMENT PROCESSING LAYER                      │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │  File Loader (CSVLoader, PyPDFLoader)                   │    │
│  │  ✓ Reads CSV files with headers & rows                  │    │
│  │  ✓ Extracts text from PDF pages                         │    │
│  └────────────────────────┬─────────────────────────────────┘    │
│                           │                                       │
│  ┌────────────────────────▼─────────────────────────────────┐    │
│  │  Text Chunking & Preprocessing                          │    │
│  │  ✓ Splits large documents into manageable chunks        │    │
│  │  ✓ Maintains context between chunks                     │    │
│  │  ✓ Removes noise (special chars, extra whitespace)      │    │
│  └────────────────────────┬─────────────────────────────────┘    │
└───────────────────────────┼────────────────────────────────────────┘
                            │
┌───────────────────────────┴────────────────────────────────────────┐
│                    EMBEDDING & VECTOR LAYER                        │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  Embedding Model: mxbai-embed-large (OllamaEmbeddings)   │   │
│  │  ✓ Converts each text chunk into 1024-dim vector         │   │
│  │  ✓ Captures semantic meaning of document content         │   │
│  │  ✓ Runs locally without external API calls              │   │
│  └────────────────────────┬─────────────────────────────────┘   │
│                           │                                       │
│  ┌────────────────────────▼─────────────────────────────────┐   │
│  │  Vector Database: ChromaDB                              │   │
│  │  ✓ Stores document embeddings                           │   │
│  │  ✓ Indexes vectors for fast similarity search           │   │
│  │  ✓ Persists data locally                                │   │
│  └────────────────────────┬─────────────────────────────────┘   │
└───────────────────────────┼────────────────────────────────────────┘
                            │
┌───────────────────────────┴────────────────────────────────────────┐
│                    RETRIEVAL & RANKING LAYER                       │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  Query Processing                                        │   │
│  │  ✓ Embeds user question into same vector space          │   │
│  │  ✓ Finds k=4 most similar document chunks               │   │
│  │  ✓ Ranks by cosine similarity                           │   │
│  └────────────────────────┬─────────────────────────────────┘   │
└───────────────────────────┼────────────────────────────────────────┘
                            │
┌───────────────────────────┴────────────────────────────────────────┐
│                    GENERATION & REASONING LAYER                    │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  LLM: llama3.2:3b (OllamaLLM)                            │   │
│  │  ✓ Takes user question + relevant document chunks       │   │
│  │  ✓ Generates coherent, context-aware answer             │   │
│  │  ✓ Runs locally, no cloud API dependencies              │   │
│  │  ✓ Lightweight (3B parameters) for fast inference        │   │
│  └────────────────────────┬─────────────────────────────────┘   │
│                           │                                       │
│  ┌────────────────────────▼─────────────────────────────────┐   │
│  │  Output Processing & Source Tracking                    │   │
│  │  ✓ Formats answer for user readability                  │   │
│  │  ✓ Tracks which document chunks were used               │   │
│  │  ✓ Provides citations/source information                │   │
│  └────────────────────────┬─────────────────────────────────┘   │
└───────────────────────────┼────────────────────────────────────────┘
                            │
                            ▼
                  ┌──────────────────────┐
                  │   User Response      │
                  │  ✓ Answer Text       │
                  │  ✓ Source Documents  │
                  │  ✓ Confidence Info   │
                  └──────────────────────┘
```

---

## 📊 Data Flow: Question-to-Answer

Here's what happens when you ask DocuScope AI a question:

### 1. **Question Input**
```
User: "What are the top products by sales?"
```

### 2. **Query Embedding**
```
Question → mxbai-embed-large → Vector (1024 dimensions)
[0.12, -0.34, 0.89, ..., 0.45]
```

### 3. **Document Retrieval**
```
ChromaDB searches vector space:
- Compares query vector to all stored chunks
- Calculates cosine similarity
- Returns top 4 most similar chunks

Results:
[Chunk A] similarity: 0.92
[Chunk B] similarity: 0.87
[Chunk C] similarity: 0.85
[Chunk D] similarity: 0.78
```

### 4. **Context Assembly**
```
Prompt Construction:
─────────────────
System: "You are a helpful AI assistant..."

Context:
"Document excerpts:
[Chunk A]: Product sales data for Q1-Q4
[Chunk B]: Sales rankings by product category
[Chunk C]: Top 10 products by revenue
[Chunk D]: Product sales trends"

User Question:
"What are the top products by sales?"
```

### 5. **Generation**
```
LLM (llama3.2:3b) generates:

"Based on the sales data, the top products by sales are:
1. Product X - $500K revenue
2. Product Y - $450K revenue
3. Product Z - $420K revenue
..."
```

### 6. **Response Delivery**
```
Output:
- Answer text (generated by LLM)
- Source chunks (where answer came from)
- Confidence metrics (optional)
```

---

## 🔧 Core Components

### Document Loaders
**Purpose:** Read different file formats and extract text

```python
# CSV Loader
CSVLoader → Reads CSV files with headers
           → Creates document per row/group

# PDF Loader  
PyPDFLoader → Extracts text from PDF pages
            → Creates document per page
```

### Embedding Model
**Model:** `mxbai-embed-large` (Ollama)

- **Dimensions:** 1024-D vectors
- **Specialty:** General-purpose embeddings
- **Speed:** ~100ms per document chunk
- **Advantage:** Runs locally, no API calls

**Alternative Models:**
- `nomic-embed-text` (smaller, faster)
- `bge-large` (specialized for dense retrieval)

### Vector Database
**Store:** ChromaDB (in-memory + persistent)

- **Vector Storage:** Stores all embeddings with metadata
- **Indexing:** Fast similarity search using HNSW algorithm
- **Persistence:** Saves data to disk by default
- **Query:** Returns top-k similar documents

### Language Model
**Model:** `llama3.2:3b` (Ollama)

- **Parameters:** 3 billion (lightweight, fast)
- **Capabilities:** Instruction-following, reasoning
- **Inference:** ~5-10 seconds per query (CPU)
- **Memory:** ~8GB RAM usage

**Alternative Models:**
- `llama3.2:1b` (smaller, faster)
- `mistral` (more powerful, larger)
- `neural-chat` (optimized for conversation)

### Retrieval Chain
**Framework:** LangChain's RetrievalQA

```python
RetrievalQA = Retriever + LLM + Prompt

1. Retriever: Gets relevant documents
2. LLM: Generates answer from documents
3. Prompt: Formats context + question
```

---

## 🔐 Privacy & Security Architecture

DocuScope AI operates in complete isolation:

```
┌─────────────────────────────────────┐
│    Your Computer (Completely Local) │
│                                     │
│  ┌──────────────────────────────┐  │
│  │  Documents (Your Files)      │  │
│  │  - Loaded from disk          │  │
│  │  - Never transmitted          │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │  Embeddings (ChromaDB)       │  │
│  │  - Stored locally             │  │
│  │  - Never sent to cloud        │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │  Models (Ollama)             │  │
│  │  - Run on your CPU/GPU        │  │
│  │  - No network calls           │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
         ↓ (No outgoing connections)
    [Internet/Cloud]
         ↓ (No incoming model updates)
```

**What Never Happens:**
- ❌ Documents sent to external APIs
- ❌ Queries logged on remote servers
- ❌ Embeddings stored in cloud
- ❌ Metadata collection

---

## ⚙️ Performance Characteristics

### Latency Breakdown (for typical query)

```
Document Loading:     100-500ms    (one-time)
Chunking:              50-200ms    (one-time)
Embedding Documents: 5-30 seconds  (one-time, depends on size)
Query Embedding:       100-200ms   (per query)
Retrieval:              10-50ms    (vector search)
LLM Generation:      5-30 seconds  (per query)
─────────────────────────────────────
Total First Query:   5-60 seconds
Total Follow-up:     5-30 seconds
```

### Memory Usage

```
Base System:        ~2GB RAM
+ Embedding Model:  ~2GB RAM
+ LLM Model:        ~3-8GB RAM (depends on model)
─────────────────────────────
Total:              ~7-12GB RAM
+ Document Data:    Variable (depends on document size)
```

### Scalability

```
Single Document:     ✅ Fast (instant after indexing)
Medium Doc (50p):    ✅ Good (few seconds per query)
Large Doc (500p):    ⚠️  Slower (10-30 seconds per query)
Multiple Docs:       ⚠️  Requires batching (see api_examples.py)
```

---

## 🔄 Processing Pipeline Modes

### Mode 1: Streamlit Web Interface (app.py)
- Real-time file uploads
- Beautiful UI with source tracking
- Best for: Interactive exploration
- Limitation: Single document at a time

### Mode 2: Command Line (main.py)
- Fast, scriptable interface
- Interactive question loop
- Best for: Scripting, automation
- Limitation: One document per session

### Mode 3: Python API (api_examples.py)
- Programmatic document analysis
- Batch processing capability
- Best for: Integration, automation
- Limitation: Requires Python knowledge

---

## 🛠️ Configuration Points

Users can customize:

```python
# Model Selection
embedding_model = "mxbai-embed-large"  # Other options available
llm_model = "llama3.2:3b"              # Other options available

# Retrieval Parameters
k = 4  # Number of documents to retrieve

# Chunking Strategy
chunk_size = ?  # (default: determined by loader)
chunk_overlap = ?  # (default: no overlap)

# LLM Parameters
temperature = 0.7  # Creativity vs consistency
top_p = 0.9        # Diversity of outputs
```

See [docs/CONFIGURATION.md](docs/CONFIGURATION.md) for advanced customization.

---

## 🎯 Key Design Decisions

### Why Ollama?
- ✅ Runs completely offline
- ✅ No API keys needed
- ✅ Privacy-first
- ✅ CPU/GPU flexible

### Why ChromaDB?
- ✅ Simple, lightweight vector store
- ✅ Built for RAG
- ✅ Persistent local storage
- ✅ Fast similarity search

### Why LangChain?
- ✅ RAG pipeline abstraction
- ✅ Document loader ecosystem
- ✅ Easy model swapping
- ✅ Chain composition

### Why llama3.2:3b?
- ✅ Small (runs on consumer hardware)
- ✅ Fast inference
- ✅ Good reasoning ability
- ✅ Instruction-following

---

## 🚀 Future Architecture Considerations

**Possible Enhancements:**

1. **Advanced Chunking**
   - Semantic chunking vs fixed-size
   - Hierarchical chunking for large documents

2. **Reranking**
   - Secondary ranking pass for better results
   - Cross-encoder models

3. **Multi-Modal**
   - Image understanding
   - Table extraction from PDFs

4. **Streaming**
   - Stream LLM responses as they generate
   - Real-time partial answers

5. **Persistence**
   - Save/load vector databases
   - Multi-session support

---

## 📚 Related Documentation

- [QUICK_START.md](QUICK_START.md) - Setup guide
- [docs/API.md](docs/API.md) - Programming interface
- [docs/CONFIGURATION.md](docs/CONFIGURATION.md) - Advanced settings
- [README.md](README.md) - Project overview

