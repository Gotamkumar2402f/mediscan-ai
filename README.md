<div align="center">

# 🩺 MediScan AI
### Next-Generation Clinical Intelligence & Diagnosis Assistant

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com)
[![Groq](https://img.shields.io/badge/Groq-f55036?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co)
[![FAISS](https://img.shields.io/badge/FAISS-0467DF?style=for-the-badge&logo=meta&logoColor=white)](https://github.com/facebookresearch/faiss)

*An advanced, multi-modal AI clinical assistant powered by Llama 3.3, Vision AI, and Hybrid RAG.*

</div>

---

## 📖 Overview

**MediScan AI** is a state-of-the-art, full-stack AI healthcare assistant. It moves beyond standard chatbots by integrating **Text, Voice, and Image** inputs. Built with a custom Glassmorphism UI, it provides accurate, context-aware medical information backed by reliable sources, while strictly adhering to medical safety protocols.

### 🎯 The Problem It Solves
Navigating medical information is hard and often leads to misinformation. MediScan AI solves this by combining a **Hybrid Retrieval-Augmented Generation (RAG)** pipeline (FAISS + BM25) with a **Medical Dataset of 1,300+ diseases**, ensuring responses are accurate, cited, and grounded in real data.

---

## ✨ Key Features

| Feature | Description |
| :--- | :--- |
| 🧠 **Hybrid RAG Search** | Combines Semantic (FAISS) and Keyword (BM25) search for pinpoint accuracy. |
| 👁️ **Vision Diagnosis** | Upload images of rashes, wounds, or X-rays for AI-powered visual analysis. |
| 🎤 **Voice-to-Text** | Speak your symptoms using Groq's ultra-fast Whisper model. |
| 🌍 **Multi-Language** | Auto-detects and replies in English, Hindi, or Urdu. |
| 🩺 **Symptom Checker** | Select symptoms from a list for a differential diagnosis. |
| 🚨 **Emergency Triage** | Instantly detects critical keywords (e.g., "chest pain") and alerts the user. |
| 📄 **PDF Export** | Generate a professional clinical report of your chat session. |
| 💾 **Memory Persistence** | SQLite backend retains chat history across sessions. |

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit, Custom CSS (Glassmorphism)
* **LLM & Routing:** Llama 3.3 (70B) via Groq API, LangChain
* **Vision AI:** Qwen 3.8-27B (Multimodal) via Groq
* **Voice AI:** Whisper Large v3 via Groq
* **Embeddings:** Hugging Face (`BAAI/bge-small-en-v1.5`)
* **Vector DB:** FAISS (Facebook AI Similarity Search)
* **Database:** SQLite3
* **PDF Engine:** `fpdf2`

---

## 🚀 Quick Start

1. Clone the repo: `git clone https://github.com/YOUR-USERNAME/mediscan-ai.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Add `.env` file with `GROQ_API_KEY` and `HF_TOKEN`.
4. Run the app: `streamlit run app.py`

---

## ⚠️ Medical Disclaimer

**MediScan AI is for educational and informational purposes only.** It is not a substitute for professional medical advice. Always seek the advice of a qualified health provider. In case of an emergency, call your local emergency services immediately.

---
<div align="center">
Built with ❤️ by Gotam Kumar
</div>
