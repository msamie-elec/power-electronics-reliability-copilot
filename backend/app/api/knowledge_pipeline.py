"""
===========================================================================
Power Electronics Reliability Copilot
Sprint 5.7 — Knowledge Pipeline Orchestrator API
===========================================================================

Purpose:
    Expose one endpoint for running the complete knowledge ingestion pipeline.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.knowledge_pipeline_service import knowledge_pipeline_service


router = APIRouter(
    prefix="/knowledge-pipeline",
    tags=["Knowledge Pipeline"],
)


class KnowledgePipelineRequest(BaseModel):
    """Request model for running the full knowledge pipeline."""

    file_path: str


@router.post("/run")
def run_knowledge_pipeline(request: KnowledgePipelineRequest):
    """Run register, chunk, embedding and FAISS indexing in one operation."""

    try:
        return knowledge_pipeline_service.run_pipeline(
            file_path=request.file_path,
        )

    except Exception as ex:
        raise HTTPException(
            status_code=400,
            detail=str(ex),
        )