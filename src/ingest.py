"""Ingest — load all sources, chunk, build FAISS only (saves RAM)."""
import sys
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from src.config import (FAISS_PATH, KNOWLEDGE_DIR, MEDLINEPLUS_DIR,
                        CHUNK_SIZE, CHUNK_OVERLAP)
from src.embeddings import get_embeddings
from src.loaders.pdf_loader import load_pdfs
from src.loaders.medlineplus_loader import load_medlineplus


def _load_txt() -> list:
    docs = []
    for txt in Path(KNOWLEDGE_DIR).rglob("*.txt"):
        try:
            text = txt.read_text(encoding="utf-8", errors="ignore").strip()
            if text:
                docs.append(Document(
                    page_content=text,
                    metadata={"source": f"Knowledge: {txt.name}", "source_type": "txt"},
                ))
        except Exception as e:
            print(f"⚠️ Failed {txt.name}: {e}")
    print(f"✅ Loaded {len(docs)} txt docs")
    return docs


def _all_documents() -> list:
    print("📚 Loading PDFs...")
    all_docs = load_pdfs()
    
    print("📚 Loading MedlinePlus (limited to 300 to save RAM)...")
    medlineplus_docs = load_medlineplus()[:300]
    all_docs.extend(medlineplus_docs)
    
    print("📚 Loading TXT files...")
    all_docs.extend(_load_txt())
    
    return all_docs


def build_vectorstore():
    print("📚 Loading documents...")
    docs = _all_documents()
    if not docs:
        raise RuntimeError("No documents found.")

    print(f"🔪 Chunking {len(docs)} docs...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500, chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " ", ""])
    chunks = splitter.split_documents(docs)
    for i, c in enumerate(chunks):
        c.metadata["chunk_id"] = i
    print(f"   → {len(chunks)} chunks")

    print(f"💾 Building FAISS (batch mode, {len(chunks)} chunks)...")
    FAISS_PATH.mkdir(parents=True, exist_ok=True)

    BATCH_SIZE = 200
    embeddings = get_embeddings()
    vs = None

    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i:i + BATCH_SIZE]
        print(f"   Batch {i // BATCH_SIZE + 1}: {len(batch)} chunks")
        if vs is None:
            vs = FAISS.from_documents(batch, embeddings)
        else:
            vs.add_documents(batch)

    vs.save_local(str(FAISS_PATH))
    print(f"✅ Done · {len(docs)} docs → {len(chunks)} chunks")
    return len(docs), len(chunks)


if __name__ == "__main__":
    build_vectorstore()