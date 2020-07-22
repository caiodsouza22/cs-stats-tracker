"""Timing windows used by opening-kill and trade detection."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.types import Milliseconds


DEFAULT_TRADE_WINDOW_MS = Milliseconds(2000)
DEFAULT_OPENING_GRACE_MS = Milliseconds(500)


@dataclass(frozen=True, slots=True)
class TimeWindow:
    start_ms: Milliseconds
    end_ms: Milliseconds

    def contains(self, tick_ms: Milliseconds) -> bool:
        return int(self.start_ms) <= int(tick_ms) <= int(self.end_ms)

    def duration(self) -> int:
        return max(0, int(self.end_ms) - int(self.start_ms))


def trade_window_after(kill_ms: Milliseconds, window_ms: Milliseconds = DEFAULT_TRADE_WINDOW_MS) -> TimeWindow:
    start = Milliseconds(int(kill_ms))
    end = Milliseconds(int(kill_ms) + int(window_ms))
    return TimeWindow(start_ms=start, end_ms=end)
