"""PDF loader."""
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from src.config import KNOWLEDGE_DIR

def load_pdfs() -> list:
    docs = []
    pdf_files = list(Path(KNOWLEDGE_DIR).rglob("*.pdf"))
    if not pdf_files:
        print(f"⚠️ No PDFs in {KNOWLEDGE_DIR}")
        return docs
    for pdf in pdf_files:
        try:
            pages = PyPDFLoader(str(pdf)).load()
            for page in pages:
                page.metadata["source"] = f"PDF: {pdf.name}"
                page.metadata["source_type"] = "pdf"
            docs.extend(pages)
            print(f"✅ Loaded {len(pages)} pages from {pdf.name}")
        except Exception as e:
            print(f"❌ Failed {pdf.name}: {e}")
    return docs