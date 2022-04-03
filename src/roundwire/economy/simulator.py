"""Lightweight round-to-round money simulator from dump inventories + outcomes."""

from __future__ import annotations

from dataclasses import dataclass, field

from roundwire.models.edition import GameEdition
from roundwire.models.match import Match
from roundwire.models.team import TeamSide
from roundwire.rules.economy_constants import constants_for
from roundwire.rules.kill_rewards import kill_reward_for
from roundwire.rules.money_awards import win_bonus
from roundwire.rules.loss_bonus import consecutive_losses_before


@dataclass
class PlayerLedger:
    player_id: str
    side: str
    cash: int = 800
    history: list[int] = field(default_factory=list)

    def snapshot(self) -> None:
        self.history.append(self.cash)


@dataclass
class MoneySimResult:
    ledgers: dict[str, PlayerLedger]
    team_cash_by_round: list[dict[str, int]]


def _clamp_money(value: int, edition: GameEdition) -> int:
    consts = constants_for(edition)
    return max(0, min(consts.max_money, value))


def simulate_team_cash(match: Match) -> MoneySimResult:
    """
    Approximate cash trajectory.

    Uses starting money, loss bonus ladder, win awards, and kill rewards.
    Equipment purchases are inferred as equipment_value deltas when inventories exist.
    """
    consts = constants_for(match.edition)
    ledgers: dict[str, PlayerLedger] = {}
    for player in match.players:
        ledgers[str(player.player_id)] = PlayerLedger(
            player_id=str(player.player_id),
            side=player.team.value,
            cash=consts.starting_money,
        )

    team_rows: list[dict[str, int]] = []
    for idx, rnd in enumerate(match.rounds):
        # apply inferred spend from inventory equipment if present
        inv_map = {str(inv.player_id): inv for inv in rnd.inventories}
        for pid, ledger in ledgers.items():
            inv = inv_map.get(pid)
            if inv is not None:
                # treat equipment_value as money already committed this round
                spend = min(ledger.cash, max(0, inv.equipment_value // 5))
                ledger.cash = _clamp_money(ledger.cash - spend, match.edition)

        # kill rewards
        for kill in rnd.kills:
            killer = ledgers.get(str(kill.killer_id))
            if killer is None:
                continue
            killer.cash = _clamp_money(
                killer.cash + kill_reward_for(kill.weapon.name, consts.kill_reward_default),
                match.edition,
            )

        # end-round awards
        for player in match.players:
            ledger = ledgers[str(player.player_id)]
            won = rnd.winner is player.team
            if won:
                ledger.cash = _clamp_money(
                    ledger.cash + win_bonus(rnd.win_reason, player.team),
                    match.edition,
                )
            else:
                streak = consecutive_losses_before(match, idx, player.team)
                steps = consts.loss_bonus_steps
                bonus = steps[max(0, min(streak, len(steps) - 1))]
                ledger.cash = _clamp_money(ledger.cash + bonus, match.edition)
            ledger.snapshot()

        team_rows.append(
            {
                "CT": sum(l.cash for l in ledgers.values() if l.side == "CT"),
                "T": sum(l.cash for l in ledgers.values() if l.side == "T"),
            }
        )

    return MoneySimResult(ledgers=ledgers, team_cash_by_round=team_rows)


def final_team_cash(match: Match) -> dict[str, int]:
    result = simulate_team_cash(match)
    if not result.team_cash_by_round:
        return {"CT": 0, "T": 0}
    return dict(result.team_cash_by_round[-1])


def player_cash_history(match: Match, player_id: str) -> list[int]:
    result = simulate_team_cash(match)
    ledger = result.ledgers.get(player_id)
    return list(ledger.history) if ledger else []
