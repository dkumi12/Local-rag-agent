"""
DocuScope AI API Usage Examples
===============================

This file demonstrates how to use DocuScope AI as a Python library
instead of through the web interface or command line.
"""

# Example 1: Basic API Usage
def basic_api_example():
    """Basic example of using DocuScope AI programmatically."""
    
    from main import DocuScopeAI
    
    # Step 1: Create instance
    app = DocuScopeAI()
    
    # Step 2: Initialize AI models
    print("🔄 Initializing AI models...")
    if not app.initialize_models():
        print("❌ Failed to initialize models")
        return
    print("✅ Models initialized!")
    
    # Step 3: Load a document
    document_path = "examples/pizza_reviews.csv"
    print(f"📄 Loading document: {document_path}")
    if not app.load_document(document_path):
        print("❌ Failed to load document")
        return
    print("✅ Document loaded!")
    
    # Step 4: Ask questions
    questions = [
        "What's the average rating?",
        "Which restaurant has the highest rating?",
        "How many reviews are there total?"
    ]
    
    for question in questions:
        print(f"\n💬 Question: {question}")
        result = app.ask_question(question)
        if result:
            print(f"🤖 Answer: {result['result']}")
        else:
            print("❌ No answer received")

# Example 2: Batch Processing Multiple Files
def batch_processing_example():
    """Process multiple documents automatically."""
    
    from main import DocuScopeAI
    import os
    
    app = DocuScopeAI()
    app.initialize_models()
    
    # List of files to process
    files = [
        "examples/pizza_reviews.csv",
        "examples/smartpdf.pdf"
    ]
    
    # Standard questions to ask each document
    questions = [
        "Summarize the main content",
        "What are the key insights?",
        "List any important numbers or statistics"
    ]
    
    results = {}
    
    for file_path in files:
        print(f"\n📄 Processing: {file_path}")
        
        if app.load_document(file_path):
            file_results = {}
            
            for question in questions:
                result = app.ask_question(question)
                if result:
                    file_results[question] = result["result"]
            
            results[file_path] = file_results
        
        print(f"✅ Completed: {file_path}")
    
    return results

# Example 3: Integration with Other Python Applications
def integration_example():
    """Show how to integrate with other Python applications."""
    
    import pandas as pd
    from main import DocuScopeAI
    
    # Simulate a web application or data pipeline
    def analyze_uploaded_file(file_path, user_question):
        """Function that could be called from a web API or data pipeline."""
        
        app = DocuScopeAI()
        
        # Initialize models (in production, you'd do this once)
        if not app.initialize_models():
            return {"error": "Failed to initialize AI models"}
        
        # Validate file
        if not app.validate_file(file_path):
            return {"error": f"Invalid file: {file_path}"}
        
        # Load document
        if not app.load_document(file_path):
            return {"error": f"Failed to process document: {file_path}"}
        
        # Get answer
        result = app.ask_question(user_question)
        if result:
            return {
                "success": True,
                "answer": result["result"],
                "sources": len(result.get("source_documents", [])),
                "file_processed": file_path
            }
        else:
            return {"error": "Failed to get answer"}
    
    # Example usage in a web application
    response = analyze_uploaded_file(
        "examples/pizza_reviews.csv",
        "What's the most popular restaurant?"
    )
    
    print("Web API Response:", response)

# Example 4: Custom Analysis Pipeline
def custom_pipeline_example():
    """Create a custom analysis pipeline."""
    
    from main import DocuScopeAI
    import json
    
    def create_document_report(file_path):
        """Generate a comprehensive report for any document."""
        
        app = DocuScopeAI()
        app.initialize_models()
        app.load_document(file_path)
        
        # Predefined analysis questions
        analysis_questions = {
            "summary": "Provide a brief summary of this document",
            "key_points": "What are the 3 most important points?",
            "statistics": "List any numbers, percentages, or statistics",
            "recommendations": "Are there any recommendations or action items?",
            "concerns": "Are there any problems or concerns mentioned?"
        }
        
        report = {
            "document": file_path,
            "analysis": {}
        }
        
        for category, question in analysis_questions.items():
            result = app.ask_question(question)
            if result:
                report["analysis"][category] = result["result"]
        
        return report
    
    # Generate report
    report = create_document_report("examples/pizza_reviews.csv")
    
    # Save report as JSON
    with open("document_analysis_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print("📊 Report generated: document_analysis_report.json")

if __name__ == "__main__":
    print("🤖 DocuScope AI API Examples")
    print("=" * 40)
    
    print("\n1. Basic API Usage:")
    # basic_api_example()  # Uncomment to run
    
    print("\n2. Batch Processing:")
    # batch_processing_example()  # Uncomment to run
    
    print("\n3. Integration Example:")
    # integration_example()  # Uncomment to run
    
    print("\n4. Custom Pipeline:")
    # custom_pipeline_example()  # Uncomment to run
    
    print("\nTo run examples, uncomment the function calls above!")
