"""Scoreboard text report."""

from __future__ import annotations

from roundwire.combat.summary import combat_summary
from roundwire.models.match import Match
from roundwire.rating.impact import impact_score
from roundwire.reports.tables import format_table
from roundwire.types import PlayerId


def scoreboard_table(match: Match) -> str:
    ct, t = match.score()
    header = (
        f"{match.team_ct_name} {ct} - {t} {match.team_t_name} "
        f"| {match.map_name} | {match.edition.value} ({match.edition.mr_label})"
    )
    rows: list[list[str]] = []
    for line in combat_summary(match):
        impact = impact_score(match, PlayerId(line.player_id))
        rows.append(
            [
                line.name,
                line.team,
                str(line.kills),
                str(line.deaths),
                str(line.assists),
                f"{line.adr:.1f}",
                f"{line.kd:.2f}",
                f"{line.hs_pct*100:.0f}%",
                f"{impact:.2f}",
            ]
        )
    table = format_table(
        ["Player", "Side", "K", "D", "A", "ADR", "K/D", "HS%", "Impact"],
        rows,
    )
    return header + "\n" + table
