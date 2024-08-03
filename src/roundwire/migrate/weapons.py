"""Weapon name rewriting for migration."""

from __future__ import annotations

from roundwire.rules.weapon_aliases import resolve_alias


def rewrite_weapon_name(name: str) -> str:
    resolved = resolve_alias(name)
    return resolved if resolved is not None else name.lower()
