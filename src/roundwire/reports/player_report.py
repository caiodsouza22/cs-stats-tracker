"""Tabular player reports for CLI and notebooks."""

from __future__ import annotations

from roundwire.models.match import Match
from roundwire.players.leaderboard import leaderboard
from roundwire.players.profile import build_all_profiles, profile_by_name
from roundwire.players.roles import infer_role
from roundwire.reports.tables import format_table
from roundwire.types import PlayerId


def player_report_table(match: Match) -> str:
    headers = ["Player", "Team", "K", "D", "A", "ADR", "K/D", "KAST", "R3.0", "OK", "Role", "Tags"]
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
                f"{profile.kast * 100:.0f}%",
                f"{profile.rating_3_0:.2f}",
                str(profile.opening_kills),
                role.primary.value,
                ",".join(profile.tags[:3]),
            ]
        )
    return format_table(headers, rows)


def player_detail_report(match: Match, name: str) -> str:
    profile = profile_by_name(match, name)
    if profile is None:
        return f"player not found: {name!r}"
    role = infer_role(match, PlayerId(profile.player_id))
    lines = [
        f"{profile.name} ({profile.team}) — {match.map_name} {match.edition.value}",
        f"K/D/A {profile.kills}/{profile.deaths}/{profile.assists}  ADR {profile.adr:.1f}  "
        f"KAST {profile.kast * 100:.0f}%  R3.0 {profile.rating_3_0:.3f}  Impact {profile.impact:.3f}",
        f"Openings {profile.opening_kills}/{profile.opening_deaths}  "
        f"HS {profile.hs_pct * 100:.0f}%  Clutches {profile.clutch_wins}  "
        f"Favorite {profile.favorite_weapon or '-'}",
        f"Role {role.primary.value}"
        + (f" / {role.secondary.value}" if role.secondary else "")
        + f"  Tags: {', '.join(profile.tags) or '-'}",
        f"Economy avg EQ {profile.economy.avg_equipment:.0f}  "
        f"armor rounds {profile.economy.rounds_with_armor}  "
        f"full WR {profile.economy.to_dict()['full_buy_wr']}",
        f"Utility spend {profile.utility.spend}  flashes {profile.utility.flashes}  "
        f"enemies flashed {profile.utility.enemies_flashed}  "
        f"eff {profile.utility.flash_efficiency:.2f}",
    ]
    if profile.weapons.lines:
        top = profile.weapons.lines[0]
        lines.append(
            f"Top weapon {top.weapon} ({top.kills} kills, {top.hs_pct * 100:.0f}% HS)"
        )
    return "\n".join(lines)


def leaderboard_report(match: Match, metric: str = "rating") -> str:
    rows = leaderboard(match, metric=metric)
    headers = ["#", "Player", "Team", metric]
    body = [[str(r.rank), r.name, r.team, f"{r.value:.3f}"] for r in rows]
    return format_table(headers, body)
