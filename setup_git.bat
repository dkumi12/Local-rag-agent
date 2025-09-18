@echo off
REM DocuScope AI - Repository Setup Script (Windows)
REM ==================================================
REM This script initializes the git repository and sets up the project for GitHub

echo 🚀 Setting up DocuScope AI repository...

REM Initialize git repository if not already done
if not exist ".git" (
    echo 📦 Initializing Git repository...
    git init
) else (
    echo ✅ Git repository already exists
)

REM Add all files
echo 📁 Adding files to git...
git add .

REM Create initial commit
echo 💾 Creating initial commit...
git commit -m "🎉 Initial commit: DocuScope AI v1.0

✨ Features:
- 📄 Document analysis for CSV and PDF files
- 🤖 Local AI processing with Ollama integration
- 🎨 Beautiful Streamlit web interface
- 💻 Interactive command-line interface
- 🔒 100% offline processing for privacy
- 📊 RAG implementation with ChromaDB
- 📚 Comprehensive documentation

🛠️ Tech Stack:
- Python 3.8+
- LangChain + Ollama
- Streamlit + Custom CSS
- ChromaDB for vector storage

🎯 Ready for production deployment!"

REM Set up main branch
echo 🌿 Setting up main branch...
git branch -M main

echo ✅ Repository setup complete!
echo.
echo 📋 Next steps:
echo 1. Create a new repository on GitHub
echo 2. Run: git remote add origin https://github.com/yourusername/docuscope-ai.git
echo 3. Run: git push -u origin main
echo.
echo 🎉 Your professional repository is ready!

pause
