"""MedlinePlus loader."""
import json
from pathlib import Path
from langchain_core.documents import Document
from src.config import MEDLINEPLUS_DIR

def load_medlineplus() -> list:
    f = Path(MEDLINEPLUS_DIR) / "topics.json"
    if not f.exists():
        print("⚠️ No MedlinePlus data. Run: python scripts/download_medlineplus.py")
        return []
    try:
        topics = json.loads(f.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"❌ Failed: {e}")
        return []

    docs = []
    for t in topics:
        title = t.get("title", "").strip()
        summary = t.get("summary", "").strip()
        if not title or not summary:
            continue
        docs.append(Document(
            page_content=f"# {title}\n\n{summary}",
            metadata={"source": f"MedlinePlus: {title}", "source_type": "medlineplus",
                      "url": t.get("url", "")},
        ))
    print(f"✅ Loaded {len(docs)} MedlinePlus topics")
    return docs