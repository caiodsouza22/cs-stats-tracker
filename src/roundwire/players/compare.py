"""Head-to-head and roster comparison helpers."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.combat.duels import head_to_head
from roundwire.models.match import Match
from roundwire.players.profile import build_player_profile
from roundwire.players.roles import infer_role
from roundwire.stats.aggregates import safe_div
from roundwire.types import PlayerId


@dataclass(frozen=True, slots=True)
class PlayerComparison:
    left_id: str
    left_name: str
    right_id: str
    right_name: str
    kills: tuple[int, int]
    deaths: tuple[int, int]
    adr: tuple[float, float]
    kd: tuple[float, float]
    kast: tuple[float, float]
    rating: tuple[float, float]
    impact: tuple[float, float]
    opening_kills: tuple[int, int]
    h2h_kills: tuple[int, int]
    roles: tuple[str, str]
    winner: str | None

    def to_dict(self) -> dict[str, object]:
        return {
            "left": {"id": self.left_id, "name": self.left_name},
            "right": {"id": self.right_id, "name": self.right_name},
            "kills": list(self.kills),
            "deaths": list(self.deaths),
            "adr": [round(self.adr[0], 1), round(self.adr[1], 1)],
            "kd": [round(self.kd[0], 2), round(self.kd[1], 2)],
            "kast": [round(self.kast[0], 3), round(self.kast[1], 3)],
            "rating": [round(self.rating[0], 3), round(self.rating[1], 3)],
            "impact": [round(self.impact[0], 3), round(self.impact[1], 3)],
            "opening_kills": list(self.opening_kills),
            "h2h_kills": list(self.h2h_kills),
            "roles": list(self.roles),
            "winner": self.winner,
        }


def compare_players(match: Match, left: PlayerId, right: PlayerId) -> PlayerComparison:
    a = build_player_profile(match, left)
    b = build_player_profile(match, right)
    duel = head_to_head(match, left, right)
    # decide edge by rating then kills
    if a.rating_3_0 > b.rating_3_0 + 0.02:
        winner = a.name
    elif b.rating_3_0 > a.rating_3_0 + 0.02:
        winner = b.name
    elif a.kills != b.kills:
        winner = a.name if a.kills > b.kills else b.name
    else:
        winner = None
    return PlayerComparison(
        left_id=a.player_id,
        left_name=a.name,
        right_id=b.player_id,
        right_name=b.name,
        kills=(a.kills, b.kills),
        deaths=(a.deaths, b.deaths),
        adr=(a.adr, b.adr),
        kd=(a.kd, b.kd),
        kast=(a.kast, b.kast),
        rating=(a.rating_3_0, b.rating_3_0),
        impact=(a.impact, b.impact),
        opening_kills=(a.opening_kills, b.opening_kills),
        h2h_kills=(duel.a_wins, duel.b_wins),
        roles=(infer_role(match, left).primary.value, infer_role(match, right).primary.value),
        winner=winner,
    )


def compare_by_name(match: Match, left_name: str, right_name: str) -> PlayerComparison | None:
    left = match.player_by_name(left_name)
    right = match.player_by_name(right_name)
    if left is None or right is None:
        return None
    return compare_players(match, left.player_id, right.player_id)


def roster_comparison(match: Match) -> list[dict[str, object]]:
    """CT vs T average profile comparison."""
    from roundwire.models.team import TeamSide
    from roundwire.players.profile import team_profile_averages

    ct = team_profile_averages(match, TeamSide.CT)
    t = team_profile_averages(match, TeamSide.T)
    keys = sorted(set(ct) | set(t))
    rows = []
    for key in keys:
        rows.append(
            {
                "metric": key,
                "CT": round(ct.get(key, 0.0), 3),
                "T": round(t.get(key, 0.0), 3),
                "delta_ct": round(ct.get(key, 0.0) - t.get(key, 0.0), 3),
            }
        )
    return rows


def pairwise_rating_gaps(match: Match) -> list[dict[str, object]]:
    profiles = [build_player_profile(match, p.player_id) for p in match.players]
    profiles = sorted(profiles, key=lambda p: -p.rating_3_0)
    gaps = []
    for i in range(len(profiles) - 1):
        gaps.append(
            {
                "higher": profiles[i].name,
                "lower": profiles[i + 1].name,
                "gap": round(profiles[i].rating_3_0 - profiles[i + 1].rating_3_0, 4),
            }
        )
    return gaps


def relative_share_card(match: Match, player_id: PlayerId) -> dict[str, float]:
    from roundwire.players.profile import damage_share, opening_share

    profile = build_player_profile(match, player_id)
    team_kills = sum(
        build_player_profile(match, p.player_id).kills
        for p in match.players
        if p.team.value == profile.team
    )
    return {
        "kill_share_team": safe_div(float(profile.kills), float(team_kills)),
        "damage_share_match": damage_share(match, player_id),
        "opening_share_match": opening_share(match, player_id),
        "rating": profile.rating_3_0,
    }
