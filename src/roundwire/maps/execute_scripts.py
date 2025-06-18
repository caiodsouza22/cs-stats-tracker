"""A few named utility execute scripts per map (examples, not a full book)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UtilStep:
    util: str
    callout: str
    delay_ms: int
    note: str


@dataclass(frozen=True, slots=True)
class ExecuteScript:
    key: str
    map_name: str
    site: str
    side: str
    steps: tuple[UtilStep, ...]
    summary: str


SCRIPTS: dict[str, ExecuteScript] = {
    "mirage_a_default": ExecuteScript(
        key="mirage_a_default",
        map_name="de_mirage",
        site="A",
        side="T",
        steps=(
            UtilStep("smoke", "stairs", 0, "one-way / stairs block"),
            UtilStep("smoke", "jungle", 400, "jungle + connector"),
            UtilStep("flash", "ramp", 900, "pop flash for ramp"),
            UtilStep("molly", "tetris", 1400, "clear tetris"),
        ),
        summary="T A default smokes on Mirage (stairs/jungle) into ramp flash",
    ),
    "mirage_b_apps": ExecuteScript(
        key="mirage_b_apps",
        map_name="de_mirage",
        site="B",
        side="T",
        steps=(
            UtilStep("smoke", "market window", 0, "window deny"),
            UtilStep("flash", "apps", 700, "apps entry flash"),
            UtilStep("molly", "bench", 1200, "bench clear"),
        ),
        summary="T B apps execute on Mirage",
    ),
    "ancient_a_cave": ExecuteScript(
        key="ancient_a_cave",
        map_name="de_ancient",
        site="A",
        side="T",
        steps=(
            UtilStep("smoke", "donut", 0, "donut block"),
            UtilStep("smoke", "temple", 350, "temple line"),
            UtilStep("flash", "cave", 800, "cave pop"),
        ),
        summary="T A cave hit on Ancient",
    ),
    "anubis_b_water": ExecuteScript(
        key="anubis_b_water",
        map_name="de_anubis",
        site="B",
        side="T",
        steps=(
            UtilStep("smoke", "bridge", 0, "bridge cross"),
            UtilStep("molly", "pillar", 600, "pillar clear"),
            UtilStep("flash", "water", 1100, "water entry"),
        ),
        summary="T B water execute on Anubis",
    ),
}


def script(key: str) -> ExecuteScript:
    return SCRIPTS[key]


def scripts_for_map(map_name: str) -> list[ExecuteScript]:
    return [s for s in SCRIPTS.values() if s.map_name == map_name]


def describe_script(key: str) -> str:
    s = script(key)
    path = " -> ".join(step.callout for step in s.steps)
    return f"{s.side} {s.site} on {s.map_name}: {path}. {s.summary}"


def describe_all_scripts() -> dict[str, str]:
    return {key: describe_script(key) for key in SCRIPTS}
