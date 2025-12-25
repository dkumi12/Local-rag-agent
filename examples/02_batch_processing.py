"""
Batch Processing Example - Analyze Multiple Documents

This example shows how to analyze multiple documents with the same set of questions,
useful for generating reports or comparing documents.
"""

from main import DocuScopeAI
import json
from pathlib import Path

def batch_analyze_documents(documents, questions):
    """
    Analyze multiple documents with predefined questions.
    
    Args:
        documents (list): List of file paths to analyze
        questions (list): List of questions to ask each document
    
    Returns:
        dict: Results organized by document and question
    """
    
    # Initialize app once
    app = DocuScopeAI()
    
    if not app.initialize_models():
        print("❌ Failed to initialize models")
        return {}
    
    results = {}
    
    # Process each document
    for doc_path in documents:
        print(f"\n📄 Processing: {doc_path}")
        
        if not Path(doc_path).exists():
            print(f"⚠️  File not found: {doc_path}")
            continue
        
        # Load document
        if not app.load_document(doc_path):
            print(f"❌ Failed to load {doc_path}")
            continue
        
        # Ask all questions
        results[doc_path] = {}
        
        for question in questions:
            print(f"   💬 {question[:50]}...")
            result = app.ask_question(question)
            
            if result:
                results[doc_path][question] = {
                    "answer": result["result"],
                    "sources": len(result.get("source_documents", []))
                }
            else:
                results[doc_path][question] = {
                    "answer": "Failed to generate answer",
                    "sources": 0
                }
        
        print(f"✅ Completed: {doc_path}")
    
    return results

def main():
    # Define documents to analyze
    documents = [
        "data/report_2023.csv",
        "data/report_2024.csv",
        "data/summary.pdf"
    ]
    
    # Define analysis questions
    questions = [
        "What is the total value or sum?",
        "What are the top 5 items?",
        "Summarize the main findings in one sentence",
        "Are there any trends or patterns?",
        "What metrics or numbers are mentioned?"
    ]
    
    print("🚀 Starting batch analysis...")
    print(f"📊 Analyzing {len(documents)} documents")
    print(f"❓ Asking {len(questions)} questions per document")
    print("=" * 60)
    
    # Run batch analysis
    results = batch_analyze_documents(documents, questions)
    
    # Save results to JSON
    output_file = "batch_analysis_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "=" * 60)
    print(f"✅ Analysis complete!")
    print(f"📊 Results saved to: {output_file}")
    
    # Print summary
    print("\n📈 Summary:")
    for doc, doc_results in results.items():
        successful = sum(1 for r in doc_results.values() if "Failed" not in r["answer"])
        print(f"  {doc}: {successful}/{len(questions)} successful")

if __name__ == "__main__":
    main()
