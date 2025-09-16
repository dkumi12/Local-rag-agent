import streamlit as st
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import CSVLoader, PyPDFLoader
from langchain.chains import RetrievalQA
from langchain_community.llms.ollama import Ollama  # ✅ Correct import path

# Set page config
st.set_page_config(page_title="📄 Local Document Q&A", layout="centered")
st.title("📄 Local Document Q&A with Ollama")
st.markdown("Upload a **CSV** or **PDF**, ask questions, and get AI-powered answers locally.")

# File uploader
uploaded_file = st.file_uploader("📁 Upload your CSV or PDF", type=["csv", "pdf"])

if uploaded_file is not None:
    file_path = f"{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Load file
    if file_path.endswith(".csv"):
        loader = CSVLoader(file_path=file_path)
    elif file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    docs = loader.load()

    # Embed docs
    embedding = OllamaEmbeddings(model="mxbai-embed-large")
    vectordb = Chroma.from_documents(documents=docs, embedding=embedding)

    # LLM
    llm = Ollama(model="llama3.2:3b")  # ✅ Match the model you pulled

    # RAG chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectordb.as_retriever(),
        return_source_documents=True
    )

    # User query input
    query = st.text_input("💬 Ask a question:", placeholder="e.g. What are people saying about the sauce?")
    if query:
        with st.spinner("Thinking..."):
            result = qa_chain({"query": query})
            st.success(result["result"])
else:
    st.info("Please upload a document to get started.")
