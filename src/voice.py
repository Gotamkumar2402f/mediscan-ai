"""Voice-to-text using Groq Whisper."""
import os
from groq import Groq
from src.config import GROQ_API_KEY

_client = Groq(api_key=GROQ_API_KEY)

def transcribe_audio(audio_path: str) -> str:
    """Convert audio file to text using Whisper."""
    try:
        with open(audio_path, "rb") as f:
            transcription = _client.audio.transcriptions.create(
                file=(audio_path, f.read()),
                model="whisper-large-v3",
                response_format="text",
            )
        return transcription.strip()
    except Exception as e:
        return f"⚠️ Audio Error: {e}"