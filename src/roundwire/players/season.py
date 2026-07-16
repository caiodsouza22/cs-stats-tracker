"""Season / multi-match roster analytics built from player histories."""

from __future__ import annotations

from dataclasses import dataclass, field

from roundwire.catalog.samples import list_samples, sample_match
from roundwire.models.match import Match
from roundwire.players.roles import PlayerRole
from roundwire.rating.history import PlayerHistory, build_histories, history_leaderboard
from roundwire.series_analytics import SeriesBook, map_pool_performance, role_stability
from roundwire.stats.aggregates import mean, safe_div
from roundwire.stats.distribution import percentile, summarize


@dataclass
class SeasonRoster:
    """Collect matches and expose roster-wide season views."""

    matches: list[Match] = field(default_factory=list)

    def add(self, match: Match) -> None:
        self.matches.append(match)

    def extend(self, matches: list[Match]) -> None:
        self.matches.extend(matches)

    def histories(self) -> dict[str, PlayerHistory]:
        return build_histories(self.matches)

    def leaderboard(self, n: int = 10) -> list[dict[str, object]]:
        return history_leaderboard(self.matches, n=n)

    def series_book(self) -> SeriesBook:
        book = SeriesBook()
        for match in self.matches:
            book.ingest_match(match)
        return book

    def map_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for match in self.matches:
            counts[match.map_name] = counts.get(match.map_name, 0) + 1
        return counts

    def edition_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for match in self.matches:
            counts[match.edition.value] = counts.get(match.edition.value, 0) + 1
        return counts

    def player_card(self, name: str) -> dict[str, object] | None:
        histories = self.histories()
        hist = histories.get(name)
        if hist is None:
            return None
        summary = hist.summary()
        summary["role_stability"] = role_stability(self.matches, name)
        summary["map_pool"] = map_pool_performance(self.matches, name)
        return summary

    def rising_players(self, min_matches: int = 2) -> list[dict[str, object]]:
        rows = []
        for name, hist in self.histories().items():
            if len(hist.points) < min_matches:
                continue
            summary = hist.summary()
            slope = float(summary["rating_slope"])
            if slope > 0:
                rows.append(
                    {
                        "name": name,
                        "matches": summary["matches"],
                        "slope": slope,
                        "mean_rating": summary["rating"]["mean"],
                    }
                )
        return sorted(rows, key=lambda r: (-r["slope"], -r["mean_rating"], r["name"]))

    def falling_players(self, min_matches: int = 2) -> list[dict[str, object]]:
        rows = []
        for name, hist in self.histories().items():
            if len(hist.points) < min_matches:
                continue
            summary = hist.summary()
            slope = float(summary["rating_slope"])
            if slope < 0:
                rows.append(
                    {
                        "name": name,
                        "matches": summary["matches"],
                        "slope": slope,
                        "mean_rating": summary["rating"]["mean"],
                    }
                )
        return sorted(rows, key=lambda r: (r["slope"], r["mean_rating"], r["name"]))

    def role_distribution(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for hist in self.histories().values():
            for point in hist.points:
                counts[point.role] = counts.get(point.role, 0) + 1
        return counts

    def consistency_table(self) -> list[dict[str, object]]:
        rows = []
        for name, hist in self.histories().items():
            ratings = [p.rating for p in hist.points]
            if len(ratings) < 2:
                continue
            summary = summarize(ratings)
            spread = summary["max"] - summary["min"]
            rows.append(
                {
                    "name": name,
                    "matches": len(ratings),
                    "mean": summary["mean"],
                    "p50": summary["p50"],
                    "spread": spread,
                    "cv": safe_div(spread, summary["mean"]) if summary["mean"] else 0.0,
                }
            )
        return sorted(rows, key=lambda r: (r["cv"], -r["mean"], r["name"]))

    def snapshot(self) -> dict[str, object]:
        return {
            "matches": len(self.matches),
            "maps": self.map_counts(),
            "editions": self.edition_counts(),
            "players": len(self.histories()),
            "leaderboard": self.leaderboard(5),
            "rising": self.rising_players()[:5],
            "falling": self.falling_players()[:5],
            "roles": self.role_distribution(),
        }


def season_from_catalog() -> SeasonRoster:
    roster = SeasonRoster()
    for sample_id in list_samples():
        roster.add(sample_match(sample_id))
    return roster


def compare_seasons(left: SeasonRoster, right: SeasonRoster) -> list[dict[str, object]]:
    left_hist = left.histories()
    right_hist = right.histories()
    names = sorted(set(left_hist) & set(right_hist))
    rows = []
    for name in names:
        l = left_hist[name].summary()
        r = right_hist[name].summary()
        rows.append(
            {
                "name": name,
                "rating_delta": float(r["rating"]["mean"]) - float(l["rating"]["mean"]),
                "adr_delta": float(r["adr"]["mean"]) - float(l["adr"]["mean"]),
                "left_matches": l["matches"],
                "right_matches": r["matches"],
            }
        )
    return sorted(rows, key=lambda r: (-abs(r["rating_delta"]), r["name"]))


def role_loyalty_score(matches: list[Match], name: str) -> float:
    """1.0 if always same primary role, lower if role hops."""
    stab = role_stability(matches, name)
    samples = int(stab["samples"])
    unique = len(stab["unique_roles"])
    if samples <= 0:
        return 0.0
    return safe_div(1.0, float(unique))


def top_map_specialists(roster: SeasonRoster, min_maps: int = 1) -> list[dict[str, object]]:
    rows = []
    for name, hist in roster.histories().items():
        by_map: dict[str, list[float]] = {}
        for point in hist.points:
            by_map.setdefault(point.map_name, []).append(point.rating)
        for mapa, vals in by_map.items():
            if len(vals) < min_maps:
                continue
            rows.append(
                {
                    "name": name,
                    "map": mapa,
                    "samples": len(vals),
                    "mean_rating": mean(vals),
                    "p90": percentile(vals, 90),
                }
            )
    return sorted(rows, key=lambda r: (-r["mean_rating"], -r["samples"], r["name"]))


KNOWN_ROLES = [role.value for role in PlayerRole]
