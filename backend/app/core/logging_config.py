"""
==============================================================================
Power Electronics Reliability Copilot
Structured Logging Configuration

File
----
logging_config.py

Purpose
-------
Configures application logging and request correlation metadata for backend
runtime diagnostics.

Responsibilities
----------------
- Configure process-wide Python logging.
- Add request correlation identifiers to HTTP requests.
- Expose request IDs in response headers.
- Avoid logging sensitive values.

Security
--------
- Does not log API keys, connection strings, passwords or tokens.
- Logs request metadata only.
- Keeps correlation IDs safe for diagnostics and support workflows.

Version
-------
v0.6.0
==============================================================================
"""

from __future__ import annotations

import logging
import os
import time
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


REQUEST_ID_HEADER = "X-Request-ID"


class RequestIdMiddleware(BaseHTTPMiddleware):
    """
    Add a correlation ID to each request and response.
    """

    async def dispatch(self, request: Request, call_next) -> Response:  # type: ignore[override]
        request_id = request.headers.get(REQUEST_ID_HEADER, str(uuid4()))
        request.state.request_id = request_id

        started_at = time.perf_counter()

        response = await call_next(request)

        duration_ms = round((time.perf_counter() - started_at) * 1000, 2)
        response.headers[REQUEST_ID_HEADER] = request_id

        logging.getLogger("app.requests").info(
            "request completed request_id=%s method=%s path=%s status_code=%s duration_ms=%s",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )

        return response


def configure_logging() -> None:
    """
    Configure application logging once during startup.
    """
    log_level = os.getenv("LOG_LEVEL", "INFO").upper().strip()

    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    logging.getLogger("azure").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
