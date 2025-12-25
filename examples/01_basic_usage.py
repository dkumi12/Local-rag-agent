"""
Basic Example - Simple Document Analysis

This example shows the simplest way to use DocuScope AI:
1. Initialize
2. Load a document
3. Ask a question
"""

from main import DocuScopeAI

def main():
    # Step 1: Create instance and initialize
    print("🚀 Starting DocuScope AI...")
    app = DocuScopeAI()
    
    if not app.initialize_models():
        print("❌ Failed to initialize models. Make sure Ollama is running.")
        return
    
    # Step 2: Load document
    document_path = "path/to/your/document.csv"  # Change this!
    print(f"\n📄 Loading: {document_path}")
    
    if not app.load_document(document_path):
        print(f"❌ Failed to load {document_path}")
        return
    
    print("✅ Document loaded successfully!")
    
    # Step 3: Ask questions
    questions = [
        "What's the main topic?",
        "Summarize the key points",
        "What are the top 5 items?"
    ]
    
    for question in questions:
        print(f"\n💬 Question: {question}")
        result = app.ask_question(question)
        
        if result:
            print(f"📌 Answer: {result['result']}\n")
        else:
            print("❌ Failed to get answer\n")

if __name__ == "__main__":
    main()
