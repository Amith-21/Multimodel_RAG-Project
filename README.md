# Enterprise Multimodal RAG (Text + Vision)

This project is an end-to-end **Multimodal Retrieval-Augmented Generation (RAG)** system that enables question answering over both:

- Text documents (TXT, PDF)
- Images (diagrams, charts, screenshots)

It combines:

- Document retrieval using embeddings + FAISS
- Image understanding using Groq Vision models
- Grounded answer generation using Groq LLMs
- A modern Streamlit user interface

---

## Live Demo

The application is deployed and accessible here:

https://rag-with-multimodality.streamlit.app/

---

## Key Features

- Text-based RAG over uploaded TXT and PDF files  
- Multimodal RAG support with image understanding  
- Vision-based image captioning using:

  `meta-llama/llama-4-scout-17b-16e-instruct`

- Embedding generation using Jina Embeddings v4 API  
- Vector similarity retrieval with FAISS  
- Simple reranking layer for improved relevance  
- Guardrails to reduce hallucinations (context-only answering)  
- Session memory with recent chat history  
- Latency tracking displayed in the UI  
- Metadata filtering (retrieve text-only, image-only, or both)

---

## Architecture Overview

1. User uploads a document (TXT/PDF)
2. Text is chunked with overlap for better retrieval
3. User optionally uploads an image
4. Image is converted into semantic text using Groq Vision
5. All chunks are embedded using Jina Embeddings v4
6. FAISS retrieves the most relevant context
7. Retrieved chunks are reranked
8. Groq LLM generates an answer grounded in retrieved context

---

## Project Structure

```bash
multimodal-rag-jina4/
├── app.py
├── requirements.txt
├── config.py
├── README.md
└── rag/
    ├── __init__.py
    ├── embeddings.py
    ├── retriever.py
    ├── chunking.py
    ├── vision.py
    ├── reranker.py
    └── llm.py
