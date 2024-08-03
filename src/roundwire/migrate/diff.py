"""Summarize migration changes."""

from __future__ import annotations

from roundwire.migrate.upgrade import migrate_match_to_cs2
from roundwire.models.match import Match


def migration_summary(match: Match) -> dict[str, object]:
    upgraded = migrate_match_to_cs2(match)
    weapon_changes = 0
    for before, after in zip(match.rounds, upgraded.rounds, strict=True):
        for bk, ak in zip(before.kills, after.kills, strict=True):
            if bk.weapon.name != ak.weapon.name:
                weapon_changes += 1
    return {
        "from_edition": match.edition.value,
        "to_edition": upgraded.edition.value,
        "weapon_rewrites": weapon_changes,
        "rounds": len(upgraded.rounds),
    }
