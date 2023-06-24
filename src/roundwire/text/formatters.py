"""Display formatters."""

from __future__ import annotations


def pct(value: float, digits: int = 0) -> str:
    return f"{value * 100:.{digits}f}%"


def signed(value: float, digits: int = 2) -> str:
    return f"{value:+.{digits}f}"


def trunc(text: str, width: int) -> str:
    if len(text) <= width:
        return text
    if width <= 3:
        return text[:width]
    return text[: width - 3] + "..."
