"""
===========================================================================
Power Electronics Reliability Copilot
Sprint 5.10 — Knowledge Graph Retrieval API
===========================================================================

Purpose:
    Expose read-only Neo4j retrieval operations for graph-aware engineering
    search, inspection and future GraphRAG.
"""

from fastapi import APIRouter, HTTPException, Query

from app.services.graph_retrieval_service import graph_retrieval_service


router = APIRouter(
    prefix="/knowledge-graph",
    tags=["Knowledge Graph Retrieval"],
)


@router.get("/entity/{name}")
def get_entity(name: str):
    entity = graph_retrieval_service.get_entity(name)

    if not entity:
        raise HTTPException(
            status_code=404,
            detail=f"Entity not found: {name}",
        )

    return {
        "status": "success",
        "entity": entity,
    }


@router.get("/search")
def search_entities(
    q: str = Query(..., description="Search text"),
    limit: int = Query(10, ge=1, le=50),
):
    return {
        "status": "success",
        "query": q,
        "results": graph_retrieval_service.search_entities(
            search_text=q,
            limit=limit,
        ),
    }


@router.get("/entity/{name}/neighbors")
def get_neighbors(
    name: str,
    limit: int = Query(25, ge=1, le=100),
):
    entity = graph_retrieval_service.get_entity(name)

    if not entity:
        raise HTTPException(
            status_code=404,
            detail=f"Entity not found: {name}",
        )

    return {
        "status": "success",
        "entity": name,
        "neighbors": graph_retrieval_service.get_neighbors(
            name=name,
            limit=limit,
        ),
    }


@router.get("/relationships")
def get_relationships(
    source: str | None = None,
    relation: str | None = None,
    target: str | None = None,
    limit: int = Query(25, ge=1, le=100),
):
    return {
        "status": "success",
        "filters": {
            "source": source,
            "relation": relation,
            "target": target,
        },
        "relationships": graph_retrieval_service.get_relationships(
            source=source,
            relation=relation,
            target=target,
            limit=limit,
        ),
    }


@router.get("/entity/{name}/evidence")
def get_entity_evidence(name: str):
    evidence = graph_retrieval_service.get_entity_evidence(name)

    if not evidence:
        raise HTTPException(
            status_code=404,
            detail=f"Entity not found: {name}",
        )

    return {
        "status": "success",
        "evidence": evidence,
    }