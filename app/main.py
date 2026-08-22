from fastapi import FastAPI, File, HTTPException, UploadFile

from app.config import settings
from app.models import AnswerResponse, DocumentSummary, QuestionRequest, SourceChunk
from app.services.documents import DocumentService
from app.services.retrieval import InMemoryRetriever


app = FastAPI(
    title=settings.app_name,
    description="Upload text documents and ask questions grounded in their content.",
    version="0.1.0",
)
retriever = InMemoryRetriever()
documents = DocumentService(retriever, settings.upload_dir)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.post("/documents", response_model=DocumentSummary, status_code=201)
async def upload_document(file: UploadFile = File(...)) -> DocumentSummary:
    if not file.filename or not file.filename.lower().endswith((".txt", ".md")):
        raise HTTPException(400, "The MVP currently supports .txt and .md files")

    payload = await file.read(settings.max_file_size_mb * 1024 * 1024 + 1)
    if len(payload) > settings.max_file_size_mb * 1024 * 1024:
        raise HTTPException(413, "File exceeds the configured size limit")
    try:
        content = payload.decode("utf-8")
        document_id, count = documents.ingest_text(file.filename, content)
    except (UnicodeDecodeError, ValueError) as exc:
        raise HTTPException(400, str(exc)) from exc
    return DocumentSummary(document_id=document_id, filename=file.filename, chunk_count=count)


@app.post("/questions", response_model=AnswerResponse)
def ask_question(request: QuestionRequest) -> AnswerResponse:
    matches = retriever.search(
        request.question, settings.top_k_results, request.document_id
    )
    if not matches:
        return AnswerResponse(
            question=request.question,
            answer="I could not find relevant information in the uploaded documents.",
            sources=[],
        )

    sources = [
        SourceChunk(
            document_id=chunk.document_id,
            filename=chunk.filename,
            chunk_index=chunk.chunk_index,
            content=chunk.content,
            score=round(score, 4),
        )
        for chunk, score in matches
    ]
    answer = "Based on the uploaded content:\n\n" + "\n\n".join(
        source.content for source in sources
    )
    return AnswerResponse(question=request.question, answer=answer, sources=sources)

