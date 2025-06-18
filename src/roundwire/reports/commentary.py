"""Short match commentary snippets for reports / demos."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CommentaryLine:
    key: str
    map_name: str
    side: str
    phase: str
    situation: str
    text: str


LINES: dict[str, CommentaryLine] = {
    "mirage_ct_early_rifle": CommentaryLine(
        "mirage_ct_early_rifle",
        "de_mirage",
        "CT",
        "early",
        "opening_rifle",
        "Early CT on de_mirage: rifle opener finds space before utility lands.",
    ),
    "mirage_t_mid_execute": CommentaryLine(
        "mirage_t_mid_execute",
        "de_mirage",
        "T",
        "mid",
        "plant_default",
        "Mid T on de_mirage: default plant after mid control.",
    ),
    "inferno_ct_late_retake": CommentaryLine(
        "inferno_ct_late_retake",
        "de_inferno",
        "CT",
        "late",
        "retake_success",
        "Late CT on de_inferno: retake converts with numbers after plant.",
    ),
    "ancient_t_early_pistol": CommentaryLine(
        "ancient_t_early_pistol",
        "de_ancient",
        "T",
        "early",
        "opening_pistol",
        "Early T on de_ancient: pistol opener forces a scramble.",
    ),
    "anubis_ct_mid_trade": CommentaryLine(
        "anubis_ct_mid_trade",
        "de_anubis",
        "CT",
        "mid",
        "trade_clean",
        "Mid CT on de_anubis: trade comes in cleanly inside two seconds.",
    ),
    "mirage_ct_late_time": CommentaryLine(
        "mirage_ct_late_time",
        "de_mirage",
        "CT",
        "late",
        "time_bleed",
        "Late CT on de_mirage: clock runs out without a plant.",
    ),
}


def line(key: str) -> CommentaryLine:
    return LINES[key]


def lines_for(map_name: str, side: str | None = None) -> list[CommentaryLine]:
    out = [ln for ln in LINES.values() if ln.map_name == map_name]
    if side is not None:
        out = [ln for ln in out if ln.side == side]
    return out


def render(key: str) -> str:
    ln = line(key)
    return f"[{ln.phase}/{ln.side}/{ln.map_name}] {ln.text}"
