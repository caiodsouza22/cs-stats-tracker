"""Match leaderboards across multiple ranking keys."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from roundwire.models.match import Match
from roundwire.players.profile import PlayerMatchProfile, build_all_profiles, build_player_profile
from roundwire.types import PlayerId


@dataclass(frozen=True, slots=True)
class LeaderboardRow:
    rank: int
    player_id: str
    name: str
    team: str
    value: float
    metric: str

    def to_dict(self) -> dict[str, object]:
        return {
            "rank": self.rank,
            "player_id": self.player_id,
            "name": self.name,
            "team": self.team,
            "value": self.value,
            "metric": self.metric,
        }


_METRICS: dict[str, Callable[[PlayerMatchProfile], float]] = {
    "kills": lambda p: float(p.kills),
    "deaths": lambda p: float(p.deaths),
    "assists": lambda p: float(p.assists),
    "adr": lambda p: p.adr,
    "kd": lambda p: p.kd,
    "kast": lambda p: p.kast,
    "rating": lambda p: p.rating_3_0,
    "impact": lambda p: p.impact,
    "opening_kills": lambda p: float(p.opening_kills),
    "hs_pct": lambda p: p.hs_pct,
    "utility_spend": lambda p: float(p.utility_spend),
    "enemies_flashed": lambda p: float(p.utility.enemies_flashed),
    "clutch_wins": lambda p: float(p.clutch_wins),
    "multi_kills": lambda p: float(p.multi_kills),
    "survival": lambda p: p.survival,
}


def available_metrics() -> list[str]:
    return sorted(_METRICS)


def leaderboard(match: Match, metric: str = "rating", limit: int = 10) -> list[LeaderboardRow]:
    if metric not in _METRICS:
        raise KeyError(f"unknown metric {metric!r}; choose from {available_metrics()}")
    key = _METRICS[metric]
    profiles = build_all_profiles(match)
    ordered = sorted(profiles, key=lambda p: (-key(p), p.name))
    rows: list[LeaderboardRow] = []
    for idx, profile in enumerate(ordered[: max(0, limit)], start=1):
        rows.append(
            LeaderboardRow(
                rank=idx,
                player_id=profile.player_id,
                name=profile.name,
                team=profile.team,
                value=round(key(profile), 4),
                metric=metric,
            )
        )
    return rows


def multi_leaderboard(match: Match, metrics: list[str] | None = None) -> dict[str, list[dict[str, object]]]:
    chosen = metrics or ["rating", "kills", "adr", "impact", "opening_kills"]
    return {metric: [row.to_dict() for row in leaderboard(match, metric)] for metric in chosen}


def rank_of(match: Match, player_id: PlayerId, metric: str = "rating") -> int | None:
    rows = leaderboard(match, metric=metric, limit=len(match.players))
    for row in rows:
        if row.player_id == str(player_id):
            return row.rank
    return None


def podium(match: Match, metric: str = "rating") -> list[LeaderboardRow]:
    return leaderboard(match, metric=metric, limit=3)


def team_leaderboard(match: Match, team: str, metric: str = "rating") -> list[LeaderboardRow]:
    key = team.upper()
    rows = [row for row in leaderboard(match, metric=metric, limit=len(match.players)) if row.team == key]
    # re-rank within team
    out: list[LeaderboardRow] = []
    for idx, row in enumerate(rows, start=1):
        out.append(
            LeaderboardRow(
                rank=idx,
                player_id=row.player_id,
                name=row.name,
                team=row.team,
                value=row.value,
                metric=row.metric,
            )
        )
    return out


def mvp(match: Match) -> LeaderboardRow | None:
    rows = leaderboard(match, metric="rating", limit=1)
    return rows[0] if rows else None


def dual_mvp(match: Match) -> dict[str, LeaderboardRow | None]:
    """Rating MVP and entry (opening kills) MVP."""
    rating = leaderboard(match, "rating", 1)
    entry = leaderboard(match, "opening_kills", 1)
    return {
        "rating_mvp": rating[0] if rating else None,
        "entry_mvp": entry[0] if entry else None,
    }
