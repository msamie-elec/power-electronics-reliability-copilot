"""
Integration tests for Sprint 5.11 Evidence-backed AI Reasoning API.

Covered endpoint:

POST /evidence-reasoning/context

Security note:
Do not print response.json(), environment variables, API keys,
Neo4j credentials, OpenAI keys, or raw exception output in these tests.
"""

from fastapi.testclient import TestClient

from app.main import app


TEST_DOCUMENT_ID = "DOC-B3198A5"
MISSING_DOCUMENT_ID = "DOC-UNKNOWN123"
TEST_QUESTION = "Why does VCE(sat) increase during power cycling?"


client = TestClient(app)


def test_build_reasoning_context_success():
    response = client.post(
        "/evidence-reasoning/context",
        json={
            "document_id": TEST_DOCUMENT_ID,
            "question": TEST_QUESTION,
            "top_k": 5,
            "graph_limit": 10,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["documentId"] == TEST_DOCUMENT_ID
    assert data["question"] == TEST_QUESTION

    assert "semanticEvidence" in data
    assert "graphEvidence" in data
    assert "reasoningContext" in data

    assert isinstance(data["semanticEvidence"], list)
    assert isinstance(data["graphEvidence"], dict)

    assert "entities" in data["graphEvidence"]
    assert "relationships" in data["graphEvidence"]

    assert data["reasoningContext"]["readyForLLM"] is True
    assert data["reasoningContext"]["semanticEvidenceCount"] >= 1


def test_build_reasoning_context_respects_top_k():
    response = client.post(
        "/evidence-reasoning/context",
        json={
            "document_id": TEST_DOCUMENT_ID,
            "question": TEST_QUESTION,
            "top_k": 2,
            "graph_limit": 10,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["semanticEvidence"]) <= 2
    assert data["reasoningContext"]["semanticEvidenceCount"] <= 2


def test_build_reasoning_context_respects_graph_limit():
    response = client.post(
        "/evidence-reasoning/context",
        json={
            "document_id": TEST_DOCUMENT_ID,
            "question": TEST_QUESTION,
            "top_k": 5,
            "graph_limit": 3,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["reasoningContext"]["graphEntityCount"] <= 3
    assert data["reasoningContext"]["graphRelationshipCount"] <= 3


def test_missing_document_returns_404():
    response = client.post(
        "/evidence-reasoning/context",
        json={
            "document_id": MISSING_DOCUMENT_ID,
            "question": TEST_QUESTION,
            "top_k": 5,
            "graph_limit": 10,
        },
    )

    assert response.status_code == 404


def test_empty_question_rejected():
    response = client.post(
        "/evidence-reasoning/context",
        json={
            "document_id": TEST_DOCUMENT_ID,
            "question": "",
            "top_k": 5,
            "graph_limit": 10,
        },
    )

    assert response.status_code in [400, 422]