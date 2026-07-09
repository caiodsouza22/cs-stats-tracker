"""Narrative money story for a single player across the match."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.economy.equipment import inventory_for_player
from roundwire.economy.simulator import player_cash_history
from roundwire.models.match import Match
from roundwire.players.economy_profile import buy_outcome_matrix, cash_series, equipment_series
from roundwire.stats.aggregates import mean
from roundwire.stats.rolling import ema, slope
from roundwire.types import PlayerId


@dataclass(frozen=True, slots=True)
class MoneyBeat:
    round_number: int
    equipment: int
    cash: int
    note: str

    def to_dict(self) -> dict[str, object]:
        return {
            "round": self.round_number,
            "equipment": self.equipment,
            "cash": self.cash,
            "note": self.note,
        }


def money_beats(match: Match, player_id: PlayerId) -> list[MoneyBeat]:
    eq = equipment_series(match, player_id)
    cash = cash_series(match, player_id)
    beats: list[MoneyBeat] = []
    for idx, rnd in enumerate(match.rounds):
        e = eq[idx] if idx < len(eq) else 0
        c = cash[idx] if idx < len(cash) else 0
        note = "standard"
        if e >= 4500:
            note = "full_load"
        elif e <= 1000:
            note = "saved"
        elif 2000 <= e < 3500:
            note = "force_ish"
        if idx > 0 and e >= eq[idx - 1] + 2500:
            note = "rebuy_spike"
        if idx > 0 and e + 2000 <= eq[idx - 1]:
            note = "save_drop"
        beats.append(MoneyBeat(int(rnd.number), e, c, note))
    return beats


def money_story(match: Match, player_id: PlayerId) -> dict[str, object]:
    beats = money_beats(match, player_id)
    eq = [float(b.equipment) for b in beats]
    simulated = player_cash_history(match, str(player_id))
    return {
        "player_id": str(player_id),
        "beats": [b.to_dict() for b in beats],
        "avg_equipment": round(mean(eq), 1),
        "equipment_slope": round(slope(eq), 3),
        "ema_equipment": [round(v, 1) for v in ema(eq, alpha=0.35)],
        "buy_matrix": buy_outcome_matrix(match, player_id),
        "simulated_cash": simulated,
        "notes": {
            "full_load": sum(1 for b in beats if b.note == "full_load"),
            "saved": sum(1 for b in beats if b.note == "saved"),
            "force_ish": sum(1 for b in beats if b.note == "force_ish"),
            "rebuy_spike": sum(1 for b in beats if b.note == "rebuy_spike"),
            "save_drop": sum(1 for b in beats if b.note == "save_drop"),
        },
    }


def poorest_round(match: Match, player_id: PlayerId) -> MoneyBeat | None:
    beats = money_beats(match, player_id)
    if not beats:
        return None
    return min(beats, key=lambda b: (b.equipment + b.cash, b.round_number))


def richest_round(match: Match, player_id: PlayerId) -> MoneyBeat | None:
    beats = money_beats(match, player_id)
    if not beats:
        return None
    return max(beats, key=lambda b: (b.equipment + b.cash, -b.round_number))


def inventory_flags(match: Match, player_id: PlayerId) -> list[dict[str, object]]:
    rows = []
    for rnd in match.rounds:
        inv = inventory_for_player(rnd, str(player_id))
        if inv is None:
            rows.append({"round": int(rnd.number), "missing": True})
            continue
        rows.append(
            {
                "round": int(rnd.number),
                "missing": False,
                "armor": inv.armor,
                "helmet": inv.helmet,
                "kit": inv.defuse_kit,
                "primary": inv.primary.name if inv.primary else None,
                "grenades": list(inv.grenades),
                "equipment_value": inv.equipment_value,
                "cash": inv.cash,
            }
        )
    return rows
