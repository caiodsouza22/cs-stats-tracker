"""Economy-aware duel / output scaling for Rating 3.0 approximation."""

from __future__ import annotations

from roundwire.models.round import Round
from roundwire.types import PlayerId


def equipment_value(round_: Round, player_id: PlayerId) -> int:
    for inv in round_.inventories:
        if inv.player_id == player_id:
            return max(0, int(inv.equipment_value))
    return 0


def side_average_equipment(round_: Round, player_ids: set[str]) -> float:
    vals = [equipment_value(round_, PlayerId(pid)) for pid in player_ids]
    if not vals:
        return 0.0
    return sum(vals) / len(vals)


def eco_kill_multiplier(round_: Round, killer_id: PlayerId, victim_id: PlayerId) -> float:
    """
    Higher when the victim is better geared than the killer.
    Clipped so anti-eco frags don't inflate the kill sub-rating.
    """
    killer_eq = max(equipment_value(round_, killer_id), 200)
    victim_eq = max(equipment_value(round_, victim_id), 200)
    raw = victim_eq / killer_eq
    return max(0.55, min(1.75, raw))


def eco_damage_multiplier(round_: Round, attacker_id: PlayerId, victim_id: PlayerId) -> float:
    return eco_kill_multiplier(round_, attacker_id, victim_id)
