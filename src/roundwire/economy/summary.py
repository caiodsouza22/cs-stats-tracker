"""Per-match economy summary rows."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.economy.classify import buy_histogram
from roundwire.economy.eco_rounds import eco_upsets
from roundwire.economy.force_buy import force_success_rate
from roundwire.economy.full_buy import full_buy_winrate
from roundwire.models.match import Match
from roundwire.models.team import TeamSide


@dataclass(frozen=True, slots=True)
class EconomySideSummary:
    side: str
    buys: dict[str, int]
    force_success: float
    full_winrate: float
    eco_upsets: int


def economy_side_summary(match: Match, side: TeamSide) -> EconomySideSummary:
    return EconomySideSummary(
        side=side.value,
        buys=buy_histogram(match, side),
        force_success=force_success_rate(match, side),
        full_winrate=full_buy_winrate(match, side),
        eco_upsets=len(eco_upsets(match, side)),
    )


def economy_match_summary(match: Match) -> list[EconomySideSummary]:
    return [
        economy_side_summary(match, TeamSide.CT),
        economy_side_summary(match, TeamSide.T),
    ]


def format_economy_summary(match: Match) -> list[str]:
    lines: list[str] = []
    for row in economy_match_summary(match):
        buys = ", ".join(f"{k}={v}" for k, v in sorted(row.buys.items()))
        lines.append(
            f"{row.side}: {buys}; forceWR={row.force_success:.2f}; "
            f"fullWR={row.full_winrate:.2f}; eco_upsets={row.eco_upsets}"
        )
    return lines
