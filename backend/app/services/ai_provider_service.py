"""
Power Electronics Reliability Copilot
AI Provider Service

Centralised AI provider abstraction for OpenAI and Azure OpenAI.

v0.6.0 introduces this service so the Engineering Copilot can switch between
local OpenAI API usage and Azure OpenAI through configuration rather than
application code changes.
"""

from typing import Any

from openai import AzureOpenAI, OpenAI

from app.config import openai_config


class AIProviderService:
    """
    Provides a unified interface for chat completion requests.

    The rest of the application does not need to know whether the active
    provider is OpenAI or Azure OpenAI.
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
        if not openai_config.api_key:
            raise ValueError(
                "OPENAI_API_KEY must be configured when AI_PROVIDER=openai."
            )

        if self._openai_client is None:
            self._openai_client = OpenAI(api_key=openai_config.api_key)

        return self._openai_client

    def _get_azure_client(self) -> AzureOpenAI:
        if not openai_config.azure_api_key:
            raise ValueError(
                "AZURE_OPENAI_API_KEY must be configured when AI_PROVIDER=azure_openai."
            )

        if not openai_config.azure_endpoint:
            raise ValueError(
                "AZURE_OPENAI_ENDPOINT must be configured when AI_PROVIDER=azure_openai."
            )

        if self._azure_client is None:
            self._azure_client = AzureOpenAI(
                api_key=openai_config.azure_api_key,
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
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }

        if response_format:
            kwargs["response_format"] = response_format

        response = self._get_openai_client().chat.completions.create(**kwargs)

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

        kwargs: dict[str, Any] = {
            "model": openai_config.azure_chat_deployment,
            "temperature": temperature,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }

        if response_format:
            kwargs["response_format"] = response_format

        response = self._get_azure_client().chat.completions.create(**kwargs)

        return response.choices[0].message.content or ""


ai_provider_service = AIProviderService()