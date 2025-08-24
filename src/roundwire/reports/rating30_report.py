"""Rating 3.0 text report."""

from __future__ import annotations

from roundwire.models.match import Match
from roundwire.rating.rating30 import rating_3_0_table
from roundwire.reports.tables import format_table


def rating30_report_table(match: Match) -> str:
    rows = [
        [
            row.name,
            f"{row.rating:.3f}",
            f"{row.kills:.2f}",
            f"{row.damage:.2f}",
            f"{row.survival:.2f}",
            f"{row.kast:.2f}",
            f"{row.multi_kills:.2f}",
            f"{row.round_swing:.2f}",
        ]
        for row in rating_3_0_table(match)
    ]
    return format_table(
        ["Player", "R3.0", "Kill", "Dmg", "Surv", "KAST", "Multi", "Swing"],
        rows,
    )
