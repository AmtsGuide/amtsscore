# Leuchtturm Checker

Runs the 8 Leuchtturm criteria against a single service URL and writes the
result to `src/data/specials/<slug>.json`. The Observable page at
`/specials/<slug>` renders the JSON.

## Usage

```bash
pip install -r tools/leuchtturm/requirements.txt
python tools/leuchtturm/check.py --slug berlin-gaststaettenanmeldung-2026
# or all at once
python tools/leuchtturm/check.py --all
```

Add a new service by appending an entry to `services.yaml`, then run the
checker with its slug.

## Criteria

| # | Criterion | Automated? |
|---|---|---|
| 1 | End-to-end digital | heuristic |
| 2 | Authentifizierung (eID / BundID / Servicekonto) | yes |
| 3 | Schema.org GovernmentService / Service markup | yes |
| 4 | Lighthouse mobile performance ≥ 70 | PSI API |
| 5 | SERP top-3 for canonical query | Brave Search API |
| 6 | Stable permalinks (no jsessionid, no `#/`) | yes |
| 7 | Pressereife / offizielle Kommunikation | manual flag in YAML |
| 8 | Reproduzierbar für andere Städte | manual flag in YAML |

Threshold for Leuchtturm-Aufnahme: **≥ 6 of 8 pass**.

## Environment

| Var | Purpose | Required? |
|---|---|---|
| `GOOGLE_PAGESPEED_API_KEY` | higher PSI quota | optional |
| `BRAVE_API_KEY` | criterion 5 (SERP) | optional but recommended |

Run with Doppler if you have the keys provisioned:

```bash
doppler run -p andx_main -c prd -- python tools/leuchtturm/check.py --slug ...
```

## Heuristic notes

Criterion 1 is a keyword heuristic (looks for "online beantragen",
"formularserver", etc.). A `passes: true` from this check is necessary but
not sufficient. Spot-check manually before claiming Leuchtturm status.
