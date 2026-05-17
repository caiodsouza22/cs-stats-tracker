"""Match-to-match comparison helpers."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.combat.summary import combat_summary
from roundwire.economy.summary import economy_match_summary
from roundwire.models.match import Match
from roundwire.players.leaderboard import mvp
from roundwire.players.profile import build_all_profiles, team_profile_averages
from roundwire.models.team import TeamSide
from roundwire.utility.summary import utility_summary


@dataclass(frozen=True, slots=True)
class MatchDelta:
    left_id: str
    right_id: str
    score_left: tuple[int, int]
    score_right: tuple[int, int]
    rounds_left: int
    rounds_right: int
    mvp_left: str | None
    mvp_right: str | None
    avg_adr_left: float
    avg_adr_right: float
    util_flash_left: int
    util_flash_right: int

    def to_dict(self) -> dict[str, object]:
        return {
            "left_id": self.left_id,
            "right_id": self.right_id,
            "score_left": list(self.score_left),
            "score_right": list(self.score_right),
            "rounds_left": self.rounds_left,
            "rounds_right": self.rounds_right,
            "mvp_left": self.mvp_left,
            "mvp_right": self.mvp_right,
            "avg_adr_left": round(self.avg_adr_left, 1),
            "avg_adr_right": round(self.avg_adr_right, 1),
            "util_flash_left": self.util_flash_left,
            "util_flash_right": self.util_flash_right,
        }


def _avg_adr(match: Match) -> float:
    lines = combat_summary(match)
    if not lines:
        return 0.0
    return sum(l.adr for l in lines) / len(lines)


def _flash_total(match: Match) -> int:
    return sum(line.enemies_flashed for line in utility_summary(match))


def compare_matches(left: Match, right: Match) -> MatchDelta:
    mvp_l = mvp(left)
    mvp_r = mvp(right)
    return MatchDelta(
        left_id=str(left.match_id),
        right_id=str(right.match_id),
        score_left=left.score(),
        score_right=right.score(),
        rounds_left=len(left.rounds),
        rounds_right=len(right.rounds),
        mvp_left=mvp_l.name if mvp_l else None,
        mvp_right=mvp_r.name if mvp_r else None,
        avg_adr_left=_avg_adr(left),
        avg_adr_right=_avg_adr(right),
        util_flash_left=_flash_total(left),
        util_flash_right=_flash_total(right),
    )


def common_player_deltas(left: Match, right: Match) -> list[dict[str, object]]:
    left_profiles = {p.name: p for p in build_all_profiles(left)}
    right_profiles = {p.name: p for p in build_all_profiles(right)}
    names = sorted(set(left_profiles) & set(right_profiles))
    rows = []
    for name in names:
        a = left_profiles[name]
        b = right_profiles[name]
        rows.append(
            {
                "name": name,
                "rating_delta": round(b.rating_3_0 - a.rating_3_0, 3),
                "adr_delta": round(b.adr - a.adr, 1),
                "kills_delta": b.kills - a.kills,
                "kd_delta": round(b.kd - a.kd, 3),
            }
        )
    return rows


def economy_delta(left: Match, right: Match) -> list[dict[str, object]]:
    l_rows = {r.side: r for r in economy_match_summary(left)}
    r_rows = {r.side: r for r in economy_match_summary(right)}
    out = []
    for side in ("CT", "T"):
        l = l_rows.get(side)
        r = r_rows.get(side)
        if l is None or r is None:
            continue
        out.append(
            {
                "side": side,
                "eco_upsets_delta": r.eco_upsets - l.eco_upsets,
                "force_success_delta": round(r.force_success - l.force_success, 3),
                "full_winrate_delta": round(r.full_winrate - l.full_winrate, 3),
            }
        )
    return out


def side_strength_delta(left: Match, right: Match) -> dict[str, dict[str, float]]:
    return {
        "left": {
            "CT": team_profile_averages(left, TeamSide.CT)["rating"],
            "T": team_profile_averages(left, TeamSide.T)["rating"],
        },
        "right": {
            "CT": team_profile_averages(right, TeamSide.CT)["rating"],
            "T": team_profile_averages(right, TeamSide.T)["rating"],
        },
    }
