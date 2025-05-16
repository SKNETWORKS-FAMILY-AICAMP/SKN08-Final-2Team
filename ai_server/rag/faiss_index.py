# rag/faiss_index.py

import faiss
import pickle
import numpy as np

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INDEX_PATH = os.path.join(BASE_DIR, "faiss_index.index")
META_PATH = os.path.join(BASE_DIR, "faiss_metadata.pkl")


def save_faiss_index(embeddings, metadata):
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    vectors = np.array(embeddings).astype("float32")
    index.add(vectors)

    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump(metadata, f)

def search(query_embedding: list[float], top_k=3):
    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "rb") as f:
        metadata = pickle.load(f)

    vector = np.array([query_embedding]).astype("float32")
    distances, indices = index.search(vector, top_k)

    return [metadata[i] for i in indices[0]]    
