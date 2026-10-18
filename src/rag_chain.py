"""RAG chain — multi-language, structured answer with follow-ups and related diseases."""
import json
from langchain_groq import ChatGroq
from src.config import GROQ_API_KEY, LLM_MODEL
from src.retriever import retrieve
from src.router import route_question
from src.safety import check_emergency, EMERGENCY_BANNER, DISCLAIMER

_llm = ChatGroq(api_key=GROQ_API_KEY, model=LLM_MODEL,
                temperature=0.3, max_tokens=2000)

PROMPT = """You are MediScan AI, an advanced clinical assistant.
IMPORTANT: You MUST reply in the SAME language as the user's question (e.g., if they ask in Hindi or Hinglish, reply in Hindi/Hinglish. If English, reply in English).
Use ONLY the provided context. Never give specific drug doses.

Return STRICT JSON:
{{
  "condition": "string or null",
  "summary": "2-3 sentences overview in the user's language",
  "symptoms": ["..."],
  "risk_factors": ["..."],
  "red_flags": ["..."],
  "treatment_overview": ["..."],
  "when_to_see_doctor": "...",
  "follow_up_questions": ["Question 1?", "Question 2?", "Question 3?"],
  "related_diseases": ["Disease A", "Disease B", "Disease C"]
}}

Specialty: {spec}
Diseases: {dis}

Context:
{ctx}

History:
{hist}

Question: {q}

JSON:"""

def _fmt(docs):
    return "\n\n".join(
        f"[{i}] ({d.metadata.get('source','?')})\n{d.page_content[:900]}"
        for i, d in enumerate(docs, 1)) or "(no context)"

def _render(p):
    lines = []
    if p.get("condition"):
        lines.append(f"**🩺 {p['condition']}**\n")
    if p.get("summary"):
        lines.append(p["summary"])
    for k, label in [
        ("symptoms", "🔍 **Symptoms / लक्षण**"),
        ("risk_factors", "⚠️ **Risk Factors**"),
        ("red_flags", "🚨 **Red Flags**"),
        ("treatment_overview", "💊 **Treatment Overview**"),
    ]:
        if p.get(k):
            lines.append(f"\n{label}")
            lines.extend(f"- {x}" for x in p[k])
    if p.get("when_to_see_doctor"):
        lines.append(f"\n👨‍⚕️ **When to see a doctor:** {p['when_to_see_doctor']}")
    return "\n".join(lines)

def answer_question(question: str, chat_history=None) -> dict:
    chat_history = chat_history or []
    emergency = check_emergency(question)
    routing = route_question(question)

    try:
        docs = retrieve(question)
    except Exception as e:
        return {"answer": f"❌ Retrieval error: {e}", "parsed": {},
                "citations": [], "topics": [], "follow_ups": [], "related_diseases": [],
                "emergency": emergency,
                "emergency_banner": EMERGENCY_BANNER if emergency else "",
                "disclaimer": DISCLAIMER}

    ctx = _fmt(docs)
    hist = "\n".join(
        f"Q: {h.get('q','')}\nA: {str(h.get('a',''))[:200]}"
        for h in chat_history[-3:]) or "(none)"

    try:
        raw = _llm.invoke(PROMPT.format(
            spec=routing.get("specialty", "general"),
            dis=", ".join(routing.get("diseases", [])) or "(none)",
            ctx=ctx, hist=hist, q=question)).content
        parsed = json.loads(raw[raw.find("{"):raw.rfind("}")+1])
    except Exception as e:
        print(f"⚠️ Parse: {e}")
        parsed = {"summary": f"(generation failed: {e})", "condition": None,
                  "symptoms": [], "risk_factors": [], "red_flags": [],
                  "treatment_overview": [], "when_to_see_doctor": "",
                  "follow_up_questions": [], "related_diseases": []}

    citations = [{"source": d.metadata.get("source","?"), "score": 0.85,
                  "snippet": d.page_content[:200]+"..."} for d in docs]

    return {
        "answer": _render(parsed),
        "parsed": parsed,
        "citations": citations,
        "topics": [routing.get("specialty","general")] + routing.get("diseases", []),
        "follow_ups": parsed.get("follow_up_questions", []),
        "related_diseases": parsed.get("related_diseases", []), # NEW
        "emergency": emergency,
        "emergency_banner": EMERGENCY_BANNER if emergency else "",
        "disclaimer": DISCLAIMER,
    }