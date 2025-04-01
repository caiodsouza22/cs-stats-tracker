"""Team-fight and man-advantage proxies from kill order."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.models.match import Match
from roundwire.models.round import Round
from roundwire.models.team import TeamSide
from roundwire.types import PlayerId


@dataclass(frozen=True, slots=True)
class FightSegment:
    round_number: int
    start_ms: int
    end_ms: int
    kills: int
    ct_kills: int
    t_kills: int
    first_blood_side: str | None

    def to_dict(self) -> dict[str, object]:
        return {
            "round": self.round_number,
            "start_ms": self.start_ms,
            "end_ms": self.end_ms,
            "kills": self.kills,
            "ct_kills": self.ct_kills,
            "t_kills": self.t_kills,
            "first_blood_side": self.first_blood_side,
        }


def _side_of(match: Match, player_id: PlayerId) -> TeamSide | None:
    player = match.player_map().get(player_id)
    return player.team if player else None


def fight_segments(match: Match, gap_ms: int = 8000) -> list[FightSegment]:
    """Cluster kills into fight bursts when gaps exceed ``gap_ms``."""
    segments: list[FightSegment] = []
    for rnd in match.rounds:
        kills = sorted(rnd.kills, key=lambda k: int(k.tick_ms))
        if not kills:
            continue
        cluster = [kills[0]]
        for kill in kills[1:]:
            if int(kill.tick_ms) - int(cluster[-1].tick_ms) <= gap_ms:
                cluster.append(kill)
            else:
                segments.append(_build_segment(match, rnd, cluster))
                cluster = [kill]
        segments.append(_build_segment(match, rnd, cluster))
    return segments


def _build_segment(match: Match, round_: Round, cluster: list) -> FightSegment:
    ct = t = 0
    for kill in cluster:
        side = _side_of(match, kill.killer_id)
        if side is TeamSide.CT:
            ct += 1
        elif side is TeamSide.T:
            t += 1
    first_side = _side_of(match, cluster[0].killer_id)
    return FightSegment(
        round_number=int(round_.number),
        start_ms=int(cluster[0].tick_ms),
        end_ms=int(cluster[-1].tick_ms),
        kills=len(cluster),
        ct_kills=ct,
        t_kills=t,
        first_blood_side=first_side.value if first_side else None,
    )


def player_fight_participation(match: Match, player_id: PlayerId, gap_ms: int = 8000) -> dict[str, object]:
    participated = 0
    total = 0
    for rnd in match.rounds:
        kills = sorted(rnd.kills, key=lambda k: int(k.tick_ms))
        if not kills:
            continue
        clusters: list[list] = [[kills[0]]]
        for kill in kills[1:]:
            if int(kill.tick_ms) - int(clusters[-1][-1].tick_ms) <= gap_ms:
                clusters[-1].append(kill)
            else:
                clusters.append([kill])
        for cluster in clusters:
            total += 1
            if any(k.killer_id == player_id or k.victim_id == player_id for k in cluster):
                participated += 1
    return {
        "player_id": str(player_id),
        "fights": total,
        "participated": participated,
        "rate": (participated / total) if total else 0.0,
    }


def man_advantage_rounds(match: Match) -> list[dict[str, object]]:
    """Rounds where one side got the first two kills (early man advantage proxy)."""
    rows = []
    for rnd in match.rounds:
        kills = sorted(rnd.kills, key=lambda k: int(k.tick_ms))
        if len(kills) < 2:
            continue
        s1 = _side_of(match, kills[0].killer_id)
        s2 = _side_of(match, kills[1].killer_id)
        if s1 is None or s2 is None or s1 is not s2:
            continue
        rows.append(
            {
                "round": int(rnd.number),
                "side": s1.value,
                "converted": rnd.winner is s1,
            }
        )
    return rows


def conversion_after_first_blood(match: Match) -> dict[str, float]:
    from roundwire.combat.first_blood import opening_conversion_for_side

    return {
        "CT": opening_conversion_for_side(match, TeamSide.CT),
        "T": opening_conversion_for_side(match, TeamSide.T),
    }
