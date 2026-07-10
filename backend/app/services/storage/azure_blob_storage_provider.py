"""
==============================================================================
Power Electronics Reliability Copilot
Azure Blob Storage Provider

File
----
azure_blob_storage_provider.py

Purpose
-------
Stores uploaded engineering documents in Azure Blob Storage while also keeping
a local processing copy for the document ingestion pipeline.

Responsibilities
----------------
- Save uploaded files to the configured Azure Blob container.
- Save a local processing copy under the configured upload directory.
- List documents stored in Azure Blob Storage.
- Return storage metadata without exposing credentials.

Security
--------
- Does not print storage keys, connection strings, SAS tokens or credentials.
- Reads Azure configuration from environment-backed application config.
- Handles storage errors without exposing secret values.

Version
-------
v0.6.1
==============================================================================
"""

from datetime import datetime
from io import BytesIO
import logging
from typing import Any

from azure.core.exceptions import AzureError, ResourceExistsError
from azure.storage.blob import BlobServiceClient, ContentSettings
from fastapi import UploadFile

from app.config import storage_config
from app.services.secrets.secret_service import secret_service
from app.services.storage.base_storage_provider import BaseStorageProvider


logger = logging.getLogger(__name__)


class AzureBlobStorageProvider(BaseStorageProvider):
    """
    Azure Blob Storage implementation of the document storage provider.
    """

    def save_uploaded_file(self, file: UploadFile) -> dict[str, Any]:
        """
        Save an uploaded file to Azure Blob Storage and keep a local processing
        copy so downstream parsing, chunking, embedding and FAISS indexing can
        operate normally.
        """
        filename = file.filename or "uploaded_document"

        storage_config.upload_dir.mkdir(parents=True, exist_ok=True)
        local_path = storage_config.upload_dir / filename

        content = file.file.read()

        local_path.write_bytes(content)

        connection_string = self._get_connection_string()

        blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )

        container_client = blob_service_client.get_container_client(
            storage_config.azure_blob_container_name
        )

        try:
            container_client.create_container()
        except ResourceExistsError:
            pass

        blob_client = container_client.get_blob_client(filename)

        blob_client.upload_blob(
            BytesIO(content),
            overwrite=True,
            content_settings=ContentSettings(
                content_type=file.content_type or "application/octet-stream"
            ),
        )

        properties = blob_client.get_blob_properties()

        return {
            "filename": filename,
            "size_bytes": properties.size,
            "uploaded_at": properties.last_modified.isoformat()
            if properties.last_modified
            else datetime.now().isoformat(timespec="seconds"),
            "storage_backend": "azure_blob",
            "local_processing_path": str(local_path),
        }

    def list_documents(self) -> list[dict[str, Any]]:
        """
        List documents stored in the configured Azure Blob container.
        """
        documents: list[dict[str, Any]] = []

        try:
            connection_string = self._get_connection_string()

            blob_service_client = BlobServiceClient.from_connection_string(
                connection_string
            )

            container_client = blob_service_client.get_container_client(
                storage_config.azure_blob_container_name
            )

            for blob in container_client.list_blobs():
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

        except AzureError:
            logger.exception("Azure Blob document listing failed.")
            return []

        return documents
    @staticmethod
    def _get_connection_string() -> str:
        """
        Retrieve the Azure Storage connection string through the secret service.
        """
        try:
            return secret_service.get_secret(
                "azure-storage-connection-string",
                fallback_env="AZURE_STORAGE_CONNECTION_STRING",
            )
        except KeyError as exc:
            raise ValueError(
                "AZURE_STORAGE_CONNECTION_STRING must be configured when "
                "DOCUMENT_STORAGE_PROVIDER=azure_blob."
            ) from exc
