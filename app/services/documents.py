from pathlib import Path
from uuid import uuid4

from app.services.chunking import chunk_text
from app.services.retrieval import IndexedChunk, InMemoryRetriever


class DocumentService:
    def __init__(self, retriever: InMemoryRetriever, upload_dir: Path) -> None:
        self.retriever = retriever
        self.upload_dir = upload_dir

    def ingest_text(self, filename: str, content: str) -> tuple[str, int]:
        document_id = uuid4().hex
        chunks = chunk_text(content)
        if not chunks:
            raise ValueError("The document does not contain readable text")

        safe_name = Path(filename).name
        destination = self.upload_dir / f"{document_id}-{safe_name}"
        destination.write_text(content, encoding="utf-8")
        self.retriever.add(
            [
                IndexedChunk(document_id, safe_name, index, chunk)
                for index, chunk in enumerate(chunks)
            ]
        )
        return document_id, len(chunks)

