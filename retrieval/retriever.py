from retrieval.vector_store import get_or_create_collection
from ingestion.embedder import embed_query


def retrieve(query: str, top_k: int = 3, collection_name: str = "datapilot_docs") -> list[dict]:
    """
    Given a plain-text query:
    1. Embed it using E5-large (with 'query:' prefix)
    2. Search ChromaDB for top_k most similar chunks
    3. Return results with content + metadata + similarity score
    """
    # Step 1: embed the query
    query_embedding = embed_query(query)

    # Step 2: search ChromaDB
    collection = get_or_create_collection(collection_name)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    # Step 3: format results
    retrieved = []
    for i in range(len(results["documents"][0])):
        retrieved.append({
            "content":    results["documents"][0][i],
            "metadata":   results["metadatas"][0][i],
            "score":      round(1 - results["distances"][0][i], 4)  # cosine similarity
        })

    return retrieved