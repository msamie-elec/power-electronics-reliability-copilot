"""
===========================================================================
Power Electronics Reliability Copilot
Sprint 5.1 — Knowledge Document Pipeline API
===========================================================================

File:
    knowledge_documents.py

Purpose:
    Expose REST endpoints for the Knowledge Document Pipeline.

Why this file exists:
    This API provides access to the document registration service.
    It acts as the entry point for engineering documents entering the
    AI processing pipeline.

Responsibilities:
    - Receive document registration requests
    - Validate incoming requests
    - Invoke the Knowledge Document Pipeline Service
    - Return structured document metadata

This API DOES NOT:
    - Parse document contents directly
    - Generate chunks
    - Create embeddings
    - Populate Neo4j

Those tasks belong to downstream pipeline services.

Pipeline Position:

Approved Engineering PDF
        │
        ▼
Knowledge Document Pipeline API
        │
        ▼
Knowledge Document Service
        │
        ▼
Knowledge Chunk Service
        │
        ▼
Knowledge Embedding Service
        │
        ▼
Knowledge Extraction
        │
        ▼
Neo4j
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.knowledge_document_service import knowledge_document_service


router = APIRouter(
    prefix="/knowledge-documents",
    tags=["Knowledge Documents"],
)


class KnowledgeDocumentRegistrationRequest(BaseModel):
    """
    Request model for registering an approved evidence PDF.
    """

    file_path: str


@router.post("/register")
def register_knowledge_document(
    request: KnowledgeDocumentRegistrationRequest,
):
    """
    Register an approved engineering evidence document
    for the Knowledge Graph pipeline.

    Parameters
    ----------
    request:
        Contains the path of an approved engineering
        evidence PDF stored inside backend/knowledge_base.

    Returns
    -------
    dict
        Registered document metadata.
    """

    try:
        return knowledge_document_service.register_document(
            file_path=request.file_path,
        )

    except Exception as ex:
        raise HTTPException(
            status_code=400,
            detail=str(ex),
        )