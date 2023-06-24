"""Tiny numeric helpers."""

from __future__ import annotations


def mean(values: list[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def safe_div(num: float, den: float, default: float = 0.0) -> float:
    if den == 0:
        return default
    return num / den


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))
