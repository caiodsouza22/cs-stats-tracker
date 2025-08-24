"""Round Swing approximation (inspired by HLTV Rating 3.0 public description).

HLTV's proprietary win-probability model is closed. This module uses a
transparent alive-count + economy + bomb heuristic so dumps without demo
telemetry still produce a useful swing signal.
"""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.combat.trades import trades_in_round
from roundwire.models.kill import Kill
from roundwire.models.match import Match
from roundwire.models.round import Round
from roundwire.models.team import TeamSide
from roundwire.models.utility_event import UtilityKind
from roundwire.rating.eco_adjust import equipment_value
from roundwire.types import PlayerId


def _player_side(match: Match, player_id: PlayerId) -> TeamSide:
    return match.player_map()[player_id].team


def win_prob_ct(
    *,
    alive_ct: int,
    alive_t: int,
    bomb_planted: bool,
    eq_ct: float,
    eq_t: float,
) -> float:
    """Rough P(CT win) from man-count, bomb, and average equipment."""
    if alive_ct <= 0 and alive_t <= 0:
        return 0.5
    if alive_ct <= 0:
        return 0.02
    if alive_t <= 0:
        return 0.98
    man = (alive_ct - alive_t) / 5.0
    eq_gap = (eq_ct - eq_t) / 5000.0
    bomb = 0.12 if bomb_planted else 0.0  # planted tends to help T — flip below
    # CT baseline ~0.5; man advantage helps CT; bomb plant hurts CT
    score = 0.50 + 0.28 * man + 0.10 * eq_gap - bomb
    return max(0.03, min(0.97, score))


def _flash_assister(round_: Round, kill: Kill) -> PlayerId | None:
    if kill.assisted_by is not None:
        return kill.assisted_by
    window = range(max(0, int(kill.tick_ms) - 4000), int(kill.tick_ms) + 1)
    for util in round_.utility:
        if util.kind is not UtilityKind.FLASH:
            continue
        if int(util.tick_ms) not in window:
            continue
        if util.enemies_flashed > 0:
            return util.thrower_id
    return None


def _damage_share_on_victim(round_: Round, victim_id: PlayerId, player_id: PlayerId) -> float:
    total = sum(d.damage for d in round_.damage if d.victim_id == victim_id)
    if total <= 0:
        return 0.0
    mine = sum(
        d.damage
        for d in round_.damage
        if d.victim_id == victim_id and d.attacker_id == player_id
    )
    return mine / total


@dataclass(frozen=True, slots=True)
class SwingCredit:
    player_id: str
    delta: float


def round_swing_credits(round_: Round, match: Match) -> list[SwingCredit]:
    """
    Attribute Round Swing for one round.

    Credit split per kill (public HLTV description, approximated):
    - final blow / kill credit
    - damage share
    - flash assist
    - trade context
    End-of-round: survivors on winning side get a small share.
    """
    alive_ct = {str(p.player_id) for p in match.players if p.team is TeamSide.CT}
    alive_t = {str(p.player_id) for p in match.players if p.team is TeamSide.T}
    credits: dict[str, float] = {str(p.player_id): 0.0 for p in match.players}

    trade_pairs = {(str(t.original.victim_id), str(t.trade.killer_id)) for t in trades_in_round(round_)}
    traded_victims = {str(t.original.victim_id) for t in trades_in_round(round_)}

    for kill in sorted(round_.kills, key=lambda k: int(k.tick_ms)):
        killer = str(kill.killer_id)
        victim = str(kill.victim_id)
        if killer not in credits or victim not in (alive_ct | alive_t):
            # still process if victim already marked dead inconsistently
            pass

        eq_ct = sum(equipment_value(round_, PlayerId(pid)) for pid in alive_ct) / max(len(alive_ct), 1)
        eq_t = sum(equipment_value(round_, PlayerId(pid)) for pid in alive_t) / max(len(alive_t), 1)
        before = win_prob_ct(
            alive_ct=len(alive_ct),
            alive_t=len(alive_t),
            bomb_planted=round_.bomb_planted,
            eq_ct=eq_ct,
            eq_t=eq_t,
        )

        # apply death
        alive_ct.discard(victim)
        alive_t.discard(victim)

        eq_ct_a = sum(equipment_value(round_, PlayerId(pid)) for pid in alive_ct) / max(len(alive_ct), 1)
        eq_t_a = sum(equipment_value(round_, PlayerId(pid)) for pid in alive_t) / max(len(alive_t), 1)
        after = win_prob_ct(
            alive_ct=len(alive_ct),
            alive_t=len(alive_t),
            bomb_planted=round_.bomb_planted,
            eq_ct=eq_ct_a,
            eq_t=eq_t_a,
        )

        killer_side = _player_side(match, kill.killer_id)
        # positive swing for the killing side
        if killer_side is TeamSide.CT:
            swing = after - before
        else:
            swing = before - after

        # credit shares
        shares: dict[str, float] = {killer: 0.40}
        # damage share among attackers on this victim
        for pid in {str(p.player_id) for p in match.players}:
            share = _damage_share_on_victim(round_, kill.victim_id, PlayerId(pid))
            if share > 0:
                shares[pid] = shares.get(pid, 0.0) + 0.30 * share
        flash = _flash_assister(round_, kill)
        if flash is not None:
            shares[str(flash)] = shares.get(str(flash), 0.0) + 0.15
        if (victim, killer) in trade_pairs or victim in traded_victims:
            shares[killer] = shares.get(killer, 0.0) + 0.10

        total_share = sum(shares.values()) or 1.0
        for pid, weight in shares.items():
            if pid in credits:
                credits[pid] += swing * (weight / total_share)

    # end-of-round contribution for winners that survived / defused narrative
    winners = [str(s) for s in round_.survivors if _player_side(match, s) is round_.winner]
    if winners:
        bonus = 0.04
        for pid in winners:
            credits[pid] = credits.get(pid, 0.0) + bonus / len(winners)

    return [SwingCredit(player_id=pid, delta=val) for pid, val in credits.items()]


def round_swing_total(match: Match, player_id: PlayerId) -> float:
    total = 0.0
    pid = str(player_id)
    for rnd in match.rounds:
        for credit in round_swing_credits(rnd, match):
            if credit.player_id == pid:
                total += credit.delta
    return total


def round_swing_per_round(match: Match, player_id: PlayerId) -> float:
    if not match.rounds:
        return 0.0
    return round_swing_total(match, player_id) / len(match.rounds)
