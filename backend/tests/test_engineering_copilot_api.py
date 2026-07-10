"""
Integration tests for Engineering Copilot API.

Security note:
These tests do not call live LLM providers and must not print secrets,
environment variables, API keys, connection strings, or credentials.
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

MOCK_ENGINEERING_RESULT = {
    "answer": MOCK_ANSWER,
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
}


client = TestClient(app)


@patch("app.api.engineering_copilot.engineering_answer_service.answer_question")
def test_engineering_copilot_ask_success(mock_answer_question):
    mock_answer_question.return_value = MOCK_ENGINEERING_RESULT

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

    assert mock_answer_question.called is True


@patch("app.api.engineering_copilot.engineering_answer_service.answer_question")
def test_engineering_copilot_response_contains_evidence(mock_answer_question):
    mock_answer_question.return_value = MOCK_ENGINEERING_RESULT

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


@patch("app.api.engineering_copilot.engineering_answer_service.answer_question")
def test_engineering_copilot_respects_top_k(mock_answer_question):
    mock_answer_question.return_value = {
        **MOCK_ENGINEERING_RESULT,
        "semanticEvidence": MOCK_ENGINEERING_RESULT["semanticEvidence"][:1],
    }

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