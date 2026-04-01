# DataPilot

A RAG-powered data engineering assistant that answers questions grounded in your ingested documents.

## Architecture

```
User Query
    |
    ▼
Streamlit UI (ui/app.py)
    |
    ▼
FastAPI Backend (api/main.py)
    |
    - Ingestion Pipeline
    |       - loader.py       — loads PDFs and text files
    |       - chunker.py      — splits documents into chunks
    |       |_ embedder.py     — generates embeddings (E5 model)
    |
    - Retrieval
    |       - vector_store.py — ChromaDB operations
    |       |_ retriever.py    — semantic search (top-k)
    |
    |_ Generation
            - prompt_builder.py — builds RAG prompt with context
            |_ llm.py            — LLaMA 3.1 via Ollama
```

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com/) with `llama3.1` model

## Setup

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd datapilot
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/Mac
   venv\Scripts\activate         # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Pull the LLaMA model via Ollama**
   ```bash
   ollama pull llama3.1
   ```

## Running the App

1. **Start Ollama** (if not already running)
   ```bash
   ollama serve
   ```

2. **Start the FastAPI backend**
   ```bash
   uvicorn api.main:app --reload
   ```

3. **Start the Streamlit frontend** (in a separate terminal)
   ```bash
   streamlit run ui/app.py
   ```

4. Open [http://localhost:8501](http://localhost:8501) in your browser.

## Usage

1. Use the **Ingest Documents** panel in the sidebar to load documents from a folder (default: `data/sample_docs`).
2. Once ingested, ask questions in the chat interface.
3. Toggle **Show sources** to see which document chunks were used to generate the answer.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Check API status and chunk count |
| POST | `/ingest` | Ingest documents from a folder |
| POST | `/query` | Ask a question (JSON response) |
| POST | `/query/stream` | Ask a question (streaming response) |
| GET | `/stats` | Vector store statistics |

## Project Structure

```
datapilot/
- api/                  # FastAPI backend
- generation/           # LLM + prompt building
- ingestion/            # Document loading, chunking, embedding
- retrieval/            # ChromaDB vector store + retriever
- ui/                   # Streamlit frontend
- data/sample_docs/     # Sample documents
- download_docs.py      # Script to download sample documents
|_ requirements.txt
```
