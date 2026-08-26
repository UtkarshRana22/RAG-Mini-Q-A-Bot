import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

def load_index(path="index.pkl"):
    with open(path, "rb") as f:
        return pickle.load(f)

def cosine_similarity(a, b):
   
    similarity=np.dot(a,b)/np.linalg.norm(a)*np.linalg.norm(b)
    return similarity

def retrieve(question, chunks, model, top_k=3):
    question_embedding = model.encode([question])[0]
    for chunk in chunks:
        try:
            score = cosine_similarity(question_embedding, chunk["embedding"])
            chunk["score"] = score
        except:
            chunk["score"]=0
       
    ranked = sorted(chunks, key=lambda c: c["score"], reverse=True)
    return ranked[:top_k]
if __name__ == "__main__":
    chunks = load_index()
    model = SentenceTransformer("all-MiniLM-L6-v2")

    question = "Does NimbusNote have a mobile widget?"
    results = retrieve(question, chunks, model, top_k=3)

    for r in results:
        print(f"[{r['score']:.3f}] {r['filename']} — {r['section']}")