"""Full per-player match profile aggregating combat, economy, and utility."""

from __future__ import annotations

from dataclasses import dataclass, field

from roundwire.combat.adr import adr_for_player, damage_total
from roundwire.combat.clutch import clutch_wins
from roundwire.combat.first_blood import died_first_count
from roundwire.combat.headshot import headshot_kills, headshot_pct
from roundwire.combat.kast import kast_pct
from roundwire.combat.kd import assist_count, death_count, kill_count, kd_ratio, kpr
from roundwire.combat.multikill import ace_rounds, multi_kill_count
from roundwire.combat.opening import opening_deaths_for, opening_kills_for
from roundwire.combat.survival import rounds_survived, survival_rate
from roundwire.combat.trades import all_trades
from roundwire.combat.weapons_usage import favorite_weapon, weapon_kills
from roundwire.economy.classify import classify_team_buy
from roundwire.models.buy_type import BuyType
from roundwire.models.match import Match
from roundwire.models.team import TeamSide
from roundwire.players.economy_profile import PlayerEconomyProfile, build_economy_profile
from roundwire.players.utility_profile import PlayerUtilityProfile, build_utility_profile
from roundwire.players.weapon_stats import WeaponBreakdown, weapon_breakdown
from roundwire.rating.impact import impact_score
from roundwire.rating.rating30 import rating_3_0
from roundwire.stats.aggregates import safe_div
from roundwire.types import PlayerId
from roundwire.utility.cost import utility_spend


@dataclass(slots=True)
class PlayerMatchProfile:
    """Observable per-player summary for a single match dump."""

    player_id: str
    name: str
    team: str
    rounds_played: int
    kills: int
    deaths: int
    assists: int
    kd: float
    kpr: float
    adr: float
    damage: int
    hs_pct: float
    hs_kills: int
    kast: float
    survival: float
    rounds_survived: int
    opening_kills: int
    opening_deaths: int
    died_first: int
    multi_kills: int
    aces: int
    clutch_wins: int
    trade_kills: int
    traded_deaths: int
    impact: float
    rating_3_0: float
    favorite_weapon: str | None
    utility_spend: int
    eco_rounds: int
    force_rounds: int
    full_rounds: int
    pistol_rounds: int
    economy: PlayerEconomyProfile
    utility: PlayerUtilityProfile
    weapons: WeaponBreakdown
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "player_id": self.player_id,
            "name": self.name,
            "team": self.team,
            "rounds_played": self.rounds_played,
            "kills": self.kills,
            "deaths": self.deaths,
            "assists": self.assists,
            "kd": round(self.kd, 3),
            "kpr": round(self.kpr, 3),
            "adr": round(self.adr, 2),
            "damage": self.damage,
            "hs_pct": round(self.hs_pct, 4),
            "hs_kills": self.hs_kills,
            "kast": round(self.kast, 4),
            "survival": round(self.survival, 4),
            "rounds_survived": self.rounds_survived,
            "opening_kills": self.opening_kills,
            "opening_deaths": self.opening_deaths,
            "died_first": self.died_first,
            "multi_kills": self.multi_kills,
            "aces": self.aces,
            "clutch_wins": self.clutch_wins,
            "trade_kills": self.trade_kills,
            "traded_deaths": self.traded_deaths,
            "impact": round(self.impact, 4),
            "rating_3_0": round(self.rating_3_0, 4),
            "favorite_weapon": self.favorite_weapon,
            "utility_spend": self.utility_spend,
            "buy_rounds": {
                "eco": self.eco_rounds,
                "force": self.force_rounds,
                "full": self.full_rounds,
                "pistol": self.pistol_rounds,
            },
            "economy": self.economy.to_dict(),
            "utility": self.utility.to_dict(),
            "weapons": self.weapons.to_dict(),
            "tags": list(self.tags),
        }


def _trade_counts(match: Match, player_id: PlayerId) -> tuple[int, int]:
    trade_kills = 0
    traded_deaths = 0
    for trade in all_trades(match):
        if trade.trade.killer_id == player_id:
            trade_kills += 1
        if trade.original.victim_id == player_id:
            traded_deaths += 1
    return trade_kills, traded_deaths


def _buy_round_counts(match: Match, side: TeamSide) -> dict[str, int]:
    counts = {"eco": 0, "force": 0, "full": 0, "pistol": 0, "semi": 0, "unknown": 0}
    for rnd in match.rounds:
        buy = classify_team_buy(rnd, match, side)
        counts[buy.value] = counts.get(buy.value, 0) + 1
    return counts


def _derive_tags(profile: PlayerMatchProfile) -> list[str]:
    tags: list[str] = []
    if profile.opening_kills >= max(3, profile.rounds_played // 5):
        tags.append("entry")
    if profile.favorite_weapon == "awp":
        tags.append("awper")
    if profile.utility.enemies_flashed >= 8 or profile.utility_spend >= 3000:
        tags.append("support")
    if profile.clutch_wins >= 2:
        tags.append("clutcher")
    if profile.hs_pct >= 0.55 and profile.kills >= 10:
        tags.append("sharpshooter")
    if profile.kd >= 1.3 and profile.adr >= 85:
        tags.append("star")
    if profile.survival >= 0.55:
        tags.append("survivor")
    if profile.trade_kills >= 4:
        tags.append("trader")
    return tags


def build_player_profile(match: Match, player_id: PlayerId) -> PlayerMatchProfile:
    player = match.player_map()[player_id]
    buys = _buy_round_counts(match, player.team)
    trade_kills, traded_deaths = _trade_counts(match, player_id)
    profile = PlayerMatchProfile(
        player_id=str(player_id),
        name=player.name,
        team=player.team.value,
        rounds_played=len(match.rounds),
        kills=kill_count(match, player_id),
        deaths=death_count(match, player_id),
        assists=assist_count(match, player_id),
        kd=kd_ratio(match, player_id),
        kpr=kpr(match, player_id),
        adr=adr_for_player(match, player_id),
        damage=damage_total(match, player_id),
        hs_pct=headshot_pct(match, player_id),
        hs_kills=headshot_kills(match, player_id),
        kast=kast_pct(match, player_id),
        survival=survival_rate(match, player_id),
        rounds_survived=rounds_survived(match, player_id),
        opening_kills=opening_kills_for(match, player_id),
        opening_deaths=opening_deaths_for(match, player_id),
        died_first=died_first_count(match, player_id),
        multi_kills=multi_kill_count(match, player_id),
        aces=len(ace_rounds(match, player_id)),
        clutch_wins=clutch_wins(match, player_id),
        trade_kills=trade_kills,
        traded_deaths=traded_deaths,
        impact=impact_score(match, player_id),
        rating_3_0=rating_3_0(match, player_id),
        favorite_weapon=favorite_weapon(match, player_id),
        utility_spend=utility_spend(match, player_id),
        eco_rounds=buys.get("eco", 0),
        force_rounds=buys.get("force", 0),
        full_rounds=buys.get("full", 0),
        pistol_rounds=buys.get("pistol", 0),
        economy=build_economy_profile(match, player_id),
        utility=build_utility_profile(match, player_id),
        weapons=weapon_breakdown(match, player_id),
    )
    profile.tags = _derive_tags(profile)
    return profile


def build_all_profiles(match: Match) -> list[PlayerMatchProfile]:
    profiles = [build_player_profile(match, p.player_id) for p in match.players]
    return sorted(profiles, key=lambda p: (-p.rating_3_0, -p.kills, p.name))


def profile_by_name(match: Match, name: str) -> PlayerMatchProfile | None:
    player = match.player_by_name(name)
    if player is None:
        return None
    return build_player_profile(match, player.player_id)


def profile_table(match: Match) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for profile in build_all_profiles(match):
        rows.append(
            {
                "name": profile.name,
                "team": profile.team,
                "kills": profile.kills,
                "deaths": profile.deaths,
                "assists": profile.assists,
                "adr": round(profile.adr, 1),
                "kd": round(profile.kd, 2),
                "kast": round(profile.kast * 100, 1),
                "rating": round(profile.rating_3_0, 3),
                "impact": round(profile.impact, 3),
                "ok": profile.opening_kills,
                "tags": ",".join(profile.tags),
            }
        )
    return rows


def team_profile_averages(match: Match, side: TeamSide) -> dict[str, float]:
    profiles = [
        build_player_profile(match, p.player_id) for p in match.players_on(side)
    ]
    if not profiles:
        return {
            "kills": 0.0,
            "adr": 0.0,
            "kd": 0.0,
            "kast": 0.0,
            "rating": 0.0,
            "impact": 0.0,
        }
    n = float(len(profiles))
    return {
        "kills": sum(p.kills for p in profiles) / n,
        "adr": sum(p.adr for p in profiles) / n,
        "kd": sum(p.kd for p in profiles) / n,
        "kast": sum(p.kast for p in profiles) / n,
        "rating": sum(p.rating_3_0 for p in profiles) / n,
        "impact": sum(p.impact for p in profiles) / n,
    }


def differential_vs_team(match: Match, player_id: PlayerId) -> dict[str, float]:
    """How far a player sits above/below their own team averages."""
    player = match.player_map()[player_id]
    profile = build_player_profile(match, player_id)
    avg = team_profile_averages(match, player.team)
    return {
        "kills_delta": profile.kills - avg["kills"],
        "adr_delta": profile.adr - avg["adr"],
        "kd_delta": profile.kd - avg["kd"],
        "kast_delta": profile.kast - avg["kast"],
        "rating_delta": profile.rating_3_0 - avg["rating"],
        "impact_delta": profile.impact - avg["impact"],
    }


def efficiency_score(match: Match, player_id: PlayerId) -> float:
    """Composite 0-100ish efficiency from K/D, ADR, and KAST."""
    profile = build_player_profile(match, player_id)
    kd_part = min(profile.kd, 2.5) / 2.5 * 40.0
    adr_part = min(profile.adr, 120.0) / 120.0 * 35.0
    kast_part = profile.kast * 25.0
    return kd_part + adr_part + kast_part


def opening_share(match: Match, player_id: PlayerId) -> float:
    total_openings = sum(opening_kills_for(match, p.player_id) for p in match.players)
    return safe_div(float(opening_kills_for(match, player_id)), float(total_openings))


def damage_share(match: Match, player_id: PlayerId) -> float:
    total = sum(damage_total(match, p.player_id) for p in match.players)
    return safe_div(float(damage_total(match, player_id)), float(total))


def weapon_diversity(match: Match, player_id: PlayerId) -> int:
    return len(weapon_kills(match, player_id))
