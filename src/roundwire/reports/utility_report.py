"""Utility usage text report."""

from __future__ import annotations

from roundwire.models.match import Match
from roundwire.reports.tables import format_table
from roundwire.utility.summary import utility_summary


def utility_summary_table(match: Match) -> str:
    rows: list[list[str]] = []
    for line in utility_summary(match):
        rows.append(
            [
                line.name,
                str(line.flashes),
                str(line.smokes),
                str(line.hes),
                str(line.fires),
                str(line.enemies_flashed),
                str(line.he_damage),
            ]
        )
    title = f"Utility — {match.map_name}"
    table = format_table(
        ["Player", "Flash", "Smoke", "HE", "Fire", "EnemiesFlashed", "HEDmg"],
        rows,
    )
    return title + "\n" + table
