"""Domain-level errors."""

from __future__ import annotations

from roundwire.errors.base import RoundwireError


class DomainError(RoundwireError):
    """Generic domain rule violation."""


class InvalidEditionError(DomainError):
    """Unknown or unsupported game edition."""


class InvalidRoundError(DomainError):
    """Round number or round content is invalid for the edition."""
