"""
Power Electronics Reliability Copilot
Project-specific exceptions.
"""


class CopilotError(Exception):
    """Base exception for Engineering Copilot errors."""


class DocumentNotFoundError(CopilotError):
    """Raised when a requested engineering document cannot be found."""


class RetrievalError(CopilotError):
    """Raised when evidence retrieval fails."""


class ReasoningError(CopilotError):
    """Raised when evidence-backed answer generation fails."""