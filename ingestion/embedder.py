from sentence_transformers import SentenceTransformer

# E5 models need a prefix for best performance
EMBED_PREFIX = "passage: "
QUERY_PREFIX  = "query: "

# Load once at module level — avoids reloading on every call
print("  Loading E5-large model (first run downloads ~1.3 GB)...")
_model = SentenceTransformer("intfloat/e5-large-v2")
print("  E5-large model loaded.")


def embed_chunks(chunks: list[dict]) -> list[dict]:
    """
    Add an 'embedding' field to each chunk dict.
    Uses E5's recommended 'passage:' prefix for documents.
    """
    texts = [EMBED_PREFIX + chunk["content"] for chunk in chunks]
    embeddings = _model.encode(texts, show_progress_bar=True, normalize_embeddings=True)

    for chunk, embedding in zip(chunks, embeddings):
        chunk["embedding"] = embedding.tolist()

    return chunks


def embed_query(query: str) -> list[float]:
    """
    Embed a user query using E5's 'query:' prefix.
    Returns a flat list of floats.
    """
    embedding = _model.encode(QUERY_PREFIX + query, normalize_embeddings=True)
    return embedding.tolist()


#💡 **Why the prefix** E5-large is trained to expect "passage: " before documents and "query: " before questions. Skipping this kills retrieval quality — this is a common mistake people skip in tutorials.



