"""Advanced combat aggregates built from core primitives."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.combat.adr import adr_by_player, adr_for_player
from roundwire.combat.first_blood import opening_conversion, opening_conversion_for_side
from roundwire.combat.headshot import headshot_pct
from roundwire.combat.kast import kast_pct
from roundwire.combat.kd import assist_count, death_count, kill_count, kd_ratio, kpr
from roundwire.combat.multikill import ace_rounds, multi_kill_count
from roundwire.combat.opening import opening_deaths_for, opening_kills_for
from roundwire.combat.survival import survival_rate
from roundwire.combat.trades import all_trades
from roundwire.combat.weapons_usage import favorite_weapon, weapon_kills
from roundwire.models.match import Match
from roundwire.models.team import TeamSide
from roundwire.types import PlayerId


@dataclass(frozen=True, slots=True)
class AdvancedCombatCard:
    player_id: str
    name: str
    team: str
    kills: int
    deaths: int
    assists: int
    kd: float
    kpr: float
    adr: float
    hs_pct: float
    kast: float
    survival: float
    opening_kills: int
    opening_deaths: int
    multi_kills: int
    aces: int
    favorite_weapon: str | None
    trade_participations: int


def trade_participations(match: Match, player_id: PlayerId) -> int:
    total = 0
    for trade in all_trades(match):
        if trade.original.killer_id == player_id or trade.trade.killer_id == player_id:
            total += 1
    return total


def advanced_card(match: Match, player_id: PlayerId) -> AdvancedCombatCard:
    player = match.player_map()[player_id]
    return AdvancedCombatCard(
        player_id=str(player_id),
        name=player.name,
        team=player.team.value,
        kills=kill_count(match, player_id),
        deaths=death_count(match, player_id),
        assists=assist_count(match, player_id),
        kd=kd_ratio(match, player_id),
        kpr=kpr(match, player_id),
        adr=adr_for_player(match, player_id),
        hs_pct=headshot_pct(match, player_id),
        kast=kast_pct(match, player_id),
        survival=survival_rate(match, player_id),
        opening_kills=opening_kills_for(match, player_id),
        opening_deaths=opening_deaths_for(match, player_id),
        multi_kills=multi_kill_count(match, player_id),
        aces=len(ace_rounds(match, player_id)),
        favorite_weapon=favorite_weapon(match, player_id),
        trade_participations=trade_participations(match, player_id),
    )


def advanced_cards(match: Match) -> list[AdvancedCombatCard]:
    cards = [advanced_card(match, p.player_id) for p in match.players]
    return sorted(cards, key=lambda c: (-c.kills, -c.adr, c.name))


def team_advanced_summary(match: Match, side: TeamSide) -> dict[str, float]:
    cards = [advanced_card(match, p.player_id) for p in match.players_on(side)]
    if not cards:
        return {
            "kills": 0.0,
            "adr": 0.0,
            "kast": 0.0,
            "opening_kills": 0.0,
            "opening_conversion": opening_conversion_for_side(match, side),
        }
    return {
        "kills": float(sum(c.kills for c in cards)),
        "adr": sum(c.adr for c in cards) / len(cards),
        "kast": sum(c.kast for c in cards) / len(cards),
        "opening_kills": float(sum(c.opening_kills for c in cards)),
        "opening_conversion": opening_conversion_for_side(match, side),
    }


def match_combat_dashboard(match: Match) -> dict[str, object]:
    return {
        "adr": adr_by_player(match),
        "opening_conversion": opening_conversion(match),
        "weapon_kills": weapon_kills(match),
        "ct": team_advanced_summary(match, TeamSide.CT),
        "t": team_advanced_summary(match, TeamSide.T),
        "players": [
            {
                "player_id": c.player_id,
                "name": c.name,
                "team": c.team,
                "kills": c.kills,
                "deaths": c.deaths,
                "adr": c.adr,
                "kast": c.kast,
            }
            for c in advanced_cards(match)
        ],
    }
