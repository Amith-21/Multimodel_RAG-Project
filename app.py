
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
        background-image: linear-gradient(0deg, transparent 24%, rgba(32, 255, 255, .05) 25%, rgba(32, 255, 255, .05) 26%, transparent 27%, transparent 74%, rgba(32, 255, 255, .05) 75%, rgba(32, 255, 255, .05) 76%, transparent 77%, transparent), linear-gradient(90deg, transparent 24%, rgba(32, 255, 255, .05) 25%, rgba(32, 255, 255, .05) 26%, transparent 27%, transparent 74%, rgba(32, 255, 255, .05) 75%, rgba(32, 255, 255, .05) 76%, transparent 77%, transparent);
        background-size: 50px 50px;
    }

    .main-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 80px;
        font-weight: 800;
        background: linear-gradient(to bottom, #ffffff 30%, #22d3ee 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 15px rgba(34, 211, 238, 0.4));
        margin-bottom: 0px;
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

    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-thumb { background: #22d3ee; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: NEURAL ANALYTICS ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=50)
    st.markdown("### `SYSTEM_TELEMETRY`")
    
    st.progress(65, text="Neural Load")
    st.progress(22, text="VRAM Usage")
    
    st.divider()
    st.markdown("### `RETRIEVAL_HYPERPARAMETERS`")
    model_mode = st.toggle("Enable Reranker", value=True)
    chunk_overlap = st.slider("Chunk Overlap", 0, 200, 50)
    
    if st.button("💀 EMERGENCY_PURGE"):
        st.session_state.clear()
        st.rerun()

# --- HEADER SECTION ---
col_t1, col_t2 = st.columns([3, 1])
with col_t1:
    st.markdown("<h1 class='main-title'>BROCODE AI</h1>", unsafe_allow_html=True)
    st.markdown("`DIR: /root/multimodal_rag/prod_v3`")

with col_t2:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<div class='status-box'>⚡ ENGINE: ACTIVE<br>🛰️ LATENCY: 42ms<br>🔐 ENCRYPTION: AES-256</div>", unsafe_allow_html=True)

# --- MULTI-STAGE STEPPER (New Feature) ---
st.markdown("### `NEURAL_PIPELINE`")
p_cols = st.columns(4)
steps = ["1. INGEST", "2. EMBED", "3. RETRIEVE", "4. SYNTHESIZE"]
for i, step in enumerate(steps):
    p_cols[i].markdown(f"**{step}**")
    p_cols[i].progress(100 if i < 3 else 0)

st.divider()

# --- INPUT AREA ---
c1, c2 = st.columns(2)
with c1:
    st.markdown("### `UPLOAD_SOURCE`")
    src = st.file_uploader("Internal Docs", type=['pdf'], label_visibility="collapsed")
with c2:
    st.markdown("### `VISION_STREAM`")
    vis = st.file_uploader("Image Assets", type=['png', 'jpg'], label_visibility="collapsed")

# --- ANALYTICS DASHBOARD (New Feature) ---
if src or vis:
    st.markdown("### `RETRIEVAL_INSIGHTS`")
    data = pd.DataFrame({
        'Chunk_ID': [f'CH-{i}' for i in range(5)],
        'Score': np.random.uniform(0.7, 0.99, 5)
    })
    fig = px.bar(data, x='Chunk_ID', y='Score', color='Score', 
                 color_continuous_scale='Cyan', template='plotly_dark')
    fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig, use_container_width=True)

# --- CHAT INTERFACE ---
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
            st.write("Scanning vector space...")
            time.sleep(1)
            st.write("Applying cross-attention to visual stream...")
            time.sleep(1)
        
        response = "ACCESS GRANTED. The analyzed documentation indicates a 94% match for your query parameters."
        st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})import streamlit as st
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
        background-image: linear-gradient(0deg, transparent 24%, rgba(32, 255, 255, .05) 25%, rgba(32, 255, 255, .05) 26%, transparent 27%, transparent 74%, rgba(32, 255, 255, .05) 75%, rgba(32, 255, 255, .05) 76%, transparent 77%, transparent), linear-gradient(90deg, transparent 24%, rgba(32, 255, 255, .05) 25%, rgba(32, 255, 255, .05) 26%, transparent 27%, transparent 74%, rgba(32, 255, 255, .05) 75%, rgba(32, 255, 255, .05) 76%, transparent 77%, transparent);
        background-size: 50px 50px;
    }

    .main-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 80px;
        font-weight: 800;
        background: linear-gradient(to bottom, #ffffff 30%, #22d3ee 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 15px rgba(34, 211, 238, 0.4));
        margin-bottom: 0px;
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

    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-thumb { background: #22d3ee; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: NEURAL ANALYTICS ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=50)
    st.markdown("### `SYSTEM_TELEMETRY`")
    
    st.progress(65, text="Neural Load")
    st.progress(22, text="VRAM Usage")
    
    st.divider()
    st.markdown("### `RETRIEVAL_HYPERPARAMETERS`")
    model_mode = st.toggle("Enable Reranker", value=True)
    chunk_overlap = st.slider("Chunk Overlap", 0, 200, 50)
    
    if st.button("💀 EMERGENCY_PURGE"):
        st.session_state.clear()
        st.rerun()

# --- HEADER SECTION ---
col_t1, col_t2 = st.columns([3, 1])
with col_t1:
    st.markdown("<h1 class='main-title'>BROCODE AI</h1>", unsafe_allow_html=True)
    st.markdown("`DIR: /root/multimodal_rag/prod_v3`")

with col_t2:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<div class='status-box'>⚡ ENGINE: ACTIVE<br>🛰️ LATENCY: 42ms<br>🔐 ENCRYPTION: AES-256</div>", unsafe_allow_html=True)

# --- MULTI-STAGE STEPPER (New Feature) ---
st.markdown("### `NEURAL_PIPELINE`")
p_cols = st.columns(4)
steps = ["1. INGEST", "2. EMBED", "3. RETRIEVE", "4. SYNTHESIZE"]
for i, step in enumerate(steps):
    p_cols[i].markdown(f"**{step}**")
    p_cols[i].progress(100 if i < 3 else 0)

st.divider()

# --- INPUT AREA ---
c1, c2 = st.columns(2)
with c1:
    st.markdown("### `UPLOAD_SOURCE`")
    src = st.file_uploader("Internal Docs", type=['pdf'], label_visibility="collapsed")
with c2:
    st.markdown("### `VISION_STREAM`")
    vis = st.file_uploader("Image Assets", type=['png', 'jpg'], label_visibility="collapsed")

# --- ANALYTICS DASHBOARD (New Feature) ---
if src or vis:
    st.markdown("### `RETRIEVAL_INSIGHTS`")
    data = pd.DataFrame({
        'Chunk_ID': [f'CH-{i}' for i in range(5)],
        'Score': np.random.uniform(0.7, 0.99, 5)
    })
    fig = px.bar(data, x='Chunk_ID', y='Score', color='Score', 
                 color_continuous_scale='Cyan', template='plotly_dark')
    fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig, use_container_width=True)

# --- CHAT INTERFACE ---
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
            st.write("Scanning vector space...")
            time.sleep(1)
            st.write("Applying cross-attention to visual stream...")
            time.sleep(1)
        
        response = "ACCESS GRANTED. The analyzed documentation indicates a 94% match for your query parameters."
        st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
