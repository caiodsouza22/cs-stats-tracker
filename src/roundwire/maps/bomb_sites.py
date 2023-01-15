"""Soft labels for bomb-site context tags on utility events."""

from __future__ import annotations

SITE_TAGS = frozenset({"A", "B", "mid", "spawn", "yard", "ramp", "apps", "palace"})


def extract_site_tags(tags: list[str] | tuple[str, ...]) -> list[str]:
    return [t for t in tags if t in SITE_TAGS]
