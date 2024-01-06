"""Impact rating text report."""

from __future__ import annotations

from roundwire.models.match import Match
from roundwire.rating.impact import impact_table
from roundwire.reports.tables import format_table


def impact_report_table(match: Match) -> str:
    rows = [
        [
            row.name,
            f"{row.impact:.3f}",
            f"{row.kpr:.2f}",
            f"{row.adr_component:.2f}",
            f"{row.survival:.2f}",
            f"{row.opening_share:.2f}",
        ]
        for row in impact_table(match)
    ]
    return format_table(
        ["Player", "Impact", "KPR", "ADR/100", "Surv", "Open"],
        rows,
    )
