"""Query router — detect specialty/disease/intent."""
import json
from langchain_groq import ChatGroq
from src.config import GROQ_API_KEY, LLM_MODEL

SPECIALTIES = [
    "cardiology", "pulmonology", "endocrinology", "neurology",
    "gastroenterology", "infectious_disease", "dermatology",
    "psychiatry", "oncology", "rheumatology", "nephrology",
    "hematology", "ophthalmology", "orthopedics", "general",
]

PROMPT = """You are a medical query router. Return ONLY JSON:
{{"specialty": "<one of: {spec}>",
 "diseases": ["..."],
 "intent": "<symptom_info|treatment|prevention|definition|emergency|other>"}}

Question: {q}
JSON:"""

def route_question(question: str) -> dict:
    try:
        llm = ChatGroq(api_key=GROQ_API_KEY, model=LLM_MODEL,
                       temperature=0, max_tokens=200)
        raw = llm.invoke(PROMPT.format(spec="|".join(SPECIALTIES), q=question)).content
        parsed = json.loads(raw[raw.find("{"):raw.rfind("}")+1])
        if parsed.get("specialty") not in SPECIALTIES:
            parsed["specialty"] = "general"
        parsed.setdefault("diseases", [])
        parsed.setdefault("intent", "other")
        return parsed
    except Exception as e:
        print(f"⚠️ Router: {e}")
        return {"specialty": "general", "diseases": [], "intent": "other"}