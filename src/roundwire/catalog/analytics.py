"""Cross-sample catalog analytics for demos and QA."""

from __future__ import annotations

from roundwire.catalog.samples import list_samples, sample_match
from roundwire.players.leaderboard import mvp
from roundwire.players.profile import build_all_profiles
from roundwire.series_analytics import SeriesBook


def catalog_mvp_table() -> list[dict[str, object]]:
    rows = []
    for sample_id in list_samples():
        match = sample_match(sample_id)
        row = mvp(match)
        rows.append(
            {
                "sample": sample_id,
                "map": match.map_name,
                "edition": match.edition.value,
                "mvp": row.name if row else None,
                "metric": row.metric if row else None,
                "value": row.value if row else None,
                "score": list(match.score()),
            }
        )
    return rows


def catalog_rating_leaders() -> list[dict[str, object]]:
    rows = []
    for sample_id in list_samples():
        match = sample_match(sample_id)
        profiles = build_all_profiles(match)
        if not profiles:
            continue
        top = profiles[0]
        rows.append(
            {
                "sample": sample_id,
                "player": top.name,
                "rating": round(top.rating_3_0, 3),
                "kills": top.kills,
                "adr": round(top.adr, 1),
            }
        )
    return rows


def catalog_series_book() -> SeriesBook:
    book = SeriesBook()
    for sample_id in list_samples():
        book.ingest_match(sample_match(sample_id))
    return book


def catalog_map_coverage() -> dict[str, int]:
    counts: dict[str, int] = {}
    for sample_id in list_samples():
        match = sample_match(sample_id)
        counts[match.map_name] = counts.get(match.map_name, 0) + 1
    return counts


def catalog_healthcheck() -> dict[str, object]:
    samples = list_samples()
    ok = 0
    problems: list[str] = []
    for sample_id in samples:
        try:
            match = sample_match(sample_id)
            if len(match.players) < 2:
                problems.append(f"{sample_id}: too few players")
            elif not match.rounds:
                problems.append(f"{sample_id}: no rounds")
            else:
                ok += 1
                _ = build_all_profiles(match)
        except Exception as exc:  # noqa: BLE001
            problems.append(f"{sample_id}: {exc}")
    return {
        "samples": len(samples),
        "ok": ok,
        "problems": problems,
        "maps": catalog_map_coverage(),
    }
