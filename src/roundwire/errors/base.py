"""Root exception type."""

from __future__ import annotations


class RoundwireError(Exception):
    """Base class for all roundwire errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
