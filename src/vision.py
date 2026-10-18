"""Vision — image analysis via Groq."""
import base64
import json
from pathlib import Path
from groq import Groq
from src.config import GROQ_API_KEY, VISION_MODEL
from src.safety import VISION_DISCLAIMER

_client = Groq(api_key=GROQ_API_KEY)

PROMPT = """Educational vision analysis for MediScan AI. Return STRICT JSON:
{{
  "image_type": "<skin|eye|xray|wound|rash|oral|other>",
  "description": "neutral factual description",
  "possible_conditions": [
    {{"name": "...", "confidence": "low|medium|high", "reasoning": "..."}}
  ],
  "red_flags": ["..."],
  "recommended_specialist": "...",
  "urgency": "routine|soon|urgent|emergency",
  "next_steps": ["..."],
  "cannot_diagnose_note": "This is not a medical diagnosis."
}}

Never claim certainty. Flag emergencies."""

def _encode(image_path):
    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    ext = Path(image_path).suffix.lower().lstrip(".")
    mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg",
            "png": "image/png", "webp": "image/webp"}.get(ext, "image/jpeg")
    return b64, mime

def analyze_image(image_path: str, user_note: str = "") -> dict:
    try:
        b64, mime = _encode(image_path)
    except Exception as e:
        return _err(f"Read failed: {e}")

    content = PROMPT
    if user_note:
        content += f"\n\nUser note: {user_note}"

    try:
        resp = _client.chat.completions.create(
            model=VISION_MODEL,
            messages=[{"role": "user", "content": [
                {"type": "text", "text": content},
                {"type": "image_url",
                 "image_url": {"url": f"data:{mime};base64,{b64}"}},
            ]}],
            temperature=0.1, 
            max_tokens=800,  # <-- Ye change kiya (1500 se 800)
            response_format={"type": "json_object"},
        )
        parsed = json.loads(resp.choices[0].message.content)
        parsed["disclaimer"] = VISION_DISCLAIMER
        return parsed
    except Exception as e:
        return _err(f"Vision failed: {e}")

def _err(msg):
    return {"image_type": "unknown", "description": msg,
            "possible_conditions": [], "red_flags": [],
            "recommended_specialist": "general physician",
            "urgency": "routine",
            "next_steps": ["Consult a doctor."],
            "cannot_diagnose_note": "Analysis unavailable.",
            "disclaimer": VISION_DISCLAIMER}

def render_vision(v):
    lines = [f"**🖼️ {v.get('image_type','unknown').title()}**\n"]
    if v.get("description"):
        lines.append(f"_{v['description']}_\n")
    if v.get("possible_conditions"):
        lines.append("**🔍 Possible conditions:**")
        for c in v["possible_conditions"]:
            lines.append(f"- **{c.get('name','?')}** — `{c.get('confidence','?')}`")
            if c.get("reasoning"):
                lines.append(f"  _{c['reasoning']}_")
    if v.get("red_flags"):
        lines.append("\n**🚨 Red flags:**")
        lines.extend(f"- {r}" for r in v["red_flags"])
    if v.get("recommended_specialist"):
        lines.append(f"\n👨‍⚕️ **Specialist:** {v['recommended_specialist']}")
    if v.get("urgency"):
        lines.append(f"⏱️ **Urgency:** `{v['urgency']}`")
    if v.get("next_steps"):
        lines.append("\n**📋 Next steps:**")
        lines.extend(f"- {s}" for s in v["next_steps"])
    if v.get("cannot_diagnose_note"):
        lines.append(f"\n⚠️ _{v['cannot_diagnose_note']}_")
    return "\n".join(lines)