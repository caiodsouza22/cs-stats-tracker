"""Exception hierarchy for roundwire."""

from roundwire.errors.base import RoundwireError
from roundwire.errors.domain import DomainError, InvalidEditionError, InvalidRoundError
from roundwire.errors.io_errors import LoadError, SaveError, SchemaError
from roundwire.errors.validation import ValidationError

__all__ = [
    "DomainError",
    "InvalidEditionError",
    "InvalidRoundError",
    "LoadError",
    "RoundwireError",
    "SaveError",
    "SchemaError",
    "ValidationError",
]
