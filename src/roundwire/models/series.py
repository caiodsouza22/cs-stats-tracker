"""Best-of series aggregation across maps."""

from __future__ import annotations

from dataclasses import dataclass, field

from roundwire.models.match import Match
from roundwire.models.team import TeamSide


@dataclass(slots=True)
class Series:
    series_id: str
    team_a: str
    team_b: str
    best_of: int = 3
    maps: list[Match] = field(default_factory=list)

    def map_wins(self) -> tuple[int, int]:
        a = 0
        b = 0
        for match in self.maps:
            winner = match.winner_side()
            if winner is None:
                continue
            ct_name = match.team_ct_name
            t_name = match.team_t_name
            if winner is TeamSide.CT:
                if ct_name == self.team_a:
                    a += 1
                elif ct_name == self.team_b:
                    b += 1
            else:
                if t_name == self.team_a:
                    a += 1
                elif t_name == self.team_b:
                    b += 1
        return a, b

    def is_complete(self) -> bool:
        needed = self.best_of // 2 + 1
        a, b = self.map_wins()
        return a >= needed or b >= needed
