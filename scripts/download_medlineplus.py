"""Download MedlinePlus topics (1000+ diseases, free)."""
import json, time, xml.etree.ElementTree as ET
from pathlib import Path
import requests

OUT = Path("data/medlineplus")
OUT.mkdir(parents=True, exist_ok=True)
URL = "https://wsearch.nlm.nih.gov/ws/query"

TERMS = ["disease", "condition", "syndrome", "disorder",
         "infection", "cancer", "diabetes", "heart", "skin",
         "mental health", "eye", "bone", "lung", "kidney"]

def fetch(term, retmax=500):
    r = requests.get(URL, params={"db": "healthTopics", "term": term, "retmax": retmax}, timeout=30)
    r.raise_for_status()
    return ET.fromstring(r.content)

def parse(root):
    docs = []
    for doc in root.iter("document"):
        title = doc.find(".//content[@name='title']")
        summary = doc.find(".//content[@name='FullSummary']")
        url = doc.find(".//content[@name='url']")
        if title is None or summary is None:
            continue
        docs.append({
            "title": title.text or "",
            "summary": summary.text or "",
            "url": url.text if url is not None else "",
        })
    return docs

def main():
    all_docs, seen = [], set()
    for term in TERMS:
        print(f"📥 Fetching: {term}")
        try:
            docs = parse(fetch(term))
            new = 0
            for d in docs:
                key = d["title"].lower().strip()
                if key and key not in seen:
                    seen.add(key)
                    all_docs.append(d)
                    new += 1
            print(f"   +{new} new (total: {len(all_docs)})")
        except Exception as e:
            print(f"   ❌ failed: {e}")
        time.sleep(1)
    out_file = OUT / "topics.json"
    out_file.write_text(json.dumps(all_docs, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n✅ Saved {len(all_docs)} unique topics → {out_file}")

if __name__ == "__main__":
    main()