"""
==============================================================================
Power Electronics Reliability Copilot
Base Secret Provider

File
----
base_secret_provider.py

Purpose
-------
Defines the common interface for application secret providers.

This abstraction allows the backend to retrieve secrets from different sources
without coupling application services to a specific secret-management backend.

Responsibilities
----------------
- Define the contract for retrieving application secrets.
- Support local development and Azure Key Vault implementations.
- Keep secret access isolated from business logic.

Security
--------
- Does not store secrets.
- Does not print secrets.
- Does not expose credentials in exceptions.
- Provider implementations must avoid logging secret values.

Version
-------
v0.6.0
==============================================================================
"""

from abc import ABC, abstractmethod


class BaseSecretProvider(ABC):
    """
    Abstract base class for secret providers.
    """

    @abstractmethod
    def get_secret(self, name: str) -> str:
        """
        Return a secret value by name.

        Args:
            name: Logical secret name used by the application.

        Returns:
            Secret value as a string.

        Raises:
            KeyError: If the secret cannot be found.
            RuntimeError: If the provider cannot retrieve the secret.
        """
        raise NotImplementedError