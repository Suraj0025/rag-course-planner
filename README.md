# 🎓 RAG Course Planning Assistant

## Overview
This project implements a Retrieval-Augmented Generation (RAG) system to answer course-related queries such as prerequisites using a combination of vector search and a language model.

---

## Features
- Document ingestion and chunking
- Semantic search using FAISS
- Context-based answer generation
- Multi-agent pipeline (Retriever + Planner)
- CLI interface (with optional Streamlit UI)

---

## Tech Stack
- Python  
- LangChain  
- HuggingFace Transformers  
- FAISS  
- Sentence Transformers  

---

## Models Used
- Embeddings: `sentence-transformers/all-MiniLM-L6-v2`  
- LLM: `distilgpt2`  

---

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Build vector database
python build_index.py

# Run CLI
python cli.py

(Optional UI)

streamlit run app.py
Example

Input:

What are prerequisites for CS301?

Output:

CS301 requires CS101 and MATH120.
Project Structure
rag-course-planner/
├── ingestion/
├── rag/
├── agents/
├── data/
├── app.py
├── cli.py
├── build_index.py
└── requirements.txt
Notes
Runs locally without API keys
Designed for simplicity and correctness
Easily extendable with better models or UI
Author

Suraj Pandurang Mahadik


---

# 🔥 Why this is perfect

- Clean ✅  
- Short ✅  
- Professional ✅  
- Shows all key points ✅  
- Recruiter-friendly ✅  

---

# 🚀 Final Step

```bash
git add README.md
git commit -m "Updated clean README"
git push
   
