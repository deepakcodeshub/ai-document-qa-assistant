import re


def normalize_text(text: str) -> str:
    """Collapse repeated whitespace while retaining readable paragraphs."""
    paragraphs = [re.sub(r"\s+", " ", part).strip() for part in text.splitlines()]
    return "\n".join(part for part in paragraphs if part)


def chunk_text(text: str, chunk_size: int = 700, overlap: int = 100) -> list[str]:
    """Split text into overlapping chunks without cutting words when possible."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be between 0 and chunk_size - 1")

    cleaned = normalize_text(text)
    if not cleaned:
        return []

    chunks: list[str] = []
    start = 0
    while start < len(cleaned):
        end = min(start + chunk_size, len(cleaned))
        if end < len(cleaned):
            boundary = cleaned.rfind(" ", start, end)
            if boundary > start:
                end = boundary
        chunks.append(cleaned[start:end].strip())
        if end >= len(cleaned):
            break
        start = max(end - overlap, start + 1)
    return chunks

