"""Scoreline helpers for matches and series."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.models.edition import GameEdition
from roundwire.models.match import Match
from roundwire.models.team import TeamSide


@dataclass(frozen=True, slots=True)
class Scoreline:
    ct: int
    t: int
    edition: GameEdition

    @property
    def total(self) -> int:
        return self.ct + self.t

    @property
    def leader(self) -> TeamSide | None:
        if self.ct > self.t:
            return TeamSide.CT
        if self.t > self.ct:
            return TeamSide.T
        return None

    def is_regulation_complete(self) -> bool:
        threshold = self.edition.win_threshold
        return self.ct >= threshold or self.t >= threshold

    def format(self) -> str:
        return f"{self.ct}:{self.t}"


def scoreline_from_match(match: Match) -> Scoreline:
    ct, t = match.score()
    return Scoreline(ct=ct, t=t, edition=match.edition)
