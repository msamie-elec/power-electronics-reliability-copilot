"""
===========================================================================
Power Electronics Reliability Copilot
Sprint 5.9B — Neo4j Graph Population API
===========================================================================

Purpose:
    Expose a FastAPI endpoint for populating the Neo4j engineering knowledge
    graph from graph-ready JSON files produced by Sprint 5.8B.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.neo4j_population_service import neo4j_population_service


router = APIRouter(
    prefix="/knowledge-graph",
    tags=["Knowledge Graph Population"],
)


class GraphPopulationRequest(BaseModel):
    """Request model for populating Neo4j from extracted knowledge JSON."""

    document_id: str


@router.post("/populate")
def populate_knowledge_graph(request: GraphPopulationRequest):
    """Populate Neo4j from a graph-ready JSON file."""

    try:
        return neo4j_population_service.populate_from_document(
            document_id=request.document_id,
        )

    except FileNotFoundError as ex:
        raise HTTPException(
            status_code=404,
            detail=str(ex),
        )

    except Exception as ex:
        raise HTTPException(
            status_code=400,
            detail=str(ex),
        )