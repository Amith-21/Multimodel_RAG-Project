import streamlit as st
import time
from pypdf import PdfReader
from PIL import Image

# --- PAGE CONFIG ---
st.set_page_config(page_title="Brocode AI", page_icon="💻", layout="wide")

# --- AESTHETIC CSS INJECTION ---
st.markdown("""
    <style>
    /* Global Deep Space Background */
    .stApp {
        background: radial-gradient(circle at center, #0a0a0a, #000000);
        color: #f0fdfa;
    }

    /* Shimmering Animated Title: Brocode AI */
    @keyframes shimmer {
        0% { background-position: -200% center; }
        100% { background-position: 200% center; }
    }

    .main-title {
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
        font-size: 72px;
        font-weight: 800;
        letter-spacing: -3px;
        background: linear-gradient(90deg, #22d3ee, #34d399, #fbbf24, #22d3ee);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 5s linear infinite;
        margin-bottom: 0px;
        line-height: 1;
        text-shadow: 0px 0px 30px rgba(34, 211, 238, 0.2);
    }

    .subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: #5eead4;
        font-weight: 500;
        letter-spacing: 4px;
        margin-top: -10px;
        margin-bottom: 50px;
        opacity: 0.8;
        text-transform: uppercase;
    }

    /* Glassmorphism Panel Refinement */
    .glass-panel {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 20px;
        padding: 35px;
        margin-bottom: 30px;
        transition: transform 0.3s ease;
    }
    
    .glass-panel:hover {
        border: 1px solid rgba(34, 211, 238, 0.3);
    }

    /* Sidebar Refinement */
    [data-testid="stSidebar"] {
        background-color: #050505;
        border-right: 1px solid #1f2937;
    }

    /* User/AI Chat Bubbles */
    .user-bubble {
        background: rgba(34, 211, 238, 0.1);
        border-left: 4px solid #22d3ee;
        padding: 15px;
        margin: 10px 0;
        border-radius: 4px 15px 15px 4px;
    }

    .ai-bubble {
        background: rgba(52, 211, 153, 0.05);
        border-left: 4px solid #34d399;
        padding: 15px;
        margin: 10px 0;
        border-radius: 4px 15px 15px 4px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- UPDATED TITLE SECTION ---
st.markdown("<h1 class='main-title'>BROCODE AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Multimodal RAG • Advanced Intelligence</p>", unsafe_allow_html=True)

# --- LAYOUT ---
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown("### 📄 Terminal_Input.docs")
    txt_file = st.file_uploader("Upload Knowledge", type=["txt", "pdf"], label_visibility="collapsed")
    if txt_file:
        st.caption(f"✅ Successfully mounted: {txt_file.name}")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown("### 🖼️ Vision_Stream.io")
    img_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
    if img_file:
        st.image(img_file, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- CHAT / LOGIC ---
if "history" not in st.session_state:
    st.session_state.history = []

query = st.chat_input("Enter Query >>")

if query:
    # Logic placeholder
    response = "Brocode AI analyzed your request. Retrieval successful from the embedded layers."
    st.session_state.history.append({"q": query, "a": response})

for chat in reversed(st.session_state.history):
    st.markdown(f'<div class="user-bubble"><b>USER:</b> {chat["q"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="ai-bubble"><b>BROCODE:</b> {chat["a"]}</div>', unsafe_allow_html=True)
