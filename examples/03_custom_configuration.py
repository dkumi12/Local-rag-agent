"""
Custom Configuration Example - Optimize for Your Needs

This example shows how to customize DocuScope AI for different scenarios:
- Speed optimized
- Quality optimized  
- Memory optimized
"""

from main import DocuScopeAI
from langchain_community.llms.ollama import Ollama
from langchain_community.embeddings import OllamaEmbeddings

# ============================================================================
# PRESET 1: Speed Optimized
# Use smaller, faster models for quick analysis
# ============================================================================

def setup_speed_optimized():
    """
    Optimized for speed. Use smaller models.
    
    Trade-off: Lower quality, but 2-5x faster
    Best for: Quick analysis, low-resource systems
    Memory: ~4-6GB
    Speed: 2-5 seconds per query
    """
    app = DocuScopeAI()
    app.initialize_models()
    
    # Use smaller models
    app.embedding = OllamaEmbeddings(model="bge-small-en")
    app.llm = Ollama(model="llama3.2:1b", temperature=0.0)
    
    # Retrieve fewer documents
    app.qa_chain.retriever.search_kwargs = {"k": 2}
    
    return app

# ============================================================================
# PRESET 2: Quality Optimized
# Use larger, more capable models for better answers
# ============================================================================

def setup_quality_optimized():
    """
    Optimized for quality. Use larger models.
    
    Trade-off: Slower, uses more memory, but higher quality
    Best for: Accurate answers, detailed analysis
    Memory: ~12-16GB
    Speed: 15-45 seconds per query
    """
    app = DocuScopeAI()
    app.initialize_models()
    
    # Use larger models
    app.embedding = OllamaEmbeddings(model="bge-large-en")
    app.llm = Ollama(model="mistral", temperature=0.3)
    
    # Retrieve more documents for better context
    app.qa_chain.retriever.search_kwargs = {"k": 8}
    
    return app

# ============================================================================
# PRESET 3: Balanced (Default)
# Good balance between speed and quality
# ============================================================================

def setup_balanced():
    """
    Balanced between speed and quality (default).
    
    Trade-off: Moderate speed and quality
    Best for: General purpose analysis
    Memory: ~7-12GB
    Speed: 5-15 seconds per query
    """
    app = DocuScopeAI()
    app.initialize_models()
    
    # Uses default models (mxbai-embed-large, llama3.2:3b)
    # k=4 by default
    
    return app

# ============================================================================
# CUSTOM CONFIGURATION EXAMPLE
# Fine-tune specific parameters
# ============================================================================

def setup_custom():
    """
    Custom configuration for specific use case.
    """
    app = DocuScopeAI()
    app.initialize_models()
    
    # Mix and match components
    app.embedding = OllamaEmbeddings(model="mxbai-embed-large")
    app.llm = Ollama(
        model="llama3.2:3b",
        temperature=0.5,      # Moderate creativity
        top_p=0.9             # Diverse outputs
    )
    
    # Custom retrieval settings
    app.qa_chain.retriever.search_kwargs = {
        "k": 5,               # Retrieve 5 documents
        "score_threshold": 0.5  # Only high-confidence matches
    }
    
    return app

# ============================================================================
# DEMONSTRATION
# ============================================================================

def main():
    """Compare different configurations on the same document."""
    
    document_path = "path/to/your/document.pdf"  # Change this!
    question = "What are the main points?"
    
    configurations = {
        "Speed Optimized": setup_speed_optimized,
        "Balanced": setup_balanced,
        "Quality Optimized": setup_quality_optimized,
        "Custom": setup_custom
    }
    
    print("🚀 Comparing DocuScope AI Configurations")
    print("=" * 70)
    print(f"Document: {document_path}")
    print(f"Question: {question}")
    print("=" * 70)
    
    for config_name, setup_func in configurations.items():
        print(f"\n📊 Testing: {config_name}")
        print("-" * 70)
        
        try:
            import time
            
            # Setup configuration
            app = setup_func()
            
            # Load document
            print(f"Loading document...")
            start_load = time.time()
            
            if not app.load_document(document_path):
                print(f"❌ Failed to load document")
                continue
            
            load_time = time.time() - start_load
            print(f"✅ Loaded in {load_time:.2f}s")
            
            # Ask question
            print(f"Asking question...")
            start_query = time.time()
            
            result = app.ask_question(question)
            
            query_time = time.time() - start_query
            
            if result:
                answer = result["result"]
                sources = len(result.get("source_documents", []))
                
                print(f"✅ Answered in {query_time:.2f}s")
                print(f"📌 Answer: {answer[:150]}...")
                print(f"📑 Sources: {sources}")
            else:
                print(f"❌ Failed to get answer")
        
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print("✅ Configuration comparison complete!")
    print("\nRecommendations:")
    print("  • Speed Optimized: For quick analysis or low-resource systems")
    print("  • Balanced: For general purpose analysis (recommended)")
    print("  • Quality Optimized: For high-accuracy requirements")
    print("  • Custom: For specific optimization needs")

if __name__ == "__main__":
    main()
