"""AWP presence and impact within a match."""

from __future__ import annotations

from roundwire.models.match import Match
from roundwire.rules.weapon_aliases import canonical_weapon_name


def _is_awp(name: str) -> bool:
    try:
        return canonical_weapon_name(name) == "awp"
    except KeyError:
        return "awp" in name.lower()


def rounds_with_awp_kill(match: Match) -> list[int]:
    out: list[int] = []
    for rnd in match.rounds:
        if any(_is_awp(k.weapon.name) for k in rnd.kills):
            out.append(int(rnd.number))
    return out


def awp_kills(match: Match) -> int:
    return sum(1 for rnd in match.rounds for k in rnd.kills if _is_awp(k.weapon.name))


def awp_round_share(match: Match) -> float:
    if not match.rounds:
        return 0.0
    return len(rounds_with_awp_kill(match)) / len(match.rounds)
