import os
from pypdf import PdfReader
from pathlib import Path


def load_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text


def load_text(file_path: str) -> str:
    """Load plain text or markdown file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def load_document(file_path: str) -> dict:
    """
    Load a single document and return a dict with
    content + metadata.
    """
    path = Path(file_path)
    ext = path.suffix.lower()

    if ext == ".pdf":
        content = load_pdf(file_path)
    elif ext in [".txt", ".md"]:
        content = load_text(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    return {
        "content": content,
        "metadata": {
            "source": path.name,
            "file_type": ext,
            "file_path": str(path.resolve()),
        }
    }


def load_documents_from_folder(folder_path: str) -> list[dict]:
    """
    Load all supported documents from a folder.
    Returns a list of document dicts.
    """
    supported = {".pdf", ".txt", ".md"}
    documents = []
    folder = Path(folder_path)

    for file in folder.iterdir():
        if file.suffix.lower() in supported:
            print(f"  Loading: {file.name}")
            doc = load_document(str(file))
            documents.append(doc)

    print(f"\n  Total documents loaded: {len(documents)}")
    return documents