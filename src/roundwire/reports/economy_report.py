"""Economy summary text report."""

from __future__ import annotations

from roundwire.economy.summary import economy_match_summary
from roundwire.models.match import Match
from roundwire.reports.tables import format_table


def economy_summary_table(match: Match) -> str:
    rows: list[list[str]] = []
    for summary in economy_match_summary(match):
        buys = summary.buys
        rows.append(
            [
                summary.side,
                str(buys.get("full", 0)),
                str(buys.get("force", 0)),
                str(buys.get("eco", 0)),
                str(buys.get("semi", 0)),
                str(buys.get("pistol", 0)),
                f"{summary.force_success*100:.0f}%",
                f"{summary.full_winrate*100:.0f}%",
                str(summary.eco_upsets),
            ]
        )
    title = f"Economy — {match.map_name} ({match.edition.value})"
    table = format_table(
        ["Side", "Full", "Force", "Eco", "Semi", "Pistol", "ForceWR", "FullWR", "EcoWins"],
        rows,
    )
    return title + "\n" + table
