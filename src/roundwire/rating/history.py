"""Historical rating tracking across a list of matches for one player name."""

from __future__ import annotations

from dataclasses import dataclass, field

from roundwire.models.match import Match
from roundwire.players.profile import build_player_profile
from roundwire.players.roles import infer_role
from roundwire.stats.aggregates import mean
from roundwire.stats.distribution import summarize
from roundwire.stats.rolling import ema, slope


@dataclass
class RatingPoint:
    match_id: str
    map_name: str
    edition: str
    rating: float
    impact: float
    adr: float
    kills: int
    role: str

    def to_dict(self) -> dict[str, object]:
        return {
            "match_id": self.match_id,
            "map": self.map_name,
            "edition": self.edition,
            "rating": round(self.rating, 4),
            "impact": round(self.impact, 4),
            "adr": round(self.adr, 1),
            "kills": self.kills,
            "role": self.role,
        }


@dataclass
class PlayerHistory:
    name: str
    points: list[RatingPoint] = field(default_factory=list)

    def ingest(self, match: Match) -> None:
        player = match.player_by_name(self.name)
        if player is None:
            return
        profile = build_player_profile(match, player.player_id)
        role = infer_role(match, player.player_id)
        self.points.append(
            RatingPoint(
                match_id=str(match.match_id),
                map_name=match.map_name,
                edition=match.edition.value,
                rating=profile.rating_3_0,
                impact=profile.impact,
                adr=profile.adr,
                kills=profile.kills,
                role=role.primary.value,
            )
        )

    def summary(self) -> dict[str, object]:
        ratings = [p.rating for p in self.points]
        return {
            "name": self.name,
            "matches": len(self.points),
            "rating": summarize(ratings),
            "impact": summarize([p.impact for p in self.points]),
            "adr": summarize([p.adr for p in self.points]),
            "mean_kills": mean([float(p.kills) for p in self.points]),
            "rating_slope": slope(ratings) if len(ratings) >= 2 else 0.0,
            "rating_ema": [round(v, 3) for v in ema(ratings)] if ratings else [],
            "roles": [p.role for p in self.points],
            "points": [p.to_dict() for p in self.points],
        }


def build_histories(matches: list[Match]) -> dict[str, PlayerHistory]:
    names: set[str] = set()
    for match in matches:
        for player in match.players:
            names.add(player.name)
    out: dict[str, PlayerHistory] = {name: PlayerHistory(name=name) for name in names}
    for match in matches:
        for history in out.values():
            history.ingest(match)
    # drop empty
    return {name: hist for name, hist in out.items() if hist.points}


def history_leaderboard(matches: list[Match], n: int = 10) -> list[dict[str, object]]:
    histories = build_histories(matches)
    rows = [hist.summary() for hist in histories.values()]
    rows.sort(key=lambda r: (-float(r["rating"]["mean"]), r["name"]))
    return rows[: max(0, n)]
