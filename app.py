import streamlit as st
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import CSVLoader, PyPDFLoader
from langchain.chains import RetrievalQA
from langchain_community.llms.ollama import Ollama

# ---------------- Page Config ----------------
st.set_page_config(page_title="DocuScope AI", page_icon="📄", layout="centered")

# ---------------- Custom Theme CSS ----------------
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
    /* Buttons */
    .stButton>button {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #0A2342;
        border-radius: 6px;
        font-family: 'Lora', serif !important;
        padding: 0.4em 1.2em;
    }
    .stButton>button:hover {
        background-color: #B87333 !important;
        color: #FFFFFF !important;
    }
    /* Text Input Box */
    .stTextInput>div>div>input {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #0A2342 !important;
        border-radius: 6px !important;
        font-family: 'Lora', serif !important;
        padding: 0.5em !important;
    }
    .stTextInput>div>div>input:focus {
        border: 1px solid #B87333 !important;
        outline: none !important;
    }
    /* File Uploader Dropzone Full Override */
    .stFileUploader div div div {
        background-color: #C6C5C0 !important; /* Force Geyser Grey */
        border: 1px dashed #0A2342 !important; /* Navy dashed border */
        border-radius: 6px !important;
        color: #000000 !important;
        font-family: 'Lora', serif !important;
    }
    /* File Uploader Text & Icons */
    .stFileUploader div div div * {
        color: #000000 !important;
        font-family: 'Lora', serif !important;
    }
    /* File Uploader Button */
    .stFileUploader div div div button {
        background-color: #0A2342 !important;  /* Navy */
        color: #FFFFFF !important;
        border-radius: 6px !important;
        font-family: 'Lora', serif !important;
        border: none !important;
    }
    .stFileUploader div div div button:hover {
        background-color: #B87333 !important;  /* Copper hover */
        color: #FFFFFF !important;
    }
    /* Answer Card */
    .answer-card {
        background: #FFFFFF;
        border: 2px solid #B87333;
        border-radius: 10px;
        padding: 15px;
        margin-top: 20px;
        color: #000000 !important;
    }
    .answer-card h3 {
        color: #B87333 !important;
        margin-bottom: 10px;
    }
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 40px;
        color: #000000 !important;
        font-size: 14px;
    }
    .footer span {
        color: #B87333;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- Header ----------------
st.markdown(
    """
    <div style="text-align:center; margin-bottom:30px;">
        <h1>
            Docu<span style="color:#0A2342;">Scope</span>
            <span style="color:#B87333;">AI</span>
        </h1>
        <p style="font-size:18px;">
            Your private AI agent for documents — classic, clear, offline insights.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------- File Upload ----------------
st.markdown("### 📂 Upload a CSV or PDF")
uploaded_file = st.file_uploader("Drag & drop or browse your document", type=["csv", "pdf"])

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
    llm = Ollama(model="llama3.2:3b")

    # RAG chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectordb.as_retriever(),
        return_source_documents=True
    )

    # ---------------- Query Section ----------------
    st.markdown("### 🔍 Ask Your Document")
    query = st.text_input("💬 Enter your question here:")

    if st.button("Ask"):
        with st.spinner("🤔 Thinking..."):
            result = qa_chain({"query": query})

            # Answer card
            st.markdown(
                f"""
                <div class="answer-card">
                    <h3>🤖 Answer</h3>
                    <p>{result["result"]}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Source documents
            with st.expander("📑 Source Documents"):
                seen = set()
                for i, doc in enumerate(result["source_documents"]):
                    snippet = doc.page_content.strip()
                    if snippet not in seen:
                        st.markdown(f"**Source {i+1}:** {snippet[:500]}...")
                        seen.add(snippet)

else:
    st.info("Please upload a document to get started.")

# ---------------- Footer ----------------
st.markdown(
    """
    <div class="footer">
        🔒 Runs fully offline. Your data never leaves your device.<br>
        <span>Developed by David Osei Kumi</span>
    </div>
    """,
    unsafe_allow_html=True,
)
