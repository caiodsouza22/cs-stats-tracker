"""Dense report pack builders for offline export / CI artifacts."""

from __future__ import annotations

import json
from pathlib import Path

from roundwire.analysis.dashboard import coaching_dashboard, slim_dashboard
from roundwire.analysis.match_story import build_match_story
from roundwire.catalog.analytics import catalog_healthcheck, catalog_mvp_table
from roundwire.maps.story import map_story
from roundwire.models.match import Match
from roundwire.players.season import SeasonRoster, season_from_catalog, top_map_specialists
from roundwire.reports.economy_report import economy_summary_table
from roundwire.reports.player_report import leaderboard_report, player_report_table
from roundwire.reports.rating30_report import rating30_report_table
from roundwire.reports.scoreboard import scoreboard_table
from roundwire.reports.utility_report import utility_summary_table


def text_report_pack(match: Match) -> str:
    story = build_match_story(match)
    chunks = [
        story.render(),
        "",
        "== Scoreboard ==",
        scoreboard_table(match),
        "",
        "== Players ==",
        player_report_table(match),
        "",
        "== Rating 3.0 ==",
        rating30_report_table(match),
        "",
        "== Leaderboard (ADR) ==",
        leaderboard_report(match, "adr"),
        "",
        "== Economy ==",
        economy_summary_table(match),
        "",
        "== Utility ==",
        utility_summary_table(match),
    ]
    return "\n".join(chunks)


def json_report_pack(match: Match) -> dict[str, object]:
    return {
        "slim": slim_dashboard(match),
        "full_keys": sorted(coaching_dashboard(match)),
        "map": map_story(match),
        "catalog_context": {
            "health": catalog_healthcheck(),
            "mvps": catalog_mvp_table(),
        },
    }


def write_report_pack(match: Match, directory: Path) -> dict[str, str]:
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    text_path = directory / "report.txt"
    json_path = directory / "report.json"
    text_path.write_text(text_report_pack(match), encoding="utf-8")
    json_path.write_text(json.dumps(json_report_pack(match), indent=2, sort_keys=True), encoding="utf-8")
    return {"text": str(text_path), "json": str(json_path)}


def season_report_pack(roster: SeasonRoster | None = None) -> dict[str, object]:
    roster = roster or season_from_catalog()
    return {
        "snapshot": roster.snapshot(),
        "consistency": roster.consistency_table()[:15],
        "specialists": top_map_specialists(roster)[:15],
        "series_players": roster.series_book().as_rows()[:20],
    }


def write_season_pack(directory: Path, roster: SeasonRoster | None = None) -> str:
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "season.json"
    path.write_text(json.dumps(season_report_pack(roster), indent=2, sort_keys=True), encoding="utf-8")
    return str(path)
