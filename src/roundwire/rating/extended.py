"""Extended rating views combining impact with KAST and opening metrics."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.combat.kast import kast_pct
from roundwire.combat.opening import opening_kills_for
from roundwire.models.match import Match
from roundwire.rating.impact import impact_score
from roundwire.rating.weights import DEFAULT_WEIGHTS, ImpactWeights
from roundwire.types import PlayerId


@dataclass(frozen=True, slots=True)
class ExtendedRating:
    player_id: str
    name: str
    impact: float
    kast: float
    opening_kills: int
    composite: float


def composite_rating(
    match: Match,
    player_id: PlayerId,
    weights: ImpactWeights = DEFAULT_WEIGHTS,
) -> float:
    """Blend impact with KAST; ``weights`` reserved for future tuning."""
    _ = weights
    base = impact_score(match, player_id)
    kast = kast_pct(match, player_id)
    return 0.75 * base + 0.25 * kast


def extended_rating(match: Match, player_id: PlayerId) -> ExtendedRating:
    player = match.player_map()[player_id]
    return ExtendedRating(
        player_id=str(player_id),
        name=player.name,
        impact=impact_score(match, player_id),
        kast=kast_pct(match, player_id),
        opening_kills=opening_kills_for(match, player_id),
        composite=composite_rating(match, player_id),
    )


def extended_table(match: Match) -> list[ExtendedRating]:
    rows = [extended_rating(match, p.player_id) for p in match.players]
    return sorted(rows, key=lambda r: (-r.composite, r.name))
