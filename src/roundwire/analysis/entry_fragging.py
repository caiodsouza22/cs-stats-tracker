"""Entry fragging and first-contact analytics by player."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.combat.opening import opening_duels
from roundwire.models.match import Match
from roundwire.stats.aggregates import safe_div
from roundwire.types import PlayerId


@dataclass(frozen=True, slots=True)
class EntryCard:
    player_id: str
    name: str
    team: str
    attempts: int
    successes: int
    traded_for: int
    converted: int
    success_rate: float
    trade_rate: float
    conversion_rate: float

    def to_dict(self) -> dict[str, object]:
        return {
            "player_id": self.player_id,
            "name": self.name,
            "team": self.team,
            "attempts": self.attempts,
            "successes": self.successes,
            "traded_for": self.traded_for,
            "converted": self.converted,
            "success_rate": round(self.success_rate, 3),
            "trade_rate": round(self.trade_rate, 3),
            "conversion_rate": round(self.conversion_rate, 3),
        }


def entry_card(match: Match, player_id: PlayerId) -> EntryCard:
    player = match.player_map()[player_id]
    attempts = successes = traded_for = converted = 0
    pmap = match.player_map()
    for duel in opening_duels(match):
        if duel.kill.killer_id == player_id:
            attempts += 1
            successes += 1
            rnd = match.round_by_number(duel.round_number)
            if rnd is not None and rnd.winner is player.team:
                converted += 1
        elif duel.kill.victim_id == player_id:
            attempts += 1
            if duel.traded:
                traded_for += 1
    return EntryCard(
        player_id=str(player_id),
        name=player.name,
        team=player.team.value,
        attempts=attempts,
        successes=successes,
        traded_for=traded_for,
        converted=converted,
        success_rate=safe_div(float(successes), float(attempts)),
        trade_rate=safe_div(float(traded_for), float(max(1, attempts - successes))),
        conversion_rate=safe_div(float(converted), float(successes)),
    )


def entry_table(match: Match) -> list[dict[str, object]]:
    rows = [entry_card(match, p.player_id).to_dict() for p in match.players]
    return sorted(rows, key=lambda r: (-r["successes"], -r["attempts"], r["name"]))


def best_entry(match: Match) -> EntryCard | None:
    cards = [entry_card(match, p.player_id) for p in match.players]
    if not cards:
        return None
    return max(cards, key=lambda c: (c.successes, c.success_rate, c.name))
