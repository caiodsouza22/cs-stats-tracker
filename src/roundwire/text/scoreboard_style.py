"""Extra scoreboard styling helpers."""

from __future__ import annotations


def align_right(text: str, width: int) -> str:
    return text.rjust(width)


def align_left(text: str, width: int) -> str:
    return text.ljust(width)


def center(text: str, width: int) -> str:
    return text.center(width)


def box(title: str, body: str) -> str:
    width = max(len(title), *(len(line) for line in body.splitlines() or [""]))
    top = "+" + "-" * (width + 2) + "+"
    title_line = f"| {title.ljust(width)} |"
    lines = [top, title_line, top.replace("-", "=")]
    for line in body.splitlines() or [""]:
        lines.append(f"| {line.ljust(width)} |")
    lines.append(top)
    return "\n".join(lines)
