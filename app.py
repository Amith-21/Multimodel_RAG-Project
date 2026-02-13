import streamlit as st
import time
import pandas as pd
import numpy as np
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="Brocode AI | Command Center", page_icon="💀", layout="wide")

# --- HIGH-TECH CYBER CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');

    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 50%, #0d1a1a 0%, #050505 100%);
    }

    .main-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 80px;
        font-weight: 800;
        background: linear-gradient(to right, #ffffff, #22d3ee, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 15px rgba(34, 211, 238, 0.4));
    }

    .status-box {
        background: rgba(34, 211, 238, 0.05);
        border: 1px solid #22d3ee;
        padding: 10px;
        border-radius: 5px;
        font-family: 'JetBrains Mono', monospace;
        color: #22d3ee;
        font-size: 0.8rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: NEURAL ANALYTICS ---
with st.sidebar:
    st.markdown("### `SYSTEM_TELEMETRY`")
    st.progress(65, text="Neural Load")
    st.progress(22, text="VRAM Usage")
    
    st.divider()
    st.markdown("### `SESSION_ECONOMICS`")
    c1, c2 = st.columns(2)
    c1.metric("TOKENS", "1.4k", "+12%")
    c2.metric("COST", "$0.003", "USD")
    
    if st.button("💀 EMERGENCY_PURGE", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# --- HEADER ---
col_t1, col_t2 = st.columns([3, 1])
with col_t1:
    st.markdown("<h1 class='main-title'>BROCODE AI</h1>", unsafe_allow_html=True)
    st.markdown("`DIR: /root/multimodal_rag/prod_v3`")

with col_t2:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<div class='status-box'>⚡ ENGINE: ACTIVE<br>🛰️ LATENCY: 42ms</div>", unsafe_allow_html=True)

# --- NEURAL PIPELINE ---
st.markdown("### `NEURAL_PIPELINE_STATUS`")
p_cols = st.columns(4)
steps = ["INGEST", "EMBED", "RETRIEVE", "SYNTHESIZE"]
for i, step in enumerate(steps):
    p_cols[i].markdown(f"**{i+1}. {step}**")
    p_cols[i].progress(100 if i < 3 else 0)

st.divider()

# --- INPUT & ANALYTICS ---
c1, c2 = st.columns([1, 1.5])
with c1:
    st.markdown("### `DATA_MOUNTS`")
    src = st.file_uploader("Internal Docs", type=['pdf'], label_visibility="collapsed")
    vis = st.file_uploader("Vision Assets", type=['png', 'jpg'], label_visibility="collapsed")

with c2:
    st.markdown("### `LATENT_SPACE_TOPOGRAPHY`")
    # Feature: 3D Vector Space Visualization
    map_data = pd.DataFrame({
        'x': np.random.randn(30), 'y': np.random.randn(30), 'z': np.random.randn(30),
        'cluster': np.random.choice(['Tech', 'Legal', 'Vision'], 30)
    })
    fig = px.scatter_3d(map_data, x='x', y='y', z='z', color='cluster', template="plotly_dark")
    fig.update_layout(margin=dict(l=0,r=0,b=0,t=0), height=300)
    st.plotly_chart(fig, use_container_width=True)

# --- CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Execute Query..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
        
    with st.chat_message("assistant"):
        with st.status("`BROCODE_REASONING...`"):
            st.write("Cross-referencing vision embeddings...")
            time.sleep(1)
        
        response = "ACCESS GRANTED. Parameters identified within embedded documentation."
        st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
