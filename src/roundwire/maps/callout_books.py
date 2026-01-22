"""Expanded callout books used by guides and tagging."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CalloutBook:
    map_name: str
    sites: tuple[str, str]
    callouts: tuple[str, ...]
    ct_defaults: tuple[str, ...]
    t_defaults: tuple[str, ...]
    execute_notes: tuple[str, ...]


BOOKS: dict[str, CalloutBook] = {
    "de_mirage": CalloutBook(
        "de_mirage",
        ("A", "B"),
        (
            "A", "B", "mid", "apps", "palace", "connector", "jungle", "window",
            "top mid", "underpass", "ladder", "cat", "short", "stairs", "tetris",
            "firebox", "sandwich", "ninja", "ticket", "market", "bench",
        ),
        ("window/connector hold", "jungle stack", "apps anchor"),
        ("mid control", "apps/palace split", "B apps rush"),
        ("stairs+jungle smokes", "window one-way", "ramp flash pop"),
    ),
    "de_inferno": CalloutBook(
        "de_inferno",
        ("A", "B"),
        (
            "A", "B", "banana", "apps", "quad", "pit", "coffins", "arch",
            "library", "balcony", "boiler", "construction", "dark", "new box",
            "second mid", "top mid", "bottom mid", "graveyard", "tree",
        ),
        ("banana control", "arch/library", "pit hold"),
        ("banana take", "apps/arch split", "fast mid-to-B"),
        ("banana mollies", "coffins smoke", "arch flash"),
    ),
    "de_nuke": CalloutBook(
        "de_nuke",
        ("A", "B"),
        (
            "A", "B", "ramp", "outside", "hut", "silo", "secret", "yard",
            "main", "heaven", "hell", "trophy", "lockers", "vent", "t red",
            "mini", "radio", "squeaky", "lobby", "big garage",
        ),
        ("outside/ramp", "hut/heaven", "secret watch"),
        ("yard pressure", "ramp hit", "silo drop"),
        ("outside smokes", "ramp mollies", "vent timing"),
    ),
    "de_overpass": CalloutBook(
        "de_overpass",
        ("A", "B"),
        (
            "A", "B", "monster", "short", "bathrooms", "park", "canal", "fountain",
            "rest", "connector", "long", "party", "pit", "truck", "toxic",
            "pipes", "water", "abc", "bank",
        ),
        ("monster/short", "bathrooms", "A long"),
        ("B monster", "A short/long", "mid control"),
        ("monster smoke", "short mollies", "toilets flash"),
    ),
    "de_ancient": CalloutBook(
        "de_ancient",
        ("A", "B"),
        (
            "A", "B", "mid", "donut", "cave", "temple", "elbow", "red",
            "door", "lane", "square", "ruins", "snakes", "trip", "window",
            "ramp", "niche", "big box",
        ),
        ("donut/mid", "cave support", "B door"),
        ("red/door", "cave hit", "mid-to-B"),
        ("donut smoke", "temple line", "cave flash"),
    ),
    "de_anubis": CalloutBook(
        "de_anubis",
        ("A", "B"),
        (
            "A", "B", "mid", "canal", "palace", "e-box", "connector", "street",
            "bridge", "water", "pillar", "camera", "heaven", "broken wall",
            "fountain", "main", "elbow",
        ),
        ("mid-to-B", "palace", "canal"),
        ("canal control", "palace/A", "water B"),
        ("bridge smoke", "palace mollies", "water flash"),
    ),
    "de_vertigo": CalloutBook(
        "de_vertigo",
        ("A", "B"),
        (
            "A", "B", "ramp", "mid", "scaffold", "elevator", "sandbags", "headshot",
            "stairs", "rafters", "generator", "t spawn", "ct spawn", "bent",
            "boost", "ladder",
        ),
        ("A ramp", "mid hold", "B scaffold"),
        ("mid-to-A", "B elevator", "ramp hit"),
        ("ramp mollies", "mid smokes", "elevator flash"),
    ),
    "de_dust2": CalloutBook(
        "de_dust2",
        ("A", "B"),
        (
            "A", "B", "long", "cat", "mid", "xbox", "suicide", "pit",
            "goose", "car", "door", "window", "t plat", "ct mid", "b doors",
            "hole", "tun", "upper tunnels",
        ),
        ("long+cat", "B doors", "mid xbox"),
        ("long unlock", "B tunnels", "cat split"),
        ("long smokes", "xbox flash", "B door mollies"),
    ),
}


def book_for(map_name: str) -> CalloutBook | None:
    from roundwire.maps.pool import normalize_map_name

    return BOOKS.get(normalize_map_name(map_name))


def all_callouts(map_name: str) -> tuple[str, ...]:
    book = book_for(map_name)
    return book.callouts if book else tuple()


def execute_notes(map_name: str) -> tuple[str, ...]:
    book = book_for(map_name)
    return book.execute_notes if book else tuple()


def default_setups(map_name: str, side: str) -> tuple[str, ...]:
    book = book_for(map_name)
    if book is None:
        return tuple()
    return book.ct_defaults if side.upper() == "CT" else book.t_defaults


def indexed_callouts() -> dict[str, list[str]]:
    return {name: list(book.callouts) for name, book in BOOKS.items()}
