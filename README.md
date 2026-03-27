# 🎥 RAG-Based Lecture Video Search System

## 🚀 Overview
This project is an AI-powered system that converts lecture videos into searchable knowledge. Users can ask questions, and the system retrieves the most relevant content using semantic search.

---

## 🧠 How It Works

1. Video → Audio extraction (FFmpeg)
2. Audio → Text transcription using Whisper
3. Text → Chunking into smaller segments
4. Chunks → Embeddings using BGE-M3 (via Ollama)
5. Query → Converted to embedding
6. Cosine similarity used to retrieve top matching chunks

---

## ⚙️ Tech Stack

- Python
- Whisper (Speech-to-Text)
- Ollama (Local LLM runtime)
- BGE-M3 (Embedding model)
- Pandas
- NumPy
- Scikit-learn (Cosine Similarity)

---

## 📂 Project Structure
videos/
audios/
transcripts/
chunks/
read_chunks.py
process_videos.py

---

## 🔍 Features

- Converts lecture videos into searchable text
- Fully local AI pipeline (no API required)
- Semantic search using embeddings
- Efficient retrieval using cosine similarity

---

## 💡 Example

**Input:**
What is HTML?
Relevant chunks from lecture videos explaining HTML concepts

---

## 🧠 Key Concepts

- Retrieval-Augmented Generation (RAG)
- Embeddings & Vector Similarity
- Cosine Similarity
- Speech-to-Text Processing

---

## ⚠️ Limitations

- No UI (currently terminal-based)
- No final LLM answer generation (retrieves chunks only)

---

## 🚀 Future Improvements

- Add LLM-based answer generation
- Build UI (Streamlit / Web app)
- Use FAISS for faster retrieval

---

## 👤 Author

Sanjana Shetty