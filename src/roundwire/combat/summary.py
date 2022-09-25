"""Per-player combat summary lines."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.combat.adr import adr_for_player
from roundwire.combat.headshot import headshot_pct
from roundwire.combat.kd import assist_count, death_count, kill_count, kd_ratio
from roundwire.combat.multikill import multi_kill_count
from roundwire.combat.opening import opening_kills_for
from roundwire.combat.survival import survival_rate
from roundwire.models.match import Match
from roundwire.types import PlayerId


@dataclass(frozen=True, slots=True)
class CombatLine:
    player_id: str
    name: str
    team: str
    kills: int
    deaths: int
    assists: int
    adr: float
    kd: float
    hs_pct: float
    opening_kills: int
    multi_kills: int
    survival: float


def combat_line(match: Match, player_id: PlayerId) -> CombatLine:
    player = match.player_map()[player_id]
    return CombatLine(
        player_id=str(player_id),
        name=player.name,
        team=player.team.value,
        kills=kill_count(match, player_id),
        deaths=death_count(match, player_id),
        assists=assist_count(match, player_id),
        adr=adr_for_player(match, player_id),
        kd=kd_ratio(match, player_id),
        hs_pct=headshot_pct(match, player_id),
        opening_kills=opening_kills_for(match, player_id),
        multi_kills=multi_kill_count(match, player_id),
        survival=survival_rate(match, player_id),
    )


def combat_summary(match: Match) -> list[CombatLine]:
    lines = [combat_line(match, p.player_id) for p in match.players]
    return sorted(lines, key=lambda row: (-row.kills, -row.adr, row.name))

def team_combat_totals(match: Match) -> dict[str, dict[str, float]]:
    """Aggregate K/D/ADR by side."""
    from roundwire.models.team import TeamSide

    out: dict[str, dict[str, float]] = {}
    for side in (TeamSide.CT, TeamSide.T):
        lines = [combat_line(match, p.player_id) for p in match.players_on(side)]
        if not lines:
            out[side.value] = {"kills": 0, "deaths": 0, "adr": 0.0}
            continue
        out[side.value] = {
            "kills": float(sum(l.kills for l in lines)),
            "deaths": float(sum(l.deaths for l in lines)),
            "adr": sum(l.adr for l in lines) / len(lines),
        }
    return out


def scoreboard_sort_key(line: CombatLine) -> tuple[float, float, str]:
    return (-float(line.kills), -line.adr, line.name)


def format_combat_line(line: CombatLine) -> str:
    return (
        f"{line.name} ({line.team}) {line.kills}/{line.deaths}/{line.assists} "
        f"ADR {line.adr:.1f} K/D {line.kd:.2f} HS {line.hs_pct*100:.0f}%"
    )


def leaders(match: Match, metric: str = "kills", n: int = 3) -> list[CombatLine]:
    lines = combat_summary(match)
    key_map = {
        "kills": lambda l: l.kills,
        "adr": lambda l: l.adr,
        "kd": lambda l: l.kd,
        "opening": lambda l: l.opening_kills,
    }
    key = key_map.get(metric, key_map["kills"])
    return sorted(lines, key=lambda l: (-float(key(l)), l.name))[: max(0, n)]
