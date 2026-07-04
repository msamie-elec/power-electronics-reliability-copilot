"""
===========================================================================
Power Electronics Reliability Copilot
Sprint 5.9 — Graph Validation API
===========================================================================
"""

from fastapi import APIRouter, HTTPException

from app.services.graph_validation_service import graph_validation_service


router = APIRouter(
    prefix="/knowledge-graph",
    tags=["Knowledge Graph Validation"],
)


@router.get("/summary")
def graph_summary():

    try:

        return {
            "status": "success",
            "summary": graph_validation_service.get_graph_summary()
        }

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex)
        )