"""
===========================================================================
Power Electronics Reliability Copilot
Sprint 5.2 — Knowledge Chunk Pipeline API
===========================================================================

File:
    knowledge_chunks.py

Purpose:
    Expose REST endpoints for creating chunks from approved engineering
    evidence documents.

Why this file exists:
    This API connects FastAPI to the Knowledge Chunk Service. It allows a
    registered evidence document to be split into traceable chunks that can
    later be embedded, indexed, analysed and linked to Neo4j.

Responsibilities:
    - Receive chunk creation requests
    - Validate document ID and file path input
    - Call the Knowledge Chunk Service
    - Return chunk creation summary

This API DOES NOT:
    - Generate embeddings
    - Search FAISS or BM25
    - Extract engineering entities
    - Populate Neo4j
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.knowledge_chunk_service import knowledge_chunk_service


router = APIRouter(
    prefix="/knowledge-chunks",
    tags=["Knowledge Chunks"],
)


class KnowledgeChunkRequest(BaseModel):
    """Request model for creating chunks from a registered evidence document."""

    document_id: str
    file_path: str


@router.post("/create")
def create_knowledge_chunks(request: KnowledgeChunkRequest):
    """
    Create traceable chunks from an approved engineering document.
    """

    try:
        return knowledge_chunk_service.create_chunks(
            document_id=request.document_id,
            file_path=request.file_path,
        )

    except Exception as ex:
        raise HTTPException(
            status_code=400,
            detail=str(ex),
        )