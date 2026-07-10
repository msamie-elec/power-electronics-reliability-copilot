"""
==============================================================================
Power Electronics Reliability Copilot
Health Diagnostics Service

File
----
health_service.py

Purpose
-------
Provides lightweight and detailed runtime diagnostics for the backend API.

Responsibilities
----------------
- Report application status, version, environment and active providers.
- Validate configured infrastructure dependencies.
- Report dependency status without exposing sensitive values.
- Support production diagnostics and cloud validation workflows.

Security
--------
- Does not return API keys, connection strings, passwords or tokens.
- Does not include secret values in error responses.
- Returns sanitised dependency status only.

Version
-------
v0.6.0
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import time
from typing import Any, Callable

from azure.core.exceptions import AzureError
from azure.storage.blob import BlobServiceClient
from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError

from app.config import (
    app_config,
    neo4j_config,
    openai_config,
    provider_config,
    secret_config,
    storage_config,
)
from app.services.secrets.secret_service import secret_service


_SERVICE_STARTED_AT = time.perf_counter()


def resolve_secret(name: str, fallback_env: str | None = None) -> str:
    """
    Resolve a secret while remaining compatible with older SecretService
    signatures that do not yet support fallback_env.
    """
    try:
        return secret_service.get_secret(name, fallback_env=fallback_env)
    except TypeError:
        return secret_service.get_secret(name)


@dataclass(frozen=True)
class DependencyResult:
    """
    Sanitised dependency check result.
    """

    name: str
    status: str
    latency_ms: float
    details: str

    def to_dict(self) -> dict[str, Any]:
        """
        Return a JSON-serialisable representation of the check result.
        """
        return {
            "status": self.status,
            "latency_ms": self.latency_ms,
            "details": self.details,
        }


class HealthService:
    """
    Builds application health and diagnostics payloads.
    """

    def lightweight_health(self) -> dict[str, Any]:
        """
        Return a lightweight health response suitable for probes.
        """
        return {
            "status": "healthy",
            "service": app_config.name,
            "version": app_config.version,
            "environment": app_config.environment,
        }

    def detailed_health(self) -> dict[str, Any]:
        """
        Return detailed dependency diagnostics.
        """
        dependency_results = [
            self._check_secret_provider(),
            self._check_storage_provider(),
            self._check_ai_provider(),
            self._check_neo4j(),
        ]

        healthy_states = {"healthy", "configured", "skipped"}
        overall_status = (
            "healthy"
            if all(result.status in healthy_states for result in dependency_results)
            else "degraded"
        )

        return {
            "status": overall_status,
            "service": app_config.name,
            "version": app_config.version,
            "environment": app_config.environment,
            "timestamp_utc": datetime.now(UTC).isoformat(timespec="seconds"),
            "uptime_seconds": round(time.perf_counter() - _SERVICE_STARTED_AT, 2),
            "providers": {
                "ai": provider_config.ai_provider,
                "storage": provider_config.storage_provider,
                "secrets": provider_config.secret_provider,
                "graph": provider_config.graph_provider,
            },
            "dependencies": {
                result.name: result.to_dict() for result in dependency_results
            },
        }

    def _run_check(
        self,
        name: str,
        check: Callable[[], str],
        error_detail: str,
    ) -> DependencyResult:
        """
        Execute a dependency check and return a sanitised result.
        """
        started_at = time.perf_counter()

        try:
            details = check()
            status = "healthy"
        except Exception:
            details = error_detail
            status = "unhealthy"

        latency_ms = round((time.perf_counter() - started_at) * 1000, 2)

        return DependencyResult(
            name=name,
            status=status,
            latency_ms=latency_ms,
            details=details,
        )

    def _check_secret_provider(self) -> DependencyResult:
        """
        Validate that the configured secret provider can resolve a required
        application secret.
        """

        def check() -> str:
            if secret_config.use_azure_key_vault:
                resolve_secret(
                    "azure-openai-api-key",
                    fallback_env="AZURE_OPENAI_API_KEY",
                )
                return "Azure Key Vault reachable. Required secret resolved."

            return "Local secret provider configured."

        return self._run_check(
            name="keyVault",
            check=check,
            error_detail="Secret provider check failed. Verify Key Vault access and required secrets.",
        )

    def _check_storage_provider(self) -> DependencyResult:
        """
        Validate the configured document storage provider.
        """

        def check() -> str:
            if storage_config.use_azure_blob_storage:
                connection_string = resolve_secret(
                    "azure-storage-connection-string",
                    fallback_env="AZURE_STORAGE_CONNECTION_STRING",
                )

                if not storage_config.azure_blob_container_name:
                    raise ValueError("Azure Blob container name is not configured.")

                client = BlobServiceClient.from_connection_string(
                    connection_string,
                    connection_timeout=10,
                    read_timeout=10,
                )

                # Account information is a lightweight service-level validation.
                client.get_account_information(timeout=10)

                container_client = client.get_container_client(
                    storage_config.azure_blob_container_name
                )

                if not container_client.exists(timeout=10):
                    raise RuntimeError("Azure Blob container is not available.")

                return "Azure Blob account and container reachable."

            storage_config.upload_dir.mkdir(parents=True, exist_ok=True)
            return "Local storage directory reachable."

        result = self._run_check(
            name="blob",
            check=check,
            error_detail=(
                "Azure Blob check failed. Verify the storage account exists, "
                "the container exists, and the Key Vault connection string is current."
            ),
        )

        # Preserve the original Azure error category without exposing secrets.
        if result.status == "unhealthy":
            return result

        return result

    def _check_ai_provider(self) -> DependencyResult:
        """
        Validate AI provider configuration and credentials.
        """

        def check() -> str:
            if openai_config.use_azure_openai:
                if not openai_config.azure_endpoint:
                    raise ValueError("Azure OpenAI endpoint is not configured.")
                if not openai_config.azure_chat_deployment:
                    raise ValueError("Azure OpenAI chat deployment is not configured.")

                resolve_secret(
                    "azure-openai-api-key",
                    fallback_env="AZURE_OPENAI_API_KEY",
                )
                return "Azure OpenAI configuration and credential resolved."

            resolve_secret("openai-api-key", fallback_env="OPENAI_API_KEY")
            return "OpenAI configuration and credential resolved."

        result = self._run_check(
            name="openai",
            check=check,
            error_detail="AI provider configuration or credential check failed.",
        )

        if result.status == "healthy":
            return DependencyResult(
                name=result.name,
                status="configured",
                latency_ms=result.latency_ms,
                details=result.details,
            )

        return result

    def _check_neo4j(self) -> DependencyResult:
        """
        Validate Neo4j connectivity using a lightweight query.
        """

        def check() -> str:
            if not neo4j_config.uri or not neo4j_config.username:
                raise ValueError("Neo4j URI or username is not configured.")

            password = resolve_secret(
                "neo4j-password",
                fallback_env="NEO4J_PASSWORD",
            )

            driver = GraphDatabase.driver(
                neo4j_config.uri,
                auth=(neo4j_config.username, password),
            )

            try:
                with driver.session(database=neo4j_config.database) as session:
                    result = session.run("RETURN 1 AS result")
                    record = result.single()

                    if not record or record["result"] != 1:
                        raise RuntimeError("Neo4j validation query failed.")

                return "Neo4j reachable. Validation query succeeded."
            finally:
                driver.close()

        return self._run_check(
            name="neo4j",
            check=check,
            error_detail="Neo4j check failed. Verify URI, username, password and database name.",
        )


health_service = HealthService()
