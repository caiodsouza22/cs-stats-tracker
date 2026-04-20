"""Cross-match series and roster book analytics."""

from __future__ import annotations

from dataclasses import dataclass, field

from roundwire.models.match import Match
from roundwire.models.series import Series
from roundwire.players.profile import build_player_profile
from roundwire.players.roles import PlayerRole, infer_role
from roundwire.stats.aggregates import mean
from roundwire.stats.distribution import summarize
from roundwire.stats.player_book import PlayerBook


@dataclass
class SeriesPlayerLine:
    name: str
    maps: int = 0
    kills: int = 0
    deaths: int = 0
    adr_samples: list[float] = field(default_factory=list)
    rating_samples: list[float] = field(default_factory=list)
    impact_samples: list[float] = field(default_factory=list)
    opening_kills: int = 0
    roles: list[str] = field(default_factory=list)
    map_names: list[str] = field(default_factory=list)

    def add(self, match: Match) -> None:
        player = match.player_by_name(self.name)
        if player is None:
            return
        profile = build_player_profile(match, player.player_id)
        role = infer_role(match, player.player_id)
        self.maps += 1
        self.kills += profile.kills
        self.deaths += profile.deaths
        self.adr_samples.append(profile.adr)
        self.rating_samples.append(profile.rating_3_0)
        self.impact_samples.append(profile.impact)
        self.opening_kills += profile.opening_kills
        self.roles.append(role.primary.value)
        self.map_names.append(match.map_name)

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "maps": self.maps,
            "kills": self.kills,
            "deaths": self.deaths,
            "kd": (self.kills / self.deaths) if self.deaths else float(self.kills),
            "adr": summarize(self.adr_samples),
            "rating": summarize(self.rating_samples),
            "impact": summarize(self.impact_samples),
            "opening_kills": self.opening_kills,
            "mean_adr": mean(self.adr_samples),
            "mean_rating": mean(self.rating_samples),
            "primary_role_mode": _mode(self.roles),
            "maps_played": sorted(set(self.map_names)),
        }


def _mode(values: list[str]) -> str | None:
    if not values:
        return None
    counts: dict[str, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    return max(counts.items(), key=lambda kv: (kv[1], kv[0]))[0]


@dataclass
class SeriesBook:
    lines: dict[str, SeriesPlayerLine] = field(default_factory=dict)

    def ingest_match(self, match: Match) -> None:
        for player in match.players:
            line = self.lines.setdefault(player.name, SeriesPlayerLine(name=player.name))
            line.add(match)

    def ingest_series(self, series: Series) -> None:
        for match in series.maps:
            self.ingest_match(match)

    def top_rating(self, n: int = 5) -> list[SeriesPlayerLine]:
        return sorted(self.lines.values(), key=lambda l: (-mean(l.rating_samples), l.name))[:n]

    def top_kills(self, n: int = 5) -> list[SeriesPlayerLine]:
        return sorted(self.lines.values(), key=lambda l: (-l.kills, l.name))[:n]

    def as_rows(self) -> list[dict[str, object]]:
        return [line.to_dict() for line in sorted(self.lines.values(), key=lambda l: l.name)]


def series_summary(series: Series) -> dict[str, object]:
    a, b = series.map_wins()
    book = SeriesBook()
    book.ingest_series(series)
    return {
        "series_id": series.series_id,
        "team_a": series.team_a,
        "team_b": series.team_b,
        "best_of": series.best_of,
        "map_wins": {"a": a, "b": b},
        "complete": series.is_complete(),
        "maps": [
            {
                "match_id": str(m.match_id),
                "map": m.map_name,
                "score": list(m.score()),
                "edition": m.edition.value,
            }
            for m in series.maps
        ],
        "players": book.as_rows(),
    }


def build_player_book(matches: list[Match]) -> PlayerBook:
    book = PlayerBook()
    for match in matches:
        book.ingest(match)
    return book


def role_stability(matches: list[Match], player_name: str) -> dict[str, object]:
    roles: list[str] = []
    for match in matches:
        player = match.player_by_name(player_name)
        if player is None:
            continue
        roles.append(infer_role(match, player.player_id).primary.value)
    return {
        "name": player_name,
        "samples": len(roles),
        "roles": roles,
        "mode": _mode(roles),
        "unique_roles": sorted(set(roles)),
        "stable": len(set(roles)) <= 2,
    }


def map_pool_performance(matches: list[Match], player_name: str) -> dict[str, dict[str, float]]:
    by_map: dict[str, list[float]] = {}
    for match in matches:
        player = match.player_by_name(player_name)
        if player is None:
            continue
        rating = build_player_profile(match, player.player_id).rating_3_0
        by_map.setdefault(match.map_name, []).append(rating)
    return {mapa: summarize(vals) for mapa, vals in sorted(by_map.items())}
