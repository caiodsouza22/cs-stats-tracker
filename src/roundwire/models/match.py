"""Match container aggregating players and rounds."""

from __future__ import annotations

from dataclasses import dataclass, field

from roundwire.models.edition import GameEdition
from roundwire.models.player import Player
from roundwire.models.round import Round
from roundwire.models.team import TeamSide
from roundwire.types import MatchId, PlayerId


@dataclass(slots=True)
class Match:
    match_id: MatchId
    map_name: str
    edition: GameEdition
    team_ct_name: str
    team_t_name: str
    players: list[Player] = field(default_factory=list)
    rounds: list[Round] = field(default_factory=list)
    series_score: tuple[int, int] | None = None
    event_name: str | None = None
    played_at: str | None = None

    def player_map(self) -> dict[PlayerId, Player]:
        return {p.player_id: p for p in self.players}

    def players_on(self, side: TeamSide) -> list[Player]:
        return [p for p in self.players if p.team == side]

    def score(self) -> tuple[int, int]:
        ct = sum(1 for r in self.rounds if r.winner is TeamSide.CT)
        t = sum(1 for r in self.rounds if r.winner is TeamSide.T)
        return ct, t

    def winner_side(self) -> TeamSide | None:
        ct, t = self.score()
        threshold = self.edition.win_threshold
        if ct >= threshold and ct > t:
            return TeamSide.CT
        if t >= threshold and t > ct:
            return TeamSide.T
        if len(self.rounds) >= self.edition.regulation_rounds:
            if ct > t:
                return TeamSide.CT
            if t > ct:
                return TeamSide.T
        return None

    def rounds_won_by(self, side: TeamSide) -> int:
        return sum(1 for rnd in self.rounds if rnd.winner is side)

    def round_by_number(self, number: int) -> Round | None:
        for rnd in self.rounds:
            if int(rnd.number) == number:
                return rnd
        return None

    def player_by_name(self, name: str) -> Player | None:
        key = name.lower()
        for player in self.players:
            if player.name.lower() == key:
                return player
        return None

    def half_scores(self) -> tuple[tuple[int, int], tuple[int, int]]:
        from roundwire.rules.mr_rules import half_length

        half = half_length(self.edition)
        first = self.rounds[:half]
        second = self.rounds[half:]

        def _score(rounds: list[Round]) -> tuple[int, int]:
            return (
                sum(1 for r in rounds if r.winner is TeamSide.CT),
                sum(1 for r in rounds if r.winner is TeamSide.T),
            )

        return _score(first), _score(second)

    def to_dict(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "match_id": str(self.match_id),
            "map_name": self.map_name,
            "edition": self.edition.value,
            "team_ct_name": self.team_ct_name,
            "team_t_name": self.team_t_name,
            "players": [p.to_dict() for p in self.players],
            "rounds": [r.to_dict() for r in self.rounds],
        }
        if self.series_score is not None:
            payload["series_score"] = list(self.series_score)
        if self.event_name is not None:
            payload["event_name"] = self.event_name
        if self.played_at is not None:
            payload["played_at"] = self.played_at
        return payload

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Match:
        players_raw = data.get("players", [])
        rounds_raw = data.get("rounds", [])
        if not isinstance(players_raw, list) or not isinstance(rounds_raw, list):
            raise ValueError("players and rounds must be arrays")
        series_raw = data.get("series_score")
        series: tuple[int, int] | None = None
        if isinstance(series_raw, list) and len(series_raw) == 2:
            series = (int(series_raw[0]), int(series_raw[1]))
        return cls(
            match_id=MatchId(str(data["match_id"])),
            map_name=str(data["map_name"]),
            edition=GameEdition.parse(str(data["edition"])),
            team_ct_name=str(data.get("team_ct_name", "CT")),
            team_t_name=str(data.get("team_t_name", "T")),
            players=[Player.from_dict(x) for x in players_raw if isinstance(x, dict)],
            rounds=[Round.from_dict(x) for x in rounds_raw if isinstance(x, dict)],
            series_score=series,
            event_name=str(data["event_name"]) if data.get("event_name") else None,
            played_at=str(data["played_at"]) if data.get("played_at") else None,
        )
