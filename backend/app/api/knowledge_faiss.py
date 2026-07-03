"""
===========================================================================
Power Electronics Reliability Copilot
Sprint 5.4 — Knowledge FAISS Index API
===========================================================================

Purpose:
    Expose REST endpoints for building FAISS indexes from knowledge embeddings.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.knowledge_faiss_service import knowledge_faiss_service


router = APIRouter(
    prefix="/knowledge-faiss",
    tags=["Knowledge FAISS"],
)


class KnowledgeFaissIndexRequest(BaseModel):
    """Request model for building a FAISS index from document embeddings."""

    document_id: str


@router.post("/build")
def build_knowledge_faiss_index(request: KnowledgeFaissIndexRequest):
    """Build FAISS index for a knowledge document."""

    try:
        return knowledge_faiss_service.build_index(
            document_id=request.document_id,
        )

    except Exception as ex:
        raise HTTPException(
            status_code=400,
            detail=str(ex),
        )