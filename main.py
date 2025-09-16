from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import CSVLoader, PyPDFLoader
from langchain.chains import RetrievalQA
from langchain_community.llms.ollama import Ollama  # ✅ Correct import

import os

# 📂 Prompt user to provide a file path
file_path = input("Enter path to your CSV or PDF file: ").strip()

# ✅ Validate file
if not os.path.exists(file_path):
    print("❌ File not found. Please check the path.")
    exit()

# 📄 Load the document
if file_path.endswith(".csv"):
    loader = CSVLoader(file_path=file_path)
elif file_path.endswith(".pdf"):
    loader = PyPDFLoader(file_path)
else:
    print("❌ Unsupported file type. Use CSV or PDF.")
    exit()

docs = loader.load()

# 🧠 Embeddings & Vector Store
embedding = OllamaEmbeddings(model="mxbai-embed-large")
vectordb = Chroma.from_documents(documents=docs, embedding=embedding)

# 🤖 Load local LLM
llm = Ollama(model="llama3.2:3b")  # ✅ Ensure model name matches Ollama list

# 🔁 Retrieval-Augmented QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectordb.as_retriever(),
    return_source_documents=True
)

# 🧠 Query loop
print("\n✅ Ready! Ask questions about the document (type 'exit' to quit):\n")

while True:
    query = input("💬 Your question: ")
    if query.lower() in ['exit', 'quit']:
        break
    result = qa_chain({"query": query})
    print("📌 Answer:", result["result"])
