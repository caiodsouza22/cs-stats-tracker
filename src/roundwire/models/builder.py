"""Fluent helpers for constructing synthetic matches in tests/examples."""

from __future__ import annotations

from roundwire.models.edition import GameEdition
from roundwire.models.match import Match
from roundwire.models.player import Player
from roundwire.models.round import Round
from roundwire.models.team import TeamSide
from roundwire.types import MatchId, PlayerId, RoundNumber


class MatchBuilder:
    def __init__(
        self,
        match_id: str,
        map_name: str,
        edition: GameEdition = GameEdition.CS2,
    ) -> None:
        self._match_id = MatchId(match_id)
        self._map_name = map_name
        self._edition = edition
        self._ct_name = "CT Side"
        self._t_name = "T Side"
        self._players: list[Player] = []
        self._rounds: list[Round] = []

    def teams(self, ct: str, t: str) -> MatchBuilder:
        self._ct_name = ct
        self._t_name = t
        return self

    def add_player(self, player_id: str, name: str, team: TeamSide) -> MatchBuilder:
        self._players.append(
            Player(player_id=PlayerId(player_id), name=name, team=team)
        )
        return self

    def add_round(self, round_: Round) -> MatchBuilder:
        self._rounds.append(round_)
        return self

    def empty_round(self, number: int, winner: TeamSide) -> MatchBuilder:
        self._rounds.append(
            Round(
                number=RoundNumber(number),
                winner=winner,
                win_reason="elimination",
            )
        )
        return self

    def build(self) -> Match:
        return Match(
            match_id=self._match_id,
            map_name=self._map_name,
            edition=self._edition,
            team_ct_name=self._ct_name,
            team_t_name=self._t_name,
            players=list(self._players),
            rounds=list(self._rounds),
        )
