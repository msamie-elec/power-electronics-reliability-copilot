from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator

from app.services.engineering_answer_service import engineering_answer_service


router = APIRouter(
    prefix="/engineering-copilot",
    tags=["Engineering Copilot"],
)


class EngineeringCopilotRequest(BaseModel):
    document_id: str = Field(..., description="Knowledge document ID")
    question: str = Field(..., description="Engineering question")
    top_k: int = Field(5, ge=1, le=20)
    graph_limit: int = Field(10, ge=1, le=50)

    @field_validator("question")
    @classmethod
    def question_must_not_be_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("question must not be empty")
        return value.strip()


@router.post("/ask")
def ask_engineering_copilot(request: EngineeringCopilotRequest):
    try:
        return engineering_answer_service.answer_question(
            document_id=request.document_id,
            question=request.question,
            top_k=request.top_k,
            graph_limit=request.graph_limit,
        )

    except FileNotFoundError as ex:
        raise HTTPException(status_code=404, detail=str(ex))

    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))