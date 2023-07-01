"""Build a structured match story from analytics primitives."""

from __future__ import annotations

from dataclasses import dataclass, field

from roundwire.analysis.anti_eco import anti_eco_success_rate
from roundwire.analysis.gaps import average_cash_gap, average_equipment_gap
from roundwire.analysis.momentum import detect_swings, lead_changes
from roundwire.analysis.opening_economy import full_buy_opening_conversion
from roundwire.analysis.pistol_conversion import pistol_conversion_rate, pistol_winners
from roundwire.analysis.trade_quality import opening_trade_rate
from roundwire.combat.advanced import advanced_cards, match_combat_dashboard
from roundwire.combat.narrative import match_blurb
from roundwire.economy.narrative import economy_blurb
from roundwire.economy.summary import economy_match_summary
from roundwire.maps.analytics import format_map_card, map_card
from roundwire.models.match import Match
from roundwire.rating.extended import extended_table
from roundwire.utility.advanced import utility_cards


@dataclass
class MatchStory:
    headline: str
    map_line: str
    pistols: list[str]
    swings: list[str] = field(default_factory=list)
    economy_notes: list[str] = field(default_factory=list)
    combat_notes: list[str] = field(default_factory=list)
    utility_notes: list[str] = field(default_factory=list)
    closing: str = ""

    def render(self) -> str:
        chunks = [self.headline, self.map_line, "Pistols: " + ", ".join(self.pistols) or "n/a"]
        if self.swings:
            chunks.append("Swings:")
            chunks.extend(f"  - {s}" for s in self.swings)
        if self.economy_notes:
            chunks.append("Economy:")
            chunks.extend(f"  - {s}" for s in self.economy_notes)
        if self.combat_notes:
            chunks.append("Combat:")
            chunks.extend(f"  - {s}" for s in self.combat_notes)
        if self.utility_notes:
            chunks.append("Utility:")
            chunks.extend(f"  - {s}" for s in self.utility_notes)
        if self.closing:
            chunks.append(self.closing)
        return "\n".join(chunks)


def build_match_story(match: Match) -> MatchStory:
    card = map_card(match)
    swings = detect_swings(match, min_length=3)
    eco = economy_match_summary(match)
    combat = advanced_cards(match)
    util = utility_cards(match)
    impact = extended_table(match)

    economy_notes = [
        economy_blurb(match),
        f"avg cash gap={average_cash_gap(match):.0f}, avg EQ gap={average_equipment_gap(match):.0f}",
        f"anti-eco success={anti_eco_success_rate(match)*100:.0f}%",
        f"pistol conversion={pistol_conversion_rate(match)*100:.0f}%",
    ]
    for row in eco:
        economy_notes.append(
            f"{row.side} buys={row.buys} eco_upsets={row.eco_upsets}"
        )

    combat_notes = [
        f"opening trade rate={opening_trade_rate(match)*100:.0f}%",
        f"full-buy opening conversion={full_buy_opening_conversion(match)*100:.0f}%",
        f"lead changes={lead_changes(match)}",
    ]
    for c in combat[:3]:
        combat_notes.append(
            f"{c.name}: {c.kills}/{c.deaths} ADR {c.adr:.0f} KAST {c.kast*100:.0f}%"
        )
    if impact:
        combat_notes.append(
            f"top composite rating: {impact[0].name} ({impact[0].composite:.3f})"
        )

    utility_notes = []
    for u in util[:3]:
        utility_notes.append(
            f"{u.name}: value={u.value_score:.1f} flashes={u.enemies_flashed} spend={u.spend}"
        )

    swing_lines = [
        f"R{s.start_round}-R{s.end_round} {s.side} x{s.length}" for s in swings
    ]

    dashboard = match_combat_dashboard(match)
    closing = (
        f"Dashboard opening conversion={float(dashboard['opening_conversion'])*100:.0f}%."
    )

    return MatchStory(
        headline=match_blurb(match),
        map_line=format_map_card(card),
        pistols=pistol_winners(match),
        swings=swing_lines,
        economy_notes=economy_notes,
        combat_notes=combat_notes,
        utility_notes=utility_notes,
        closing=closing,
    )
