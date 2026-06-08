"""Heuristic role inference from match behavior."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from roundwire.models.match import Match
from roundwire.players.profile import build_player_profile
from roundwire.players.utility_profile import support_index
from roundwire.players.weapon_stats import awp_dependency
from roundwire.stats.aggregates import safe_div
from roundwire.types import PlayerId


class PlayerRole(str, Enum):
    ENTRY = "entry"
    AWPER = "awper"
    SUPPORT = "support"
    LURKER = "lurker"
    ANCHOR = "anchor"
    STAR = "star"
    FLEX = "flex"


@dataclass(frozen=True, slots=True)
class RoleScore:
    role: PlayerRole
    score: float
    reasons: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RoleAssignment:
    player_id: str
    name: str
    team: str
    primary: PlayerRole
    secondary: PlayerRole | None
    scores: tuple[RoleScore, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "player_id": self.player_id,
            "name": self.name,
            "team": self.team,
            "primary": self.primary.value,
            "secondary": self.secondary.value if self.secondary else None,
            "scores": [
                {"role": s.role.value, "score": round(s.score, 3), "reasons": list(s.reasons)}
                for s in self.scores
            ],
        }


def _score_roles(match: Match, player_id: PlayerId) -> list[RoleScore]:
    profile = build_player_profile(match, player_id)
    rounds = max(1, profile.rounds_played)
    scores: list[RoleScore] = []

    entry_score = (
        profile.opening_kills * 2.0
        + profile.opening_deaths * 0.5
        - profile.utility.smokes * 0.2
    ) / rounds
    entry_reasons = []
    if profile.opening_kills >= 3:
        entry_reasons.append(f"{profile.opening_kills} opening kills")
    if profile.died_first >= 3:
        entry_reasons.append(f"{profile.died_first} first deaths")
    scores.append(RoleScore(PlayerRole.ENTRY, entry_score, tuple(entry_reasons)))

    awp_score = awp_dependency(match, player_id) * 5.0 + (
        1.5 if profile.favorite_weapon == "awp" else 0.0
    )
    awp_reasons = []
    if profile.favorite_weapon == "awp":
        awp_reasons.append("AWP favorite weapon")
    if awp_dependency(match, player_id) >= 0.25:
        awp_reasons.append(f"AWP kill share {awp_dependency(match, player_id):.0%}")
    scores.append(RoleScore(PlayerRole.AWPER, awp_score, tuple(awp_reasons)))

    support_raw = support_index(match, player_id)
    support_score = support_raw + profile.utility.smokes / rounds + profile.assists / rounds
    support_reasons = []
    if profile.utility.enemies_flashed >= 6:
        support_reasons.append(f"{profile.utility.enemies_flashed} enemies flashed")
    if profile.utility.smokes >= 5:
        support_reasons.append(f"{profile.utility.smokes} smokes")
    scores.append(RoleScore(PlayerRole.SUPPORT, support_score, tuple(support_reasons)))

    # lurker proxy: mid/late kills, fewer openings, decent survival
    late_kills = 0
    for rnd in match.rounds:
        for kill in rnd.kills_for(player_id):
            if int(kill.tick_ms) >= 45000:
                late_kills += 1
    lurker_score = (
        late_kills * 1.4
        + profile.survival * 2.0
        - profile.opening_kills * 0.8
        + profile.clutch_wins
    ) / rounds
    lurker_reasons = []
    if late_kills >= 3:
        lurker_reasons.append(f"{late_kills} late-round kills")
    if profile.clutch_wins:
        lurker_reasons.append(f"{profile.clutch_wins} clutch wins")
    scores.append(RoleScore(PlayerRole.LURKER, lurker_score, tuple(lurker_reasons)))

    # CT anchor proxy: high survival + utility on CT side, fewer openings
    anchor_score = 0.0
    if profile.team == "CT":
        anchor_score = (
            profile.survival * 3.0
            + profile.utility.smokes / rounds
            + profile.utility.fires / rounds
            - profile.opening_kills / rounds
        )
    anchor_reasons = []
    if profile.team == "CT" and profile.survival >= 0.5:
        anchor_reasons.append("CT survival hold")
    scores.append(RoleScore(PlayerRole.ANCHOR, anchor_score, tuple(anchor_reasons)))

    star_score = profile.kd * 1.2 + profile.adr / 50.0 + profile.rating_3_0
    star_reasons = []
    if profile.kd >= 1.2:
        star_reasons.append(f"K/D {profile.kd:.2f}")
    if profile.rating_3_0 >= 1.1:
        star_reasons.append(f"R3.0 {profile.rating_3_0:.2f}")
    scores.append(RoleScore(PlayerRole.STAR, star_score, tuple(star_reasons)))

    # flex: balanced mid scores across roles
    core = [entry_score, awp_score, support_score, lurker_score]
    flex_score = 2.0 - (max(core) - min(core))
    flex_reasons = ("balanced distribution across roles",)
    scores.append(RoleScore(PlayerRole.FLEX, max(0.0, flex_score), flex_reasons))

    return sorted(scores, key=lambda s: (-s.score, s.role.value))


def infer_role(match: Match, player_id: PlayerId) -> RoleAssignment:
    player = match.player_map()[player_id]
    scores = _score_roles(match, player_id)
    primary = scores[0].role if scores else PlayerRole.FLEX
    secondary = None
    if len(scores) > 1 and scores[1].score >= scores[0].score * 0.75:
        secondary = scores[1].role
    return RoleAssignment(
        player_id=str(player_id),
        name=player.name,
        team=player.team.value,
        primary=primary,
        secondary=secondary,
        scores=tuple(scores),
    )


def role_table(match: Match) -> list[dict[str, object]]:
    rows = [infer_role(match, p.player_id).to_dict() for p in match.players]
    return sorted(rows, key=lambda r: (r["team"], r["name"]))


def roles_for_team(match: Match, side: str) -> list[RoleAssignment]:
    key = side.upper()
    return [
        infer_role(match, p.player_id)
        for p in match.players
        if p.team.value == key
    ]


def role_counts(match: Match) -> dict[str, int]:
    counts: dict[str, int] = {}
    for player in match.players:
        role = infer_role(match, player.player_id).primary.value
        counts[role] = counts.get(role, 0) + 1
    return counts


def confidence(match: Match, player_id: PlayerId) -> float:
    """0-1 confidence that primary role stands above the pack."""
    scores = _score_roles(match, player_id)
    if len(scores) < 2:
        return 1.0
    top, second = scores[0].score, scores[1].score
    return safe_div(top - second, max(abs(top), 1.0))
