import streamlit as st
import time
from pypdf import PdfReader
from PIL import Image
import io

# Mock imports based on your structure
from rag.embeddings import get_jina_embeddings
from rag.vision import describe_image
from rag.chunking import chunk_text
from rag.retriever import FAISSRetriever
from rag.reranker import simple_rerank
from rag.llm import ask_llm

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Nexus Multimodal AI",
    page_icon="🧠",
    layout="wide"
)

# --- CUSTOM THEME & STYLING ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    
    /* Glassmorphism Panels */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
    
    .main-title {
        font-size: 48px;
        font-weight: 800;
        background: linear-gradient(to right, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }

    /* Customizing sidebar */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.8);
    }

    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- APP LOGO & HEADER ---
st.markdown("<div class='main-title'>Nexus RAG</div>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; font-size: 1.1rem;'>Advanced Intelligence over Documents & Visuals</p>", unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if "history" not in st.session_state:
    st.session_state.history = []
if "processed_data" not in st.session_state:
    st.session_state.processed_data = None

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
    st.title("Control Center")
    
    with st.expander("🔑 API Credentials", expanded=True):
        groq_key = st.text_input("Groq API Key", type="password")
        jina_key = st.text_input("Jina API Key", type="password")

    with st.expander("🛠️ Model Settings", expanded=True):
        model = st.selectbox("LLM Model", ["llama-3.1-8b-instant", "llama3-70b-8192"])
        filter_type = st.select_slider("Retrieval Priority", options=["text", "all", "image"], value="all")
        chunk_size = st.slider("Chunk Size", 256, 1024, 512)

    if st.button("Clear Conversation"):
        st.session_state.history = []
        st.rerun()

# --- MAIN LAYOUT ---


col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📄 Knowledge Ingestion")
    txt_file = st.file_uploader("Drop PDF or TXT", type=["txt", "pdf"])
    
    if txt_file:
        st.success(f"Loaded: {txt_file.name}")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("🖼️ Visual Context")
    img_file = st.file_uploader("Drop Image", type=["png", "jpg", "jpeg"])
    
    if img_file:
        st.image(img_file, caption="Preview", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- PROCESSING LOGIC ---
if txt_file and groq_key and jina_key:
    if st.session_state.processed_data is None:
        with st.status("🧠 Building Knowledge Base...", expanded=True) as status:
            st.write("Extracting text from document...")
            if txt_file.name.endswith(".pdf"):
                reader = PdfReader(txt_file)
                raw_text = "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
            else:
                raw_text = txt_file.read().decode("utf-8")

            st.write("Chunking content...")
            chunks = chunk_text(raw_text)
            metadata = [{"type": "text"} for _ in chunks]

            if img_file:
                st.write("Analyzing image with Vision AI...")
                image_bytes = img_file.getvalue()
                vision_text = describe_image(image_bytes, groq_key)
                if vision_text:
                    chunks.append(f"IMAGE CONTEXT: {vision_text}")
                    metadata.append({"type": "image"})

            st.write("Generating Jina Embeddings...")
            embeddings = get_jina_embeddings(chunks, jina_key)
            retriever = FAISSRetriever(embeddings, metadata)
            
            st.session_state.processed_data = (chunks, retriever)
            status.update(label="Knowledge Base Ready!", state="complete", expanded=False)

    # --- QUERY INTERFACE ---
    chunks, retriever = st.session_state.processed_data
    
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    query = st.chat_input("Ask anything about your data...")
    
    if query:
        with st.spinner("Searching and Reasoning..."):
            start = time.time()
            query_emb = get_jina_embeddings([query], jina_key)
            
            f = None if filter_type == "all" else filter_type
            ids = retriever.search(query_emb, top_k=5, filter_type=f)
            
            retrieved_docs = [chunks[i] for i in ids]
            reranked = simple_rerank(query, retrieved_docs)
            context = "\n\n".join(reranked[:3])
            
            answer = ask_llm(context, query, groq_key, model)
            latency = round(time.time() - start, 2)
            
            st.session_state.history.append({"q": query, "a": answer, "time": latency})

    # --- DISPLAY CONVERSATION ---
    for chat in reversed(st.session_state.history):
        with st.chat_message("user"):
            st.write(chat["q"])
        with st.chat_message("assistant"):
            st.write(chat["a"])
            st.caption(f"⏱️ Latency: {chat['time']}s")
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.warning("⚡ Waiting for API Keys and Documents to initialize.")
