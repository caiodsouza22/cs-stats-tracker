"""Matchup sheets: player vs opposing roster."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.combat.duels import head_to_head
from roundwire.models.match import Match
from roundwire.models.team import TeamSide
from roundwire.players.profile import build_player_profile
from roundwire.types import PlayerId


@dataclass(frozen=True, slots=True)
class MatchupRow:
    opponent_id: str
    opponent_name: str
    kills: int
    deaths: int
    kd: float

    def to_dict(self) -> dict[str, object]:
        return {
            "opponent_id": self.opponent_id,
            "opponent_name": self.opponent_name,
            "kills": self.kills,
            "deaths": self.deaths,
            "kd": round(self.kd, 3),
        }


def matchup_sheet(match: Match, player_id: PlayerId) -> list[MatchupRow]:
    player = match.player_map()[player_id]
    rows: list[MatchupRow] = []
    for opponent in match.players:
        if opponent.team is player.team:
            continue
        duel = head_to_head(match, player_id, opponent.player_id)
        # duel.a_wins is for first arg
        kills = duel.a_wins
        deaths = duel.b_wins
        kd = float(kills) if deaths == 0 else kills / deaths
        rows.append(
            MatchupRow(
                opponent_id=str(opponent.player_id),
                opponent_name=opponent.name,
                kills=kills,
                deaths=deaths,
                kd=kd,
            )
        )
    return sorted(rows, key=lambda r: (-r.kills, -r.kd, r.opponent_name))


def matchup_table(match: Match, player_id: PlayerId) -> list[dict[str, object]]:
    return [row.to_dict() for row in matchup_sheet(match, player_id)]


def best_matchup(match: Match, player_id: PlayerId) -> MatchupRow | None:
    rows = matchup_sheet(match, player_id)
    if not rows:
        return None
    return max(rows, key=lambda r: (r.kills - r.deaths, r.kd, r.kills))


def worst_matchup(match: Match, player_id: PlayerId) -> MatchupRow | None:
    rows = matchup_sheet(match, player_id)
    if not rows:
        return None
    return min(rows, key=lambda r: (r.kills - r.deaths, r.kd, -r.deaths))


def team_matchup_matrix(match: Match) -> list[dict[str, object]]:
    """Compact CT vs T kill matrix by player names."""
    cts = match.players_on(TeamSide.CT)
    ts = match.players_on(TeamSide.T)
    rows = []
    for ct in cts:
        for t in ts:
            duel = head_to_head(match, ct.player_id, t.player_id)
            rows.append(
                {
                    "ct": ct.name,
                    "t": t.name,
                    "ct_kills": duel.a_wins,
                    "t_kills": duel.b_wins,
                }
            )
    return rows


def soft_target(match: Match, player_id: PlayerId) -> str | None:
    """Opponent this player farmed the most."""
    best = best_matchup(match, player_id)
    return best.opponent_name if best and best.kills > 0 else None


def problem_opponent(match: Match, player_id: PlayerId) -> str | None:
    worst = worst_matchup(match, player_id)
    return worst.opponent_name if worst and worst.deaths > worst.kills else None


def matchup_summary(match: Match, player_id: PlayerId) -> dict[str, object]:
    profile = build_player_profile(match, player_id)
    rows = matchup_sheet(match, player_id)
    return {
        "player": profile.name,
        "team": profile.team,
        "rows": [r.to_dict() for r in rows],
        "soft_target": soft_target(match, player_id),
        "problem_opponent": problem_opponent(match, player_id),
        "plus_minus": sum(r.kills - r.deaths for r in rows),
    }
