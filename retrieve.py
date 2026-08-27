import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
THRESH_HOLD=0.35

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
def querier(question):
    chunks = load_index()
    model = SentenceTransformer("all-MiniLM-L6-v2")

    
    results = retrieve(question, chunks, model, top_k=3)
    context=''
    for r in results:
        
       # print(f"[{r['score']:.3f}] {r['filename']} — {r['section']}")
        if r['score']>THRESH_HOLD:
            if context=='':
                context+=f"[{r['score']:.3f}] {r['filename']} {r['section']} — {r['text']}"
            else:
                context+='\n'+f"[{r['score']:.3f}] {r['filename']} {r['section']} — {r['text']}"
    return context
