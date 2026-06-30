from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.rag_service import answer_question_with_retrieval

router = APIRouter(prefix="/rag", tags=["RAG"])


class RagRequest(BaseModel):
    query: str = Field(..., min_length=3)
    top_k: int = Field(default=5, ge=1, le=10)


@router.post("/answer")
def answer_question(request: RagRequest) -> dict:
    return answer_question_with_retrieval(
        query=request.query,
        top_k=request.top_k,
    )