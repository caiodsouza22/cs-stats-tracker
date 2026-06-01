"""Per-player economy participation and spend patterns."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.economy.classify import classify_team_buy
from roundwire.economy.equipment import inventory_for_player
from roundwire.economy.pistol import is_pistol_round
from roundwire.models.buy_type import BuyType
from roundwire.models.match import Match
from roundwire.stats.aggregates import mean, safe_div
from roundwire.types import PlayerId


@dataclass(slots=True)
class PlayerEconomyProfile:
    player_id: str
    avg_equipment: float
    avg_cash: float
    max_equipment: int
    min_equipment: int
    full_buy_wins: int
    full_buy_losses: int
    eco_wins: int
    force_wins: int
    pistol_wins: int
    rounds_with_armor: int
    rounds_with_helmet: int
    rounds_with_kit: int
    avg_grenade_count: float
    spend_intensity: float

    def to_dict(self) -> dict[str, object]:
        return {
            "player_id": self.player_id,
            "avg_equipment": round(self.avg_equipment, 1),
            "avg_cash": round(self.avg_cash, 1),
            "max_equipment": self.max_equipment,
            "min_equipment": self.min_equipment,
            "full_buy_wins": self.full_buy_wins,
            "full_buy_losses": self.full_buy_losses,
            "eco_wins": self.eco_wins,
            "force_wins": self.force_wins,
            "pistol_wins": self.pistol_wins,
            "rounds_with_armor": self.rounds_with_armor,
            "rounds_with_helmet": self.rounds_with_helmet,
            "rounds_with_kit": self.rounds_with_kit,
            "avg_grenade_count": round(self.avg_grenade_count, 2),
            "spend_intensity": round(self.spend_intensity, 3),
            "full_buy_wr": round(
                safe_div(
                    float(self.full_buy_wins),
                    float(self.full_buy_wins + self.full_buy_losses),
                ),
                3,
            ),
        }


def build_economy_profile(match: Match, player_id: PlayerId) -> PlayerEconomyProfile:
    player = match.player_map()[player_id]
    equipment_vals: list[float] = []
    cash_vals: list[float] = []
    grenade_counts: list[float] = []
    full_wins = full_losses = eco_wins = force_wins = pistol_wins = 0
    armor = helmet = kit = 0

    for rnd in match.rounds:
        inv = inventory_for_player(rnd, str(player_id))
        team_buy = classify_team_buy(rnd, match, player.team)
        won = rnd.winner is player.team
        if inv is not None:
            equipment_vals.append(float(inv.equipment_value))
            cash_vals.append(float(inv.cash))
            grenade_counts.append(float(len(inv.grenades)))
            if inv.armor:
                armor += 1
            if inv.helmet:
                helmet += 1
            if inv.defuse_kit:
                kit += 1
        if team_buy is BuyType.FULL:
            if won:
                full_wins += 1
            else:
                full_losses += 1
        elif team_buy is BuyType.ECO and won:
            eco_wins += 1
        elif team_buy is BuyType.FORCE and won:
            force_wins += 1
        if is_pistol_round(rnd, match.edition) and won:
            pistol_wins += 1

    avg_eq = mean(equipment_vals)
    # intensity: share of rounds above team-ish full threshold (~4000)
    intense = sum(1 for v in equipment_vals if v >= 3500)
    spend_intensity = safe_div(float(intense), float(len(equipment_vals) or 1))

    return PlayerEconomyProfile(
        player_id=str(player_id),
        avg_equipment=avg_eq,
        avg_cash=mean(cash_vals),
        max_equipment=int(max(equipment_vals)) if equipment_vals else 0,
        min_equipment=int(min(equipment_vals)) if equipment_vals else 0,
        full_buy_wins=full_wins,
        full_buy_losses=full_losses,
        eco_wins=eco_wins,
        force_wins=force_wins,
        pistol_wins=pistol_wins,
        rounds_with_armor=armor,
        rounds_with_helmet=helmet,
        rounds_with_kit=kit,
        avg_grenade_count=mean(grenade_counts),
        spend_intensity=spend_intensity,
    )


def equipment_series(match: Match, player_id: PlayerId) -> list[int]:
    out: list[int] = []
    for rnd in match.rounds:
        inv = inventory_for_player(rnd, str(player_id))
        out.append(inv.equipment_value if inv else 0)
    return out


def cash_series(match: Match, player_id: PlayerId) -> list[int]:
    out: list[int] = []
    for rnd in match.rounds:
        inv = inventory_for_player(rnd, str(player_id))
        out.append(inv.cash if inv else 0)
    return out


def buy_outcome_matrix(match: Match, player_id: PlayerId) -> dict[str, dict[str, int]]:
    """Wins/losses keyed by the player's team buy type that round."""
    player = match.player_map()[player_id]
    matrix: dict[str, dict[str, int]] = {}
    for rnd in match.rounds:
        buy = classify_team_buy(rnd, match, player.team).value
        bucket = matrix.setdefault(buy, {"wins": 0, "losses": 0})
        if rnd.winner is player.team:
            bucket["wins"] += 1
        else:
            bucket["losses"] += 1
    return matrix


def underbought_wins(match: Match, player_id: PlayerId) -> list[int]:
    """Rounds won while team was eco/force (potential upset participation)."""
    player = match.player_map()[player_id]
    out: list[int] = []
    for rnd in match.rounds:
        buy = classify_team_buy(rnd, match, player.team)
        if buy in {BuyType.ECO, BuyType.FORCE} and rnd.winner is player.team:
            out.append(int(rnd.number))
    return out


def overinvested_losses(match: Match, player_id: PlayerId, threshold: int = 4000) -> list[int]:
    player = match.player_map()[player_id]
    out: list[int] = []
    for rnd in match.rounds:
        inv = inventory_for_player(rnd, str(player_id))
        if inv is None:
            continue
        if inv.equipment_value >= threshold and rnd.winner is not player.team:
            out.append(int(rnd.number))
    return out
