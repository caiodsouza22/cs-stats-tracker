"""Coaching-oriented round concepts linked to analytics hooks."""
from __future__ import annotations

from dataclasses import dataclass

from roundwire.models.buy_type import BuyType
from roundwire.models.match import Match
from roundwire.economy.classify import classify_round_buy


@dataclass(frozen=True, slots=True)
class CoachingTopic:
    key: str
    summary: str


TOPICS: dict[str, CoachingTopic] = {
    'pistol': CoachingTopic('pistol', 'Pistol rounds set half tempo; survive with utility denial.'),
    'eco': CoachingTopic('eco', 'Eco rounds bank for the next rifle buy; avoid hero peeks.'),
    'force': CoachingTopic('force', 'Force buys seek trades and plants, not perfect executes.'),
    'full': CoachingTopic('full', 'Full buys pair rifles with smokes/flashes for site hits.'),
    'awp': CoachingTopic('awp', 'AWP rounds need exit fraggers and flash support.'),
    'retake': CoachingTopic('retake', 'Retakes hinge on synchronized utility, not solo peeks.'),
    'execute': CoachingTopic('execute', 'Executes start with map control then overlapping smokes.'),
    'mid': CoachingTopic('mid', 'Mid control opens rotates; lose mid and lose options.'),
    'trade': CoachingTopic('trade', 'Trade discipline turns lost openers into even rounds.'),
    'default': CoachingTopic('default', 'Defaults gather info; do not overcommit early timers.'),
    'stack': CoachingTopic('stack', 'Stacks punish over-rotations but bleed map control.'),
    'lurk': CoachingTopic('lurk', 'Lurks create timing splits; coordinate with the hit.'),
    'contact': CoachingTopic('contact', 'Contact plays reduce utility spend, raise aim variance.'),
    'slow': CoachingTopic('slow', 'Slow paces burn clock for post-plant advantages.'),
    'fast': CoachingTopic('fast', 'Fast paces catch unset setups before utility lands.'),
}


def topic(key: str) -> CoachingTopic:
    return TOPICS[key]


def topics_for_buy(buy: BuyType) -> list[CoachingTopic]:
    mapping = {
        BuyType.PISTOL: ['pistol'],
        BuyType.ECO: ['eco', 'stack'],
        BuyType.FORCE: ['force', 'contact'],
        BuyType.SEMI: ['force', 'awp'],
        BuyType.FULL: ['full', 'execute', 'default'],
        BuyType.UNKNOWN: ['default'],
    }
    return [TOPICS[k] for k in mapping.get(buy, ['default'])]

def advice(key: str, match: Match) -> str:
    item = TOPICS[key]
    ct, t = match.score()
    return f'{item.key} advice on {match.map_name} ({ct}-{t}): {item.summary}'


def round_advice(match: Match, round_number: int) -> list[str]:
    rnd = match.round_by_number(round_number)
    if rnd is None:
        return []
    buys = classify_round_buy(rnd, match)
    out: list[str] = []
    for side, buy in buys.items():
        for top in topics_for_buy(buy):
            out.append(f'{side}: ' + advice(top.key, match))
    return out


def all_advice(match: Match) -> dict[str, str]:
    return {key: advice(key, match) for key in TOPICS}

