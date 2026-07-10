"""
==============================================================================
Power Electronics Reliability Copilot
Health Diagnostics API

File
----
health.py

Purpose
-------
Exposes lightweight and detailed health diagnostics endpoints.

Responsibilities
----------------
- Provide a lightweight health probe for runtime availability checks.
- Provide detailed dependency diagnostics for cloud validation.
- Keep response payloads free from secret values.

Security
--------
- Does not expose credentials.
- Does not expose secret values.
- Returns dependency status only.

Version
-------
v0.6.0
==============================================================================
"""

from fastapi import APIRouter

from app.services.health_service import health_service


router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
def get_health() -> dict:
    """
    Return lightweight health status.
    """
    return health_service.lightweight_health()


@router.get("/details")
def get_health_details() -> dict:
    """
    Return detailed dependency diagnostics.
    """
    return health_service.detailed_health()
