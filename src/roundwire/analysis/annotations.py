"""Annotate rounds with derived labels for coaching dashboards."""
from __future__ import annotations

from dataclasses import dataclass, field

from roundwire.combat.opening import first_kill, was_traded
from roundwire.economy.classify import classify_round_buy
from roundwire.economy.pistol import is_pistol_round
from roundwire.models.buy_type import BuyType
from roundwire.models.match import Match
from roundwire.models.round import Round
from roundwire.models.team import TeamSide


@dataclass(slots=True)
class RoundAnnotation:
    number: int
    winner: str
    ct_buy: str
    t_buy: str
    pistol: bool
    opening_side: str | None
    opening_traded: bool
    kill_count: int
    util_count: int
    bomb_planted: bool
    labels: list[str] = field(default_factory=list)


def annotate_round(match: Match, round_: Round) -> RoundAnnotation:
    buys = classify_round_buy(round_, match)
    fk = first_kill(round_)
    opening_side = None
    traded = False
    if fk is not None:
        killer = match.player_map().get(fk.killer_id)
        opening_side = killer.team.value if killer else None
        traded = was_traded(round_, fk)
    labels: list[str] = []
    pistol = is_pistol_round(round_, match.edition)
    if pistol:
        labels.append('pistol')
    if buys['CT'] is BuyType.ECO and buys['T'] is BuyType.FULL:
        labels.append('ct_eco_vs_full')
    if buys['T'] is BuyType.ECO and buys['CT'] is BuyType.FULL:
        labels.append('t_eco_vs_full')
    if buys['CT'] is BuyType.FORCE or buys['T'] is BuyType.FORCE:
        labels.append('force_round')
    if round_.bomb_planted:
        labels.append('plant')
        if round_.winner is TeamSide.CT:
            labels.append('retake_or_defuse')
        else:
            labels.append('post_plant_convert')
    if traded:
        labels.append('opening_traded')
    if len(round_.kills) >= 8:
        labels.append('high_kill')
    if len(round_.utility) >= 6:
        labels.append('util_heavy')
    return RoundAnnotation(
        number=int(round_.number),
        winner=round_.winner.value,
        ct_buy=buys['CT'].value,
        t_buy=buys['T'].value,
        pistol=pistol,
        opening_side=opening_side,
        opening_traded=traded,
        kill_count=len(round_.kills),
        util_count=len(round_.utility),
        bomb_planted=round_.bomb_planted,
        labels=labels,
    )


def annotate_match(match: Match) -> list[RoundAnnotation]:
    return [annotate_round(match, rnd) for rnd in match.rounds]


def label_histogram(match: Match) -> dict[str, int]:
    counts: dict[str, int] = {}
    for ann in annotate_match(match):
        for label in ann.labels:
            counts[label] = counts.get(label, 0) + 1
    return counts


def rounds_with_label(match: Match, label: str) -> list[int]:
    return [a.number for a in annotate_match(match) if label in a.labels]

LABEL_BLURBS: dict[str, str] = {
    'pistol': 'Half-opening round with limited economy.',
    'ct_eco_vs_full': 'CT saved against a T gun buy.',
    't_eco_vs_full': 'T saved against a CT gun buy.',
    'force_round': 'At least one side forced.',
    'plant': 'Bomb was planted.',
    'retake_or_defuse': 'CT won after a plant.',
    'post_plant_convert': 'T converted a post-plant.',
    'opening_traded': 'Opening kill was traded quickly.',
    'high_kill': 'Unusually high kill count.',
    'util_heavy': 'Heavy utility usage.',
}


def explain_labels(labels: list[str]) -> list[str]:
    return [LABEL_BLURBS.get(label, f'unknown label {label}') for label in labels]


def annotation_table(match: Match) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for ann in annotate_match(match):
        rows.append({
            'number': ann.number,
            'winner': ann.winner,
            'ct_buy': ann.ct_buy,
            't_buy': ann.t_buy,
            'labels': list(ann.labels),
            'opening_side': ann.opening_side,
            'traded': ann.opening_traded,
        })
    return rows

