# Player statistics

roundwire builds rich **per-player** views on top of match JSON dumps.

## Profiles

`roundwire.players.profile.build_player_profile(match, player_id)` returns combat,
economy, utility, weapons, Rating 3.0, impact, and derived tags (`entry`, `awper`,
`support`, `clutcher`, ...).

```python
from roundwire.catalog import sample_match
from roundwire.players import build_player_profile, leaderboard, mvp

match = sample_match("cs2_01")
pid = match.players[0].player_id
profile = build_player_profile(match, pid)
print(profile.name, profile.rating_3_0, profile.tags)
print(mvp(match))
for row in leaderboard(match, "adr", limit=5):
    print(row.rank, row.name, row.value)
```

CLI:

```text
roundwire players path/to/match.json
roundwire players path/to/match.json --name "lux"
roundwire leaderboard path/to/match.json --metric rating
```

## Roles

`infer_role` scores entry / AWPer / support / lurker / anchor / star / flex from
openings, AWP share, utility, late kills, and rating. Primary + optional secondary.

## Form, streaks, splits

Rolling windows label hot/cold stretches. Streak helpers cover kill participation,
deathless runs, win/loss, and multi-kill rounds. `half_splits` / `side_splits`
break performance by half and starting side.

## Matchups and opening quality

`matchup_sheet` builds head-to-head rows versus the enemy roster. Opening quality
tracks conversion, trade rate, and opener weapon mix.

## Money and weapon economy

`money_story` labels save / force / full / rebuy beats. `weapon_economy` estimates
catalog spend efficiency and kill rewards.

## Season / multi-match

`SeasonRoster` and `rating.history.PlayerHistory` track rating slopes, role
stability, and map specialists across dumps.

## Coaching dashboard

`analysis.dashboard.coaching_dashboard(match)` aggregates roles, leaderboards,
entry/support tables, economy swings, and export payloads for UI work.

## Export

`match_player_export(match)` and `player_pack(match, player_id)` produce JSON-ready
dicts. `reports.pack.text_report_pack` writes a printable multi-section report.

## Related modules

- `players.callouts` — utility tag affinity
- `players.clutch_book` — survivor clutch proxies
- `players.timeline` — per-player event feed
- `analysis.pace` — round duration bands
- `analysis.assist_graph` — assist / flash networks
- `maps.callout_books` / `maps.nade_lines` — map reference data
- `series_analytics` — best-of series books

See also `docs/rating.md` for Rating 3.0 notes.
