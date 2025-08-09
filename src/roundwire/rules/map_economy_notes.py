"""Map-specific economy / buy rhythm notes (qualitative helpers)."""

from __future__ import annotations

from roundwire.maps.pool import normalize_map_name

NOTES: dict[str, dict[str, str]] = {
    "de_mirage": {
        "ct_bias": "mid control rewards early rifles",
        "t_bias": "apps/palace executes need multi-smoke outlay",
        "eco_tip": "T force MAC10 mid can punish CT overpeeks",
    },
    "de_inferno": {
        "ct_bias": "banana control consumes utility budget",
        "t_bias": "banana takes often require mollies + flashes",
        "eco_tip": "CT eco with dualies on apartments can steal rounds",
    },
    "de_nuke": {
        "ct_bias": "ramp and outside rotate tax utility",
        "t_bias": "outside control buys time for silo/ramp splits",
        "eco_tip": "T ramp force with armor is common",
    },
    "de_overpass": {
        "ct_bias": "monster/short setups spend smokes early",
        "t_bias": "B executes are smoke-heavy",
        "eco_tip": "CT A site pistol stacks remain viable",
    },
    "de_vertigo": {
        "ct_bias": "A ramp fights define first mid-round buys",
        "t_bias": "mid control enables A/B flex",
        "eco_tip": "AWP pickups swing force rounds hard",
    },
    "de_ancient": {
        "ct_bias": "donut/mid utility lines are expensive",
        "t_bias": "red/door executes consume HE+flash",
        "eco_tip": "cave/elbow peeks punish underfunded CTs",
    },
    "de_anubis": {
        "ct_bias": "mid-to-B control wants early rifles",
        "t_bias": "canal control sets pace",
        "eco_tip": "T mid force can snowball into B hits",
    },
    "de_dust2": {
        "ct_bias": "long control historically CT-leaning",
        "t_bias": "long unlocks A site splits",
        "eco_tip": "scout mid remains classic eco pick",
    },
}


def notes_for_map(map_name: str) -> dict[str, str]:
    key = normalize_map_name(map_name)
    return dict(NOTES.get(key, {
        "ct_bias": "unknown",
        "t_bias": "unknown",
        "eco_tip": "unknown",
    }))


def all_noted_maps() -> list[str]:
    return sorted(NOTES)
