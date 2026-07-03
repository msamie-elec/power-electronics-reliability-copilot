"""
===========================================================================
Power Electronics Reliability Copilot
Sprint 5.8 — Knowledge Extraction API
===========================================================================

Purpose:
    Expose REST endpoints for extracting graph-ready engineering knowledge
    from approved knowledge chunks.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.knowledge_extraction_service import knowledge_extraction_service


router = APIRouter(
    prefix="/knowledge-extraction",
    tags=["Knowledge Extraction"],
)


class KnowledgeExtractionRequest(BaseModel):
    """Request model for extracting knowledge from chunked evidence documents."""

    document_id: str
    max_chunks: int | None = None


@router.post("/run")
def run_knowledge_extraction(request: KnowledgeExtractionRequest):
    """Extract graph-ready entities and relationships from knowledge chunks."""

    try:
        return knowledge_extraction_service.extract_knowledge(
            document_id=request.document_id,
            max_chunks=request.max_chunks,
        )

    except Exception as ex:
        raise HTTPException(
            status_code=400,
            detail=str(ex),
        )