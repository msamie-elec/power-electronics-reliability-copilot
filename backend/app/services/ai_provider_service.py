"""
==============================================================================
Power Electronics Reliability Copilot
AI Provider Service

File
----
ai_provider_service.py

Purpose
-------
Provides a central AI provider abstraction for OpenAI and Azure OpenAI.

Responsibilities
----------------
- Route chat completion requests to OpenAI or Azure OpenAI.
- Keep provider-specific request construction outside business services.
- Support Azure OpenAI deployment-based model routing.
- Avoid sending unsupported optional parameters to Azure reasoning/newer models.
- Log provider errors without exposing API keys or credentials.

Security
--------
- Does not print API keys.
- Does not print Azure OpenAI credentials.
- Does not print full request payloads.
- Logs only sanitised provider error details.

Version
-------
v0.6.1
==============================================================================
"""

import logging
from typing import Any

from openai import AzureOpenAI, BadRequestError, OpenAI, OpenAIError

from app.config import openai_config
from app.services.secrets.secret_service import secret_service


logger = logging.getLogger(__name__)


class AIProviderService:
    """
    Provides a unified interface for chat completion requests.
    """

    def __init__(self) -> None:
        self._openai_client: OpenAI | None = None
        self._azure_client: AzureOpenAI | None = None

    def generate_chat_completion(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
        use_extraction_model: bool = False,
        response_format: dict[str, Any] | None = None,
    ) -> str:
        """
        Generate a chat completion using the configured AI provider.
        """
        if openai_config.use_azure_openai:
            return self._generate_with_azure_openai(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=temperature,
                response_format=response_format,
            )

        return self._generate_with_openai(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=temperature,
            use_extraction_model=use_extraction_model,
            response_format=response_format,
        )

    def _get_openai_client(self) -> OpenAI:
        try:
            api_key = secret_service.get_secret(
                "openai-api-key",
                fallback_env="OPENAI_API_KEY",
            )
        except KeyError as exc:
            raise ValueError(
                "OPENAI_API_KEY must be configured when AI_PROVIDER=openai."
            ) from exc

        if self._openai_client is None:
            self._openai_client = OpenAI(api_key=api_key)

        return self._openai_client

    def _get_azure_client(self) -> AzureOpenAI:
        try:
            azure_api_key = secret_service.get_secret(
                "azure-openai-api-key",
                fallback_env="AZURE_OPENAI_API_KEY",
            )
        except KeyError as exc:
            raise ValueError(
                "AZURE_OPENAI_API_KEY must be configured when AI_PROVIDER=azure_openai."
            ) from exc

        if not openai_config.azure_endpoint:
            raise ValueError(
                "AZURE_OPENAI_ENDPOINT must be configured when AI_PROVIDER=azure_openai."
            )

        if self._azure_client is None:
            self._azure_client = AzureOpenAI(
                api_key=azure_api_key,
                api_version=openai_config.azure_api_version,
                azure_endpoint=openai_config.azure_endpoint,
            )

        return self._azure_client

    def _generate_with_openai(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        use_extraction_model: bool,
        response_format: dict[str, Any] | None,
    ) -> str:
        model = (
            openai_config.extraction_model
            if use_extraction_model
            else openai_config.model
        )

        kwargs: dict[str, Any] = {
            "model": model,
            "temperature": temperature,
            "messages": self._build_messages(system_prompt, user_prompt),
        }

        if response_format:
            kwargs["response_format"] = response_format

        try:
            response = self._get_openai_client().chat.completions.create(**kwargs)
        except OpenAIError as exc:
            self._log_provider_error("OpenAI", model, exc)
            raise

        return response.choices[0].message.content or ""

    def _generate_with_azure_openai(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        response_format: dict[str, Any] | None,
    ) -> str:
        if not openai_config.azure_chat_deployment:
            raise ValueError(
                "AZURE_OPENAI_CHAT_DEPLOYMENT must be configured when AI_PROVIDER=azure_openai."
            )

        deployment = openai_config.azure_chat_deployment

        kwargs: dict[str, Any] = {
            "model": deployment,
            "messages": self._build_messages(system_prompt, user_prompt),
        }

        if self._supports_temperature(deployment):
            kwargs["temperature"] = temperature

        if response_format and self._supports_response_format(deployment):
            kwargs["response_format"] = response_format

        try:
            response = self._get_azure_client().chat.completions.create(**kwargs)
        except BadRequestError as exc:
            self._log_provider_error("Azure OpenAI", deployment, exc)
            raise
        except OpenAIError as exc:
            self._log_provider_error("Azure OpenAI", deployment, exc)
            raise

        return response.choices[0].message.content or ""

    @staticmethod
    def _build_messages(system_prompt: str, user_prompt: str) -> list[dict[str, str]]:
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

    @staticmethod
    def _supports_temperature(deployment_name: str) -> bool:
        """
        Return whether the configured deployment should receive temperature.

        Some Azure OpenAI reasoning/newer deployments reject sampling parameters
        such as temperature. The current Azure deployment uses gpt-5-mini, so
        temperature is intentionally omitted for gpt-5/o-series style names.
        """
        name = deployment_name.lower().strip()

        restricted_prefixes = (
            "gpt-5",
            "o1",
            "o3",
            "o4",
        )

        return not name.startswith(restricted_prefixes)

    @staticmethod
    def _supports_response_format(deployment_name: str) -> bool:
        """
        Return whether response_format should be sent to the deployment.

        This remains conservative for Azure newer/reasoning models to avoid
        avoidable 400 responses. OpenAI provider requests still support
        response_format through the OpenAI path.
        """
        name = deployment_name.lower().strip()

        restricted_prefixes = (
            "gpt-5",
            "o1",
            "o3",
            "o4",
        )

        return not name.startswith(restricted_prefixes)

    @staticmethod
    def _log_provider_error(
        provider: str,
        model_or_deployment: str,
        exc: Exception,
    ) -> None:
        """
        Log provider failure details without exposing secrets.
        """
        status_code = getattr(exc, "status_code", None)
        error_code = getattr(exc, "code", None)
        message = getattr(exc, "message", None) or str(exc)

        logger.error(
            "%s request failed model_or_deployment=%s status_code=%s code=%s message=%s",
            provider,
            model_or_deployment,
            status_code,
            error_code,
            message,
        )


ai_provider_service = AIProviderService()