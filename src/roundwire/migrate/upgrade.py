"""Upgrade match edition and weapon names to CS2."""

from __future__ import annotations

from copy import deepcopy

from roundwire.migrate.weapons import rewrite_weapon_name
from roundwire.models.damage import DamageEvent
from roundwire.models.edition import GameEdition
from roundwire.models.inventory import InventorySnapshot
from roundwire.models.kill import Kill
from roundwire.models.match import Match
from roundwire.models.round import Round
from roundwire.models.weapon import Weapon


def _rewrite_weapon(weapon: Weapon) -> Weapon:
    return Weapon(name=rewrite_weapon_name(weapon.name))


def _rewrite_kill(kill: Kill) -> Kill:
    return Kill(
        killer_id=kill.killer_id,
        victim_id=kill.victim_id,
        weapon=_rewrite_weapon(kill.weapon),
        tick_ms=kill.tick_ms,
        headshot=kill.headshot,
        wallbang=kill.wallbang,
        noscope=kill.noscope,
        through_smoke=kill.through_smoke,
        assisted_by=kill.assisted_by,
    )


def _rewrite_damage(event: DamageEvent) -> DamageEvent:
    return DamageEvent(
        attacker_id=event.attacker_id,
        victim_id=event.victim_id,
        weapon=_rewrite_weapon(event.weapon),
        damage=event.damage,
        tick_ms=event.tick_ms,
        hitgroup=event.hitgroup,
        armor_damage=event.armor_damage,
    )


def _rewrite_inventory(inv: InventorySnapshot) -> InventorySnapshot:
    return InventorySnapshot(
        player_id=inv.player_id,
        cash=inv.cash,
        equipment_value=inv.equipment_value,
        primary=_rewrite_weapon(inv.primary) if inv.primary else None,
        secondary=_rewrite_weapon(inv.secondary) if inv.secondary else None,
        armor=inv.armor,
        helmet=inv.helmet,
        defuse_kit=inv.defuse_kit,
        grenades=[rewrite_weapon_name(g) for g in inv.grenades],
    )


def _rewrite_round(round_: Round) -> Round:
    return Round(
        number=round_.number,
        winner=round_.winner,
        win_reason=round_.win_reason,
        bomb_planted=round_.bomb_planted,
        inventories=[_rewrite_inventory(i) for i in round_.inventories],
        kills=[_rewrite_kill(k) for k in round_.kills],
        damage=[_rewrite_damage(d) for d in round_.damage],
        utility=list(round_.utility),
        survivors=list(round_.survivors),
        duration_ms=round_.duration_ms,
    )


def migrate_match_to_cs2(match: Match) -> Match:
    """Return a new Match with edition=CS2 and canonical weapon names."""
    # deepcopy not strictly needed because we rebuild, but keeps intent clear
    _ = deepcopy
    return Match(
        match_id=match.match_id,
        map_name=match.map_name,
        edition=GameEdition.CS2,
        team_ct_name=match.team_ct_name,
        team_t_name=match.team_t_name,
        players=list(match.players),
        rounds=[_rewrite_round(r) for r in match.rounds],
        series_score=match.series_score,
        event_name=match.event_name,
        played_at=match.played_at,
    )


def migrate_if_csgo(match: Match) -> Match:
    if match.edition is GameEdition.CS2:
        return match
    return migrate_match_to_cs2(match)
