"""Halftime side-switch helpers."""

from __future__ import annotations

from roundwire.models.edition import GameEdition
from roundwire.models.player import Player
from roundwire.models.team import TeamSide
from roundwire.rules.mr_rules import half_length


def should_switch_sides(round_number: int, edition: GameEdition) -> bool:
    return round_number == half_length(edition) + 1


def switched_players(players: list[Player]) -> list[Player]:
    out: list[Player] = []
    for p in players:
        out.append(
            Player(
                player_id=p.player_id,
                name=p.name,
                team=p.team.opposite(),
                steam_id=p.steam_id,
                country=p.country,
                tags=list(p.tags),
            )
        )
    return out
