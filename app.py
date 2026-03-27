import streamlit as st
import requests
import numpy as np
import joblib
from sklearn.metrics.pairwise import cosine_similarity

# 🔹 Load embeddings once
@st.cache_resource
def load_data():
    return joblib.load("embeddings.joblib")

df = load_data()


# 🔹 Embedding function
def create_embedding(text_list):
    r = requests.post(
        "http://localhost:11434/api/embed",
        json={
            "model": "bge-m3",
            "input": text_list
        }
    )
    return r.json()["embeddings"]


# 🔹 LLM function
def generate_answer(prompt):
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3",
            "prompt": prompt,
            "temperature": 0.3,
            "num_predict": 200,
            "stream": False
        }
    )
    return r.json()["response"]


# 🔹 RAG pipeline
def get_answer(query):
    query_embedding = create_embedding([query])[0]

    embeddings_matrix = np.vstack(df["embedding"].values)

    similarities = cosine_similarity(
        embeddings_matrix,
        [query_embedding]
    ).flatten()

    top_k = 3
    top_indices = similarities.argsort()[::-1][:top_k]

    results = df.iloc[top_indices]

    context = "\n\n".join(
        [f"Source {i+1}:\n{row['text']}" for i, (_, row) in enumerate(results.iterrows())]
    )

    prompt = f"""
You are a helpful teaching assistant.

Instructions:
- Answer ONLY from the context
- Explain simply
- Use bullet points
- Give example if possible
- If not found say "I don't know"

Context:
{context}

Question:
{query}

Answer:
"""

    answer = generate_answer(prompt)

    return answer


# 🖥️ UI STARTS HERE

st.set_page_config(page_title="AI Teaching Assistant", layout="wide")

st.title("🎓 AI Teaching Assistant")
st.write("Ask questions from your lecture videos!")

# 💬 Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
query = st.chat_input("Ask your question...")

if query:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.write(query)

    # Generate answer
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤔"):
            answer = get_answer(query)
            st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})