"""Normalize and scale numeric series for comparisons."""

from __future__ import annotations

from roundwire.stats.aggregates import mean, safe_div


def minmax(values: list[float]) -> list[float]:
    if not values:
        return []
    lo = min(values)
    hi = max(values)
    if hi == lo:
        return [0.5 for _ in values]
    return [(v - lo) / (hi - lo) for v in values]


def zscores(values: list[float]) -> list[float]:
    if not values:
        return []
    avg = mean(values)
    var = mean([(v - avg) ** 2 for v in values])
    std = var ** 0.5
    if std < 1e-12:
        return [0.0 for _ in values]
    return [(v - avg) / std for v in values]


def softmax(values: list[float]) -> list[float]:
    if not values:
        return []
    peak = max(values)
    exps = [pow(2.718281828, v - peak) for v in values]
    total = sum(exps)
    return [e / total for e in exps]


def rescale(values: list[float], low: float = 0.0, high: float = 1.0) -> list[float]:
    normed = minmax(values)
    span = high - low
    return [low + v * span for v in normed]


def share(values: list[float]) -> list[float]:
    total = sum(values)
    return [safe_div(v, total) for v in values]


def rankdata(values: list[float], *, descending: bool = True) -> list[int]:
    """Competition ranks starting at 1."""
    indexed = list(enumerate(values))
    indexed.sort(key=lambda iv: (-iv[1] if descending else iv[1], iv[0]))
    ranks = [0] * len(values)
    for rank, (idx, _value) in enumerate(indexed, start=1):
        ranks[idx] = rank
    return ranks
