import os
import json
import re

TRANSCRIPTS_DIR = "transcripts"
CHUNKS_DIR = "chunks"

os.makedirs(CHUNKS_DIR, exist_ok=True)

CHUNK_SIZE = 1200   # 🔥 bigger chunk
OVERLAP = 200       # 🔥 overlap for context


def split_into_sentences(text):
    # Split text into sentences
    sentences = re.split(r'(?<=[.!?]) +', text)
    return sentences


for file in os.listdir(TRANSCRIPTS_DIR):
    if not file.endswith(".json"):
        continue

    with open(os.path.join(TRANSCRIPTS_DIR, file), "r", encoding="utf-8") as f:
        data = json.load(f)

    # 🔹 Combine transcript
    full_text = " ".join([segment["text"] for segment in data])

    sentences = split_into_sentences(full_text)

    chunks = []
    current_chunk = ""
    chunk_id = 0

    for sentence in sentences:
        # Add sentence if within size
        if len(current_chunk) + len(sentence) <= CHUNK_SIZE:
            current_chunk += " " + sentence
        else:
            # 🔥 Filter small/weak chunks
            if len(current_chunk.split()) > 30:
                chunks.append({
                    "chunk_id": chunk_id,
                    "source_file": file,
                    "text": current_chunk.strip()
                })
                chunk_id += 1

            # 🔥 overlap logic
            overlap_text = current_chunk[-OVERLAP:]
            current_chunk = overlap_text + " " + sentence

    # Add last chunk
    if len(current_chunk.split()) > 30:
        chunks.append({
            "chunk_id": chunk_id,
            "source_file": file,
            "text": current_chunk.strip()
        })

    output_file = file.replace(".json", "_chunks.json")

    with open(os.path.join(CHUNKS_DIR, output_file), "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=4)

    print(f"✅ Created {len(chunks)} chunks for {file}")

print("\n🎉 Smart chunking complete!")