"""Side-by-side scoreboard extensions with rating and role columns."""

from __future__ import annotations

from roundwire.models.match import Match
from roundwire.players.profile import build_all_profiles
from roundwire.players.roles import infer_role
from roundwire.reports.tables import format_table
from roundwire.types import PlayerId


def extended_scoreboard_rows(match: Match) -> list[list[str]]:
    rows: list[list[str]] = []
    for profile in build_all_profiles(match):
        role = infer_role(match, PlayerId(profile.player_id))
        rows.append(
            [
                profile.name,
                profile.team,
                str(profile.kills),
                str(profile.deaths),
                str(profile.assists),
                f"{profile.adr:.1f}",
                f"{profile.kd:.2f}",
                f"{profile.kast * 100:.0f}",
                f"{profile.rating_3_0:.2f}",
                f"{profile.impact:.2f}",
                str(profile.opening_kills),
                role.primary.value,
            ]
        )
    return rows


def extended_scoreboard_table(match: Match) -> str:
    headers = [
        "Player",
        "Team",
        "K",
        "D",
        "A",
        "ADR",
        "K/D",
        "KAST%",
        "R3.0",
        "Imp",
        "OK",
        "Role",
    ]
    return format_table(headers, extended_scoreboard_rows(match))


def team_blocks(match: Match) -> str:
    """Render CT block then T block."""
    from roundwire.models.team import TeamSide

    chunks: list[str] = []
    for side in (TeamSide.CT, TeamSide.T):
        name = match.team_ct_name if side is TeamSide.CT else match.team_t_name
        profiles = [p for p in build_all_profiles(match) if p.team == side.value]
        headers = ["Player", "K", "D", "A", "ADR", "R3.0", "Role"]
        rows = []
        for profile in profiles:
            role = infer_role(match, PlayerId(profile.player_id))
            rows.append(
                [
                    profile.name,
                    str(profile.kills),
                    str(profile.deaths),
                    str(profile.assists),
                    f"{profile.adr:.1f}",
                    f"{profile.rating_3_0:.2f}",
                    role.primary.value,
                ]
            )
        chunks.append(f"== {name} ({side.value}) ==")
        chunks.append(format_table(headers, rows))
    ct, t = match.score()
    chunks.append(f"Final: {ct}:{t}")
    return "\n".join(chunks)
