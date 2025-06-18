"""Named round scenarios for demos and coaching notes."""

from __future__ import annotations

from dataclasses import dataclass

from roundwire.models.buy_type import BuyType


@dataclass(frozen=True, slots=True)
class RoundScenario:
    key: str
    map_name: str
    winner: str
    buy_focus: str
    win_reason: str
    bomb_planted: bool
    note: str
    tension: int

    @property
    def buy_type(self) -> BuyType:
        return BuyType(self.buy_focus) if self.buy_focus in BuyType._value2member_map_ else BuyType.UNKNOWN


SCENARIOS: dict[str, RoundScenario] = {
    "pistol_ct_win_mirage": RoundScenario(
        "pistol_ct_win_mirage", "de_mirage", "CT", "pistol", "elimination", False,
        "CT wins pistol with util denial on Mirage.", 3,
    ),
    "pistol_t_plant_mirage": RoundScenario(
        "pistol_t_plant_mirage", "de_mirage", "T", "pistol", "bomb_exploded", True,
        "T plants on pistol and converts on Mirage.", 6,
    ),
    "eco_ct_steal_anubis": RoundScenario(
        "eco_ct_steal_anubis", "de_anubis", "CT", "eco", "elimination", False,
        "CT ecos steal vs T full on Anubis.", 8,
    ),
    "force_mid_pick_ancient": RoundScenario(
        "force_mid_pick_ancient", "de_ancient", "T", "force", "elimination", False,
        "T force finds mid opener on Ancient.", 5,
    ),
    "full_execute_a_mirage": RoundScenario(
        "full_execute_a_mirage", "de_mirage", "T", "full", "bomb_exploded", True,
        "T full execute onto A on Mirage.", 4,
    ),
    "retake_b_anubis": RoundScenario(
        "retake_b_anubis", "de_anubis", "CT", "full", "defuse", True,
        "CT retakes B after plant on Anubis.", 9,
    ),
    "anti_eco_clean_mirage": RoundScenario(
        "anti_eco_clean_mirage", "de_mirage", "T", "full", "elimination", False,
        "T anti-eco clears without overpeeking.", 2,
    ),
    "bonus_loss_ancient": RoundScenario(
        "bonus_loss_ancient", "de_ancient", "CT", "force", "elimination", False,
        "CT bonus round fails; loss bonus stacks.", 7,
    ),
    "reentry_mirage": RoundScenario(
        "reentry_mirage", "de_mirage", "T", "full", "bomb_exploded", True,
        "Re-hit A after failed first contact on Mirage.", 6,
    ),
    "time_bleed_ct_anubis": RoundScenario(
        "time_bleed_ct_anubis", "de_anubis", "CT", "full", "time", False,
        "CT runs the clock without a plant attempt.", 4,
    ),
    "clutch_1v2_ancient": RoundScenario(
        "clutch_1v2_ancient", "de_ancient", "T", "full", "bomb_exploded", True,
        "T 1v2 post-plant clutch on Ancient.", 10,
    ),
    "eco_t_steal_mirage": RoundScenario(
        "eco_t_steal_mirage", "de_mirage", "T", "eco", "bomb_exploded", True,
        "T ecos plant vs CT full on Mirage.", 8,
    ),
}


def scenario(key: str) -> RoundScenario:
    return SCENARIOS[key]


def scenarios_for_map(map_name: str) -> list[RoundScenario]:
    return [s for s in SCENARIOS.values() if s.map_name == map_name]


def scenarios_for_winner(side: str) -> list[RoundScenario]:
    return [s for s in SCENARIOS.values() if s.winner == side]


def scenarios_with_plant() -> list[RoundScenario]:
    return [s for s in SCENARIOS.values() if s.bomb_planted]


def describe(key: str) -> str:
    s = scenario(key)
    plant = "plant" if s.bomb_planted else "no-plant"
    return (
        f"{s.key}: {s.map_name} {s.winner} wins via {s.win_reason} "
        f"({s.buy_focus}, {plant}, tension={s.tension}). {s.note}"
    )


def describe_all() -> dict[str, str]:
    return {key: describe(key) for key in SCENARIOS}


def high_tension(min_tension: int = 7) -> list[RoundScenario]:
    return [s for s in SCENARIOS.values() if s.tension >= min_tension]
