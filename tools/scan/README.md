# Deep Per-Topic Scan

Multi-tier per-topic measurement. Currently KFZ-Zulassung only; same pattern
will replicate for Halteverbot, GmbH-Gründung, and the wider TOTAL run.

This is the **real** AmtsScore measurement (vs `tools/prescore/` which is
the bürger-outcome warmup). 9 dimensions per city, equal-weighted
composite. **Cost is intentionally not a dimension.**

## Usage

```bash
doppler run -p andx_main -c prd -- python tools/scan/kfz.py
```

Wall-clock ~5-8 minutes for 20 cities (rate-limited by per-page fetches +
Mozilla Observatory polling).

## Tiers

Each tier requires different infrastructure:

| Tier | Cost | Source | What it measures |
|---|---|---|---|
| 1 | free | AmtsGuide Facts API | Field enrichment from existing data |
| 2 | rate-limited | Per-page fetch + Mozilla Observatory | Site-level signals |
| 3 | API key | Brave Search | External pain signals |

## Dimensions (KFZ-Zulassung)

| # | Tier | Key | Source | Logic |
|---|---|---|---|---|
| 1 | 1 | speed | `wartezeit` parsed to days | fewer days → higher |
| 2 | 1 | online | `ikfz` boolean | 10 if available |
| 3 | 1 | access | `standorte` count | more → higher |
| 4 | 1 | friction | `terminpflicht` | walk-in = 10, appointment = 5 |
| 5 | 2 | auth | scan `links.termin` page | eID / BundID / BerlinID / Servicekonto / AusweisApp |
| 6 | 2 | schema | scan `links.termin` page | JSON-LD GovernmentService / Service / CivicStructure |
| 7 | 2 | llmstxt | HEAD `/llms.txt` at stadt-domain | HTTP 200 = 10 |
| 8 | 2 | https | Mozilla Observatory grade | A+→10, F→0 |
| 9 | 3 | press | Brave Search "kritik wartezeit" count | fewer results → higher (inverse) |

## Output

`src/data/kfz_enriched.json`:

```json
{
  "generated_at": "...",
  "topic": "kfz-zulassung",
  "n_cities": 20,
  "dimensions": [{"key": "speed", "label": "Wartezeit", "tier": 1, "invert": true}, ...],
  "cities": [
    {
      "slug": "bonn",
      "city": "Bonn",
      "authority": "...",
      "source_url": "https://...",
      "stadt_domain": "bonn.de",
      "raw": {...},
      "dimensions": {"speed": 9.7, "online": 10.0, ..., "https": null},
      "composite": 5.3,
      "rank": 1
    }
  ]
}
```

## Env

| Var | Required? | Used for |
|---|---|---|
| `BRAVE_API_KEY` | recommended | Tier 3 press-pain. Without it: `press` dim is null for all cities. |
| `GOOGLE_PAGESPEED_API_KEY` | future | Lighthouse mobile (D4). Not yet wired in. |

## Known issues / caveats

- **Mozilla Observatory transient 502.** Their public API returns Bad
  Gateway on bursts. When this happens, `https` dim is null for all
  cities and drops from the composite. Re-run to recover.
- **Stadt-domain mapping is hand-curated** in `STADT_DOMAIN` dict. Most
  major cities use `<slug>.de`, but exceptions (Köln = `stadt-koeln.de`,
  Münster = `stadt-muenster.de`, Frankfurt = `frankfurt.de`).
- **eID detection is keyword-based.** Pattern-match on the linked
  Termin-URL page. False negatives possible if the page lazy-loads
  the auth widget via JS. Mitigation: extend `check_eid_buttons()`
  patterns over time.
- **Schema.org check parses JSON-LD only.** Microdata or RDFa would be
  missed.
- **Brave press-pain has low discrimination** at default settings. Most
  cities return similar result counts. Needs better query design or
  time-filtered news API.
- **terminpflicht is 19/20.** The "friction" dimension is mostly noise
  on KFZ — almost all cities require appointments. Useful for other
  topics where walk-in is common.

## Adding a new topic

Each topic has a bespoke shape in the AmtsGuide Facts API (Halteverbot
uses `locations` dict, KFZ uses `results` list). Per-topic scan modules
needed. Copy `kfz.py`, adapt:

1. The data fetch + per-city iteration
2. The Tier 1 extracted fields (different topics expose different keys)
3. The dimension definitions in `out["dimensions"]`
4. The composite weighting if you deviate from equal-weight

## Reproducibility

The tool is fully reproducible — anyone with the API keys can re-run
and verify. No private state, no internal data dependencies. This is
core to AmtsScore's brand independence: the methodology is the data.
