"""Extra serialization helpers beyond dataclass to_dict/from_dict."""

from __future__ import annotations

import json

from roundwire.models.match import Match
from roundwire.models.player import Player
from roundwire.models.round import Round


def match_to_json(match: Match, *, indent: int | None = 2) -> str:
    return json.dumps(match.to_dict(), indent=indent, sort_keys=True)


def match_from_json(text: str) -> Match:
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("JSON root must be an object")
    return Match.from_dict(data)


def players_to_rows(players: list[Player]) -> list[dict[str, str]]:
    return [
        {
            "player_id": str(p.player_id),
            "name": p.name,
            "team": p.team.value,
            "country": p.country or "",
        }
        for p in players
    ]


def rounds_to_compact(rounds: list[Round]) -> list[dict[str, object]]:
    return [
        {
            "number": int(r.number),
            "winner": r.winner.value,
            "reason": r.win_reason,
            "kills": len(r.kills),
            "utility": len(r.utility),
            "planted": r.bomb_planted,
        }
        for r in rounds
    ]


def compact_match_view(match: Match) -> dict[str, object]:
    ct, t = match.score()
    return {
        "match_id": str(match.match_id),
        "map": match.map_name,
        "edition": match.edition.value,
        "score": {"CT": ct, "T": t},
        "players": players_to_rows(match.players),
        "rounds": rounds_to_compact(match.rounds),
    }
