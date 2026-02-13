import streamlit as st
import time
import pandas as pd
import numpy as np
import plotly.express as px
from pypdf import PdfReader

# --- IMPORT YOUR RAG CORE ---
# Ensure these files exist in your 'rag/' folder
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
    .stApp { background-color: #050505; color: #f0fdfa; font-family: 'JetBrains Mono', monospace; }
    .main-title {
        font-size: 72px; font-weight: 800;
        background: linear-gradient(to right, #ffffff, #22d3ee, #34d399);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 15px rgba(34, 211, 238, 0.4));
    }
    .status-box { background: rgba(34, 211, 238, 0.05); border: 1px solid #22d3ee; padding: 10px; border-radius: 5px; color: #22d3ee; font-size: 0.8rem; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: CONFIG & API KEYS ---
with st.sidebar:
    st.markdown("### `SYSTEM_AUTH`")
    groq_key = st.text_input("GROQ_API_KEY", type="password")
    jina_key = st.text_input("JINA_API_KEY", type="password")
    
    st.divider()
    st.markdown("### `SYSTEM_TELEMETRY`")
    st.progress(65, text="Neural Load")
    
    if st.button("💀 PURGE_SESSION", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# --- HEADER ---
st.markdown("<h1 class='main-title'>BROCODE AI</h1>", unsafe_allow_html=True)
st.markdown("`DIR: /root/multimodal_rag/prod_v3`")

# --- DATA INGESTION ---
c1, c2 = st.columns(2)
with c1:
    st.markdown("### `DOC_MOUNT`")
    txt_file = st.file_uploader("Internal Docs", type=['pdf', 'txt'], label_visibility="collapsed")
with c2:
    st.markdown("### `VIS_MOUNT`")
    img_file = st.file_uploader("Vision Assets", type=['png', 'jpg'], label_visibility="collapsed")

# --- RAG INITIALIZATION ---
if txt_file and groq_key and jina_key:
    if "retriever" not in st.session_state:
        with st.status("`INITIALIZING_NEURAL_LAYERS...`"):
            # 1. Text Extraction
            if txt_file.name.endswith(".pdf"):
                reader = PdfReader(txt_file)
                raw_text = "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
            else:
                raw_text = txt_file.read().decode("utf-8")

            # 2. Chunking
            chunks = chunk_text(raw_text)
            metadata = [{"type": "text"} for _ in chunks]

            # 3. Vision Integration
            if img_file:
                st.write("Processing Vision Stream...")
                vision_text = describe_image(img_file.read(), groq_key)
                chunks.append(f"IMAGE_ANALYSIS: {vision_text}")
                metadata.append({"type": "image"})

            # 4. Vectorization
            st.write("Generating Jina Embeddings...")
            embs = get_jina_embeddings(chunks, jina_key)
            st.session_state.retriever = FAISSRetriever(embs, metadata)
            st.session_state.chunks = chunks
            st.success("KNOWLEDGE_BASE_MOUNTED")

    # --- CHAT INTERFACE ---
    st.divider()
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Execute Intelligence Query..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
            
        with st.chat_message("assistant"):
            with st.status("`RAG_ORCHESTRATION...`"):
                # Search
                q_emb = get_jina_embeddings([prompt], jina_key)
                ids = st.session_state.retriever.search(q_emb, top_k=5)
                retrieved = [st.session_state.chunks[i] for i in ids]
                
                # Rerank & Final Answer
                context_docs = simple_rerank(prompt, retrieved)
                context = "\n\n".join(context_docs[:3])
                
                # CALL THE LLM FOR THE REAL ANSWER
                answer = ask_llm(context, prompt, groq_key, "llama-3.1-8b-instant")
            
            st.write(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
            # Feature: Show Sources in a Code Block
            with st.expander("`VIEW_SOURCE_CHUNKS`"):
                st.code(context, language="markdown")

else:
    st.info("⚡ READY_STATE_WAITING: Please provide API keys and upload source files.")
