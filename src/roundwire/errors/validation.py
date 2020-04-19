"""Validation failures for match dumps and in-memory models."""

from __future__ import annotations

from roundwire.errors.base import RoundwireError


class ValidationError(RoundwireError):
    """Raised when a match dump or model fails structural validation."""

    def __init__(self, message: str, *, field: str | None = None) -> None:
        super().__init__(message)
        self.field = field
