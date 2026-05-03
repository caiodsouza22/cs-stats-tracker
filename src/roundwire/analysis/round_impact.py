"""Per-round impact attribution for each player."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.combat.opening import first_kill, was_traded
from roundwire.models.match import Match
from roundwire.models.round import Round
from roundwire.rating.round_swing import round_swing_credits
from roundwire.types import PlayerId


@dataclass(frozen=True, slots=True)
class RoundImpact:
    round_number: int
    player_id: str
    name: str
    kills: float
    damage: float
    opening: float
    trade: float
    util: float
    swing: float
    total: float
    won: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "round": self.round_number,
            "player_id": self.player_id,
            "name": self.name,
            "kills": round(self.kills, 3),
            "damage": round(self.damage, 3),
            "opening": round(self.opening, 3),
            "trade": round(self.trade, 3),
            "util": round(self.util, 3),
            "swing": round(self.swing, 3),
            "total": round(self.total, 3),
            "won": self.won,
        }


def _swing_for(round_: Round, match: Match, player_id: PlayerId) -> float:
    pid = str(player_id)
    for credit in round_swing_credits(round_, match):
        if credit.player_id == pid:
            return float(credit.delta)
    return 0.0


def round_impact_for(
    match: Match,
    round_: Round,
    player_id: PlayerId,
) -> RoundImpact:
    player = match.player_map()[player_id]
    kills = float(len(round_.kills_for(player_id)))
    damage = round_.damage_dealt_by(player_id) / 100.0
    fk = first_kill(round_)
    opening = 0.0
    trade = 0.0
    if fk is not None and fk.killer_id == player_id:
        opening = 1.25
        if was_traded(round_, fk):
            opening -= 0.35
    if fk is not None and fk.victim_id == player_id and was_traded(round_, fk):
        trade += 0.25
    if fk is not None:
        for later in round_.kills:
            if later.killer_id == player_id and later.victim_id == fk.killer_id and later is not fk:
                trade += 0.8
                break
    util = 0.0
    for event in round_.utility:
        if event.thrower_id != player_id:
            continue
        util += 0.15
        util += event.enemies_flashed * 0.2
        util += event.damage_dealt / 80.0
    swing = _swing_for(round_, match, player_id)
    total = kills + damage + opening + trade + util + swing
    return RoundImpact(
        round_number=int(round_.number),
        player_id=str(player_id),
        name=player.name,
        kills=kills,
        damage=damage,
        opening=opening,
        trade=trade,
        util=util,
        swing=swing,
        total=total,
        won=round_.winner is player.team,
    )


def round_impacts(match: Match, player_id: PlayerId) -> list[RoundImpact]:
    return [round_impact_for(match, rnd, player_id) for rnd in match.rounds]


def top_impact_rounds(match: Match, player_id: PlayerId, n: int = 5) -> list[RoundImpact]:
    return sorted(round_impacts(match, player_id), key=lambda r: (-r.total, r.round_number))[:n]


def match_round_mvp(match: Match) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for rnd in match.rounds:
        best: RoundImpact | None = None
        for player in match.players:
            card = round_impact_for(match, rnd, player.player_id)
            if best is None or card.total > best.total:
                best = card
        if best is not None:
            rows.append(best.to_dict())
    return rows


def cumulative_impact(match: Match, player_id: PlayerId) -> list[float]:
    total = 0.0
    out: list[float] = []
    for card in round_impacts(match, player_id):
        total += card.total
        out.append(total)
    return out


def impact_leaderboard(match: Match) -> list[dict[str, object]]:
    rows = []
    for player in match.players:
        cards = round_impacts(match, player.player_id)
        total = sum(c.total for c in cards)
        rows.append(
            {
                "player_id": str(player.player_id),
                "name": player.name,
                "team": player.team.value,
                "total_impact": round(total, 3),
                "avg_impact": round(total / max(1, len(cards)), 3),
            }
        )
    return sorted(rows, key=lambda r: (-r["total_impact"], r["name"]))
