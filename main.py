from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import CSVLoader
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama

# Load CSV and split into documents
loader = CSVLoader(file_path='pizza_reviews.csv')
docs = loader.load()

# Set up embedding
embedding = OllamaEmbeddings(model="mxbai-embed-large")
vectordb = Chroma.from_documents(documents=docs, embedding=embedding)

# Set up Ollama LLM
llm = Ollama(model="llama3.2:3b")

# Build RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectordb.as_retriever(),
    return_source_documents=True
)

# Query the AI
while True:
    query = input("Ask a question: ")
    if query.lower() in ['exit', 'quit']:
        break
    result = qa_chain({"query": query})
    print("\n📌 Answer:", result["result"])
