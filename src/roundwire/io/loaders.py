"""JSON match dump loaders and writers."""

from __future__ import annotations

import json
from pathlib import Path

from roundwire.errors.io_errors import LoadError, SaveError, SchemaError
from roundwire.models.match import Match
from roundwire.models.validation import validate_match


def load_match(path: Path | str) -> Match:
    file_path = Path(path)
    try:
        raw = file_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise LoadError(f"cannot read match dump: {exc}", path=file_path) from exc
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise LoadError(f"invalid JSON: {exc}", path=file_path) from exc
    if not isinstance(data, dict):
        raise SchemaError("match dump root must be an object")
    try:
        match = Match.from_dict(data)
        validate_match(match)
    except (KeyError, TypeError, ValueError) as exc:
        raise SchemaError(str(exc)) from exc
    return match


def save_match(match: Match, path: Path | str, *, indent: int = 2) -> None:
    file_path = Path(path)
    try:
        validate_match(match)
        payload = json.dumps(match.to_dict(), indent=indent, sort_keys=True)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(payload + "\n", encoding="utf-8")
    except OSError as exc:
        raise SaveError(f"cannot write match dump: {exc}", path=file_path) from exc


def load_match_dict(data: dict[str, object]) -> Match:
    from roundwire.io.validate_dump import validate_dump

    validate_dump(data)
    match = Match.from_dict(data)
    validate_match(match)
    return match
