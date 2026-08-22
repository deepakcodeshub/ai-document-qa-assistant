from pydantic import BaseModel, Field


class DocumentSummary(BaseModel):
    document_id: str
    filename: str
    chunk_count: int


class QuestionRequest(BaseModel):
    question: str = Field(min_length=3, max_length=500)
    document_id: str | None = None


class SourceChunk(BaseModel):
    document_id: str
    filename: str
    chunk_index: int
    content: str
    score: float


class AnswerResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceChunk]

