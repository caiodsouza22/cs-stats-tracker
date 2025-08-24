# Rating 3.0 (HLTV-inspired)

HLTV Rating 3.0 (2025) combines six sub-ratings:

1. **Kills** (eco-adjusted)
2. **Damage** (eco-adjusted)
3. **Survival**
4. **KAST**
5. **Multi-kills**
6. **Round Swing** (new in 3.0 — replaces classic Impact)

After the October 2025 hotfix, public commentary puts approximate weights near:

| Sub-rating   | Weight |
|--------------|--------|
| Round Swing  | 0.33   |
| Kills        | 0.25   |
| Damage       | 0.14   |
| Survival     | 0.10   |
| KAST         | 0.10   |
| Multi-kills  | 0.08   |

## roundwire implementation

```python
from roundwire.rating import rating_3_0, rating_3_0_table

rows = rating_3_0_table(match)
print(rows[0].rating, rows[0].round_swing)
```

**Important:** HLTV does not publish the proprietary Round Swing win-probability
model. `roundwire.rating.round_swing` uses an open heuristic (alive counts,
equipment gap, bomb plant, damage share / flash / trade credit). Values are
**inspired by** Rating 3.0 and will **not** match hltv.org digit-for-digit.

The older `impact_score` helper remains available as a simpler internal metric.
