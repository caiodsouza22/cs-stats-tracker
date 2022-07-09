"""Trade kill enumeration beyond openings."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.models.kill import Kill
from roundwire.models.match import Match
from roundwire.models.round import Round
from roundwire.models.timing import DEFAULT_TRADE_WINDOW_MS, trade_window_after
from roundwire.types import Milliseconds


@dataclass(frozen=True, slots=True)
class TradeKill:
    round_number: int
    original: Kill
    trade: Kill


def trades_in_round(
    round_: Round,
    window_ms: Milliseconds = DEFAULT_TRADE_WINDOW_MS,
) -> list[TradeKill]:
    sorted_kills = sorted(round_.kills, key=lambda k: int(k.tick_ms))
    found: list[TradeKill] = []
    for i, kill in enumerate(sorted_kills):
        window = trade_window_after(kill.tick_ms, window_ms)
        for later in sorted_kills[i + 1 :]:
            if not window.contains(later.tick_ms):
                break
            if later.victim_id == kill.killer_id:
                found.append(
                    TradeKill(
                        round_number=int(round_.number),
                        original=kill,
                        trade=later,
                    )
                )
                break
    return found


def all_trades(match: Match) -> list[TradeKill]:
    out: list[TradeKill] = []
    for rnd in match.rounds:
        out.extend(trades_in_round(rnd))
    return out
