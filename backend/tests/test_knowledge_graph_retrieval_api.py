"""
Integration tests for Sprint 5.10 Knowledge Graph Retrieval API.

Covered endpoints:

GET /knowledge-graph/summary
GET /knowledge-graph/entity/IGBT Module
GET /knowledge-graph/search?q=IGBT
GET /knowledge-graph/entity/IGBT Module/neighbors
GET /knowledge-graph/relationships
GET /knowledge-graph/relationships?relation=INCLUDES
GET /knowledge-graph/relationships?source=IGBT Module
GET /knowledge-graph/entity/IGBT Module/evidence

Negative tests:

GET /knowledge-graph/entity/UnknownEntity123 -> 404
GET /knowledge-graph/entity/UnknownEntity123/evidence -> 404
"""

# Security note:
# Do not print response.json(), environment variables, API keys,
# Neo4j credentials, or raw exception output in these tests.

from fastapi.testclient import TestClient

from app.main import app


TEST_ENTITY_NAME = "IGBT Module"
UNKNOWN_ENTITY_NAME = "UnknownEntity123"
TEST_SEARCH_QUERY = "IGBT"
TEST_RELATIONSHIP_TYPE = "INCLUDES"


client = TestClient(app)


def test_graph_summary_endpoint():
    response = client.get("/knowledge-graph/summary")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert "summary" in data
    assert data["summary"]["totalNodes"] > 0
    assert data["summary"]["totalRelationships"] > 0
    assert "nodeLabels" in data["summary"]
    assert "relationshipTypes" in data["summary"]


def test_get_existing_entity():
    response = client.get(f"/knowledge-graph/entity/{TEST_ENTITY_NAME}")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert "entity" in data
    assert "properties" in data["entity"]

    properties = data["entity"]["properties"]

    assert properties.get("name") == TEST_ENTITY_NAME


def test_get_missing_entity_returns_404():
    response = client.get(f"/knowledge-graph/entity/{UNKNOWN_ENTITY_NAME}")

    assert response.status_code == 404


def test_search_entities():
    response = client.get(
        "/knowledge-graph/search",
        params={"q": TEST_SEARCH_QUERY, "limit": 10},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["query"] == TEST_SEARCH_QUERY
    assert isinstance(data["results"], list)
    assert len(data["results"]) >= 1


def test_get_neighbors_for_existing_entity():
    response = client.get(
        f"/knowledge-graph/entity/{TEST_ENTITY_NAME}/neighbors",
        params={"limit": 25},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["entity"] == TEST_ENTITY_NAME
    assert isinstance(data["neighbors"], list)
    assert len(data["neighbors"]) >= 1


def test_get_all_relationships():
    response = client.get(
        "/knowledge-graph/relationships",
        params={"limit": 25},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert isinstance(data["relationships"], list)
    assert len(data["relationships"]) >= 1


def test_get_relationships_by_type():
    response = client.get(
        "/knowledge-graph/relationships",
        params={"relation": TEST_RELATIONSHIP_TYPE, "limit": 25},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert isinstance(data["relationships"], list)
    assert len(data["relationships"]) >= 1

    for relationship in data["relationships"]:
        assert relationship["relationshipType"] == TEST_RELATIONSHIP_TYPE


def test_get_relationships_by_source():
    response = client.get(
        "/knowledge-graph/relationships",
        params={"source": TEST_ENTITY_NAME, "limit": 25},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert isinstance(data["relationships"], list)
    assert len(data["relationships"]) >= 1


def test_get_entity_evidence():
    response = client.get(f"/knowledge-graph/entity/{TEST_ENTITY_NAME}/evidence")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert "evidence" in data
    assert "sourceDocuments" in data["evidence"]
    assert "evidenceChunkIds" in data["evidence"]


def test_get_missing_entity_evidence_returns_404():
    response = client.get(f"/knowledge-graph/entity/{UNKNOWN_ENTITY_NAME}/evidence")

    assert response.status_code == 404