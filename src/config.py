"""MediScan AI Configuration"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# LLM
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
VISION_MODEL = os.getenv("VISION_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct")

# Embeddings
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-large-en-v1.5")
RERANKER_MODEL = os.getenv("RERANKER_MODEL", "BAAI/bge-reranker-base")

# Paths
ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = ROOT / "data" / "knowledge"
MEDLINEPLUS_DIR = ROOT / "data" / "medlineplus"
IMAGE_DIR = ROOT / "data" / "images"
VECTORSTORE_DIR = ROOT / "data" / "vectorstore"
FAISS_PATH = VECTORSTORE_DIR / "faiss_index"
BM25_PATH = VECTORSTORE_DIR / "bm25.pkl"
MEMORY_DB = ROOT / "data" / "chat_memory.db"

for p in [KNOWLEDGE_DIR, MEDLINEPLUS_DIR, IMAGE_DIR, VECTORSTORE_DIR]:
    p.mkdir(parents=True, exist_ok=True)

# Retrieval
RETRIEVE_K = int(os.getenv("RETRIEVE_K", "20"))
RERANK_TOP_N = int(os.getenv("RERANK_TOP_N", "4"))
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "120"))