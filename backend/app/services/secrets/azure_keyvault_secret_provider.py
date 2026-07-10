"""
==============================================================================
Power Electronics Reliability Copilot
Azure Key Vault Secret Provider

File
----
azure_keyvault_secret_provider.py

Purpose
-------
Provides Azure Key Vault backed secret retrieval for cloud environments.

This provider isolates Azure Key Vault access behind the common secret provider
interface so application services do not depend directly on Azure SDK calls.

Responsibilities
----------------
- Retrieve secrets from Azure Key Vault.
- Use Azure DefaultAzureCredential for authentication.
- Keep Azure secret access isolated from application business logic.
- Return sanitised errors without exposing secret values.

Security
--------
- Does not store secrets.
- Does not print secrets.
- Does not log secret values.
- Uses Azure identity-based authentication.
- Error messages must not include secret contents.

Version
-------
v0.6.0
==============================================================================
"""

from azure.core.exceptions import AzureError, ResourceNotFoundError
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from app.services.secrets.base_secret_provider import BaseSecretProvider


class AzureKeyVaultSecretProvider(BaseSecretProvider):
    """
    Secret provider backed by Azure Key Vault.
    """

    def __init__(self, key_vault_name: str) -> None:
        if not key_vault_name:
            raise ValueError("Azure Key Vault name must be configured.")

        vault_url = f"https://{key_vault_name}.vault.azure.net"

        self._client = SecretClient(
            vault_url=vault_url,
            credential=DefaultAzureCredential(),
        )

    def get_secret(self, name: str) -> str:
        """
        Return a secret value from Azure Key Vault.

        Args:
            name: Azure Key Vault secret name.

        Returns:
            Secret value as a string.

        Raises:
            KeyError: If the requested secret is not found.
            RuntimeError: If Azure Key Vault cannot be reached.
        """
        try:
            secret = self._client.get_secret(name)
        except ResourceNotFoundError as exc:
            raise KeyError(f"Azure Key Vault secret not found: {name}") from exc
        except AzureError as exc:
            raise RuntimeError(
                f"Unable to retrieve Azure Key Vault secret: {name}"
            ) from exc

        if not secret.value:
            raise KeyError(f"Azure Key Vault secret is empty: {name}")

        return secret.value