"""Side economy + combat join tables for half and buy contexts."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.economy.classify import classify_team_buy
from roundwire.economy.pistol import is_pistol_round
from roundwire.models.buy_type import BuyType
from roundwire.models.match import Match
from roundwire.models.team import TeamSide
from roundwire.players.profile import build_player_profile
from roundwire.rules.mr_rules import half_length
from roundwire.stats.aggregates import mean, safe_div
from roundwire.types import PlayerId


@dataclass(frozen=True, slots=True)
class ContextStat:
    label: str
    rounds: int
    kills: float
    adr: float
    win_rate: float

    def to_dict(self) -> dict[str, object]:
        return {
            "label": self.label,
            "rounds": self.rounds,
            "kills": round(self.kills, 2),
            "adr": round(self.adr, 1),
            "win_rate": round(self.win_rate, 3),
        }


def _context_for_rounds(
    match: Match,
    player_id: PlayerId,
    rounds,
    label: str,
) -> ContextStat:
    player = match.player_map()[player_id]
    kills = damage = wins = 0
    for rnd in rounds:
        kills += len(rnd.kills_for(player_id))
        damage += rnd.damage_dealt_by(player_id)
        if rnd.winner is player.team:
            wins += 1
    n = len(list(rounds)) if not isinstance(rounds, list) else len(rounds)
    # rounds may be generator consumed — fix by using list
    return ContextStat(
        label=label,
        rounds=n,
        kills=safe_div(float(kills), float(n)),
        adr=safe_div(float(damage), float(n)),
        win_rate=safe_div(float(wins), float(n)),
    )


def buy_context_stats(match: Match, player_id: PlayerId) -> list[ContextStat]:
    player = match.player_map()[player_id]
    buckets: dict[str, list] = {}
    for rnd in match.rounds:
        buy = classify_team_buy(rnd, match, player.team).value
        buckets.setdefault(buy, []).append(rnd)
    return [
        _context_for_rounds(match, player_id, rounds, f"buy:{buy}")
        for buy, rounds in sorted(buckets.items())
    ]


def half_context_stats(match: Match, player_id: PlayerId) -> list[ContextStat]:
    half = half_length(match.edition)
    first = match.rounds[:half]
    second = match.rounds[half:]
    return [
        _context_for_rounds(match, player_id, first, "half:first"),
        _context_for_rounds(match, player_id, second, "half:second"),
    ]


def pistol_context_stats(match: Match, player_id: PlayerId) -> ContextStat:
    pistols = [rnd for rnd in match.rounds if is_pistol_round(rnd, match.edition)]
    return _context_for_rounds(match, player_id, pistols, "pistol")


def context_report(match: Match, player_id: PlayerId) -> dict[str, object]:
    profile = build_player_profile(match, player_id)
    return {
        "player": profile.name,
        "team": profile.team,
        "buys": [c.to_dict() for c in buy_context_stats(match, player_id)],
        "halves": [c.to_dict() for c in half_context_stats(match, player_id)],
        "pistol": pistol_context_stats(match, player_id).to_dict(),
    }


def team_buy_win_table(match: Match) -> list[dict[str, object]]:
    rows = []
    for side in (TeamSide.CT, TeamSide.T):
        for buy in BuyType:
            rounds = [
                rnd
                for rnd in match.rounds
                if classify_team_buy(rnd, match, side) is buy
            ]
            if not rounds:
                continue
            wins = sum(1 for rnd in rounds if rnd.winner is side)
            rows.append(
                {
                    "side": side.value,
                    "buy": buy.value,
                    "rounds": len(rounds),
                    "wins": wins,
                    "win_rate": wins / len(rounds),
                }
            )
    return rows


def clutch_by_buy(match: Match, player_id: PlayerId) -> dict[str, float]:
    from roundwire.players.clutch_book import clutch_cases

    player = match.player_map()[player_id]
    buckets: dict[str, list[bool]] = {}
    for case in clutch_cases(match, player_id, max_allies=2):
        rnd = match.round_by_number(case.round_number)
        if rnd is None:
            continue
        buy = classify_team_buy(rnd, match, player.team).value
        buckets.setdefault(buy, []).append(case.won)
    return {buy: mean([1.0 if w else 0.0 for w in wins]) for buy, wins in buckets.items()}
