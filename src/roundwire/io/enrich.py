"""Synthetic but structured round-event enrichers for sparse dumps."""

from __future__ import annotations

from roundwire.models.damage import DamageEvent
from roundwire.models.kill import Kill
from roundwire.models.match import Match
from roundwire.models.round import Round
from roundwire.models.team import TeamSide
from roundwire.models.utility_event import UtilityEvent, UtilityKind
from roundwire.models.weapon import Weapon
from roundwire.types import Milliseconds, PlayerId, RoundNumber


def estimate_missing_survivors(round_: Round, match: Match) -> list[PlayerId]:
    """If survivors empty, approximate as players who did not die in the round."""
    if round_.survivors:
        return list(round_.survivors)
    dead = {kill.victim_id for kill in round_.kills}
    return [p.player_id for p in match.players if p.player_id not in dead]


def enrich_round_survivors(match: Match) -> Match:
    """Return a shallow-copied match with survivors filled when missing."""
    rounds: list[Round] = []
    for rnd in match.rounds:
        survivors = estimate_missing_survivors(rnd, match)
        rounds.append(
            Round(
                number=rnd.number,
                winner=rnd.winner,
                win_reason=rnd.win_reason,
                bomb_planted=rnd.bomb_planted,
                inventories=list(rnd.inventories),
                kills=list(rnd.kills),
                damage=list(rnd.damage),
                utility=list(rnd.utility),
                survivors=survivors,
                duration_ms=rnd.duration_ms,
            )
        )
    return Match(
        match_id=match.match_id,
        map_name=match.map_name,
        edition=match.edition,
        team_ct_name=match.team_ct_name,
        team_t_name=match.team_t_name,
        players=list(match.players),
        rounds=rounds,
        series_score=match.series_score,
        event_name=match.event_name,
        played_at=match.played_at,
    )


def damage_from_kills_proxy(round_: Round) -> list[DamageEvent]:
    """Invent damage events from kills when damage array is empty (demo gaps)."""
    if round_.damage:
        return list(round_.damage)
    events: list[DamageEvent] = []
    for kill in round_.kills:
        dmg = 100 if kill.headshot else 80
        events.append(
            DamageEvent(
                attacker_id=kill.killer_id,
                victim_id=kill.victim_id,
                weapon=kill.weapon,
                damage=dmg,
                tick_ms=kill.tick_ms,
                hitgroup="head" if kill.headshot else "chest",
            )
        )
    return events


def enrich_round_damage(match: Match) -> Match:
    rounds: list[Round] = []
    for rnd in match.rounds:
        rounds.append(
            Round(
                number=rnd.number,
                winner=rnd.winner,
                win_reason=rnd.win_reason,
                bomb_planted=rnd.bomb_planted,
                inventories=list(rnd.inventories),
                kills=list(rnd.kills),
                damage=damage_from_kills_proxy(rnd),
                utility=list(rnd.utility),
                survivors=list(rnd.survivors),
                duration_ms=rnd.duration_ms,
            )
        )
    return Match(
        match_id=match.match_id,
        map_name=match.map_name,
        edition=match.edition,
        team_ct_name=match.team_ct_name,
        team_t_name=match.team_t_name,
        players=list(match.players),
        rounds=rounds,
        series_score=match.series_score,
        event_name=match.event_name,
        played_at=match.played_at,
    )


def summarize_sparsity(match: Match) -> dict[str, object]:
    rounds = len(match.rounds) or 1
    return {
        "rounds": len(match.rounds),
        "avg_kills": sum(len(r.kills) for r in match.rounds) / rounds,
        "avg_damage_events": sum(len(r.damage) for r in match.rounds) / rounds,
        "avg_utility": sum(len(r.utility) for r in match.rounds) / rounds,
        "survivor_coverage": sum(1 for r in match.rounds if r.survivors) / rounds,
        "inventory_coverage": sum(1 for r in match.rounds if r.inventories) / rounds,
    }
