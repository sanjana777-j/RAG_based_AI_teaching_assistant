RAG-Based AI Teaching Assistant
Upload a lecture, podcast, or any audio/video — ask questions, get answers grounded in what was actually said.
What it does
Most AI assistants just make stuff up. This one only answers from your content. You drop in a video or audio file, it transcribes it, indexes it, and then when you ask something, it finds the relevant parts and uses those to generate a response.
How it works

Audio/video gets transcribed via Whisper
Transcript is split into overlapping chunks so context isn't lost at boundaries
Chunks are embedded and stored locally (the embeddings.joblib file)
On a query, the closest chunks are retrieved semantically
Those chunks get passed to an LLM which produces the final answer

Stack

Streamlit — UI
Whisper — speech-to-text
Sentence Transformers — embeddings + vector search
Claude / OpenAI — answer generation

Project layout
rag_based_ai/
├── app.py                 # Streamlit frontend
├── process_incoming.py    # Entry point for new files
├── process_videos.py      # Handles video → audio extraction
├── stt.py                 # Whisper transcription
├── create_chunks.py       # Splits transcript into chunks
├── read_chunks.py         # Loads chunks + runs similarity search
└── embeddings.joblib      # Persisted embeddings (auto-generated)
Getting started
bashpip install -r requirements.txt
streamlit run app.py
Drop a file in the UI, wait for processing, then start asking questions.
