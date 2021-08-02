"""Lightweight schema checks for raw JSON dicts."""

from __future__ import annotations

from roundwire.errors.io_errors import SchemaError


REQUIRED_ROOT = ("match_id", "map_name", "edition", "players", "rounds")


def assert_root_schema(data: dict[str, object]) -> None:
    for key in REQUIRED_ROOT:
        if key not in data:
            raise SchemaError(f"missing root field: {key}", path_hint=key)
    if not isinstance(data["players"], list):
        raise SchemaError("players must be an array", path_hint="players")
    if not isinstance(data["rounds"], list):
        raise SchemaError("rounds must be an array", path_hint="rounds")
