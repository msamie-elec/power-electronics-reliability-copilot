"""
Power Electronics Reliability Copilot
Documents API

Exposes document registry endpoints used by the frontend workspace.
The API layer remains thin and delegates document registry construction
to the Document Registry Service.
"""

from fastapi import APIRouter

from app.services.document_registry_service import document_registry_service

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get("")
def list_documents() -> dict:
    return {
        "documents": document_registry_service.list_documents()
    }