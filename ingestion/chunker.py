def chunk_text(text: str, chunk_size: int = 512, overlap: int = 50) -> list[str]:
    """
    Split text into overlapping chunks by word count.
    - chunk_size: number of words per chunk
    - overlap: number of words to overlap between chunks
    """
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap  # slide forward with overlap

    return chunks


def chunk_documents(documents: list[dict], chunk_size: int = 512, overlap: int = 50) -> list[dict]:
    """
    Take a list of loaded document dicts and return
    a flat list of chunk dicts with metadata preserved.
    """
    all_chunks = []

    for doc in documents:
        chunks = chunk_text(doc["content"], chunk_size, overlap)

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "content": chunk,
                "metadata": {
                    **doc["metadata"],          # carry over source, file_type etc.
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                }
            })

    print(f"  Total chunks created: {len(all_chunks)}")
    return all_chunks