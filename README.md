# AI-Powered Document Q&A Assistant

A FastAPI project for uploading documents and asking questions grounded in their content. The current MVP supports UTF-8 text and Markdown files, creates overlapping chunks, retrieves relevant passages, and returns answers with source information.

## Why this project

This repository turns Generative AI concepts into a practical backend system. It provides a clean foundation for adding embeddings, PostgreSQL with pgvector, an LLM, evaluation, and AWS deployment.

## Current features

- FastAPI health, document-upload, and question endpoints
- Safe `.txt` and `.md` ingestion with configurable file-size limits
- Overlapping text chunking
- Dependency-light local similarity retrieval
- Answers accompanied by source chunks and relevance scores
- Unit tests for chunking and retrieval
- Docker and VS Code configurations

## Architecture

```text
Client -> FastAPI -> Document service -> Chunking -> Retriever
                   \-> Local uploads      \-> Source-grounded response
```

The in-memory retriever intentionally keeps the first version easy to run. A future `PgVectorRetriever` can implement the same search boundary without changing the API routes.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the interactive API documentation.

## Test

Without installing API dependencies, the core tests run with Python's standard library:

```powershell
python -m unittest discover -s tests -v
```

After installing the development requirements:

```powershell
pytest
```

## Example workflow

1. Upload a UTF-8 `.txt` or `.md` file through `POST /documents`.
2. Copy the returned `document_id`.
3. Send a question to `POST /questions` with that ID.
4. Review the answer and its source chunks.

## Roadmap

- PDF and DOCX text extraction
- Embedding generation and PostgreSQL/pgvector storage
- LLM-based answer generation with citations
- Authentication and per-user document collections
- Retrieval and answer-quality evaluation
- Structured logging and observability
- Docker Compose PostgreSQL service
- AWS deployment and CI/CD

## Technology

Python, FastAPI, RAG foundations, PostgreSQL/pgvector roadmap, Docker, and AWS deployment roadmap.


