# rag/load_restaurants.py

import os
import requests
from embedder import get_embedding
from faiss_index import save_faiss_index

DJANGO_URL = os.getenv("DJANGO_BASE_URL", "http://localhost:8000")

def fetch_restaurants():
    url = f"{DJANGO_URL}/restaurant/list"
    print(f"[DEBUG] 요청 URL: {url}")
    res = requests.get(url)
    print("📦 응답 코드:", res.status_code)
    print("📨 응답 내용:", res.text[:300])  # 미리보기

    res.raise_for_status()
    return res.json()

def build_and_save_faiss():
    data = fetch_restaurants()

    texts = []
    metadata = []

    for r in data:
        keyword = r.get("keyword", "")
        if not keyword:
            continue
        texts.append(keyword)
        metadata.append({
            "name": r["name"],
            "address": r["address"],
            "rating": r.get("rating", None)
        })

    print(f"총 restaurant 개수: {len(data)}")
    print(f"임베딩 대상 keyword 개수: {len(texts)}")


    embeddings = [get_embedding(text) for text in texts]
    save_faiss_index(embeddings, metadata)

if __name__ == "__main__":
    build_and_save_faiss()
