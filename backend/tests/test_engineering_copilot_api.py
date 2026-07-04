"""
Integration tests for Sprint 5.12 Engineering Copilot API.

Covered endpoint:

POST /engineering-copilot/ask

Security note:
Do not print response.json(), environment variables, API keys,
Neo4j credentials, OpenAI keys, or raw exception output in these tests.

The LLM call is mocked so these tests do not use OpenAI credits.
"""

from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


TEST_DOCUMENT_ID = "DOC-B3198A5"
MISSING_DOCUMENT_ID = "DOC-UNKNOWN123"
TEST_QUESTION = "Why does VCE(sat) increase during power cycling?"
MOCK_ANSWER = """
1. Engineering Answer
The increase in VCE(sat) may be associated with degradation mechanisms in the IGBT module.

2. Supporting Document Evidence
The answer is based on retrieved semantic evidence.

3. Supporting Graph Reasoning
The answer is supported by graph relationships.

4. Confidence Level
Medium.

5. Recommended Next Step
Inspect the module for bond wire and thermal cycling related degradation.
"""


client = TestClient(app)


@patch("app.services.engineering_answer_service.generate_evidence_backed_answer")
def test_engineering_copilot_ask_success(mock_generate_answer):
    mock_generate_answer.return_value = MOCK_ANSWER

    response = client.post(
        "/engineering-copilot/ask",
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
    assert data["answer"] == MOCK_ANSWER

    assert "semanticEvidence" in data
    assert "graphEvidence" in data
    assert "reasoningContext" in data

    assert isinstance(data["semanticEvidence"], list)
    assert isinstance(data["graphEvidence"], dict)

    assert mock_generate_answer.called is True


@patch("app.services.engineering_answer_service.generate_evidence_backed_answer")
def test_engineering_copilot_response_contains_evidence(mock_generate_answer):
    mock_generate_answer.return_value = MOCK_ANSWER

    response = client.post(
        "/engineering-copilot/ask",
        json={
            "document_id": TEST_DOCUMENT_ID,
            "question": TEST_QUESTION,
            "top_k": 3,
            "graph_limit": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["semanticEvidence"]) >= 1
    assert "entities" in data["graphEvidence"]
    assert "relationships" in data["graphEvidence"]
    assert data["reasoningContext"]["readyForLLM"] is True


@patch("app.services.engineering_answer_service.generate_evidence_backed_answer")
def test_engineering_copilot_respects_top_k(mock_generate_answer):
    mock_generate_answer.return_value = MOCK_ANSWER

    response = client.post(
        "/engineering-copilot/ask",
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


def test_engineering_copilot_missing_document_returns_404():
    response = client.post(
        "/engineering-copilot/ask",
        json={
            "document_id": MISSING_DOCUMENT_ID,
            "question": TEST_QUESTION,
            "top_k": 5,
            "graph_limit": 10,
        },
    )

    assert response.status_code == 404


def test_engineering_copilot_empty_question_rejected():
    response = client.post(
        "/engineering-copilot/ask",
        json={
            "document_id": TEST_DOCUMENT_ID,
            "question": "",
            "top_k": 5,
            "graph_limit": 10,
        },
    )

    assert response.status_code == 422