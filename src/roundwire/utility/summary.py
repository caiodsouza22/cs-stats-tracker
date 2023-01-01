"""Utility summary rows for reports."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.models.match import Match
from roundwire.utility.flashes import enemies_flashed_total, teammates_flashed_total
from roundwire.utility.he import he_damage, he_throws
from roundwire.utility.molotov import fire_damage, fire_throws
from roundwire.utility.smoke import smoke_count
from roundwire.utility.usage import utility_counts


@dataclass(frozen=True, slots=True)
class UtilityLine:
    player_id: str
    name: str
    flashes: int
    smokes: int
    hes: int
    fires: int
    enemies_flashed: int
    team_flashed: int
    he_damage: int
    fire_damage: int


def utility_summary(match: Match) -> list[UtilityLine]:
    lines: list[UtilityLine] = []
    for player in match.players:
        counts = utility_counts(match, player.player_id)
        lines.append(
            UtilityLine(
                player_id=str(player.player_id),
                name=player.name,
                flashes=counts.get("flash", 0),
                smokes=smoke_count(match, player.player_id),
                hes=he_throws(match, player.player_id),
                fires=fire_throws(match, player.player_id),
                enemies_flashed=enemies_flashed_total(match, player.player_id),
                team_flashed=teammates_flashed_total(match, player.player_id),
                he_damage=he_damage(match, player.player_id),
                fire_damage=fire_damage(match, player.player_id),
            )
        )
    return sorted(lines, key=lambda r: (-r.enemies_flashed, -r.flashes, r.name))


def format_utility_line(line: UtilityLine) -> str:
    return (
        f"{line.name}: flash={line.flashes} smoke={line.smokes} he={line.hes} "
        f"fire={line.fires} enemies_flashed={line.enemies_flashed} "
        f"he_dmg={line.he_damage} fire_dmg={line.fire_damage}"
    )


def top_flashers(match: Match, n: int = 3) -> list[UtilityLine]:
    return utility_summary(match)[: max(0, n)]
