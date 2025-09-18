# 📊 Examples

This directory contains sample files for testing DocuScope AI.

## Sample Files

### 🍕 pizza_reviews.csv
Sample restaurant review dataset with ratings and locations.

**Try asking:**
- "What's the average rating across all reviews?"
- "Which restaurant has the highest rating?"
- "Show me reviews from New York"

### 📑 smartpdf.pdf
Example PDF document for testing document analysis.

**Try asking:**
- "Summarize the main points"
- "What are the key recommendations?"
- "List any important dates mentioned"

## Usage

```bash
# Web interface
streamlit run app.py
# Then upload one of these files

# CLI interface  
python main.py examples/pizza_reviews.csv
python main.py examples/smartpdf.pdf
```

## More Examples

For your own documents, try questions like:

**Business Data:**
- "What are the sales trends?"
- "Which products perform best?"
- "Show me customer demographics"

**Research Papers:**
- "What methodology was used?"
- "What are the main findings?"
- "List the key references"
