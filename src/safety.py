"""Safety — emergency detection + disclaimers."""

EMERGENCY_KEYWORDS = [
    "chest pain", "heart attack", "can't breathe", "cannot breathe",
    "difficulty breathing", "suicide", "suicidal", "kill myself",
    "severe bleeding", "unconscious", "stroke", "seizure",
    "poisoning", "overdose", "anaphylaxis",
    "saans nahi", "seene me dard", "khoon", "behosh", "dil ka daura",
]

EMERGENCY_BANNER = (
    "🚨 **EMERGENCY DETECTED** 🚨\n\n"
    "If this is a medical emergency, call your local emergency number **IMMEDIATELY**.\n\n"
    "🇮🇳 India: **108 / 112** | 🇺🇸 US: **911** | 🇬🇧 UK: **999**\n\n"
    "_This tool cannot replace emergency services._"
)

DISCLAIMER = (
    "⚕️ Educational information only — not a diagnosis or prescription. "
    "Always consult a licensed healthcare professional."
)

VISION_DISCLAIMER = (
    "🖼️ Image analysis is educational only. Visual AI cannot replace a specialist's examination."
)

def check_emergency(text: str) -> bool:
    t = (text or "").lower()
    return any(k in t for k in EMERGENCY_KEYWORDS)