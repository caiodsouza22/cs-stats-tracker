"""Economy swing narratives for whole match and players."""

from __future__ import annotations

from roundwire.economy.bank import bank_trajectory, compare_banks
from roundwire.economy.classify import classify_round_buy
from roundwire.models.buy_type import BuyType
from roundwire.models.match import Match
from roundwire.models.team import TeamSide
from roundwire.players.money_story import money_story
from roundwire.stats.aggregates import mean


def economy_swing_report(match: Match) -> dict[str, object]:
    banks = compare_banks(match)
    gaps = [abs(ct - t) for _n, ct, t in banks]
    full_vs_eco = []
    for rnd in match.rounds:
        buys = classify_round_buy(rnd, match)
        if buys["CT"] is BuyType.FULL and buys["T"] is BuyType.ECO:
            full_vs_eco.append({"round": int(rnd.number), "favored": "CT", "converted": rnd.winner is TeamSide.CT})
        elif buys["T"] is BuyType.FULL and buys["CT"] is BuyType.ECO:
            full_vs_eco.append({"round": int(rnd.number), "favored": "T", "converted": rnd.winner is TeamSide.T})
    return {
        "avg_bank_gap": round(mean([float(g) for g in gaps]), 1) if gaps else 0.0,
        "max_bank_gap": max(gaps) if gaps else 0,
        "full_vs_eco": full_vs_eco,
        "ct_trajectory": [s.to_dict() if hasattr(s, "to_dict") else {
            "round": s.round_number, "cash": s.cash, "equipment": s.equipment
        } for s in bank_trajectory(match, TeamSide.CT)],
        "t_trajectory": [{
            "round": s.round_number, "cash": s.cash, "equipment": s.equipment
        } for s in bank_trajectory(match, TeamSide.T)],
    }


def player_economy_briefs(match: Match) -> list[dict[str, object]]:
    rows = []
    for player in match.players:
        story = money_story(match, player.player_id)
        rows.append(
            {
                "name": player.name,
                "team": player.team.value,
                "avg_equipment": story["avg_equipment"],
                "notes": story["notes"],
                "equipment_slope": story["equipment_slope"],
            }
        )
    return sorted(rows, key=lambda r: (-float(r["avg_equipment"]), r["name"]))


def loss_bonus_pressure(match: Match) -> list[dict[str, object]]:
    from roundwire.economy.loss_bonus import streak_lengths

    rows = []
    for side in (TeamSide.CT, TeamSide.T):
        streaks = streak_lengths(match, side)
        rows.append(
            {
                "side": side.value,
                "max_streak": max(streaks) if streaks else 0,
                "avg_streak": round(mean([float(s) for s in streaks]), 2) if streaks else 0.0,
                "series": streaks,
            }
        )
    return rows
