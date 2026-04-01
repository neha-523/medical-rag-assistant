import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY"] = "False"

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ingestion.loader import load_documents_from_folder
from ingestion.chunker import chunk_documents
from ingestion.embedder import embed_chunks
from retrieval.vector_store import (
    add_chunks_to_collection,
    get_collection_stats,
    reset_collection,
)
from retrieval.retriever import retrieve
from generation.prompt_builder import build_prompt, format_sources
from generation.llm import generate_answer

app = FastAPI(title="DataPilot API")


class IngestRequest(BaseModel):
    folder_path: str = "data/sample_docs"
    chunk_size: int = 512
    overlap: int = 50
    reset: bool = True


class QueryRequest(BaseModel):
    question: str
    top_k: int = 3


@app.get("/health")
def health():
    stats = get_collection_stats()
    return {"status": "ok", "vector_store": stats}


@app.post("/ingest")
def ingest(req: IngestRequest):
    try:
        if req.reset:
            reset_collection()

        docs = load_documents_from_folder(req.folder_path)
        chunks = chunk_documents(docs, chunk_size=req.chunk_size, overlap=req.overlap)
        chunks = embed_chunks(chunks)
        add_chunks_to_collection(chunks)

        stats = get_collection_stats()
        return {
            "documents_loaded": len(docs),
            "chunks_stored": stats["total_chunks"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query")
def query(req: QueryRequest):
    try:
        chunks = retrieve(req.question, top_k=req.top_k)
        if not chunks:
            return {
                "answer": "No relevant documents found. Please ingest documents first.",
                "sources": [],
                "chunks_retrieved": 0,
            }

        prompt = build_prompt(req.question, chunks)
        answer = generate_answer(prompt)
        sources = format_sources(chunks)

        return {
            "answer": answer,
            "sources": sources,
            "chunks_retrieved": len(chunks),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
