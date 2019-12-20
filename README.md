# roundwire

CS2 match analytics in pure Python. Load a JSON dump, then pull scoreboard,
MR12 economy, utility, combat sheets, and an HLTV-inspired Rating 3.0.

Bundled samples cover Mirage / Anubis / Ancient. CS:GO dumps still import for
migration; new work assumes `GameEdition.CS2`. Not a `.dem` parser — stdlib
JSON only.

## Install

```bash
pip install -e ".[dev]"
```

## Quick start

```python
from roundwire import rating_3_0_table, scoreboard_table
from roundwire.catalog import sample_match

match = sample_match("cs2_01")
print(scoreboard_table(match))
for row in rating_3_0_table(match)[:3]:
    print(row.name, round(row.rating, 3), round(row.round_swing, 3))
```

```bash
roundwire scoreboard examples/match_cs2_01.json
roundwire rating examples/match_cs2_03.json
roundwire players examples/match_cs2_01.json
roundwire players examples/match_cs2_01.json --name "lux"
roundwire leaderboard examples/match_cs2_01.json --metric adr
roundwire migrate examples/match_csgo_01.json --summary
```

## Player stats

`roundwire.players` builds per-player profiles (combat, economy, utility, weapons),
role inference, form/streaks, matchups, and JSON export packs. See `docs/player_stats.md`.

## Layout

- `src/roundwire` — models, rules, economy, combat, players, Rating 3.0, CLI
- `tests` — pytest against the sample matches
- `docs` — CS2 vs CS:GO notes, rating formula, player stats
- `examples` — CS2 dumps + demo scripts

No third-party runtime dependencies. Typed (`py.typed`).
