"""Clutch and low-number situation book for a player."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.models.match import Match
from roundwire.models.team import TeamSide
from roundwire.types import PlayerId


@dataclass(frozen=True, slots=True)
class ClutchCase:
    round_number: int
    alive_allies: int
    alive_enemies_proxy: int
    won: bool
    kills_in_round: int
    bomb_planted: bool
    win_reason: str

    def to_dict(self) -> dict[str, object]:
        return {
            "round": self.round_number,
            "alive_allies": self.alive_allies,
            "alive_enemies_proxy": self.alive_enemies_proxy,
            "won": self.won,
            "kills_in_round": self.kills_in_round,
            "bomb_planted": self.bomb_planted,
            "win_reason": self.win_reason,
        }


def _alive(match: Match, survivors: list[PlayerId], side: TeamSide) -> list[PlayerId]:
    pmap = match.player_map()
    return [pid for pid in survivors if pid in pmap and pmap[pid].team is side]


def clutch_cases(match: Match, player_id: PlayerId, max_allies: int = 1) -> list[ClutchCase]:
    """Rounds where player is among few survivors on their side at end state.

    Dump format only exposes end-of-round survivors, so this is a post-hoc
    clutch proxy rather than a live 1vX detector.
    """
    player = match.player_map().get(player_id)
    if player is None:
        return []
    out: list[ClutchCase] = []
    for rnd in match.rounds:
        allies = _alive(match, rnd.survivors, player.team)
        if player_id not in allies:
            continue
        if len(allies) > max_allies:
            continue
        enemies = _alive(match, rnd.survivors, player.team.opposite())
        # enemies alive at end is usually 0 on a win; use kills as intensity proxy
        out.append(
            ClutchCase(
                round_number=int(rnd.number),
                alive_allies=len(allies),
                alive_enemies_proxy=max(len(enemies), len(rnd.kills_for(player_id))),
                won=rnd.winner is player.team,
                kills_in_round=len(rnd.kills_for(player_id)),
                bomb_planted=rnd.bomb_planted,
                win_reason=rnd.win_reason,
            )
        )
    return out


def clutch_winrate(match: Match, player_id: PlayerId, max_allies: int = 1) -> float:
    cases = clutch_cases(match, player_id, max_allies=max_allies)
    if not cases:
        return 0.0
    return sum(1 for c in cases if c.won) / len(cases)


def multi_kill_clutches(match: Match, player_id: PlayerId) -> list[ClutchCase]:
    return [c for c in clutch_cases(match, player_id, max_allies=2) if c.kills_in_round >= 2 and c.won]


def post_plant_survivor_wins(match: Match, player_id: PlayerId) -> list[int]:
    player = match.player_map().get(player_id)
    if player is None:
        return []
    out: list[int] = []
    for rnd in match.rounds:
        if not rnd.bomb_planted:
            continue
        if player_id not in rnd.survivors:
            continue
        if rnd.winner is player.team:
            out.append(int(rnd.number))
    return out


def clutch_book(match: Match, player_id: PlayerId) -> dict[str, object]:
    cases = clutch_cases(match, player_id, max_allies=2)
    solo = [c for c in cases if c.alive_allies == 1]
    return {
        "cases": [c.to_dict() for c in cases],
        "solo_cases": len(solo),
        "solo_wins": sum(1 for c in solo if c.won),
        "solo_wr": (sum(1 for c in solo if c.won) / len(solo)) if solo else 0.0,
        "multi_kill_clutches": [c.to_dict() for c in multi_kill_clutches(match, player_id)],
        "post_plant_survivor_wins": post_plant_survivor_wins(match, player_id),
    }
