"""
===========================================================================
Power Electronics Reliability Copilot
Sprint 5.5 — Knowledge Semantic Search API
===========================================================================

Purpose:
    Expose REST endpoints for semantic search over the knowledge FAISS index.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.knowledge_retrieval_service import knowledge_retrieval_service


router = APIRouter(
    prefix="/knowledge-search",
    tags=["Knowledge Search"],
)


class KnowledgeSearchRequest(BaseModel):
    """Request model for searching the knowledge FAISS index."""

    document_id: str
    query: str
    top_k: int = 5


@router.post("/search")
def search_knowledge(request: KnowledgeSearchRequest):
    """Search indexed knowledge chunks semantically."""

    try:
        return knowledge_retrieval_service.search(
            document_id=request.document_id,
            query=request.query,
            top_k=request.top_k,
        )

    except Exception as ex:
        raise HTTPException(
            status_code=400,
            detail=str(ex),
        )