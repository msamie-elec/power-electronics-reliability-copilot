from fastapi import APIRouter

from app.services.file_service import list_uploaded_documents

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get("")
def list_documents() -> dict:
    return {"documents": list_uploaded_documents()}