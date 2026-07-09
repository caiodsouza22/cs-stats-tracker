"""Weapon economy: cost efficiency and kill value by catalog prices."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from roundwire.models.match import Match
from roundwire.players.weapon_stats import weapon_breakdown
from roundwire.rules.weapon_aliases import WEAPON_CATALOG, canonical_weapon_name, weapon_cost
from roundwire.stats.aggregates import safe_div
from roundwire.types import PlayerId


@dataclass(frozen=True, slots=True)
class WeaponValueLine:
    weapon: str
    kills: int
    cost: int
    spend_proxy: int
    value_per_kill: float
    kills_per_buy_proxy: float

    def to_dict(self) -> dict[str, object]:
        return {
            "weapon": self.weapon,
            "kills": self.kills,
            "cost": self.cost,
            "spend_proxy": self.spend_proxy,
            "value_per_kill": round(self.value_per_kill, 2),
            "kills_per_buy_proxy": round(self.kills_per_buy_proxy, 3),
        }


def _canon(name: str) -> str:
    try:
        return canonical_weapon_name(name)
    except KeyError:
        return name.lower()


def weapon_value_table(match: Match, player_id: PlayerId) -> list[WeaponValueLine]:
    breakdown = weapon_breakdown(match, player_id)
    lines: list[WeaponValueLine] = []
    for line in breakdown.lines:
        try:
            cost = weapon_cost(line.weapon)
        except KeyError:
            cost = 0
        # proxy: assume one "buy" per distinct round the weapon got a kill
        rounds_used = set()
        for rnd in match.rounds:
            if any(_canon(k.weapon.name) == line.weapon for k in rnd.kills_for(player_id)):
                rounds_used.add(int(rnd.number))
        buys = max(1, len(rounds_used))
        spend = cost * buys
        lines.append(
            WeaponValueLine(
                weapon=line.weapon,
                kills=line.kills,
                cost=cost,
                spend_proxy=spend,
                value_per_kill=safe_div(float(spend), float(line.kills)),
                kills_per_buy_proxy=safe_div(float(line.kills), float(buys)),
            )
        )
    return sorted(lines, key=lambda l: (-l.kills, l.weapon))


def team_weapon_spend_proxy(match: Match) -> dict[str, int]:
    totals = {"CT": 0, "T": 0}
    for player in match.players:
        for line in weapon_value_table(match, player.player_id):
            totals[player.team.value] += line.spend_proxy
    return totals


def cheapest_kills(match: Match, player_id: PlayerId, n: int = 5) -> list[WeaponValueLine]:
    lines = [line for line in weapon_value_table(match, player_id) if line.kills > 0]
    return sorted(lines, key=lambda l: (l.value_per_kill, -l.kills))[: max(0, n)]


def rifle_vs_eco_weapon_mix(match: Match, player_id: PlayerId) -> dict[str, float]:
    from roundwire.economy.classify import classify_team_buy
    from roundwire.models.buy_type import BuyType

    player = match.player_map()[player_id]
    rifle = eco = other = 0
    for rnd in match.rounds:
        buy = classify_team_buy(rnd, match, player.team)
        for kill in rnd.kills_for(player_id):
            weapon = _canon(kill.weapon.name)
            meta = WEAPON_CATALOG.get(weapon, {})
            slot = str(meta.get("slot", "unknown"))
            if buy is BuyType.FULL and slot == "rifle":
                rifle += 1
            elif buy in {BuyType.ECO, BuyType.FORCE} and slot in {"pistol", "smg", "shotgun"}:
                eco += 1
            else:
                other += 1
    total = rifle + eco + other
    return {
        "rifle_on_full": safe_div(float(rifle), float(total)),
        "eco_weapons": safe_div(float(eco), float(total)),
        "other": safe_div(float(other), float(total)),
    }


def awp_investment_rounds(match: Match, player_id: PlayerId) -> list[int]:
    out = []
    for rnd in match.rounds:
        invs = [inv for inv in rnd.inventories if inv.player_id == player_id]
        for inv in invs:
            if inv.primary and _canon(inv.primary.name) == "awp":
                out.append(int(rnd.number))
                break
    return out


def kill_reward_estimate(match: Match, player_id: PlayerId) -> int:
    from roundwire.rules.kill_rewards import kill_reward_for

    total = 0
    for rnd in match.rounds:
        for kill in rnd.kills_for(player_id):
            total += kill_reward_for(kill.weapon.name)
    return total


def weapon_slot_efficiency(match: Match, player_id: PlayerId) -> dict[str, dict[str, float]]:
    slots: dict[str, dict[str, float]] = defaultdict(lambda: {"kills": 0.0, "spend": 0.0})
    for line in weapon_value_table(match, player_id):
        meta = WEAPON_CATALOG.get(line.weapon, {})
        slot = str(meta.get("slot", "unknown"))
        slots[slot]["kills"] += line.kills
        slots[slot]["spend"] += line.spend_proxy
    out = {}
    for slot, vals in slots.items():
        out[slot] = {
            "kills": vals["kills"],
            "spend": vals["spend"],
            "spend_per_kill": safe_div(vals["spend"], vals["kills"]),
        }
    return out
