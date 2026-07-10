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

    def get_secret(self, name: str) -> str:
        """
        Retrieve a secret from the active provider.
        """
        return self._provider.get_secret(name)

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