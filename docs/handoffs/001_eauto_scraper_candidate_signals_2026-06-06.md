# E-Auto Scraper Candidate Signals Handoff

Date: 2026-06-06
Target repo: `/Users/andx/amtsscore_github`
Source system: AmtsGuide scraper output
Source path: `/Users/andx/codex_scraper/output/intake-clusters/eauto/`

## Purpose

This handoff tells the AmtsScore repo how to intake the new E-Auto cluster data.
The data is suitable for an internal or preview E-Auto scoring surface, candidate
signal review, and future import tooling. It is not, by itself, permission to
publish an official public AmtsScore rating.

## Controlling Files

Use these files as the intake authority:

- `/Users/andx/codex_scraper/output/intake-clusters/eauto/amtsscore.json`
- `/Users/andx/codex_scraper/output/intake-clusters/eauto/amtsscore.md`
- `/Users/andx/codex_scraper/output/intake-clusters/eauto/summary.json`
- `/Users/andx/codex_scraper/output/intake-clusters/eauto/summary.md`
- `/Users/andx/codex_scraper/output/intake-clusters/eauto/final_audit.json`
- `/Users/andx/codex_scraper/output/intake-clusters/eauto/web_consumer_contract.json`
- `/Users/andx/codex_scraper/output/intake-clusters/eauto/consumer_validation/web.json`
- `/Users/andx/codex_scraper/output/intake-clusters/eauto/provider_coverage.json`

The most important file for AmtsScore is `amtsscore.json`. It contains candidate
signals projected from writer-bundle artifacts.

## What The Data Is

The scraper produced an accepted E-Auto intake cluster with AmtsScore candidate
signals.

Observed summary:

- Cluster: `eauto`
- Status: `accepted`
- AmtsScore signal generation date: 2026-06-04
- Cluster summary date: 2026-06-05
- Topics: 19
- Candidate-ready topics: 19
- Partial topics: 0
- Candidate signals: 133
- Blocked signals: 0
- Provider rows used as evidence: `false`
- Network used by this intake run: `false`
- Paid services used by this intake run: `false`

The signal contract is `scraper_amtsscore_candidate_signals`, version `1.0`.
The mode is `intake_cluster_writer_bundle_projection`.

## What The Data Is Not

The candidate signals do not prove:

- public publication on `amtsscore.de`
- current website route behavior
- official fact completeness
- full scrape coverage for every adjacent topic
- a finished public scoring methodology
- a final public score

Provider rows are explicitly separated from official evidence. They may be useful
as sales or provider diagnostics, but they must not become legal, official,
subsidy, tax, registration, fee, payout, or authority evidence.

## Topic Matrix

All 19 topics have `candidate_signals_ready` with 7 candidate signals each.

Core publishable AmtsGuide topics:

- `e-auto-foerderung`
- `wallbox-foerderung`
- `kfz-zulassung`
- `thg-quote`
- `kfz-steuer`
- `e-auto-laden`
- `wallbox-installation`
- `ladestation`
- `ladesaeule`
- `ladeinfrastruktur`
- `e-kennzeichen`
- `umweltbonus`

Bridge-only topics:

- `pv-wallbox`
- `solarstrom-auto-laden`
- `solaranlage`
- `energieberater`
- `solarteur`

Closed or historical-fallback topics:

- `gebrauchtwagen-eauto-foerderung`
- `e-auto-versicherung`

## Candidate Signal Shape

Each topic currently has these signal categories:

- `intake_cluster_context`
- `writer_intake_quality`
- `source_quality`
- `fact_quality`
- `coverage`
- `calculator_quality`
- `provider_boundary`

Example fields available per topic:

- writer bundle status
- source manifest coverage
- official source count
- total source count
- fact count
- official fact count
- source-backed fact count
- unknown count
- jurisdiction and local scope
- tool/calculator surface diagnostic
- provider evidence separation

## Recommended AmtsScore Intake

Build a repo-local importer or manual data preparation step that converts
`amtsscore.json` into a static data file under `static/data/`, for example:

- `static/data/eauto_prescore.json`

The first public-safe surface should be framed as a candidate or preview signal
view, not as a final official AmtsScore rating.

Possible implementation path:

1. Add a parser that reads `amtsscore.json`.
2. Normalize topic slugs, signal categories, and source artifact references.
3. Store a derived static JSON file in `static/data/`.
4. Add an E-Auto topic route only if the page copy makes the status clear.
5. Keep public labels like "candidate signals", "preview", or "methodology
   review" until the scoring formula is finalized.
6. Do not use provider rows in the public score.
7. Link back to AmtsGuide E-Auto pages only as topic context, not as proof of an
   AmtsScore rating.

## Public Copy Guardrails

Allowed language:

- candidate signals
- preview analysis
- source coverage
- fact coverage
- unknown-state count
- provider evidence excluded
- methodology review

Avoid language that implies finality:

- official score
- final AmtsScore rating
- complete public evaluation
- fully verified score
- complete government benchmark

Avoid using provider data as official evidence.

## Current Repo Fit

The current AmtsScore repo is a SvelteKit static app. It has:

- a homepage
- a Halteverbot topic page
- static JSON data under `static/data/`
- no current E-Auto route
- no visible repo-local deploy script

The live `amtsscore.de` site currently appears to serve an older Observable build,
while this repo builds a SvelteKit `dist`. Confirm the deployment path before
publishing an E-Auto AmtsScore surface.

## Minimum Acceptance Criteria For First Intake

Before merging an E-Auto AmtsScore intake:

- `pnpm build` passes
- the derived E-Auto JSON validates against a small local schema
- the page does not call candidate signals a final score
- provider rows are not used as official evidence
- bridge-only and closed topic states remain visible in internal data
- public routes do not expose empty or speculative pages
- deployment target is confirmed

## Open Decisions

- Exact E-Auto public route, for example `/e-auto/` or `/topics/e-auto/`
- Whether first publication is internal, preview, or public methodology comment
- How candidate signals map to a 0-10 score, if at all
- Whether E-Auto should be scored as one cluster or multiple topic surfaces
- Whether bridge-only topics contribute context only or score penalties
- How unknown-state counts should affect score confidence

