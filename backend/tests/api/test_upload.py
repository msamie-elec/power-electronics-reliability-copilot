"""
==============================================================================
Power Electronics Reliability Copilot
Upload API Tests

File
----
test_upload.py

Purpose
-------
Tests the upload endpoint using isolated local test storage.

Security
--------
- Does not call Azure Blob Storage.
- Does not use live credentials.
- Does not print secrets.

Version
-------
v0.6.0
==============================================================================
"""

from app.services.document_storage_service import document_storage_service


def test_upload_endpoint(client, tmp_path, monkeypatch):
    monkeypatch.setattr(
        document_storage_service,
        "_get_provider",
        lambda: document_storage_service._local_provider,
    )

    sample_file = tmp_path / "Graph.txt"
    sample_file.write_text(
        "This is a test engineering document for upload validation.",
        encoding="utf-8",
    )

    with sample_file.open("rb") as file:
        response = client.post(
            "/upload",
            files={
                "files": (
                    "Graph.txt",
                    file,
                    "text/plain",
                )
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert "uploaded_files" in data
    assert len(data["uploaded_files"]) == 1
    assert data["uploaded_files"][0]["filename"] == "Graph.txt"