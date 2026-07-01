def test_rag_endpoint(client):
    response = client.post(
        "/rag/answer",
        json={
            "query": "graph construction",
            "top_k": 3,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "confidence" in data
    assert "sources" in data