"""Symptom Checker — Differential Diagnosis."""
import json
from langchain_groq import ChatGroq
from src.config import GROQ_API_KEY, LLM_MODEL
from src.retriever import retrieve

_llm = ChatGroq(api_key=GROQ_API_KEY, model=LLM_MODEL, temperature=0.2, max_tokens=1500)

PROMPT = """You are a medical AI. A patient has selected the following symptoms:
{symptoms}

Based on these symptoms, suggest the top 3 most likely conditions.
Return STRICT JSON:
{{
  "conditions": [
    {{
      "name": "Disease Name",
      "confidence": "High/Medium/Low",
      "reasoning": "Why these symptoms match this disease (1-2 sentences).",
      "red_flags": "Any emergency signs to watch out for."
    }}
  ],
  "disclaimer": "This is not a diagnosis. Please consult a doctor."
}}
JSON:"""

def check_symptoms(symptom_list: list) -> dict:
    """Takes a list of symptoms and returns probable conditions."""
    if not symptom_list:
        return {"error": "No symptoms provided."}
        
    symptoms_text = ", ".join(symptom_list)
    
    # Optional: RAG retrieval based on symptoms to give context to LLM
    try:
        docs = retrieve(symptoms_text)
        context = "\n".join([d.page_content[:500] for d in docs[:3]])
    except Exception:
        context = "(No extra context available)"
        
    try:
        raw = _llm.invoke(PROMPT.format(symptoms=symptoms_text)).content
        parsed = json.loads(raw[raw.find("{"):raw.rfind("}")+1])
        return parsed
    except Exception as e:
        return {"error": f"Failed to analyze: {e}"}