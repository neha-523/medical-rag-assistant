import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"

import streamlit as st
import requests

API_BASE = "http://localhost:8000"

# ── Page config ──
st.set_page_config(
    page_title="DataPilot",
    page_icon="🚀",
    layout="wide"
)

# ── Sidebar ──
with st.sidebar:
    st.title("🚀 DataPilot")
    st.caption("RAG-powered data engineering assistant")
    st.divider()

    # Health check
    st.subheader("System Status")
    try:
        health = requests.get(f"{API_BASE}/health", timeout=3).json()
        chunks = health["vector_store"]["total_chunks"]
        if chunks > 0:
            st.success(f"✅ Connected — {chunks} chunks indexed")
        else:
            st.warning("⚠️ Connected but no documents ingested")
    except Exception:
        st.error("❌ API not reachable. Start the FastAPI server first.")

    st.divider()

    # Ingest panel
    st.subheader("📂 Ingest Documents")
    folder_path = st.text_input(
        "Folder path",
        value="data/sample_docs",
        help="Path to folder containing PDF, TXT, or MD files"
    )
    chunk_size = st.slider("Chunk size (words)", 100, 1000, 512, 50)
    top_k = st.slider("Chunks to retrieve (top-k)", 1, 5, 3)
    reset = st.checkbox("Reset collection before ingesting", value=True)

    if st.button("🔄 Ingest Documents", use_container_width=True):
        with st.spinner("Ingesting documents..."):
            try:
                resp = requests.post(
                    f"{API_BASE}/ingest",
                    json={
                        "folder_path": folder_path,
                        "chunk_size": chunk_size,
                        "overlap": 50,
                        "reset": reset
                    },
                    timeout=600
                )
                result = resp.json()
                if resp.status_code == 200:
                    st.success(
                        f"✅ Ingested {result['documents_loaded']} docs "
                        f"→ {result['chunks_stored']} chunks"
                    )
                    st.rerun()
                else:
                    st.error(f"Error: {result.get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Failed: {e}")

    st.divider()
    st.caption("Built with LLaMA 3.1 · E5-large · ChromaDB · FastAPI")

# ── Main chat area ──
st.title("💬 Ask DataPilot")
st.caption("Ask anything about your ingested data engineering documents")

# Init chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "show_sources" not in st.session_state:
    st.session_state.show_sources = True

st.session_state.show_sources = st.toggle("Show sources", value=True)

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and "sources" in msg and st.session_state.show_sources:
            with st.expander(f"📚 Sources ({len(msg['sources'])} chunks retrieved)"):
                for src in msg["sources"]:
                    st.markdown(
                        f"**[{src['source_number']}] {src['file']}** "
                        f"— relevance: `{src['relevance_score']}`"
                    )
                    st.caption(src["preview"])
                    st.divider()

# Chat input
if prompt := st.chat_input("e.g. What is the SLA for the ETL pipeline?"):

    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get answer from API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                resp = requests.post(
                    f"{API_BASE}/query",
                    json={"question": prompt, "top_k": top_k},
                    timeout=600
                )
                if resp.status_code == 200:
                    data = resp.json()
                    answer = data["answer"]
                    sources = data["sources"]

                    st.markdown(answer)

                    if st.session_state.show_sources:
                        with st.expander(f"📚 Sources ({data['chunks_retrieved']} chunks retrieved)"):
                            for src in sources:
                                st.markdown(
                                    f"**[{src['source_number']}] {src['file']}** "
                                    f"— relevance: `{src['relevance_score']}`"
                                )
                                st.caption(src["preview"])
                                st.divider()

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })

                else:
                    error = resp.json().get("detail", "Unknown error")
                    st.error(f"API Error: {error}")

            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to API. Make sure FastAPI is running on port 8000.")
            except Exception as e:
                st.error(f"Error: {e}")