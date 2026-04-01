import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY"] = "False"

import chromadb
from chromadb.config import Settings


# Initialize a persistent ChromaDB client
# Data is saved to disk at ./chroma_db/
def get_client() -> chromadb.ClientAPI:
    client = chromadb.PersistentClient(path="./chroma_db")
    return client


def get_or_create_collection(collection_name: str = "datapilot_docs"):
    """
    Get existing collection or create a new one.
    We use cosine similarity since E5 vectors are normalized.
    """
    client = get_client()
    collection = client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}
    )
    return collection


def add_chunks_to_collection(chunks: list[dict], collection_name: str = "datapilot_docs"):
    """
    Insert embedded chunks into ChromaDB.
    Each chunk needs: id, embedding, document text, metadata.
    """
    collection = get_or_create_collection(collection_name)

    ids         = []
    embeddings  = []
    documents   = []
    metadatas   = []

    for i, chunk in enumerate(chunks):
        # Build a unique ID from source filename + chunk index
        source = chunk["metadata"].get("source", "unknown")
        chunk_idx = chunk["metadata"].get("chunk_index", i)
        unique_id = f"{source}_chunk_{chunk_idx}"

        ids.append(unique_id)
        embeddings.append(chunk["embedding"])
        documents.append(chunk["content"])
        metadatas.append(chunk["metadata"])

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )

    print(f"  Stored {len(ids)} chunks into collection '{collection_name}'")
    return collection


def get_collection_stats(collection_name: str = "datapilot_docs") -> dict:
    """Return how many chunks are stored in the collection."""
    collection = get_or_create_collection(collection_name)
    count = collection.count()
    return {"collection": collection_name, "total_chunks": count}


def reset_collection(collection_name: str = "datapilot_docs"):
    """
    Delete and recreate the collection.
    Useful when re-ingesting updated documents.
    Safely handles the case where collection doesn't exist yet.
    """
    client = get_client()
    try:
        client.delete_collection(name=collection_name)
        print(f"  Collection '{collection_name}' cleared.")
    except ValueError:
        print(f"  Collection '{collection_name}' doesn't exist yet — creating fresh.")
    return get_or_create_collection(collection_name)