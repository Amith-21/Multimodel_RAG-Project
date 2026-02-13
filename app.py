import streamlit as st
import time
import pandas as pd
from pypdf import PdfReader

# --- CORE RAG IMPORTS ---
from rag.embeddings import get_jina_embeddings
from rag.vision import describe_image
from rag.chunking import chunk_text
from rag.retriever import FAISSRetriever
from rag.reranker import simple_rerank
from rag.llm import ask_llm

# --- PAGE CONFIG ---
st.set_page_config(page_title="Brocode AI | Command Center", page_icon="💀", layout="wide")

# --- HIGH-TECH CYBER CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    .stApp { background-color: #050505; color: #22d3ee; font-family: 'JetBrains Mono', monospace; }
    .main-title { font-size: 64px; font-weight: 800; background: linear-gradient(90deg, #fff, #22d3ee, #34d399); -webkit-background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0 0 10px rgba(34, 211, 238, 0.3)); }
    .css-1n76uvr { background: rgba(34, 211, 238, 0.05); border: 1px solid #22d3ee; border-radius: 10px; }
    .token-meter { font-size: 0.7rem; color: #34d399; text-align: right; margin-top: -10px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: SYSTEM METRICS ---
with st.sidebar:
    st.markdown("### `SYSTEM_TELEMETRY`")
    groq_key = st.text_input("GROQ_API_KEY", type="password")
    jina_key = st.text_input("JINA_API_KEY", type="password")
    
    st.divider()
    if "chunks" in st.session_state:
        st.markdown(f"**MEMORY_LOAD:** `{len(st.session_state.chunks)} Chunks`")
        with st.expander("🔎 DOCUMENT_X-RAY"):
            for i, c in enumerate(st.session_state.chunks[:5]):
                st.caption(f"CHUNK_{i}: {c[:50]}...")
    
    if st.button("💀 PURGE_MEMORY", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# --- HEADER ---
st.markdown("<h1 class='main-title'>BROCODE AI</h1>", unsafe_allow_html=True)

# --- DATA INGESTION ---
col1, col2 = st.columns(2)
with col1:
    txt_file = st.file_uploader("📂 MOUNT_TEXT_ASSETS", type=['pdf', 'txt'])
with col2:
    img_file = st.file_uploader("👁️ SYNC_VISION_STREAM", type=['png', 'jpg'])

# --- NEURAL ENGINE WARMUP ---
if txt_file and groq_key and jina_key:
    if "retriever" not in st.session_state:
        with st.status("`WARMING_NEURAL_LAYERS...`"):
            # Extraction
            text = "\n".join([p.extract_text() for p in PdfReader(txt_file).pages]) if txt_file.name.endswith(".pdf") else txt_file.read().decode()
            chunks = chunk_text(text)
            
            # Vision Logic
            if img_file:
                st.write("Cross-referencing vision stream...")
                v_desc = describe_image(img_file.read(), groq_key)
                chunks.append(f"VISION_INPUT_ANALYSIS: {v_desc}")
            
            # Embedding
            st.write("Mapping latent space...")
            embeddings = get_jina_embeddings(chunks, jina_key)
            st.session_state.retriever = FAISSRetriever(embeddings, [{"id": i} for i in range(len(chunks))])
            st.session_state.chunks = chunks
            st.session_state.init = True

    # --- INTELLIGENCE INTERFACE ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Interaction Logic
    if prompt := st.chat_input("Execute Intelligence Request..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # 1. CHAIN OF THOUGHT (The Ghosting Feature)
            with st.status("`GHOST_REASONING_IN_PROGRESS...`"):
                st.write("Searching vector database...")
                q_emb = get_jina_embeddings([prompt], jina_key)
                ids = st.session_state.retriever.search(q_emb, top_k=3)
                relevant = [st.session_state.chunks[i] for i in ids]
                
                st.write("Analyzing contextual relevance...")
                context = "\n\n".join(relevant)
                
                st.write("Synthesizing final intelligence...")
                final_answer = ask_llm(context, prompt, groq_key, "llama-3.1-8b-instant")
            
            # 2. OUTPUT DISPLAY
            st.markdown(final_answer)
            st.session_state.messages.append({"role": "assistant", "content": final_answer})
            
            # 3. TOKEN METER
            st.markdown(f"<div class='token-meter'>EST_TOKENS: {len(final_answer)//4 + len(context)//4} // STATUS: OPTIMAL</div>", unsafe_allow_html=True)

else:
    st.warning("⚠️ SYSTEM_OFFLINE: Mount knowledge assets and provide API credentials.")
