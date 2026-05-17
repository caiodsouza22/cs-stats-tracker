"""Round pacing: duration bands, stall detection, time wins."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.models.match import Match
from roundwire.models.team import TeamSide
from roundwire.stats.aggregates import mean, safe_div


@dataclass(frozen=True, slots=True)
class PaceBand:
    label: str
    min_ms: int
    max_ms: int
    rounds: int
    ct_wins: int
    t_wins: int

    def to_dict(self) -> dict[str, object]:
        total = max(1, self.rounds)
        return {
            "label": self.label,
            "min_ms": self.min_ms,
            "max_ms": self.max_ms,
            "rounds": self.rounds,
            "ct_wins": self.ct_wins,
            "t_wins": self.t_wins,
            "ct_wr": round(self.ct_wins / total, 3),
            "t_wr": round(self.t_wins / total, 3),
        }


DEFAULT_BANDS = (
    ("ultra_fast", 0, 30000),
    ("fast", 30000, 55000),
    ("standard", 55000, 90000),
    ("slow", 90000, 140000),
)


def round_durations(match: Match) -> list[int]:
    out = []
    for rnd in match.rounds:
        if rnd.duration_ms > 0:
            out.append(rnd.duration_ms)
            continue
        ticks = [int(k.tick_ms) for k in rnd.kills] + [int(u.tick_ms) for u in rnd.utility]
        out.append(max(ticks) if ticks else 0)
    return out


def pace_bands(match: Match, bands: tuple[tuple[str, int, int], ...] = DEFAULT_BANDS) -> list[PaceBand]:
    durs = round_durations(match)
    result: list[PaceBand] = []
    for label, lo, hi in bands:
        ct = t = n = 0
        for rnd, dur in zip(match.rounds, durs):
            if lo <= dur < hi:
                n += 1
                if rnd.winner is TeamSide.CT:
                    ct += 1
                else:
                    t += 1
        result.append(PaceBand(label, lo, hi, n, ct, t))
    return result


def pace_report(match: Match) -> dict[str, object]:
    durs = [float(d) for d in round_durations(match)]
    time_wins = sum(1 for rnd in match.rounds if rnd.win_reason in {"time", "timeout"})
    return {
        "avg_duration_ms": round(mean(durs), 1),
        "max_duration_ms": max(durs) if durs else 0.0,
        "min_duration_ms": min(durs) if durs else 0.0,
        "time_wins": time_wins,
        "time_win_rate": safe_div(float(time_wins), float(len(match.rounds))),
        "bands": [b.to_dict() for b in pace_bands(match)],
        "plant_rate": safe_div(
            float(sum(1 for r in match.rounds if r.bomb_planted)),
            float(len(match.rounds)),
        ),
    }


def stall_rounds(match: Match, threshold_ms: int = 100000) -> list[int]:
    return [
        int(rnd.number)
        for rnd, dur in zip(match.rounds, round_durations(match))
        if dur >= threshold_ms
    ]


def blowout_rounds(match: Match, max_kills: int = 3, max_ms: int = 35000) -> list[int]:
    durs = round_durations(match)
    out = []
    for rnd, dur in zip(match.rounds, durs):
        if len(rnd.kills) <= max_kills and dur <= max_ms:
            out.append(int(rnd.number))
    return out
