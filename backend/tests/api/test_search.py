def test_search_endpoint(client):
    response = client.post(
        "/search",
        json={
            "query": "graph",
            "top_k": 3,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "results" in data
    assert "query" in data