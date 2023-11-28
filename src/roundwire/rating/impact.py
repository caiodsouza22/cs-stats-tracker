"""Documented impact score formula (CS2-leaning weights by default)."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.combat.adr import adr_for_player
from roundwire.combat.kd import kpr
from roundwire.combat.multikill import multi_kill_count
from roundwire.combat.opening import opening_kills_for
from roundwire.combat.survival import survival_rate
from roundwire.models.edition import GameEdition
from roundwire.models.match import Match
from roundwire.types import PlayerId


@dataclass(frozen=True, slots=True)
class ImpactWeights:
    kpr: float
    adr: float
    survival: float
    opening: float
    multi: float


@dataclass(frozen=True, slots=True)
class ImpactBreakdown:
    player_id: str
    name: str
    kpr: float
    adr_component: float
    survival: float
    opening_share: float
    multi_bonus: float
    impact: float


def impact_weights(edition: GameEdition) -> ImpactWeights:
    """
    CS2 nudges ADR a bit higher (utility damage + MR12 pace).
    CS:GO keeps the older balance.
    """
    if edition is GameEdition.CS2:
        return ImpactWeights(kpr=0.38, adr=0.28, survival=0.18, opening=0.14, multi=0.05)
    return ImpactWeights(kpr=0.40, adr=0.25, survival=0.20, opening=0.15, multi=0.05)


def impact_score(match: Match, player_id: PlayerId) -> float:
    """
    impact = w_k*KPR + w_a*(ADR/100) + w_s*Surv% + w_o*OpeningShare
             + w_m*multi_kill_rounds
    Weights depend on GameEdition (see impact_weights / docs/rating.md).
    """
    rounds = len(match.rounds) or 1
    w = impact_weights(match.edition)
    kpr_v = kpr(match, player_id)
    adr_v = adr_for_player(match, player_id) / 100.0
    surv = survival_rate(match, player_id)
    opening_share = opening_kills_for(match, player_id) / rounds
    multi_bonus = w.multi * multi_kill_count(match, player_id)
    value = (
        w.kpr * kpr_v
        + w.adr * adr_v
        + w.survival * surv
        + w.opening * opening_share
        + multi_bonus
    )
    return max(0.0, value)


def impact_breakdown(match: Match, player_id: PlayerId) -> ImpactBreakdown:
    player = match.player_map()[player_id]
    rounds = len(match.rounds) or 1
    w = impact_weights(match.edition)
    return ImpactBreakdown(
        player_id=str(player_id),
        name=player.name,
        kpr=kpr(match, player_id),
        adr_component=adr_for_player(match, player_id) / 100.0,
        survival=survival_rate(match, player_id),
        opening_share=opening_kills_for(match, player_id) / rounds,
        multi_bonus=w.multi * multi_kill_count(match, player_id),
        impact=impact_score(match, player_id),
    )


def impact_table(match: Match) -> list[ImpactBreakdown]:
    rows = [impact_breakdown(match, p.player_id) for p in match.players]
    return sorted(rows, key=lambda r: (-r.impact, r.name))


def impact_spread(match: Match) -> float:
    scores = [impact_score(match, p.player_id) for p in match.players]
    if not scores:
        return 0.0
    return max(scores) - min(scores)


def median_impact(match: Match) -> float:
    scores = sorted(impact_score(match, p.player_id) for p in match.players)
    if not scores:
        return 0.0
    mid = len(scores) // 2
    if len(scores) % 2:
        return scores[mid]
    return (scores[mid - 1] + scores[mid]) / 2.0


def above_average_players(match: Match) -> list[str]:
    scores = {str(p.player_id): impact_score(match, p.player_id) for p in match.players}
    if not scores:
        return []
    avg = sum(scores.values()) / len(scores)
    return sorted(pid for pid, val in scores.items() if val >= avg)


def explain_impact(match: Match, player_id: PlayerId) -> str:
    row = impact_breakdown(match, player_id)
    return (
        f"{row.name}: impact={row.impact:.3f} "
        f"(kpr={row.kpr:.2f}, adr/100={row.adr_component:.2f}, "
        f"surv={row.survival:.2f}, open={row.opening_share:.2f}, "
        f"multi={row.multi_bonus:.2f})"
    )
