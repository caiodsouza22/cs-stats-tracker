"""Estimated utility spend using weapon catalog prices."""

from __future__ import annotations

from roundwire.models.match import Match
from roundwire.models.utility_event import UtilityKind
from roundwire.rules.weapon_aliases import weapon_cost
from roundwire.types import PlayerId

_KIND_TO_WEAPON = {
    UtilityKind.FLASH: "flashbang",
    UtilityKind.SMOKE: "smokegrenade",
    UtilityKind.HE: "hegrenade",
    UtilityKind.MOLOTOV: "molotov",
    UtilityKind.INCENDIARY: "incgrenade",
    UtilityKind.DECOY: "decoy",
}


def utility_spend(match: Match, player_id: PlayerId | None = None) -> int:
    total = 0
    for rnd in match.rounds:
        for event in rnd.utility:
            if player_id is not None and event.thrower_id != player_id:
                continue
            weapon = _KIND_TO_WEAPON.get(event.kind)
            if weapon is None:
                continue
            total += weapon_cost(weapon)
    return total
