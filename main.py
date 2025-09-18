"""
DocuScope AI - Command Line Interface
=====================================

A privacy-first document analysis tool that uses local AI models to provide
intelligent insights from CSV and PDF files through an interactive CLI.

Usage:
    python main.py [file_path]

Author: David Osei Kumi
License: MIT
"""

import os
import sys
import logging
from pathlib import Path
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    from langchain_community.embeddings import OllamaEmbeddings
    from langchain_community.vectorstores import Chroma
    from langchain_community.document_loaders import CSVLoader, PyPDFLoader
    from langchain.chains import RetrievalQA
    from langchain_community.llms.ollama import Ollama
except ImportError as e:
    print(f"❌ Missing required dependencies: {e}")
    print("📦 Install with: pip install -r requirements.txt")
    sys.exit(1)

class DocuScopeAI:
    """Main class for DocuScope AI CLI application."""
    
    def __init__(self):
        """Initialize the DocuScope AI system."""
        self.qa_chain = None
        self.embedding = None
        self.llm = None
        
    def initialize_models(self) -> bool:
        """Initialize the AI models."""
        try:
            print("🔄 Initializing AI models...")
            
            # Initialize embedding model
            self.embedding = OllamaEmbeddings(model="mxbai-embed-large")
            print("✅ Embedding model loaded: mxbai-embed-large")
            
            # Initialize language model
            self.llm = Ollama(model="llama3.2:3b")
            print("✅ Language model loaded: llama3.2:3b")
            
            return True
            
        except Exception as e:
            print(f"❌ Error initializing models: {e}")
            print("\n🔧 Troubleshooting:")
            print("1. Ensure Ollama is running: ollama serve")
            print("2. Install required models:")
            print("   ollama pull llama3.2:3b")
            print("   ollama pull mxbai-embed-large")
            return False
    
    def validate_file(self, file_path: str) -> bool:
        """Validate the input file."""
        if not file_path:
            print("❌ No file path provided.")
            return False
            
        path = Path(file_path)
        
        if not path.exists():
            print(f"❌ File not found: {file_path}")
            return False
            
        if not path.is_file():
            print(f"❌ Path is not a file: {file_path}")
            return False
            
        if path.suffix.lower() not in ['.csv', '.pdf']:
            print(f"❌ Unsupported file type: {path.suffix}")
            print("📄 Supported formats: CSV (.csv), PDF (.pdf)")
            return False
            
        return True
    
    def load_document(self, file_path: str) -> bool:
        """Load and process a document."""
        try:
            print(f"📄 Loading document: {file_path}")
            path = Path(file_path)
            
            # Choose appropriate loader
            if path.suffix.lower() == ".csv":
                loader = CSVLoader(file_path=file_path)
            elif path.suffix.lower() == ".pdf":
                loader = PyPDFLoader(file_path)
            else:
                print("❌ Unsupported file type.")
                return False
            
            # Load documents
            print("🔄 Processing document content...")
            docs = loader.load()
            
            if not docs:
                print("❌ No content found in the document.")
                return False
                
            print(f"✅ Loaded {len(docs)} document chunks")
            
            # Create vector store
            print("🔄 Creating vector database...")
            vectordb = Chroma.from_documents(
                documents=docs, 
                embedding=self.embedding
            )
            print("✅ Vector database created")
            
            # Create QA chain
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                retriever=vectordb.as_retriever(search_kwargs={"k": 4}),
                return_source_documents=True
            )
            
            print("🎉 Document processed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error loading document: {e}")
            logger.error(f"Document loading error: {e}")
            return False
    
    def ask_question(self, query: str) -> Optional[dict]:
        """Ask a question about the document."""
        if not self.qa_chain:
            print("❌ No document loaded. Please load a document first.")
            return None
            
        try:
            print("🤔 Thinking...")
            result = self.qa_chain({"query": query})
            return result
            
        except Exception as e:
            print(f"❌ Error processing question: {e}")
            logger.error(f"Question processing error: {e}")
            return None
    
    def interactive_session(self):
        """Run an interactive Q&A session."""
        print("\n" + "="*60)
        print("🤖 DocuScope AI - Interactive Session")
        print("="*60)
        print("📝 Type your questions below (type 'exit' to quit)")
        print("💡 Try questions like:")
        print("   • 'Summarize the main points'")
        print("   • 'What are the key findings?'")
        print("   • 'Show me the top 5 items by value'")
        print("-"*60)
        
        while True:
            try:
                # Get user input
                query = input("\n💬 Your question: ").strip()
                
                # Check for exit commands
                if query.lower() in ['exit', 'quit', 'q', 'bye']:
                    print("\n👋 Thank you for using DocuScope AI!")
                    break
                
                # Skip empty queries
                if not query:
                    continue
                
                # Process the question
                result = self.ask_question(query)
                
                if result:
                    print(f"\n📌 Answer:")
                    print("-" * 40)
                    print(result["result"])
                    
                    # Show sources if available
                    if result.get("source_documents"):
                        print(f"\n📑 Sources:")
                        print("-" * 40)
                        seen = set()
                        for i, doc in enumerate(result["source_documents"][:3]):
                            snippet = doc.page_content.strip()
                            if snippet not in seen and len(snippet) > 10:
                                print(f"[{i+1}] {snippet[:200]}...")
                                seen.add(snippet)
                
            except KeyboardInterrupt:
                print("\n\n👋 Session interrupted. Goodbye!")
                break
            except EOFError:
                print("\n\n👋 Session ended. Goodbye!")
                break

def print_banner():
    """Print application banner."""
    print("\n" + "="*60)
    print("📄 DocuScope AI - Document Analysis Tool")
    print("="*60)
    print("🔒 Privacy-first • 🤖 AI-powered • 📊 Local processing")
    print("="*60)

def print_usage():
    """Print usage information."""
    print("\n📖 Usage:")
    print("  python main.py                    # Interactive file selection")
    print("  python main.py <file_path>        # Direct file processing")
    print("\n📄 Supported formats: CSV, PDF")

def get_file_path() -> Optional[str]:
    """Get file path from user input."""
    while True:
        try:
            file_path = input("\n📂 Enter path to your CSV or PDF file: ").strip()
            
            if not file_path:
                continue
                
            # Handle quoted paths
            if file_path.startswith('"') and file_path.endswith('"'):
                file_path = file_path[1:-1]
            elif file_path.startswith("'") and file_path.endswith("'"):
                file_path = file_path[1:-1]
                
            return file_path
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            return None
        except EOFError:
            print("\n👋 Goodbye!")
            return None

def main():
    """Main application entry point."""
    print_banner()
    
    # Initialize DocuScope AI
    app = DocuScopeAI()
    
    # Initialize models
    if not app.initialize_models():
        sys.exit(1)
    
    # Get file path
    file_path = None
    
    if len(sys.argv) > 1:
        # File path provided as command line argument
        file_path = sys.argv[1]
    else:
        # Interactive file selection
        print_usage()
        file_path = get_file_path()
    
    if not file_path:
        sys.exit(0)
    
    # Validate file
    if not app.validate_file(file_path):
        sys.exit(1)
    
    # Load document
    if not app.load_document(file_path):
        sys.exit(1)
    
    # Start interactive session
    app.interactive_session()

if __name__ == "__main__":
    main()
