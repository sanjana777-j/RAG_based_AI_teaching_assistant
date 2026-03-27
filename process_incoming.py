import requests
import numpy as np
import joblib
from sklearn.metrics.pairwise import cosine_similarity

# 🔹 Casual inputs (greetings etc.)
CASUAL_INPUTS = ["hi", "hello", "good morning", "good evening", "hey"]


# 🔹 Embedding
def create_embedding(text_list):
    r = requests.post(
        "http://localhost:11434/api/embed",
        json={
            "model": "bge-m3",
            "input": text_list
        }
    )

    if r.status_code != 200:
        raise Exception(f"Embedding API failed: {r.text}")

    return r.json().get("embeddings", [])


# 🔹 LLM
def generate_answer(prompt):
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3",          # ⚡ fast model
            "prompt": prompt,
            "temperature": 0.2,       # 🔥 low = less hallucination
            "num_predict": 200,
            "stream": False
        }
    )

    if r.status_code != 200:
        raise Exception(f"LLM API failed: {r.text}")

    return r.json().get("response", "")


# 🔹 Load embeddings
df = joblib.load("embeddings.joblib")

print("📊 Loaded columns:", df.columns)

if "embedding" not in df.columns:
    raise Exception("❌ 'embedding' column missing. Re-run read_chunks.py")

print("🤖 RAG Assistant Ready\n")


while True:
    query = input("❓ Ask a Question: ")

    if query.lower() == "exit":
        break

    query_lower = query.lower().strip()

    # 🔥 STEP 1: Handle casual inputs
    if query_lower in CASUAL_INPUTS:
        print("\n💡 Final Answer:\n")
        print("Hey 😊 I’m your lecture assistant. Ask me something from your lecture!")
        print("\n" + "-"*50)
        continue

    # 🔹 Create query embedding
    query_embedding = create_embedding([query])[0]

    embeddings_matrix = np.vstack(df["embedding"].values)

    similarities = cosine_similarity(
        embeddings_matrix,
        [query_embedding]
    ).flatten()

    top_k = 3
    top_indices = similarities.argsort()[::-1][:top_k]

    results = df.iloc[top_indices]

    # 🔥 STEP 2: Similarity threshold check
    max_similarity = similarities[top_indices[0]]

    if max_similarity < 0.4:
        print("\n💡 Final Answer:\n")
        print("I can only answer questions related to your lecture content 😊")
        print("\n" + "-"*50)
        continue

    # 🔍 Show retrieved context (debug)
    print("\n🔍 Retrieved Context:")
    for _, row in results.iterrows():
        print(f"\n📌 {row['title']} ({row['number']})")
        print(row['text'][:150] + "...")

    # 🔥 Better context formatting
    context = "\n\n".join(
        [f"Source {i+1}:\n{row['text']}" for i, (_, row) in enumerate(results.iterrows())]
    )

    # 🔥 STRICT PROMPT
    prompt = f"""
You are a strict AI teaching assistant.

Rules:
- Answer ONLY if the answer is clearly present in the context
- If NOT present, reply EXACTLY: "I don't know"
- Do NOT use outside knowledge
- Do NOT guess

Context:
{context}

Question:
{query}

Answer:
"""

    # 🔹 Generate answer
    answer = generate_answer(prompt)

    print("\n💡 Final Answer:\n")
    print(answer)
    print("\n" + "-"*50)