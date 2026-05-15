# Pre-AmtsScore Deriver

Derives a per-city Pre-AmtsScore from the AmtsGuide Facts API. **NOT** the
full AmtsScore (12 digital-performance dimensions). A precursor measuring
bürger-outcome (speed + online availability) that we can publish before
the full per-website scan is built.

## Why not cost?

Cost was previously a 40% component and was dropped. Most German service
fees are federally regulated (FZV for KFZ, GNotKG for Notar) — variance
is noise, not a quality signal. Cost remains as raw context on tables
but is never weighted into a score.

## Usage

```bash
python tools/prescore/derive.py        # fetches API → src/data/prescore.json
python tools/prescore/gen_pages.py     # regenerates src/staedte/*.md + src/bundeslaender/*.md
```

`derive.py` covers three topics: Halteverbot, KFZ-Zulassung,
GmbH-Gründung. Halteverbot data is filtered to `type=city` (Berlin
Bezirke are excluded from the ranking; they're kept separately in
`halteverbot_bezirke` for the Halteverbot topic page).

## Output shape

`src/data/prescore.json`:

```json
{
  "generated_at": "2026-05-16T...",
  "source": "AmtsGuide Facts API",
  "topics": [
    {
      "slug": "halteverbot",
      "label": "Halteverbot",
      "n_cities": 11,
      "cities": [
        {
          "city": "Essen",
          "city_slug": "essen",
          "bundesland": "Nordrhein-Westfalen",
          "score": 9.5,
          "speed": 9.0,
          "cost": null,           // raw, not scored
          "online": null,
          "raw": {"speed_days": 14, "cost_eur": 25, "online_available": null},
          "meta": {"authority": null, "source_url": null, "verified_at": "2026-01-15", "status": "verified"},
          "rank": 1
        }
      ]
    }
  ],
  "city_summary": [{"city": "Leipzig", ...}],
  "state_summary": [{"bundesland": "Sachsen", ...}],
  "halteverbot_bezirke": [...],
  "data_gaps": [{"slug": "halteverbot", "null_cost": 6, ...}],
  "method": "..."
}
```

## Adding a new topic

1. Add a `gather_<topic>()` function returning a list of `{city_slug,
   city, _speed_raw, _cost_raw, _online_raw, meta}` dicts.
2. Add the topic to the `topics` list in `main()`.
3. If the topic introduces new authority types, extend `BUNDESLAND` mapping
   if needed.

## Limitations

- Heuristic `parse_days()` handles German wartezeit strings ("ca. 14 Tage",
  "mehrere Wochen", "sofort"). Returns null for unparseable strings.
- The composite weighting (speed 40%, speed 40%, online 20%) is held over
  from the v0 cost-weighted version. With cost removed, the weights
  collapse — effectively speed is dominant. A future v0.2 should
  rebalance.
- Pre-AmtsScore measures **bürger outcome** (delay, online availability),
  not **website quality**. The full AmtsScore (D1-D12) is the actual
  scan target; see `tools/scan/`.
