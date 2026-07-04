"""
===========================================================================
Power Electronics Reliability Copilot
Sprint 5.11 — Evidence-backed AI Reasoning API
===========================================================================
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field, field_validator

from app.services.evidence_reasoning_service import evidence_reasoning_service


router = APIRouter(
    prefix="/evidence-reasoning",
    tags=["Evidence-backed AI Reasoning"],
)


class ReasoningContextRequest(BaseModel):
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

@router.post("/context")
def build_reasoning_context(request: ReasoningContextRequest):
    try:
        return evidence_reasoning_service.build_reasoning_context(
            document_id=request.document_id,
            question=request.question,
            top_k=request.top_k,
            graph_limit=request.graph_limit,
        )

    except FileNotFoundError as ex:
        raise HTTPException(
            status_code=404,
            detail=str(ex),
        )

    except Exception as ex:
        raise HTTPException(
            status_code=500,
            detail=str(ex),
        )