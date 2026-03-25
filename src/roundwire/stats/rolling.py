"""Rolling window helpers for form and series analytics."""

from __future__ import annotations

from roundwire.stats.aggregates import mean


def rolling_mean(values: list[float], window: int) -> list[float | None]:
    if window <= 0:
        raise ValueError("window must be positive")
    out: list[float | None] = []
    for i in range(len(values)):
        if i + 1 < window:
            out.append(None)
            continue
        chunk = values[i + 1 - window : i + 1]
        out.append(mean(chunk))
    return out


def rolling_sum(values: list[float], window: int | None = None) -> list[float]:
    """If window is None, return cumulative sum; else rolling sum."""
    if window is None:
        total = 0.0
        out: list[float] = []
        for value in values:
            total += value
            out.append(total)
        return out
    if window <= 0:
        raise ValueError("window must be positive")
    out = []
    for i in range(len(values)):
        start = max(0, i + 1 - window)
        out.append(sum(values[start : i + 1]))
    return out


def rolling_max(values: list[float], window: int) -> list[float | None]:
    if window <= 0:
        raise ValueError("window must be positive")
    out: list[float | None] = []
    for i in range(len(values)):
        if i + 1 < window:
            out.append(None)
            continue
        out.append(max(values[i + 1 - window : i + 1]))
    return out


def rolling_min(values: list[float], window: int) -> list[float | None]:
    if window <= 0:
        raise ValueError("window must be positive")
    out: list[float | None] = []
    for i in range(len(values)):
        if i + 1 < window:
            out.append(None)
            continue
        out.append(min(values[i + 1 - window : i + 1]))
    return out


def ema(values: list[float], alpha: float = 0.3) -> list[float]:
    if not values:
        return []
    if not 0 < alpha <= 1:
        raise ValueError("alpha must be in (0, 1]")
    out = [values[0]]
    for value in values[1:]:
        out.append(alpha * value + (1 - alpha) * out[-1])
    return out


def slope(values: list[float]) -> float:
    """Simple least-squares slope against index."""
    n = len(values)
    if n < 2:
        return 0.0
    xs = list(range(n))
    x_mean = mean([float(x) for x in xs])
    y_mean = mean(values)
    num = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, values))
    den = sum((x - x_mean) ** 2 for x in xs)
    return num / den if den else 0.0
