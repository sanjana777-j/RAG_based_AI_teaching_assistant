import requests
import os
import json
import pandas as pd
import joblib

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


def extract_text(chunk):
    # 🔥 Try all possible fields
    for key, value in chunk.items():
        if isinstance(value, str) and len(value.strip()) > 20:
            return value.strip()
    return ""


folder_path = "chunks"
files = os.listdir(folder_path)

all_data = []
chunk_id = 0

for file in files:
    with open(os.path.join(folder_path, file), "r", encoding="utf-8") as f:
        content = json.load(f)

    print(f"\n🚀 Processing: {file}")

    if isinstance(content, list):
        chunks = content
    else:
        chunks = content.get("chunks", [])

    valid_chunks = []

    for chunk in chunks:
        text = extract_text(chunk)

        if text != "":
            valid_chunks.append({
                "text": text,
                "title": chunk.get("title", ""),
                "number": chunk.get("number", "")
            })

    if not valid_chunks:
        print("⚠️ Skipping file (no usable text)")
        continue

    print(f"✅ Found {len(valid_chunks)} valid chunks")

    texts = [c["text"] for c in valid_chunks]

    embeddings = create_embedding(texts)

    for i, chunk in enumerate(valid_chunks):
        all_data.append({
            "chunk_id": chunk_id,
            "title": chunk["title"],
            "number": chunk["number"],
            "text": chunk["text"],
            "embedding": embeddings[i]
        })
        chunk_id += 1


# ✅ FINAL CHECK (no crash now)
if len(all_data) == 0:
    raise Exception("❌ No usable data found in ANY file")

df = pd.DataFrame(all_data)

print("\n📊 Columns:", df.columns)
print("📊 Total rows:", len(df))

joblib.dump(df, "embeddings.joblib")

print("💾 Saved as embeddings.joblib")