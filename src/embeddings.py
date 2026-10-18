"""Embeddings — BGE-large."""
from langchain_huggingface import HuggingFaceEmbeddings
from src.config import EMBEDDING_MODEL

_cache = None

def get_embeddings():
    global _cache
    if _cache is None:
        _cache = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
    return _cache