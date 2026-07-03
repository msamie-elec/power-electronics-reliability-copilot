"""
===========================================================================
Power Electronics Reliability Copilot
Sprint 5.3 — Knowledge Embedding Pipeline API
===========================================================================

File:
    knowledge_embeddings.py

Purpose:
    Expose REST endpoints for generating embeddings from approved knowledge
    chunks.

Why this file exists:
    This API connects FastAPI to the Knowledge Embedding Service. It allows
    registered and chunked evidence documents to be converted into vector
    embeddings for later FAISS indexing and semantic retrieval.

Responsibilities:
    - Receive embedding creation requests
    - Validate document ID input
    - Call the Knowledge Embedding Service
    - Return embedding creation summary

This API DOES NOT:
    - Create chunks
    - Search FAISS
    - Perform BM25 retrieval
    - Extract engineering entities
    - Populate Neo4j
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.knowledge_embedding_service import knowledge_embedding_service


router = APIRouter(
    prefix="/knowledge-embeddings",
    tags=["Knowledge Embeddings"],
)


class KnowledgeEmbeddingRequest(BaseModel):
    """Request model for generating embeddings from knowledge chunks."""

    document_id: str


@router.post("/create")
def create_knowledge_embeddings(request: KnowledgeEmbeddingRequest):
    """
    Generate embeddings for all chunks belonging to a knowledge document.
    """

    try:
        return knowledge_embedding_service.create_embeddings(
            document_id=request.document_id,
        )

    except Exception as ex:
        raise HTTPException(
            status_code=400,
            detail=str(ex),
        )