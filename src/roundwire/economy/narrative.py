"""Economy narrative helpers."""

from __future__ import annotations

from roundwire.economy.summary import economy_match_summary
from roundwire.models.match import Match


def economy_blurb(match: Match) -> str:
    rows = economy_match_summary(match)
    bits: list[str] = []
    for row in rows:
        bits.append(
            f"{row.side} logged {row.buys.get('full', 0)} full buys, "
            f"{row.buys.get('force', 0)} forces, {row.buys.get('eco', 0)} ecos "
            f"({row.eco_upsets} eco upsets)."
        )
    return " ".join(bits)
