"""
==============================================================================
Power Electronics Reliability Copilot
Local Secret Provider

File
----
local_secret_provider.py

Purpose
-------
Provides local development secret retrieval from environment variables.

This provider supports local development and test execution where secrets are
loaded from `.env` or the operating system environment.

Responsibilities
----------------
- Retrieve secrets from environment variables.
- Preserve compatibility with existing local `.env` configuration.
- Keep local secret retrieval isolated from application business logic.

Security
--------
- Does not store secrets.
- Does not print secrets.
- Does not log secret values.
- Raises sanitised errors without exposing secret contents.

Version
-------
v0.6.0
==============================================================================
"""

import os

from app.services.secrets.base_secret_provider import BaseSecretProvider


class LocalSecretProvider(BaseSecretProvider):
    """
    Secret provider backed by environment variables.
    """

    def get_secret(self, name: str) -> str:
        """
        Return a secret value from environment variables.

        Args:
            name: Environment variable name.

        Returns:
            Secret value as a string.

        Raises:
            KeyError: If the requested secret is not available.
        """
        secret_value = os.getenv(name, "")

        if not secret_value:
            raise KeyError(f"Local secret is not configured: {name}")

        return secret_value