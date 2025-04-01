"""Damage breakdowns by hitgroup and weapon."""

from __future__ import annotations

from collections import Counter, defaultdict

from roundwire.models.hitgroup import normalize_hitgroup
from roundwire.models.match import Match
from roundwire.rules.weapon_aliases import canonical_weapon_name
from roundwire.types import PlayerId


def damage_by_hitgroup(match: Match, player_id: PlayerId | None = None) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for rnd in match.rounds:
        for event in rnd.damage:
            if player_id is not None and event.attacker_id != player_id:
                continue
            counter[normalize_hitgroup(event.hitgroup)] += event.damage
    return dict(counter)


def damage_by_weapon(match: Match, player_id: PlayerId | None = None) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for rnd in match.rounds:
        for event in rnd.damage:
            if player_id is not None and event.attacker_id != player_id:
                continue
            try:
                weapon = canonical_weapon_name(event.weapon.name)
            except KeyError:
                weapon = event.weapon.name.lower()
            counter[weapon] += event.damage
    return dict(counter)


def armor_damage_total(match: Match, player_id: PlayerId | None = None) -> int:
    total = 0
    for rnd in match.rounds:
        for event in rnd.damage:
            if player_id is not None and event.attacker_id != player_id:
                continue
            total += event.armor_damage
    return total


def damage_received(match: Match, player_id: PlayerId) -> int:
    return sum(
        event.damage
        for rnd in match.rounds
        for event in rnd.damage
        if event.victim_id == player_id
    )


def damage_delta(match: Match, player_id: PlayerId) -> int:
    dealt = sum(
        event.damage
        for rnd in match.rounds
        for event in rnd.damage
        if event.attacker_id == player_id
    )
    return dealt - damage_received(match, player_id)


def per_round_damage(match: Match, player_id: PlayerId) -> list[int]:
    return [rnd.damage_dealt_by(player_id) for rnd in match.rounds]


def teammates_damaged(match: Match) -> dict[str, int]:
    """Count self-team damage events if teams known (rare in clean dumps)."""
    pmap = match.player_map()
    counter: dict[str, int] = defaultdict(int)
    for rnd in match.rounds:
        for event in rnd.damage:
            att = pmap.get(event.attacker_id)
            vic = pmap.get(event.victim_id)
            if att and vic and att.team is vic.team and att.player_id != vic.player_id:
                counter[str(att.player_id)] += event.damage
    return dict(counter)
