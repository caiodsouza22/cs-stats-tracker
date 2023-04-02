"""Map control proxies from bomb plants and site tags."""

from __future__ import annotations

from collections import Counter

from roundwire.maps.bomb_sites import extract_site_tags
from roundwire.models.match import Match
from roundwire.models.team import TeamSide


def plant_rate(match: Match) -> float:
    if not match.rounds:
        return 0.0
    return sum(1 for r in match.rounds if r.bomb_planted) / len(match.rounds)


def post_plant_wins(match: Match) -> float:
    planted = [r for r in match.rounds if r.bomb_planted]
    if not planted:
        return 0.0
    return sum(1 for r in planted if r.winner is TeamSide.T) / len(planted)


def site_mention_share(match: Match) -> dict[str, float]:
    counter: Counter[str] = Counter()
    total = 0
    for rnd in match.rounds:
        for event in rnd.utility:
            tags = extract_site_tags(event.tags)
            for tag in tags:
                counter[tag] += 1
                total += 1
    if total == 0:
        return {}
    return {k: v / total for k, v in counter.items()}


def ct_hold_without_plant(match: Match) -> float:
    """CT win rate on rounds without a plant."""
    rounds = [r for r in match.rounds if not r.bomb_planted]
    if not rounds:
        return 0.0
    return sum(1 for r in rounds if r.winner is TeamSide.CT) / len(rounds)


def t_timeout_wins(match: Match) -> int:
    return sum(1 for r in match.rounds if r.winner is TeamSide.T and r.win_reason == "time")
