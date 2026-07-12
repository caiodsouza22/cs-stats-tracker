"""Callout / site affinity inferred from utility tags and plants."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass

from roundwire.maps.bomb_sites import extract_site_tags
from roundwire.models.match import Match
from roundwire.stats.aggregates import safe_div
from roundwire.types import PlayerId


@dataclass(frozen=True, slots=True)
class CalloutAffinity:
    player_id: str
    name: str
    tag_counts: dict[str, int]
    top_tags: tuple[str, ...]
    plant_rounds_present: int
    post_plant_kills: int

    def to_dict(self) -> dict[str, object]:
        return {
            "player_id": self.player_id,
            "name": self.name,
            "tag_counts": dict(self.tag_counts),
            "top_tags": list(self.top_tags),
            "plant_rounds_present": self.plant_rounds_present,
            "post_plant_kills": self.post_plant_kills,
        }


def callout_affinity(match: Match, player_id: PlayerId) -> CalloutAffinity:
    player = match.player_map()[player_id]
    tags: Counter[str] = Counter()
    plant_present = 0
    post_plant_kills = 0
    for rnd in match.rounds:
        for event in rnd.utility:
            if event.thrower_id != player_id:
                continue
            for tag in extract_site_tags(event.tags):
                tags[tag] += 1
        if rnd.bomb_planted:
            # presence proxy: any event or kill in planted round
            touched = any(k.killer_id == player_id or k.victim_id == player_id for k in rnd.kills)
            touched = touched or any(u.thrower_id == player_id for u in rnd.utility)
            if touched or player_id in rnd.survivors:
                plant_present += 1
            for kill in rnd.kills_for(player_id):
                if int(kill.tick_ms) >= 45000:
                    post_plant_kills += 1
    top = tuple(t for t, _ in tags.most_common(5))
    return CalloutAffinity(
        player_id=str(player_id),
        name=player.name,
        tag_counts=dict(tags),
        top_tags=top,
        plant_rounds_present=plant_present,
        post_plant_kills=post_plant_kills,
    )


def affinity_table(match: Match) -> list[dict[str, object]]:
    return [callout_affinity(match, p.player_id).to_dict() for p in match.players]


def team_tag_heatmap(match: Match) -> dict[str, dict[str, int]]:
    heat: dict[str, Counter[str]] = {"CT": Counter(), "T": Counter()}
    pmap = match.player_map()
    for rnd in match.rounds:
        for event in rnd.utility:
            thrower = pmap.get(event.thrower_id)
            if thrower is None:
                continue
            for tag in extract_site_tags(event.tags):
                heat[thrower.team.value][tag] += 1
    return {side: dict(counter) for side, counter in heat.items()}


def tag_share(match: Match, player_id: PlayerId) -> dict[str, float]:
    aff = callout_affinity(match, player_id)
    total = sum(aff.tag_counts.values())
    return {tag: safe_div(float(n), float(total)) for tag, n in aff.tag_counts.items()}


def dominant_site(match: Match, player_id: PlayerId) -> str | None:
    aff = callout_affinity(match, player_id)
    site_tags = {k: v for k, v in aff.tag_counts.items() if k in {"A", "B"}}
    if not site_tags:
        return None
    return max(site_tags.items(), key=lambda kv: kv[1])[0]


def mid_control_throws(match: Match, player_id: PlayerId) -> int:
    aff = callout_affinity(match, player_id)
    return aff.tag_counts.get("mid", 0) + aff.tag_counts.get("yard", 0) + aff.tag_counts.get("ramp", 0)
