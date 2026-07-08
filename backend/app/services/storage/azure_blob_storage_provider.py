"""
Power Electronics Reliability Copilot
Azure Blob Storage Provider
"""

from typing import Any

from fastapi import UploadFile

from app.config import storage_config
from app.services.storage.base_storage_provider import BaseStorageProvider


class AzureBlobStorageProvider(BaseStorageProvider):
    def save_uploaded_file(self, file: UploadFile) -> dict[str, Any]:
        from azure.storage.blob import BlobServiceClient

        filename = file.filename or "uploaded_document"

        blob_service_client = BlobServiceClient.from_connection_string(
            storage_config.azure_storage_connection_string
        )

        container_client = blob_service_client.get_container_client(
            storage_config.azure_blob_container_name
        )

        try:
            container_client.create_container()
        except Exception:
            pass

        blob_client = container_client.get_blob_client(filename)
        blob_client.upload_blob(file.file, overwrite=True)

        properties = blob_client.get_blob_properties()

        return {
            "filename": filename,
            "size_bytes": properties.size,
            "uploaded_at": properties.last_modified.isoformat()
            if properties.last_modified
            else None,
            "storage_backend": "azure_blob",
        }

    def list_documents(self) -> list[dict[str, Any]]:
        from azure.storage.blob import BlobServiceClient

        blob_service_client = BlobServiceClient.from_connection_string(
            storage_config.azure_storage_connection_string
        )

        container_client = blob_service_client.get_container_client(
            storage_config.azure_blob_container_name
        )

        documents: list[dict[str, Any]] = []

        try:
            blobs = container_client.list_blobs()
        except Exception:
            return documents

        for blob in blobs:
            documents.append(
                {
                    "filename": blob.name,
                    "size_bytes": blob.size,
                    "uploaded_at": blob.last_modified.isoformat()
                    if blob.last_modified
                    else None,
                    "storage_backend": "azure_blob",
                }
            )

        return documents