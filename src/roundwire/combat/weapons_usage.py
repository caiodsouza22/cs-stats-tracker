"""Weapon usage frequencies from kills."""

from __future__ import annotations

from collections import Counter

from roundwire.models.match import Match
from roundwire.rules.weapon_aliases import canonical_weapon_name
from roundwire.types import PlayerId


def weapon_kills(match: Match, player_id: PlayerId | None = None) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for rnd in match.rounds:
        for kill in rnd.kills:
            if player_id is not None and kill.killer_id != player_id:
                continue
            try:
                name = canonical_weapon_name(kill.weapon.name)
            except KeyError:
                name = kill.weapon.name.lower()
            counter[name] += 1
    return dict(counter)


def favorite_weapon(match: Match, player_id: PlayerId) -> str | None:
    usage = weapon_kills(match, player_id)
    if not usage:
        return None
    return max(usage.items(), key=lambda kv: kv[1])[0]
