import json
import pickle
from sentence_transformers import SentenceTransformer

def load_chunks(path="chunks.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def build_index(chunks, model_name="all-MiniLM-L6-v2"):
    model = SentenceTransformer(model_name)
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts)
    for chunk, embedding in zip(chunks, embeddings):
        chunk["embedding"] = embedding
    return chunks

if __name__ == "__main__":
    chunks = load_chunks()
    indexed = build_index(chunks)
    with open("index.pkl", "wb") as f:
        pickle.dump(indexed, f)
    print(f"Indexed {len(indexed)} chunks")
    print("Sample embedding length:", len(indexed[0]["embedding"]))