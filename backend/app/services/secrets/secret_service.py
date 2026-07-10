"""
==============================================================================
Power Electronics Reliability Copilot
Secret Service

File
----
secret_service.py

Purpose
-------
Provides a single application-wide entry point for retrieving secrets.

The Secret Service selects the appropriate secret provider based on the active
application configuration. Application services should always obtain secrets
through this service rather than accessing environment variables or Azure Key
Vault directly.

Responsibilities
----------------
- Select the active secret provider.
- Delegate secret retrieval to the configured provider.
- Keep application services independent from secret storage technology.
- Support both local development and Azure deployments.

Security
--------
- Does not store secrets.
- Does not cache secrets.
- Does not expose secret values.
- Does not log sensitive information.

Version
-------
v0.6.0
==============================================================================
"""

import os

from app.config import AZURE_KEY_VAULT_NAME, SECRET_PROVIDER
from app.services.secrets.azure_keyvault_secret_provider import (
    AzureKeyVaultSecretProvider,
)
from app.services.secrets.base_secret_provider import BaseSecretProvider
from app.services.secrets.local_secret_provider import LocalSecretProvider


class SecretService:
    """
    Provides application-wide secret retrieval.
    """

    def __init__(self) -> None:
        self._provider = self._create_provider()

    _LOCAL_ENV_ALIASES: dict[str, str] = {
        "openai-api-key": "OPENAI_API_KEY",
        "azure-openai-api-key": "AZURE_OPENAI_API_KEY",
        "azure-storage-connection-string": "AZURE_STORAGE_CONNECTION_STRING",
        "neo4j-password": "NEO4J_PASSWORD",
    }

    def get_secret(self, name: str, fallback_env: str | None = None) -> str:
        """
        Retrieve a secret from the active provider.

        Args:
            name: Provider-native secret name. For Azure Key Vault, use
                Azure-safe names such as ``azure-openai-api-key``.
            fallback_env: Optional local environment variable name used when
                the active provider cannot return the secret.

        Returns:
            Secret value as a string.

        Raises:
            KeyError: If the secret cannot be resolved.
        """
        try:
            return self._provider.get_secret(name)
        except (KeyError, RuntimeError):
            env_name = fallback_env or self._LOCAL_ENV_ALIASES.get(name)

            if env_name:
                fallback_value = os.getenv(env_name, "")

                if fallback_value:
                    return fallback_value

            raise

    @staticmethod
    def _create_provider() -> BaseSecretProvider:
        """
        Create the configured secret provider.
        """
        provider = SECRET_PROVIDER.lower().strip()

        if provider == "azure_key_vault":
            return AzureKeyVaultSecretProvider(
                key_vault_name=AZURE_KEY_VAULT_NAME,
            )

        return LocalSecretProvider()


secret_service = SecretService()