import math
import re
from collections import Counter
from dataclasses import dataclass


TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9]+")


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_PATTERN.findall(text)]


def cosine_similarity(left: Counter[str], right: Counter[str]) -> float:
    common = left.keys() & right.keys()
    numerator = sum(left[token] * right[token] for token in common)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    if not left_norm or not right_norm:
        return 0.0
    return numerator / (left_norm * right_norm)


@dataclass(frozen=True)
class IndexedChunk:
    document_id: str
    filename: str
    chunk_index: int
    content: str


class InMemoryRetriever:
    """Small local retriever that can later be replaced with pgvector."""

    def __init__(self) -> None:
        self._chunks: list[IndexedChunk] = []

    def add(self, chunks: list[IndexedChunk]) -> None:
        self._chunks.extend(chunks)

    def search(
        self, question: str, top_k: int = 3, document_id: str | None = None
    ) -> list[tuple[IndexedChunk, float]]:
        query_vector = Counter(tokenize(question))
        candidates = (
            chunk
            for chunk in self._chunks
            if document_id is None or chunk.document_id == document_id
        )
        scored = [
            (chunk, cosine_similarity(query_vector, Counter(tokenize(chunk.content))))
            for chunk in candidates
        ]
        scored.sort(key=lambda item: item[1], reverse=True)
        return [item for item in scored[:top_k] if item[1] > 0]

