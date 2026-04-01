def build_prompt(query: str, retrieved_chunks: list[dict]) -> str:
    """
    Build a RAG prompt by injecting retrieved context
    into a structured template before the user's question.
    """

    # Format each chunk with its source for citation
    context_blocks = []
    for i, chunk in enumerate(retrieved_chunks, start=1):
        source = chunk["metadata"].get("source", "unknown")
        score  = chunk.get("score", 0)
        context_blocks.append(
            f"[Source {i}: {source} | Relevance: {score}]\n{chunk['content']}"
        )

    context_text = "\n\n---\n\n".join(context_blocks)

    prompt = f"""You are DataPilot, an expert data engineering assistant.
You answer questions strictly based on the provided context documents.
If the answer is not in the context, say "I don't have that information in the loaded documents."
Always mention which source you used.

CONTEXT:
{context_text}

---

QUESTION: {query}

ANSWER:"""

    return prompt


def format_sources(retrieved_chunks: list[dict]) -> list[dict]:
    """
    Return a clean list of sources for the API response.
    """
    sources = []
    for i, chunk in enumerate(retrieved_chunks, start=1):
        sources.append({
            "source_number": i,
            "file": chunk["metadata"].get("source", "unknown"),
            "relevance_score": chunk.get("score", 0),
            "preview": chunk["content"][:150] + "..."
        })
    return sources