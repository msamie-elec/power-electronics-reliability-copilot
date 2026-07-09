"""
==============================================================================
Power Electronics Reliability Copilot
Local Storage Provider

File
----
local_storage_provider.py

Purpose
-------
Stores uploaded engineering documents on the local filesystem for development
and local testing.

Security
--------
- Does not store secrets.
- Does not print credentials.
- Uses configured local upload directory.

Version
-------
v0.6.1
==============================================================================
"""

from datetime import datetime
import shutil
from typing import Any

from fastapi import UploadFile

from app.config import storage_config
from app.services.storage.base_storage_provider import BaseStorageProvider


class LocalStorageProvider(BaseStorageProvider):
    """
    Local filesystem implementation of the document storage provider.
    """

    def save_uploaded_file(self, file: UploadFile) -> dict[str, Any]:
        storage_config.upload_dir.mkdir(parents=True, exist_ok=True)

        filename = file.filename or "uploaded_document"
        destination = storage_config.upload_dir / filename

        file.file.seek(0)

        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "filename": filename,
            "size_bytes": destination.stat().st_size,
            "uploaded_at": datetime.fromtimestamp(
                destination.stat().st_mtime
            ).isoformat(timespec="seconds"),
            "storage_backend": "local",
            "local_processing_path": str(destination),
        }

    def list_documents(self) -> list[dict[str, Any]]:
        storage_config.upload_dir.mkdir(parents=True, exist_ok=True)

        documents: list[dict[str, Any]] = []

        for path in storage_config.upload_dir.iterdir():
            if path.is_file() and path.name != ".gitkeep":
                documents.append(
                    {
                        "filename": path.name,
                        "size_bytes": path.stat().st_size,
                        "uploaded_at": datetime.fromtimestamp(
                            path.stat().st_mtime
                        ).isoformat(timespec="seconds"),
                        "storage_backend": "local",
                    }
                )

        return documents