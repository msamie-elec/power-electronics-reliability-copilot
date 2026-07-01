from fastapi import APIRouter, HTTPException

from app.services.neo4j_service import test_neo4j_connection

router = APIRouter(prefix="/graph", tags=["Graph"])


@router.get("/health")
def graph_health_check() -> dict:
    try:
        return test_neo4j_connection()
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Neo4j connection failed: {error}",
        )