"""Hitgroup normalization for damage events."""

from __future__ import annotations

HITGROUPS = frozenset(
    {
        "generic",
        "head",
        "chest",
        "stomach",
        "left_arm",
        "right_arm",
        "left_leg",
        "right_leg",
        "neck",
    }
)


def normalize_hitgroup(value: str) -> str:
    key = value.strip().lower().replace(" ", "_").replace("-", "_")
    aliases = {
        "hg": "head",
        "helmet": "head",
        "body": "chest",
        "torso": "chest",
        "leg": "left_leg",
        "arm": "left_arm",
    }
    if key in aliases:
        return aliases[key]
    if key in HITGROUPS:
        return key
    return "generic"
