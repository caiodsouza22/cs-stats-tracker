# CS2 first (legacy CS:GO)

roundwire targets **CS2**. CS:GO support exists so you can import old JSON
dumps and upgrade them.

| Aspect | CS2 (default) | CS:GO (legacy) |
|--------|---------------|----------------|
| Edition | `GameEdition.CS2` | `GameEdition.CSGO` |
| Regulation | MR12 (first to 13) | MR15 (first to 16) |
| Weapon names | Canonical CS2 catalog | Legacy `weapon_*` strings |
| Samples | `cs2_01` … `cs2_03` | `csgo_01`, `csgo_02` |

`migrate_match_to_cs2(match)` sets edition to CS2 and rewrites weapon names
through the alias table. Prefer starting from CS2 samples when building new
pipelines.
