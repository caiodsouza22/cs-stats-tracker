"""In-memory match validation helpers."""

from __future__ import annotations

from roundwire.errors.validation import ValidationError
from roundwire.models.match import Match


def validate_match(match: Match) -> None:
    if not match.players:
        raise ValidationError("match has no players", field="players")
    if len(match.players) < 2:
        raise ValidationError("match needs at least two players", field="players")
    ids = [p.player_id for p in match.players]
    if len(ids) != len(set(ids)):
        raise ValidationError("duplicate player_id values", field="players")
    seen_rounds: set[int] = set()
    for rnd in match.rounds:
        n = int(rnd.number)
        if n in seen_rounds:
            raise ValidationError(f"duplicate round number {n}", field="rounds")
        seen_rounds.add(n)
        if n < 1:
            raise ValidationError(f"invalid round number {n}", field="rounds")
