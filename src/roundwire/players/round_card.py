"""Per-round player cards for timeline and form analysis."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.combat.opening import first_kill, was_traded
from roundwire.economy.classify import classify_team_buy
from roundwire.economy.equipment import inventory_for_player
from roundwire.models.match import Match
from roundwire.models.round import Round
from roundwire.models.utility_event import UtilityKind
from roundwire.types import PlayerId


@dataclass(frozen=True, slots=True)
class PlayerRoundCard:
    round_number: int
    player_id: str
    team: str
    kills: int
    deaths: int
    assists: int
    damage: int
    survived: bool
    opening_kill: bool
    opening_death: bool
    traded_opening: bool
    equipment_value: int
    cash: int
    team_buy: str
    won: bool
    flashes: int
    enemies_flashed: int
    util_thrown: int
    headshots: int
    multi_kill: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "round": self.round_number,
            "player_id": self.player_id,
            "team": self.team,
            "kills": self.kills,
            "deaths": self.deaths,
            "assists": self.assists,
            "damage": self.damage,
            "survived": self.survived,
            "opening_kill": self.opening_kill,
            "opening_death": self.opening_death,
            "traded_opening": self.traded_opening,
            "equipment_value": self.equipment_value,
            "cash": self.cash,
            "team_buy": self.team_buy,
            "won": self.won,
            "flashes": self.flashes,
            "enemies_flashed": self.enemies_flashed,
            "util_thrown": self.util_thrown,
            "headshots": self.headshots,
            "multi_kill": self.multi_kill,
        }


def player_round_card(match: Match, round_: Round, player_id: PlayerId) -> PlayerRoundCard:
    player = match.player_map()[player_id]
    kills = round_.kills_for(player_id)
    deaths = round_.deaths_for(player_id)
    fk = first_kill(round_)
    opening_kill = fk is not None and fk.killer_id == player_id
    opening_death = fk is not None and fk.victim_id == player_id
    traded = bool(fk and opening_death and was_traded(round_, fk))
    inv = inventory_for_player(round_, str(player_id))
    flashes = enemies = util = 0
    for event in round_.utility:
        if event.thrower_id != player_id:
            continue
        util += 1
        if event.kind is UtilityKind.FLASH:
            flashes += 1
            enemies += event.enemies_flashed
    assists = sum(1 for k in round_.kills if k.assisted_by == player_id)
    return PlayerRoundCard(
        round_number=int(round_.number),
        player_id=str(player_id),
        team=player.team.value,
        kills=len(kills),
        deaths=len(deaths),
        assists=assists,
        damage=round_.damage_dealt_by(player_id),
        survived=player_id in round_.survivors,
        opening_kill=opening_kill,
        opening_death=opening_death,
        traded_opening=traded,
        equipment_value=inv.equipment_value if inv else 0,
        cash=inv.cash if inv else 0,
        team_buy=classify_team_buy(round_, match, player.team).value,
        won=round_.winner is player.team,
        flashes=flashes,
        enemies_flashed=enemies,
        util_thrown=util,
        headshots=sum(1 for k in kills if k.headshot),
        multi_kill=len(kills) >= 2,
    )


def player_round_log(match: Match, player_id: PlayerId) -> list[PlayerRoundCard]:
    return [player_round_card(match, rnd, player_id) for rnd in match.rounds]


def impactful_rounds(match: Match, player_id: PlayerId, min_kills: int = 2) -> list[int]:
    return [
        card.round_number
        for card in player_round_log(match, player_id)
        if card.kills >= min_kills or card.opening_kill or card.enemies_flashed >= 2
    ]


def quiet_rounds(match: Match, player_id: PlayerId) -> list[int]:
    return [
        card.round_number
        for card in player_round_log(match, player_id)
        if card.kills == 0 and card.damage < 20 and card.util_thrown == 0
    ]


def kast_mask(match: Match, player_id: PlayerId) -> list[bool]:
    """Per-round whether the player got a KAST tick (approx via card fields + trades)."""
    from roundwire.combat.trades import trades_in_round

    mask: list[bool] = []
    for rnd in match.rounds:
        card = player_round_card(match, rnd, player_id)
        traded = any(
            t.trade.killer_id == player_id for t in trades_in_round(rnd)
        )
        mask.append(
            card.kills > 0
            or card.assists > 0
            or card.survived
            or traded
        )
    return mask


def damage_series(match: Match, player_id: PlayerId) -> list[int]:
    return [card.damage for card in player_round_log(match, player_id)]


def kill_series(match: Match, player_id: PlayerId) -> list[int]:
    return [card.kills for card in player_round_log(match, player_id)]
