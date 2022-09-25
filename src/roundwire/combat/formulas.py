"""Named combat formulas and scaling helpers."""

from __future__ import annotations

from roundwire.models.match import Match
from roundwire.stats.aggregates import clamp, safe_div
from roundwire.types import PlayerId


def rating1_style(kills: int, deaths: int, rounds: int) -> float:
    """Very rough classic-style rating component (not HLTV)."""
    if rounds <= 0:
        return 0.0
    return safe_div(float(kills), float(max(deaths, 1))) * safe_div(float(kills), float(rounds))


def impact_ish(openings: int, multi: int, rounds: int) -> float:
    return safe_div(float(openings * 2 + multi), float(max(rounds, 1)))


def surv_component(survived: int, rounds: int) -> float:
    return safe_div(float(survived), float(max(rounds, 1)))


def adr_component(damage: int, rounds: int) -> float:
    return safe_div(float(damage), float(max(rounds, 1))) / 100.0


def blend(parts: list[tuple[float, float]]) -> float:
    if not parts:
        return 0.0
    num = sum(w * v for w, v in parts)
    den = sum(w for w, _v in parts)
    return safe_div(num, den)


def soft_score(value: float, *, center: float = 1.0, scale: float = 0.5) -> float:
    return clamp(1.0 + (value - center) * scale, 0.0, 2.5)


def player_formula_pack(match: Match, player_id: PlayerId) -> dict[str, float]:
    from roundwire.combat.adr import damage_total
    from roundwire.combat.kd import death_count, kill_count
    from roundwire.combat.multikill import multi_kill_count
    from roundwire.combat.opening import opening_kills_for
    from roundwire.combat.survival import rounds_survived

    rounds = len(match.rounds)
    kills = kill_count(match, player_id)
    deaths = death_count(match, player_id)
    dmg = damage_total(match, player_id)
    openings = opening_kills_for(match, player_id)
    multi = multi_kill_count(match, player_id)
    survived = rounds_survived(match, player_id)
    return {
        "rating1_style": rating1_style(kills, deaths, rounds),
        "impact_ish": impact_ish(openings, multi, rounds),
        "surv": surv_component(survived, rounds),
        "adr": adr_component(dmg, rounds),
        "blended": blend(
            [
                (0.4, rating1_style(kills, deaths, rounds)),
                (0.3, adr_component(dmg, rounds)),
                (0.2, surv_component(survived, rounds)),
                (0.1, impact_ish(openings, multi, rounds)),
            ]
        ),
        "soft": soft_score(safe_div(float(kills), float(max(rounds, 1))), center=0.7),
    }


def team_formula_pack(match: Match) -> dict[str, dict[str, float]]:
    out: dict[str, dict[str, float]] = {}
    for player in match.players:
        out[str(player.player_id)] = player_formula_pack(match, player.player_id)
    return out
