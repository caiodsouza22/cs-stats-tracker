"""Compose a multi-section text report for a match."""

from __future__ import annotations

from roundwire.analysis.match_overview import match_overview
from roundwire.combat.narrative import match_blurb, player_blurb
from roundwire.economy.narrative import economy_blurb
from roundwire.models.match import Match
from roundwire.reports.economy_report import economy_summary_table
from roundwire.reports.impact_report import impact_report_table
from roundwire.reports.round_log import round_log_table
from roundwire.reports.scoreboard import scoreboard_table
from roundwire.reports.utility_report import utility_summary_table
from roundwire.text.scoreboard_style import box


def full_text_report(match: Match, *, include_rounds: bool = True) -> str:
    sections = [
        box("Match", match_blurb(match)),
        box("Scoreboard", scoreboard_table(match)),
        box("Economy", economy_summary_table(match) + "\n" + economy_blurb(match)),
        box("Utility", utility_summary_table(match)),
        box("Impact", impact_report_table(match)),
    ]
    if include_rounds:
        sections.append(box("Round log", round_log_table(match)))
    overview = match_overview(match)
    sections.append(box("Overview JSON-ish", str(overview)))
    # highlight top player if present
    if match.players:
        top_name = match.players[0].name
        # prefer overview top fragger when available
        frag = overview.get("top_fragger")
        if isinstance(frag, str):
            top_name = frag
        sections.append(box("Player spotlight", player_blurb(match, top_name)))
    return "\n\n".join(sections)


def compact_report(match: Match) -> str:
    ct, t = match.score()
    return (
        f"{match.map_name} {ct}:{t} ({match.edition.value})\n"
        f"{match_blurb(match)}\n"
        f"{economy_blurb(match)}"
    )
