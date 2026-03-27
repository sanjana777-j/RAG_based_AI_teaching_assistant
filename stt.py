import whisper
import os
import json

model = whisper.load_model("small")  # better for your i5

audio_files = os.listdir("audios")

for file in audio_files:
    if file.endswith(".mp3"):
        print(f"Transcribing {file}...")

        result = model.transcribe(
            audio=f"audios/{file}",
            language="en"
        )

        chunks = []
        for segment in result["segments"]:
            chunks.append({
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"]
            })

        output_file = file.replace(".mp3", ".json")

        with open(f"transcripts/{output_file}", "w") as f:
            json.dump(chunks, f, indent=4)

        print(f"Saved {output_file}")