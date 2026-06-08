"""Rolling form and hot/cold detection across rounds."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.models.match import Match
from roundwire.players.round_card import damage_series, kill_series, player_round_log
from roundwire.stats.aggregates import mean, safe_div
from roundwire.stats.rolling import rolling_mean, rolling_sum
from roundwire.types import PlayerId


@dataclass(frozen=True, slots=True)
class FormWindow:
    start_round: int
    end_round: int
    kills: float
    adr: float
    win_rate: float
    label: str

    def to_dict(self) -> dict[str, object]:
        return {
            "start_round": self.start_round,
            "end_round": self.end_round,
            "kills": round(self.kills, 2),
            "adr": round(self.adr, 1),
            "win_rate": round(self.win_rate, 3),
            "label": self.label,
        }


def _label(kills: float, adr: float, wr: float) -> str:
    if kills >= 1.2 and adr >= 90 and wr >= 0.55:
        return "hot"
    if kills <= 0.4 and adr <= 45 and wr <= 0.4:
        return "cold"
    if wr >= 0.65:
        return "winning"
    if wr <= 0.35:
        return "losing"
    return "steady"


def form_windows(match: Match, player_id: PlayerId, window: int = 5) -> list[FormWindow]:
    cards = player_round_log(match, player_id)
    if not cards:
        return []
    kills = [float(c.kills) for c in cards]
    dmg = [float(c.damage) for c in cards]
    wins = [1.0 if c.won else 0.0 for c in cards]
    k_roll = rolling_mean(kills, window)
    d_roll = rolling_mean(dmg, window)
    w_roll = rolling_mean(wins, window)
    out: list[FormWindow] = []
    for i, (k, d, w) in enumerate(zip(k_roll, d_roll, w_roll)):
        if k is None or d is None or w is None:
            continue
        start = cards[i - window + 1].round_number
        end = cards[i].round_number
        out.append(
            FormWindow(
                start_round=start,
                end_round=end,
                kills=k,
                adr=d,
                win_rate=w,
                label=_label(k, d, w),
            )
        )
    return out


def current_form(match: Match, player_id: PlayerId, window: int = 5) -> FormWindow | None:
    windows = form_windows(match, player_id, window=window)
    return windows[-1] if windows else None


def hot_streak_rounds(match: Match, player_id: PlayerId, window: int = 5) -> list[FormWindow]:
    return [w for w in form_windows(match, player_id, window=window) if w.label == "hot"]


def cold_streak_rounds(match: Match, player_id: PlayerId, window: int = 5) -> list[FormWindow]:
    return [w for w in form_windows(match, player_id, window=window) if w.label == "cold"]


def form_summary(match: Match, player_id: PlayerId) -> dict[str, object]:
    windows = form_windows(match, player_id)
    labels = [w.label for w in windows]
    return {
        "windows": len(windows),
        "hot": labels.count("hot"),
        "cold": labels.count("cold"),
        "steady": labels.count("steady"),
        "winning": labels.count("winning"),
        "losing": labels.count("losing"),
        "latest": windows[-1].to_dict() if windows else None,
        "avg_rolling_kills": round(mean([w.kills for w in windows]), 3),
        "avg_rolling_adr": round(mean([w.adr for w in windows]), 2),
    }


def momentum_delta(match: Match, player_id: PlayerId, window: int = 4) -> float:
    """Late-window kills minus early-window kills (positive = finishing strong)."""
    kills = [float(k) for k in kill_series(match, player_id)]
    if len(kills) < window * 2:
        return 0.0
    early = mean(kills[:window])
    late = mean(kills[-window:])
    return late - early


def consistency_index(match: Match, player_id: PlayerId) -> float:
    """Lower variance in damage series => higher consistency (0-1-ish)."""
    series = [float(x) for x in damage_series(match, player_id)]
    if len(series) < 2:
        return 1.0
    avg = mean(series)
    var = mean([(x - avg) ** 2 for x in series])
    # map: 0 variance -> 1.0, high variance -> approaches 0
    return safe_div(1.0, 1.0 + (var ** 0.5) / 40.0)


def cumulative_kills(match: Match, player_id: PlayerId) -> list[float]:
    return rolling_sum([float(k) for k in kill_series(match, player_id)])
