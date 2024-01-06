"""Per-round log text report."""

from __future__ import annotations

from roundwire.economy.classify import classify_round_buy
from roundwire.models.match import Match
from roundwire.reports.tables import format_table


def round_log_table(match: Match) -> str:
    rows: list[list[str]] = []
    for rnd in match.rounds:
        buys = classify_round_buy(rnd, match)
        rows.append(
            [
                str(int(rnd.number)),
                rnd.winner.value,
                rnd.win_reason,
                "Y" if rnd.bomb_planted else "N",
                buys["CT"].value,
                buys["T"].value,
                str(len(rnd.kills)),
            ]
        )
    title = f"Rounds — {match.map_name} score {match.score()[0]}:{match.score()[1]}"
    table = format_table(
        ["#", "Winner", "Reason", "Bomb", "CT Buy", "T Buy", "Kills"],
        rows,
    )
    return title + "\n" + table
