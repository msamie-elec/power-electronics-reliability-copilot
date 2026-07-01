from pathlib import Path


def test_upload_endpoint(client):
    sample_file = Path("documents/Graph.txt")

    with sample_file.open("rb") as f:
        response = client.post(
            "/upload",
            files={
                "files": (
                    "Graph.txt",
                    f,
                    "text/plain",
                )
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert "uploaded_files" in data