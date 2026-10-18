"""FAISS retriever — minimal, safe across LangChain versions."""
import pickle
from functools import lru_cache

from langchain_community.vectorstores import FAISS
from src.config import FAISS_PATH, BM25_PATH, RETRIEVE_K
from src.embeddings import get_embeddings

@lru_cache(maxsize=1)
def _load_faiss():
    print("📂 Loading FAISS index...")
    return FAISS.load_local(
        str(FAISS_PATH), get_embeddings(),
        allow_dangerous_deserialization=True)

def retrieve(query: str):
    try:
        vs = _load_faiss()
        docs = vs.similarity_search(query, k=RETRIEVE_K)
        print(f"✅ Retrieved {len(docs)} docs")
        return docs
    except Exception as e:
        print(f"⚠️ Retrieval failed: {e}")
        return []