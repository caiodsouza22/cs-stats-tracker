"""Cross-metric correlation helpers across the roster."""

from __future__ import annotations

from roundwire.models.match import Match
from roundwire.players.profile import build_all_profiles
from roundwire.stats.matrix import pearson


def roster_metric_vectors(match: Match) -> dict[str, list[float]]:
    profiles = build_all_profiles(match)
    return {
        "rating": [p.rating_3_0 for p in profiles],
        "impact": [p.impact for p in profiles],
        "adr": [p.adr for p in profiles],
        "kd": [p.kd for p in profiles],
        "kast": [p.kast for p in profiles],
        "openings": [float(p.opening_kills) for p in profiles],
        "utility_spend": [float(p.utility_spend) for p in profiles],
        "enemies_flashed": [float(p.utility.enemies_flashed) for p in profiles],
    }


def rating_correlations(match: Match) -> dict[str, float]:
    vectors = roster_metric_vectors(match)
    rating = vectors["rating"]
    out = {}
    for key in ("impact", "adr", "kd", "kast", "openings", "utility_spend", "enemies_flashed"):
        out[key] = pearson(rating, vectors[key])
    return out


def correlation_matrix(match: Match) -> list[dict[str, object]]:
    keys = ["rating", "impact", "adr", "kd", "kast", "openings"]
    vectors = roster_metric_vectors(match)
    rows = []
    for a in keys:
        row: dict[str, object] = {"metric": a}
        for b in keys:
            row[b] = round(pearson(vectors[a], vectors[b]), 3)
        rows.append(row)
    return rows


def underrated_by_rating(match: Match, gap: float = 0.05) -> list[dict[str, object]]:
    """Players whose impact exceeds rating by ``gap`` (rough signal)."""
    rows = []
    for profile in build_all_profiles(match):
        delta = profile.impact - profile.rating_3_0
        if delta >= gap:
            rows.append(
                {
                    "name": profile.name,
                    "team": profile.team,
                    "rating": profile.rating_3_0,
                    "impact": profile.impact,
                    "delta": delta,
                }
            )
    return sorted(rows, key=lambda r: (-r["delta"], r["name"]))
