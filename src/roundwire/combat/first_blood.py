"""First blood (opening) conversion into round wins."""

from __future__ import annotations

from roundwire.combat.opening import first_kill, opening_duels
from roundwire.models.match import Match
from roundwire.models.team import TeamSide
from roundwire.types import PlayerId


def opening_conversion(match: Match) -> float:
    """Share of rounds where the opening killer's side won the round."""
    duels = opening_duels(match)
    if not duels:
        return 0.0
    pmap = match.player_map()
    converted = 0
    for duel in duels:
        killer = pmap.get(duel.kill.killer_id)
        rnd = next(r for r in match.rounds if int(r.number) == duel.round_number)
        if killer is not None and rnd.winner is killer.team:
            converted += 1
    return converted / len(duels)


def opening_conversion_for_side(match: Match, side: TeamSide) -> float:
    pmap = match.player_map()
    relevant = 0
    converted = 0
    for duel in opening_duels(match):
        killer = pmap.get(duel.kill.killer_id)
        if killer is None or killer.team is not side:
            continue
        relevant += 1
        rnd = next(r for r in match.rounds if int(r.number) == duel.round_number)
        if rnd.winner is side:
            converted += 1
    return 0.0 if relevant == 0 else converted / relevant


def first_blood_players(match: Match) -> dict[str, int]:
    counts: dict[str, int] = {}
    for duel in opening_duels(match):
        key = str(duel.kill.killer_id)
        counts[key] = counts.get(key, 0) + 1
    return counts


def died_first_count(match: Match, player_id: PlayerId) -> int:
    return sum(1 for d in opening_duels(match) if d.kill.victim_id == player_id)


def opening_weapon_freq(match: Match) -> dict[str, int]:
    freq: dict[str, int] = {}
    for rnd in match.rounds:
        fk = first_kill(rnd)
        if fk is None:
            continue
        name = fk.weapon.name.lower()
        freq[name] = freq.get(name, 0) + 1
    return freq
