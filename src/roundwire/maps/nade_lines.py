"""Grenade line catalogue (illustrative timings, not a line-up database)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NadeLine:
    key: str
    map_name: str
    side: str
    util: str
    from_area: str
    to_area: str
    delay_ms: int
    purpose: str


LINES: tuple[NadeLine, ...] = (
    NadeLine("mirage_window_smoke", "de_mirage", "T", "smoke", "t spawn", "window", 0, "mid control"),
    NadeLine("mirage_stairs_smoke", "de_mirage", "T", "smoke", "top mid", "stairs", 400, "A execute"),
    NadeLine("mirage_jungle_smoke", "de_mirage", "T", "smoke", "top mid", "jungle", 450, "A execute"),
    NadeLine("mirage_ramp_flash", "de_mirage", "T", "flash", "underpass", "ramp", 900, "A entry"),
    NadeLine("mirage_apps_molly", "de_mirage", "T", "molotov", "apps", "bench", 0, "B clear"),
    NadeLine("mirage_connector_smoke", "de_mirage", "CT", "smoke", "ct spawn", "connector", 0, "mid deny"),
    NadeLine("inferno_banana_molly", "de_inferno", "T", "molotov", "t banana", "logs", 0, "banana take"),
    NadeLine("inferno_coffins_smoke", "de_inferno", "T", "smoke", "banana", "coffins", 600, "B execute"),
    NadeLine("inferno_arch_flash", "de_inferno", "T", "flash", "second mid", "arch", 800, "A split"),
    NadeLine("inferno_pit_molly", "de_inferno", "CT", "molotov", "pit", "pit", 0, "A hold"),
    NadeLine("nuke_outside_smoke", "de_nuke", "T", "smoke", "t red", "outside", 0, "yard"),
    NadeLine("nuke_ramp_molly", "de_nuke", "T", "molotov", "lobby", "ramp", 200, "ramp clear"),
    NadeLine("nuke_hut_smoke", "de_nuke", "T", "smoke", "outside", "hut", 500, "A hit"),
    NadeLine("nuke_secret_smoke", "de_nuke", "CT", "smoke", "lobby", "secret", 0, "B deny"),
    NadeLine("ancient_donut_smoke", "de_ancient", "T", "smoke", "mid", "donut", 0, "mid control"),
    NadeLine("ancient_temple_smoke", "de_ancient", "T", "smoke", "cave", "temple", 350, "A cave"),
    NadeLine("ancient_cave_flash", "de_ancient", "T", "flash", "elbow", "cave", 700, "A entry"),
    NadeLine("ancient_red_molly", "de_ancient", "T", "molotov", "mid", "red", 0, "B prep"),
    NadeLine("anubis_bridge_smoke", "de_anubis", "T", "smoke", "canal", "bridge", 0, "B water"),
    NadeLine("anubis_palace_molly", "de_anubis", "T", "molotov", "street", "palace", 200, "A clear"),
    NadeLine("anubis_water_flash", "de_anubis", "T", "flash", "canal", "water", 900, "B entry"),
    NadeLine("anubis_mid_smoke", "de_anubis", "CT", "smoke", "connector", "mid", 0, "mid deny"),
    NadeLine("overpass_monster_smoke", "de_overpass", "T", "smoke", "t spawn", "monster", 0, "B prep"),
    NadeLine("overpass_short_molly", "de_overpass", "T", "molotov", "bathrooms", "short", 300, "A short"),
    NadeLine("overpass_toilet_flash", "de_overpass", "T", "flash", "connector", "bathrooms", 600, "A split"),
    NadeLine("vertigo_ramp_molly", "de_vertigo", "T", "molotov", "t ramp", "sandbags", 0, "A ramp"),
    NadeLine("vertigo_mid_smoke", "de_vertigo", "T", "smoke", "t mid", "mid", 0, "mid pace"),
    NadeLine("vertigo_elevator_flash", "de_vertigo", "T", "flash", "scaffold", "elevator", 800, "B hit"),
    NadeLine("dust2_long_smoke", "de_dust2", "T", "smoke", "t long", "long doors", 0, "long unlock"),
    NadeLine("dust2_xbox_flash", "de_dust2", "T", "flash", "t mid", "xbox", 400, "mid"),
    NadeLine("dust2_b_door_molly", "de_dust2", "T", "molotov", "tunnels", "b doors", 0, "B hit"),
)


def line(key: str) -> NadeLine:
    for item in LINES:
        if item.key == key:
            return item
    raise KeyError(key)


def lines_for_map(map_name: str) -> list[NadeLine]:
    from roundwire.maps.pool import normalize_map_name

    key = normalize_map_name(map_name)
    return [item for item in LINES if item.map_name == key]


def lines_for_side(map_name: str, side: str) -> list[NadeLine]:
    side_key = side.upper()
    return [item for item in lines_for_map(map_name) if item.side == side_key]


def util_kinds_on_map(map_name: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in lines_for_map(map_name):
        counts[item.util] = counts.get(item.util, 0) + 1
    return counts


def describe_line(key: str) -> str:
    item = line(key)
    return (
        f"{item.side} {item.util} on {item.map_name}: {item.from_area} -> {item.to_area} "
        f"@{item.delay_ms}ms ({item.purpose})"
    )


def catalog_size() -> int:
    return len(LINES)
