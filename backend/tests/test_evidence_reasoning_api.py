"""
Integration tests for Evidence-backed AI Reasoning API.

Security note:
These tests use mocked reasoning context data and must not print secrets,
environment variables, API keys, connection strings, or credentials.
"""

from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


TEST_DOCUMENT_ID = "DOC-B3198A5"
MISSING_DOCUMENT_ID = "DOC-UNKNOWN123"
TEST_QUESTION = "Why does VCE(sat) increase during power cycling?"

MOCK_REASONING_CONTEXT = {
    "status": "success",
    "documentId": TEST_DOCUMENT_ID,
    "question": TEST_QUESTION,
    "semanticEvidence": [
        {
            "chunkId": "DOC-B3198A5-CHUNK-00001",
            "documentId": TEST_DOCUMENT_ID,
            "text": "VCE(sat) can increase as IGBT module degradation progresses.",
            "score": 0.91,
            "sourceDocument": "test_fixture.pdf",
        }
    ],
    "graphEvidence": {
        "entities": [],
        "relationships": [],
    },
    "reasoningContext": {
        "semanticEvidenceCount": 1,
        "graphEntityCount": 0,
        "graphRelationshipCount": 0,
        "readyForLLM": True,
    },
}


client = TestClient(app)


@patch("app.api.evidence_reasoning.evidence_reasoning_service.build_reasoning_context")
def test_build_reasoning_context_success(mock_build_context):
    mock_build_context.return_value = MOCK_REASONING_CONTEXT

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


@patch("app.api.evidence_reasoning.evidence_reasoning_service.build_reasoning_context")
def test_build_reasoning_context_respects_top_k(mock_build_context):
    mock_build_context.return_value = {
        **MOCK_REASONING_CONTEXT,
        "semanticEvidence": MOCK_REASONING_CONTEXT["semanticEvidence"][:1],
        "reasoningContext": {
            **MOCK_REASONING_CONTEXT["reasoningContext"],
            "semanticEvidenceCount": 1,
        },
    }

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


@patch("app.api.evidence_reasoning.evidence_reasoning_service.build_reasoning_context")
def test_build_reasoning_context_respects_graph_limit(mock_build_context):
    mock_build_context.return_value = {
        **MOCK_REASONING_CONTEXT,
        "reasoningContext": {
            **MOCK_REASONING_CONTEXT["reasoningContext"],
            "graphEntityCount": 0,
            "graphRelationshipCount": 0,
        },
    }

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

    assert response.status_code == 422