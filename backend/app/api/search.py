from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.search_service import search_similar_chunks

router = APIRouter(prefix="/search", tags=["Search"])


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=3)
    top_k: int = Field(default=5, ge=1, le=20)


@router.post("")
def search_documents(request: SearchRequest) -> dict:
    return search_similar_chunks(
        query=request.query,
        top_k=request.top_k,
    )