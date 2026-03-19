"""Utility timing patterns relative to executes and openings."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.combat.opening import first_kill
from roundwire.models.match import Match
from roundwire.models.utility_event import UtilityKind
from roundwire.stats.aggregates import mean
from roundwire.types import PlayerId


@dataclass(frozen=True, slots=True)
class UtilTimingCard:
    player_id: str
    name: str
    pre_open_util: int
    post_open_util: int
    avg_throw_ms: float
    flash_before_kill: int
    smoke_before_plant_proxy: int

    def to_dict(self) -> dict[str, object]:
        return {
            "player_id": self.player_id,
            "name": self.name,
            "pre_open_util": self.pre_open_util,
            "post_open_util": self.post_open_util,
            "avg_throw_ms": round(self.avg_throw_ms, 1),
            "flash_before_kill": self.flash_before_kill,
            "smoke_before_plant_proxy": self.smoke_before_plant_proxy,
        }


def util_timing_card(match: Match, player_id: PlayerId) -> UtilTimingCard:
    player = match.player_map()[player_id]
    pre = post = flash_setup = smoke_early = 0
    throws: list[float] = []
    for rnd in match.rounds:
        fk = first_kill(rnd)
        open_ms = int(fk.tick_ms) if fk else None
        for event in rnd.utility:
            if event.thrower_id != player_id:
                continue
            throws.append(float(event.tick_ms))
            if open_ms is None:
                continue
            if int(event.tick_ms) <= open_ms:
                pre += 1
                if event.kind is UtilityKind.FLASH:
                    flash_setup += 1
            else:
                post += 1
            if event.kind is UtilityKind.SMOKE and int(event.tick_ms) <= 25000:
                smoke_early += 1
    return UtilTimingCard(
        player_id=str(player_id),
        name=player.name,
        pre_open_util=pre,
        post_open_util=post,
        avg_throw_ms=mean(throws),
        flash_before_kill=flash_setup,
        smoke_before_plant_proxy=smoke_early,
    )


def util_timing_table(match: Match) -> list[dict[str, object]]:
    rows = [util_timing_card(match, p.player_id).to_dict() for p in match.players]
    return sorted(rows, key=lambda r: (-r["pre_open_util"], r["name"]))


def setup_flash_rate(match: Match, player_id: PlayerId) -> float:
    card = util_timing_card(match, player_id)
    total = card.pre_open_util + card.post_open_util
    return (card.flash_before_kill / total) if total else 0.0


def early_smoke_share(match: Match, player_id: PlayerId) -> float:
    card = util_timing_card(match, player_id)
    from roundwire.utility.smoke import smoke_count

    total = smoke_count(match, player_id)
    return (card.smoke_before_plant_proxy / total) if total else 0.0
