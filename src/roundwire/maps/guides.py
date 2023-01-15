"""Per-map callout guides for tagging utility and narratives."""
from __future__ import annotations

from dataclasses import dataclass

from roundwire.maps.pool import normalize_map_name


@dataclass(frozen=True, slots=True)
class MapGuide:
    map_name: str
    sites: tuple[str, str]
    callouts: tuple[str, ...]
    ct_focus: str
    t_focus: str


GUIDES: dict[str, MapGuide] = {
    'de_mirage': MapGuide('de_mirage', ('A', 'B'), ('A', 'B', 'mid', 'apps', 'connector', 'jungle', 'window', 'top mid',), 'window/connector control', 'apps/mid defaults'),
    'de_inferno': MapGuide('de_inferno', ('A', 'B'), ('A', 'B', 'banana', 'apps', 'quad', 'pit', 'coffins', 'arch',), 'banana + arch', 'banana takes and apps'),
    'de_nuke': MapGuide('de_nuke', ('A', 'B'), ('A', 'B', 'ramp', 'outside', 'hut', 'silo', 'secret', 'yard',), 'outside/ramp', 'yard pressure into silo'),
    'de_overpass': MapGuide('de_overpass', ('A', 'B'), ('A', 'B', 'monster', 'short', 'bathrooms', 'park', 'canal', 'fountain',), 'monster/short', 'B monster executes'),
    'de_vertigo': MapGuide('de_vertigo', ('A', 'B'), ('A', 'B', 'ramp', 'mid', 'scaffold', 'elevator', 'sandbags', 'headshot',), 'A ramp', 'mid-to-A pace'),
    'de_ancient': MapGuide('de_ancient', ('A', 'B'), ('A', 'B', 'mid', 'donut', 'cave', 'temple', 'elbow', 'red',), 'donut/mid', 'red/door splits'),
    'de_anubis': MapGuide('de_anubis', ('A', 'B'), ('A', 'B', 'mid', 'canal', 'palace', 'e-box', 'connector', 'street',), 'mid-to-B', 'canal control'),
    'de_dust2': MapGuide('de_dust2', ('A', 'B'), ('A', 'B', 'long', 'cat', 'mid', 'xbox', 'suicide', 'pit',), 'long + cat', 'long unlocks'),
    'de_train': MapGuide('de_train', ('A', 'B'), ('A', 'B', 'ivy', 'popdog', 'alley', 'bombtrain', 'ladder', 'side',), 'ivy/pop', 'alley splits'),
    'de_cache': MapGuide('de_cache', ('A', 'B'), ('A', 'B', 'mid', 'checker', 'highway', 'sunroom', 'quad', 'boost',), 'mid/checker', 'B highway'),
}


def guide_for(map_name: str) -> MapGuide | None:
    return GUIDES.get(normalize_map_name(map_name))


def callouts_for(map_name: str) -> tuple[str, ...]:
    guide = guide_for(map_name)
    return guide.callouts if guide else tuple()


def format_guide(map_name: str) -> str:
    g = guide_for(map_name)
    if g is None:
        return f'no guide for {map_name}'
    calls = ', '.join(g.callouts)
    return (
        f'{g.map_name}: sites={g.sites[0]}/{g.sites[1]}; '
        f'CT focus={g.ct_focus}; T focus={g.t_focus}; callouts={calls}'
    )


def all_guide_summaries() -> dict[str, str]:
    return {name: format_guide(name) for name in GUIDES}

def focus(map_name: str) -> tuple[str, str] | None:
    guide = guide_for(map_name)
    if guide is None:
        return None
    return guide.ct_focus, guide.t_focus


def sites(map_name: str) -> tuple[str, str] | None:
    guide = guide_for(map_name)
    return None if guide is None else guide.sites


def narrative(map_name: str) -> str:
    guide = guide_for(map_name)
    if guide is None:
        return f'no guide for {map_name}'
    return (
        f'{guide.map_name} rewards teams that prioritize {guide.ct_focus} '
        f'on CT and {guide.t_focus} on T. Key callouts: ' + ', '.join(guide.callouts) + '.'
    )

