"""Aggregate a player book across multiple matches by display name."""

from __future__ import annotations

from dataclasses import dataclass, field

from roundwire.combat.adr import adr_for_player
from roundwire.combat.kd import death_count, kill_count
from roundwire.combat.opening import opening_kills_for
from roundwire.models.match import Match
from roundwire.rating.impact import impact_score
from roundwire.stats.aggregates import mean
from roundwire.stats.distribution import summarize


@dataclass
class PlayerBookEntry:
    name: str
    matches: int = 0
    kills: int = 0
    deaths: int = 0
    opening_kills: int = 0
    impact_samples: list[float] = field(default_factory=list)
    adr_samples: list[float] = field(default_factory=list)
    maps: list[str] = field(default_factory=list)

    def add_match(self, match: Match) -> None:
        player = match.player_by_name(self.name)
        if player is None:
            return
        self.matches += 1
        self.kills += kill_count(match, player.player_id)
        self.deaths += death_count(match, player.player_id)
        self.opening_kills += opening_kills_for(match, player.player_id)
        self.impact_samples.append(impact_score(match, player.player_id))
        self.adr_samples.append(adr_for_player(match, player.player_id))
        self.maps.append(match.map_name)

    def summary(self) -> dict[str, object]:
        return {
            "name": self.name,
            "matches": self.matches,
            "kills": self.kills,
            "deaths": self.deaths,
            "kd": (self.kills / self.deaths) if self.deaths else float(self.kills),
            "opening_kills": self.opening_kills,
            "impact": summarize(self.impact_samples),
            "adr": summarize(self.adr_samples),
            "maps": sorted(set(self.maps)),
            "mean_impact": mean(self.impact_samples),
            "mean_adr": mean(self.adr_samples),
        }


@dataclass
class PlayerBook:
    entries: dict[str, PlayerBookEntry] = field(default_factory=dict)

    def ingest(self, match: Match) -> None:
        for player in match.players:
            entry = self.entries.setdefault(player.name, PlayerBookEntry(name=player.name))
            entry.add_match(match)

    def top_by_kills(self, n: int = 5) -> list[PlayerBookEntry]:
        return sorted(self.entries.values(), key=lambda e: (-e.kills, e.name))[:n]

    def top_by_impact(self, n: int = 5) -> list[PlayerBookEntry]:
        return sorted(
            self.entries.values(),
            key=lambda e: (-mean(e.impact_samples), e.name),
        )[:n]

    def as_rows(self) -> list[dict[str, object]]:
        return [e.summary() for e in sorted(self.entries.values(), key=lambda e: e.name)]
