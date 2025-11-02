"""Detailed rating component cards for coaching UIs."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.models.match import Match
from roundwire.players.profile import build_player_profile
from roundwire.rating.impact import impact_score
from roundwire.rating.rating30 import rating_3_0, rating_3_0_table
from roundwire.rating.round_swing import round_swing_per_round, round_swing_total
from roundwire.stats.normalize import minmax, rankdata
from roundwire.types import PlayerId


@dataclass(frozen=True, slots=True)
class RatingCard:
    player_id: str
    name: str
    team: str
    rating_3_0: float
    impact: float
    swing_total: float
    swing_pr: float
    kills: int
    adr: float
    kast: float
    rank_rating: int
    rank_impact: int

    def to_dict(self) -> dict[str, object]:
        return {
            "player_id": self.player_id,
            "name": self.name,
            "team": self.team,
            "rating_3_0": round(self.rating_3_0, 4),
            "impact": round(self.impact, 4),
            "swing_total": round(self.swing_total, 4),
            "swing_pr": round(self.swing_pr, 4),
            "kills": self.kills,
            "adr": round(self.adr, 1),
            "kast": round(self.kast, 4),
            "rank_rating": self.rank_rating,
            "rank_impact": self.rank_impact,
        }


def rating_cards(match: Match) -> list[RatingCard]:
    profiles = [build_player_profile(match, p.player_id) for p in match.players]
    ratings = [p.rating_3_0 for p in profiles]
    impacts = [p.impact for p in profiles]
    r_ranks = rankdata(ratings, descending=True)
    i_ranks = rankdata(impacts, descending=True)
    cards: list[RatingCard] = []
    for idx, profile in enumerate(profiles):
        pid = PlayerId(profile.player_id)
        cards.append(
            RatingCard(
                player_id=profile.player_id,
                name=profile.name,
                team=profile.team,
                rating_3_0=profile.rating_3_0,
                impact=profile.impact,
                swing_total=round_swing_total(match, pid),
                swing_pr=round_swing_per_round(match, pid),
                kills=profile.kills,
                adr=profile.adr,
                kast=profile.kast,
                rank_rating=r_ranks[idx],
                rank_impact=i_ranks[idx],
            )
        )
    return sorted(cards, key=lambda c: (c.rank_rating, c.name))


def rating_component_matrix(match: Match) -> list[dict[str, object]]:
    table = rating_3_0_table(match)
    rows = []
    for row in table:
        # Rating30Breakdown fields
        rows.append(
            {
                "name": row.name,
                "rating": round(row.rating, 4),
                "kills": round(row.kills, 4),
                "damage": round(row.damage, 4),
                "survival": round(row.survival, 4),
                "kast": round(row.kast, 4),
                "multi_kills": round(row.multi_kills, 4),
                "round_swing": round(row.round_swing, 4),
            }
        )
    return rows


def normalized_rating_vector(match: Match) -> dict[str, list[float]]:
    cards = rating_cards(match)
    return {
        "names": [c.name for c in cards],
        "rating_norm": minmax([c.rating_3_0 for c in cards]),
        "impact_norm": minmax([c.impact for c in cards]),
        "swing_norm": minmax([c.swing_total for c in cards]),
        "adr_norm": minmax([c.adr for c in cards]),
    }


def rating_gap_to_mvp(match: Match, player_id: PlayerId) -> float:
    cards = rating_cards(match)
    if not cards:
        return 0.0
    best = cards[0].rating_3_0
    mine = next((c.rating_3_0 for c in cards if c.player_id == str(player_id)), 0.0)
    return best - mine


def impact_vs_rating_delta(match: Match, player_id: PlayerId) -> float:
    """Positive means impact rank is better than rating rank (underrated by R3.0)."""
    cards = rating_cards(match)
    card = next((c for c in cards if c.player_id == str(player_id)), None)
    if card is None:
        return 0.0
    return float(card.rank_rating - card.rank_impact)
