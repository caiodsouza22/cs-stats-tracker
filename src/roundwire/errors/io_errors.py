"""I/O related errors."""

from __future__ import annotations

from pathlib import Path

from roundwire.errors.base import RoundwireError


class LoadError(RoundwireError):
    """Failed to load a match dump from disk."""

    def __init__(self, message: str, *, path: Path | None = None) -> None:
        super().__init__(message)
        self.path = path


class SaveError(RoundwireError):
    """Failed to write a match dump to disk."""

    def __init__(self, message: str, *, path: Path | None = None) -> None:
        super().__init__(message)
        self.path = path


class SchemaError(RoundwireError):
    """JSON dump does not match the expected schema."""

    def __init__(self, message: str, *, path_hint: str | None = None) -> None:
        super().__init__(message)
        self.path_hint = path_hint
