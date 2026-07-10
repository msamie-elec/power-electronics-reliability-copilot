"""
==============================================================================
Power Electronics Reliability Copilot
Application Telemetry Configuration

File
----
telemetry.py

Purpose
-------
Configures Azure Monitor / Application Insights telemetry for the FastAPI
backend when telemetry is enabled.

Responsibilities
----------------
- Enable Azure Monitor OpenTelemetry integration when configured.
- Keep telemetry optional for local development and tests.
- Avoid hard dependency failures when telemetry packages are not installed.
- Avoid exposing secrets through logs or telemetry setup errors.

Security
--------
- Does not log connection string values.
- Does not export secret values.
- Degrades safely when telemetry is disabled or unavailable.

Version
-------
v0.6.0
==============================================================================
"""

from __future__ import annotations

import logging
import os

from fastapi import FastAPI


logger = logging.getLogger(__name__)


def telemetry_enabled() -> bool:
    """
    Return whether runtime telemetry is enabled.
    """
    return os.getenv("ENABLE_TELEMETRY", "false").lower().strip() in {
        "1",
        "true",
        "yes",
        "on",
    }


def get_applicationinsights_connection_string() -> str:
    """
    Return the configured Application Insights connection string.
    """
    return os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING", "").strip()


def configure_telemetry(app: FastAPI) -> None:
    """
    Configure Azure Monitor OpenTelemetry integration.

    Telemetry is intentionally optional so the backend remains runnable in
    local and test environments without Azure Monitor packages installed.
    """
    if not telemetry_enabled():
        logger.info("Application telemetry is disabled.")
        return

    connection_string = get_applicationinsights_connection_string()

    if not connection_string:
        logger.warning(
            "ENABLE_TELEMETRY is true but APPLICATIONINSIGHTS_CONNECTION_STRING is not configured."
        )
        return

    try:
        from azure.monitor.opentelemetry import configure_azure_monitor
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    except ImportError:
        logger.warning(
            "Azure Monitor telemetry packages are not installed. Telemetry was not enabled."
        )
        return

    try:
        configure_azure_monitor(connection_string=connection_string)
        FastAPIInstrumentor.instrument_app(app)
        logger.info("Azure Monitor telemetry configured successfully.")
    except Exception:
        logger.exception("Azure Monitor telemetry configuration failed.")
