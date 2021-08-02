"""Deep validation for raw match dump dictionaries before model parse."""

from __future__ import annotations

from roundwire.errors.io_errors import SchemaError
from roundwire.errors.validation import ValidationError
from roundwire.io.schema import assert_root_schema


def validate_player_dict(data: dict[str, object], index: int) -> None:
    for key in ("player_id", "name", "team"):
        if key not in data:
            raise SchemaError(f"players[{index}] missing {key}", path_hint=f"players[{index}].{key}")


def validate_round_dict(data: dict[str, object], index: int) -> None:
    for key in ("number", "winner", "win_reason"):
        if key not in data:
            raise SchemaError(f"rounds[{index}] missing {key}", path_hint=f"rounds[{index}].{key}")
    number = data["number"]
    if not isinstance(number, int) or isinstance(number, bool) or number < 1:
        raise ValidationError(f"rounds[{index}].number must be a positive int", field="rounds")


def validate_dump(data: dict[str, object]) -> None:
    assert_root_schema(data)
    players = data["players"]
    rounds = data["rounds"]
    assert isinstance(players, list)
    assert isinstance(rounds, list)
    if not players:
        raise ValidationError("players array is empty", field="players")
    for i, player in enumerate(players):
        if not isinstance(player, dict):
            raise SchemaError(f"players[{i}] must be object", path_hint=f"players[{i}]")
        validate_player_dict(player, i)
    for i, rnd in enumerate(rounds):
        if not isinstance(rnd, dict):
            raise SchemaError(f"rounds[{i}] must be object", path_hint=f"rounds[{i}]")
        validate_round_dict(rnd, i)
