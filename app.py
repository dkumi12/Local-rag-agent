"""
DocuScope AI - Streamlit Web Application
==========================================

A privacy-first document analysis tool that uses local AI models to provide
intelligent insights from CSV and PDF files through a beautiful web interface.

Author: David Osei Kumi
License: MIT
"""

import streamlit as st
import os
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from langchain_community.embeddings import OllamaEmbeddings
    from langchain_community.vectorstores import Chroma
    from langchain_community.document_loaders import CSVLoader, PyPDFLoader
    from langchain.chains import RetrievalQA
    from langchain_community.llms.ollama import Ollama
except ImportError as e:
    st.error(f"Missing required dependencies: {e}")
    st.stop()

# ---------------- Page Configuration ----------------
st.set_page_config(
    page_title="DocuScope AI",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------- Custom Styling ----------------
def load_custom_css():
    """Load custom CSS styling for the application."""
    st.markdown(
        """
        <link href="https://fonts.googleapis.com/css2?family=Lora:wght@400;700&display=swap" rel="stylesheet">
        <style>
        body, .stApp {
            background-color: #C6C5C0 !important; /* Pantone 413C Geyser Grey */
            font-family: 'Lora', serif !important;
            color: #000000 !important;
        }
        h1, h2, h3, h4, h5, h6, p, div, span, label {
            font-family: 'Lora', serif !important;
            color: #000000 !important;
        }
        /* Button Styles */
        .stButton>button {
            background-color: #FFFFFF !important;
            color: #000000 !important;
            border: 1px solid #0A2342;
            border-radius: 6px;
            font-family: 'Lora', serif !important;
            padding: 0.4em 1.2em;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #B87333 !important;
            color: #FFFFFF !important;
            transform: translateY(-1px);
        }
        /* Input Field Styles */
        .stTextInput>div>div>input {
            background-color: #FFFFFF !important;
            color: #000000 !important;
            border: 1px solid #0A2342 !important;
            border-radius: 6px !important;
            font-family: 'Lora', serif !important;
            padding: 0.5em !important;
        }
        .stTextInput>div>div>input:focus {
            border: 2px solid #B87333 !important;
            outline: none !important;
            box-shadow: 0 0 5px rgba(184, 115, 51, 0.3);
        }
        /* File Uploader Styling */
        .stFileUploader div div div {
            background-color: #C6C5C0 !important;
            border: 2px dashed #0A2342 !important;
            border-radius: 8px !important;
            color: #000000 !important;
            font-family: 'Lora', serif !important;
            padding: 1em;
        }
        .stFileUploader div div div button {
            background-color: #0A2342 !important;
            color: #FFFFFF !important;
            border-radius: 6px !important;
            font-family: 'Lora', serif !important;
            border: none !important;
        }
        .stFileUploader div div div button:hover {
            background-color: #B87333 !important;
        }
        /* Answer Card Styling */
        .answer-card {
            background: linear-gradient(135deg, #FFFFFF 0%, #F8F8F8 100%);
            border: 2px solid #B87333;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
            color: #000000 !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .answer-card h3 {
            color: #B87333 !important;
            margin-bottom: 15px;
            font-weight: 700;
        }
        /* Footer Styling */
        .footer {
            text-align: center;
            margin-top: 40px;
            color: #000000 !important;
            font-size: 14px;
            padding: 20px 0;
            border-top: 1px solid #0A2342;
        }
        .footer span {
            color: #B87333;
            font-weight: 600;
        }
        /* Loading Spinner */
        .stSpinner {
            color: #B87333 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def render_header():
    """Render the application header."""
    st.markdown(
        """
        <div style="text-align:center; margin-bottom:30px;">
            <h1 style="font-size: 3em; margin-bottom: 10px;">
                Docu<span style="color:#0A2342;">Scope</span>
                <span style="color:#B87333;">AI</span>
            </h1>
            <p style="font-size:18px; color: #666; font-style: italic;">
                Your private AI agent for documents — classic, clear, offline insights.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def initialize_models() -> tuple:
    """Initialize the AI models and return them."""
    try:
        # Initialize embeddings model
        embedding = OllamaEmbeddings(model="mxbai-embed-large")
        
        # Initialize language model
        llm = Ollama(model="llama3.2:3b")
        
        return embedding, llm
    except Exception as e:
        st.error(f"❌ Error initializing models: {e}")
        st.info("Please ensure Ollama is running and models are installed:")
        st.code("""
        ollama pull llama3.2:3b
        ollama pull mxbai-embed-large
        """)
        st.stop()

def process_document(file_path: str, embedding, llm) -> Optional[RetrievalQA]:
    """Process a document and return a QA chain."""
    try:
        # Load document based on file type
        if file_path.endswith(".csv"):
            loader = CSVLoader(file_path=file_path)
            logger.info(f"Loading CSV file: {file_path}")
        elif file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
            logger.info(f"Loading PDF file: {file_path}")
        else:
            st.error("❌ Unsupported file type. Please upload a CSV or PDF file.")
            return None

        # Load and split documents
        docs = loader.load()
        logger.info(f"Loaded {len(docs)} document chunks")

        if not docs:
            st.error("❌ No content found in the document. Please check the file.")
            return None

        # Create vector store
        vectordb = Chroma.from_documents(documents=docs, embedding=embedding)
        logger.info("Created vector database")

        # Create QA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=vectordb.as_retriever(search_kwargs={"k": 4}),
            return_source_documents=True
        )

        return qa_chain

    except Exception as e:
        st.error(f"❌ Error processing document: {e}")
        logger.error(f"Document processing error: {e}")
        return None

def render_footer():
    """Render the application footer."""
    st.markdown(
        """
        <div class="footer">
            🔒 Runs fully offline. Your data never leaves your device.<br>
            Built with ❤️ using LangChain, Streamlit, and Ollama<br>
            <span>Developed by <a href="https://www.linkedin.com/in/david-osei-kumi" target="_blank" style="color: #B87333; text-decoration: none;">David Osei Kumi</a></span>
        </div>
        """,
        unsafe_allow_html=True,
    )

def main():
    """Main application function."""
    # Load styling
    load_custom_css()
    
    # Render header
    render_header()
    
    # Initialize models
    embedding, llm = initialize_models()
    
    # File upload section
    st.markdown("### 📂 Upload Your Document")
    uploaded_file = st.file_uploader(
        "Drag & drop or browse your document",
        type=["csv", "pdf"],
        help="Supported formats: CSV and PDF files"
    )

    if uploaded_file is not None:
        # Save uploaded file
        file_path = f"temp_{uploaded_file.name}"
        
        try:
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Display file info
            file_size = os.path.getsize(file_path) / 1024  # KB
            st.success(f"✅ Uploaded: {uploaded_file.name} ({file_size:.1f} KB)")
            
            # Process document
            with st.spinner("🔄 Processing document..."):
                qa_chain = process_document(file_path, embedding, llm)
            
            if qa_chain:
                st.success("🎉 Document processed successfully!")
                
                # Query section
                st.markdown("### 🔍 Ask Your Document")
                query = st.text_input(
                    "💬 Enter your question here:",
                    placeholder="e.g., What are the main insights from this document?"
                )

                if st.button("🚀 Ask", type="primary"):
                    if query.strip():
                        with st.spinner("🤔 Thinking..."):
                            try:
                                result = qa_chain({"query": query})
                                
                                # Display answer
                                st.markdown(
                                    f"""
                                    <div class="answer-card">
                                        <h3>🤖 AI Response</h3>
                                        <p>{result["result"]}</p>
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )

                                # Display source documents
                                if result.get("source_documents"):
                                    with st.expander("📑 Source Documents"):
                                        seen = set()
                                        for i, doc in enumerate(result["source_documents"]):
                                            snippet = doc.page_content.strip()
                                            if snippet not in seen and len(snippet) > 10:
                                                st.markdown(f"**Source {i+1}:**")
                                                st.markdown(f"```\n{snippet[:500]}...\n```")
                                                seen.add(snippet)
                                
                            except Exception as e:
                                st.error(f"❌ Error processing query: {e}")
                                logger.error(f"Query processing error: {e}")
                    else:
                        st.warning("⚠️ Please enter a question before asking.")
            
        except Exception as e:
            st.error(f"❌ Error saving file: {e}")
            logger.error(f"File saving error: {e}")
        
        finally:
            # Clean up temporary file
            if os.path.exists(file_path):
                os.remove(file_path)

    else:
        st.info("📤 Please upload a document to get started.")
        
        # Show example usage
        with st.expander("💡 Example Questions"):
            st.markdown("""
            **For CSV files:**
            - "What are the top 5 items by value?"
            - "Show me trends in the data"
            - "What's the average price?"
            
            **For PDF files:**
            - "Summarize the main points"
            - "What are the key recommendations?"
            - "Find information about [specific topic]"
            """)

    # Render footer
    render_footer()

if __name__ == "__main__":
    main()
