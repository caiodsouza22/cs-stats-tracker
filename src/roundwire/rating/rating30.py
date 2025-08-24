"""HLTV-inspired Rating 3.0 approximation for CS2 dumps.

Public HLTV description (2025): six sub-ratings — Kills, Damage, Survival,
KAST, Multi-Kills, Round Swing — with eco context. October 2025 hotfix weights
put Kills at ~25% and Round Swing at ~33%.

This is **not** the proprietary HLTV formula. Round Swing here uses an open
alive-count / economy / bomb heuristic. Numbers will not match hltv.org.
"""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.combat.kast import kast_pct
from roundwire.combat.multikill import multi_kill_count
from roundwire.combat.survival import survival_rate
from roundwire.models.match import Match
from roundwire.rating.eco_adjust import eco_damage_multiplier, eco_kill_multiplier
from roundwire.rating.round_swing import round_swing_per_round
from roundwire.types import PlayerId


@dataclass(frozen=True, slots=True)
class Rating30Weights:
    """Post–Oct 2025 public weight targets (normalized to 1.0)."""

    kills: float = 0.25
    round_swing: float = 0.33
    damage: float = 0.14
    survival: float = 0.10
    kast: float = 0.10
    multi_kills: float = 0.08


DEFAULT_RATING30_WEIGHTS = Rating30Weights()


@dataclass(frozen=True, slots=True)
class Rating30Breakdown:
    player_id: str
    name: str
    rating: float
    kills: float
    damage: float
    survival: float
    kast: float
    multi_kills: float
    round_swing: float
    raw_swing_pr: float


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _relative(value: float, mean: float) -> float:
    """Map raw stat so a match-average player sits near 1.0."""
    if mean <= 1e-9:
        return 1.0 if value <= 1e-9 else 1.5
    return value / mean


def eco_adjusted_kills(match: Match, player_id: PlayerId) -> float:
    total = 0.0
    for rnd in match.rounds:
        for kill in rnd.kills_for(player_id):
            total += eco_kill_multiplier(rnd, kill.killer_id, kill.victim_id)
    return total


def eco_adjusted_damage(match: Match, player_id: PlayerId) -> float:
    total = 0.0
    for rnd in match.rounds:
        for dmg in rnd.damage:
            if dmg.attacker_id != player_id:
                continue
            total += dmg.damage * eco_damage_multiplier(rnd, dmg.attacker_id, dmg.victim_id)
    return total


def multi_kill_rate(match: Match, player_id: PlayerId) -> float:
    if not match.rounds:
        return 0.0
    return multi_kill_count(match, player_id) / len(match.rounds)


def rating_3_0(
    match: Match,
    player_id: PlayerId,
    *,
    weights: Rating30Weights = DEFAULT_RATING30_WEIGHTS,
) -> float:
    return rating_3_0_breakdown(match, player_id, weights=weights).rating


def rating_3_0_breakdown(
    match: Match,
    player_id: PlayerId,
    *,
    weights: Rating30Weights = DEFAULT_RATING30_WEIGHTS,
) -> Rating30Breakdown:
    players = list(match.players)
    raw_kills = [eco_adjusted_kills(match, p.player_id) for p in players]
    raw_dmg = [eco_adjusted_damage(match, p.player_id) for p in players]
    raw_surv = [survival_rate(match, p.player_id) for p in players]
    raw_kast = [kast_pct(match, p.player_id) for p in players]
    raw_multi = [multi_kill_rate(match, p.player_id) for p in players]
    raw_swing = [round_swing_per_round(match, p.player_id) for p in players]

    # Shift swing so average ~ mid-pack; use absolute deviation from 0 + offset
    # Swing can be negative; convert to positive contribution via softplus-ish shift
    swing_shifted = [s + 0.15 for s in raw_swing]
    # ensure non-negative for relative scaling
    swing_shifted = [max(0.01, s) for s in swing_shifted]

    means = {
        "kills": _mean(raw_kills),
        "damage": _mean(raw_dmg),
        "survival": _mean(raw_surv),
        "kast": _mean(raw_kast),
        "multi": _mean(raw_multi),
        "swing": _mean(swing_shifted),
    }

    idx = next(i for i, p in enumerate(players) if p.player_id == player_id)
    kills_s = _relative(raw_kills[idx], means["kills"])
    dmg_s = _relative(raw_dmg[idx], means["damage"])
    surv_s = _relative(raw_surv[idx], means["survival"])
    kast_s = _relative(raw_kast[idx], means["kast"])
    multi_s = _relative(raw_multi[idx], means["multi"])
    swing_s = _relative(swing_shifted[idx], means["swing"])

    rating = (
        weights.kills * kills_s
        + weights.damage * dmg_s
        + weights.survival * surv_s
        + weights.kast * kast_s
        + weights.multi_kills * multi_s
        + weights.round_swing * swing_s
    )
    player = match.player_map()[player_id]
    return Rating30Breakdown(
        player_id=str(player_id),
        name=player.name,
        rating=max(0.0, rating),
        kills=kills_s,
        damage=dmg_s,
        survival=surv_s,
        kast=kast_s,
        multi_kills=multi_s,
        round_swing=swing_s,
        raw_swing_pr=raw_swing[idx],
    )


def rating_3_0_table(
    match: Match,
    *,
    weights: Rating30Weights = DEFAULT_RATING30_WEIGHTS,
) -> list[Rating30Breakdown]:
    rows = [rating_3_0_breakdown(match, p.player_id, weights=weights) for p in match.players]
    return sorted(rows, key=lambda r: (-r.rating, r.name))


# Aliases matching HLTV naming in docs / CLI
rating30 = rating_3_0
rating30_table = rating_3_0_table
