import os
import uuid
import traceback
import streamlit as st
from datetime import datetime

# 1. Page Config
st.set_page_config(
    page_title="MediScan AI — Advanced Clinical Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ================= ADVANCED GLASSMORPHISM CSS =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
    --primary: #00f2fe;
    --secondary: #4facfe;
    --accent: #43e97b;
    --bg-dark: #070b14;
    --glass-bg: rgba(255, 255, 255, 0.03);
    --glass-border: rgba(255, 255, 255, 0.08);
    --glass-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    --text-main: #e2e8f0;
    --text-muted: #94a3b8;
}

* { font-family: 'Outfit', sans-serif; }

.stApp {
    background-color: var(--bg-dark);
    background-image: 
        radial-gradient(at 0% 0%, rgba(79, 172, 254, 0.15) 0px, transparent 50%),
        radial-gradient(at 100% 0%, rgba(67, 233, 123, 0.15) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(0, 242, 254, 0.1) 0px, transparent 50%),
        radial-gradient(at 0% 100%, rgba(79, 172, 254, 0.1) 0px, transparent 50%);
    background-attachment: fixed;
    color: var(--text-main);
}

section[data-testid="stSidebar"] {
    background: rgba(7, 11, 20, 0.6) !important;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-right: 1px solid var(--glass-border);
    box-shadow: var(--glass-shadow);
}

h1 {
    font-weight: 800 !important;
    background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -1px;
}
h2, h3 { font-weight: 600 !important; color: var(--primary) !important; }

.glass-card {
    background: var(--glass-bg);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    padding: 20px;
    box-shadow: var(--glass-shadow);
    margin-bottom: 20px;
    transition: transform 0.3s ease, border-color 0.3s ease;
}
.glass-card:hover {
    transform: translateY(-2px);
    border-color: rgba(0, 242, 254, 0.3);
}

.badge {
    display: inline-block;
    background: rgba(0, 242, 254, 0.1);
    border: 1px solid rgba(0, 242, 254, 0.2);
    color: var(--primary);
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    margin-right: 8px;
    margin-bottom: 8px;
    letter-spacing: 0.5px;
}

.disclaimer {
    background: rgba(251, 191, 36, 0.1);
    border-left: 4px solid #fbbf24;
    padding: 15px;
    border-radius: 8px;
    color: #fde68a;
    font-size: 0.9rem;
    margin-bottom: 20px;
}

[data-testid="stChatMessage"] {
    background: var(--glass-bg) !important;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid var(--glass-border) !important;
    border-radius: 16px !important;
    box-shadow: var(--glass-shadow);
    padding: 15px !important;
}

[data-testid="stChatInput"] {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 16px !important;
    box-shadow: var(--glass-shadow) !important;
}

.stButton > button {
    background: linear-gradient(135deg, rgba(79, 172, 254, 0.8) 0%, rgba(0, 242, 254, 0.8) 100%) !important;
    backdrop-filter: blur(10px);
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(0, 242, 254, 0.2) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(0, 242, 254, 0.4) !important;
}

.stTextInput input, .stFileUploader, .stSelectbox, .stMultiSelect {
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid var(--glass-border) !important;
    color: white !important;
    border-radius: 12px !important;
}

.citation-card {
    background: rgba(0, 0, 0, 0.2);
    border-left: 3px solid var(--primary);
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("""
<div style="text-align: center; padding: 20px 0;">
    <h1 style="font-size: 3.5rem; margin-bottom: 0;">🩺 MediScan AI</h1>
    <p style="color: #94a3b8; font-size: 1.1rem; font-weight: 300;">Advanced Clinical Knowledge Assistant</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; margin-bottom: 30px;">
    <span class="badge">⚡ Hybrid RAG</span>
    <span class="badge">👁️ Vision Analysis</span>
    <span class="badge">🎤 Voice Input</span>
    <span class="badge">🌍 Multi-Language</span>
    <span class="badge">📄 PDF Export</span>
</div>
""", unsafe_allow_html=True)

# ================= SAFE IMPORTS =================
try:
    from src.rag_chain import answer_question
    from src.vision import analyze_image, render_vision
    from src.voice import transcribe_audio
    from src.symptom_checker import check_symptoms
    from src.safety import DISCLAIMER, VISION_DISCLAIMER, check_emergency
    from src.memory import save_turn, clear_history
    from src.loaders.image_loader import save_uploaded_image, is_valid_image
    from src.config import IMAGE_DIR
    from src.pdf_export import generate_pdf
    app_ready = True
except Exception as e:
    st.error("🚨 **System Initialization Error**")
    st.code(traceback.format_exc(), language="python")
    app_ready = False

if app_ready:
    st.markdown(f'<div class="disclaimer">⚕️ {DISCLAIMER}</div>', unsafe_allow_html=True)

    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if "chat" not in st.session_state:
        st.session_state.chat = []
    if "pending_q" not in st.session_state:
        st.session_state.pending_q = None

    # ================= SIDEBAR =================
    with st.sidebar:
        st.markdown("### ⚙️ Control Panel")
        
        # Language Selector
        st.markdown("<p style='color:#94a3b8; font-size:0.9rem; margin-bottom:5px;'>🌐 Response Language</p>", unsafe_allow_html=True)
        lang = st.selectbox("Select Language", ["Auto-Detect", "English", "Hindi", "Urdu"], label_visibility="collapsed")
        
        st.markdown("---")
        
        # Export Buttons
        st.markdown("<p style='color:#94a3b8; font-size:0.9rem; margin-bottom:5px;'>📥 Export Report</p>", unsafe_allow_html=True)
        if st.session_state.chat:
            chat_text = "\n\n".join([f"You: {t['q']}\nAI: {t['a']}" for t in st.session_state.chat])
            st.download_button("Download TXT", data=chat_text, file_name=f"mediscan_{datetime.now().strftime('%Y%m%d')}.txt", mime="text/plain", use_container_width=True)
            
            if st.button("Generate PDF Report", use_container_width=True):
                with st.spinner("Generating PDF..."):
                    pdf_path = f"report_{st.session_state.session_id[:6]}.pdf"
                    try:
                        generate_pdf(st.session_state.chat, pdf_path)
                        with open(pdf_path, "rb") as f:
                            st.download_button("📄 Click to Download PDF", data=f, file_name=f"MediScan_Report.pdf", mime="application/pdf", use_container_width=True)
                        os.remove(pdf_path)
                    except Exception as e:
                        st.error(f"PDF Error: {e}")

        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.chat = []
            clear_history(st.session_state.session_id)
            st.rerun()
            
        st.markdown("---")
        
        # ================= SYMPTOM CHECKER =================
        st.markdown("### 🩺 Symptom Checker")
        st.markdown("<p style='color:#94a3b8; font-size:0.85rem;'>Select your symptoms to find probable conditions.</p>", unsafe_allow_html=True)
        
        all_symptoms = [
            "Fever", "Cough", "Headache", "Fatigue", "Nausea", 
            "Chest Pain", "Shortness of Breath", "Sore Throat", 
            "Runny Nose", "Body Ache", "Diarrhea", "Vomiting"
        ]
        
        selected_symptoms = st.multiselect("Select Symptoms", all_symptoms, label_visibility="collapsed")
        
        if st.button("🔍 Check Symptoms", use_container_width=True):
            if not selected_symptoms:
                st.warning("Please select at least one symptom.")
            else:
                with st.spinner("Analyzing symptoms..."):
                    result = check_symptoms(selected_symptoms)
                    st.session_state.symptom_result = result
                    
        # Display Symptom Results inside Sidebar
        if "symptom_result" in st.session_state and st.session_state.symptom_result:
            res = st.session_state.symptom_result
            if "error" in res:
                st.error(res["error"])
            else:
                for cond in res.get("conditions", []):
                    st.markdown(f"""
                    <div class="glass-card" style="padding:12px; margin-bottom:10px;">
                        <strong style="color:var(--primary);">{cond.get('name','')}</strong> 
                        <span style="float:right; font-size:0.8rem; color:#43e97b;">{cond.get('confidence','')}</span><br>
                        <span style="font-size:0.85rem; color:#e2e8f0;">{cond.get('reasoning','')}</span><br>
                        <span style="font-size:0.8rem; color:#fbbf24;">🚨 {cond.get('red_flags','')}</span>
                    </div>
                    """, unsafe_allow_html=True)
                st.caption(res.get("disclaimer", ""))

        st.markdown("---")
        st.markdown("### 🔬 Vision Analysis")
        st.markdown("<p style='color:#94a3b8; font-size:0.85rem;'>Upload a medical image (skin, X-ray, rash) for AI analysis.</p>", unsafe_allow_html=True)
        
        img_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png", "webp"], label_visibility="collapsed")
        img_note = st.text_input("Context (optional)", placeholder="e.g. red rash on arm for 3 days")
        
        if img_file and st.button("🔍 Analyze Image", use_container_width=True):
            with st.spinner("Analyzing image..."):
                try:
                    path = save_uploaded_image(img_file, IMAGE_DIR)
                    if not is_valid_image(path):
                        st.error("Invalid image file.")
                    else:
                        result = analyze_image(path, img_note)
                        st.session_state.vision_result = result
                        st.session_state.vision_image = path
                except Exception as e:
                    st.error(f"Vision Error: {e}")

        st.markdown("---")
        st.caption(f"Session ID: `{st.session_state.session_id[:8]}`")

    # ================= MAIN LAYOUT =================
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 💬 Clinical Chat")
        
        if st.session_state.pending_q:
            q_to_run = st.session_state.pending_q
            st.session_state.pending_q = None
            st.session_state.chat.append({"q": q_to_run, "a": "Analyzing...", "citations": [], "emergency": False, "follow_ups": [], "related_diseases": []})
            st.rerun()

        for i, turn in enumerate(st.session_state.chat):
            with st.chat_message("user", avatar="🧑‍💻"):
                st.write(turn["q"])
            with st.chat_message("assistant", avatar="🩺"):
                if turn.get("emergency"):
                    st.error(turn.get("emergency_banner", ""))
                
                st.markdown(turn["a"])
                
                if turn.get("citations"):
                    with st.expander("📎 View Citations"):
                        for c in turn["citations"]:
                            st.markdown(f"""
                            <div class="citation-card">
                                <strong style="color:var(--primary);">📄 {c['source']}</strong><br>
                                <span style="color:#94a3b8; font-size:0.9rem;">{c['snippet']}</span>
                            </div>
                            """, unsafe_allow_html=True)
                
                if i == len(st.session_state.chat) - 1:
                    if turn.get("follow_ups"):
                        st.markdown("<p style='color:#94a3b8; font-size:0.85rem; margin-top:15px; margin-bottom:5px;'>💡 Ask Next:</p>", unsafe_allow_html=True)
                        cols = st.columns(len(turn["follow_ups"]))
                        for idx, fq in enumerate(turn["follow_ups"]):
                            with cols[idx]:
                                if st.button(fq, key=f"fq_{i}_{idx}", use_container_width=True):
                                    st.session_state.pending_q = fq
                                    st.rerun()
                    
                    if turn.get("related_diseases"):
                        st.markdown("<p style='color:#94a3b8; font-size:0.85rem; margin-top:15px; margin-bottom:5px;'>🔗 Related Diseases:</p>", unsafe_allow_html=True)
                        cols = st.columns(len(turn["related_diseases"]))
                        for idx, rd in enumerate(turn["related_diseases"]):
                            with cols[idx]:
                                if st.button(f"About {rd}", key=f"rd_{i}_{idx}", use_container_width=True):
                                    st.session_state.pending_q = f"Tell me about {rd}"
                                    st.rerun()

        # Voice Input
        st.markdown("<p style='color:#94a3b8; font-size:0.9rem; margin-top:20px; margin-bottom:5px;'>🎤 Voice Input</p>", unsafe_allow_html=True)
        audio_val = st.audio_input("Record a voice query", label_visibility="collapsed")
        if audio_val:
            with st.spinner("Transcribing voice..."):
                temp_path = "temp_audio.wav"
                with open(temp_path, "wb") as f:
                    f.write(audio_val.getbuffer())
                text = transcribe_audio(temp_path)
                os.remove(temp_path)
                
                if text and not text.startswith("⚠️"):
                    st.session_state.pending_q = text
                    st.rerun()
                else:
                    st.error(text)

        # Chat Input
        user_input = st.chat_input("Ask about symptoms, diseases, or treatments...")
        if user_input:
            if lang != "Auto-Detect":
                question = f"[Reply strictly in {lang}] {user_input}"
            else:
                question = user_input

            with st.chat_message("user", avatar="🧑‍💻"):
                st.write(user_input)
            with st.chat_message("assistant", avatar="🩺"):
                if check_emergency(user_input):
                    st.error("🚨 **EMERGENCY DETECTED** — Call 108 / 112 / 911 immediately!")
                
                with st.spinner("Consulting medical database..."):
                    try:
                        out = answer_question(question, chat_history=[{"q": t["q"], "a": t["a"]} for t in st.session_state.chat])
                        st.markdown(out["answer"])
                        if out.get("citations"):
                            with st.expander("📎 View Citations", expanded=True):
                                for c in out["citations"]:
                                    st.markdown(f"""
                                    <div class="citation-card">
                                        <strong style="color:var(--primary);">📄 {c['source']}</strong><br>
                                        <span style="color:#94a3b8; font-size:0.9rem;">{c['snippet']}</span>
                                    </div>
                                    """, unsafe_allow_html=True)
                        st.caption(out.get("disclaimer", ""))
                        
                        save_turn(st.session_state.session_id, "user", user_input)
                        save_turn(st.session_state.session_id, "assistant", out["answer"])
                        st.session_state.chat.append({
                            "q": user_input, "a": out["answer"], 
                            "citations": out.get("citations", []), 
                            "follow_ups": out.get("follow_ups", []),
                            "related_diseases": out.get("related_diseases", []),
                            "emergency": out.get("emergency", False),
                            "emergency_banner": out.get("emergency_banner", "")
                        })
                    except Exception as e:
                        st.error(f"Chat Error: {e}")
            st.rerun()

    with col2:
        if "vision_result" in st.session_state and st.session_state.vision_result:
            st.markdown("### 👁️ Vision Results")
            st.image(st.session_state.vision_image, use_container_width=True)
            st.markdown(f"""
            <div class="glass-card">
                {render_vision(st.session_state.vision_result)}
            </div>
            """, unsafe_allow_html=True)
            if st.button("Clear Results"):
                del st.session_state.vision_result
                del st.session_state.vision_image
                st.rerun()
        else:
            st.markdown("""
            <div class="glass-card" style="text-align: center; padding: 40px 20px;">
                <h2 style="font-size: 3rem; margin-bottom: 10px;">🩻</h2>
                <h3 style="color: #94a3b8 !important;">No Image Uploaded</h3>
                <p style="color: #64748b; font-size: 0.9rem;">Use the sidebar to upload a medical image for AI analysis.</p>
            </div>
            """, unsafe_allow_html=True)