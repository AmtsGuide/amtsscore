# E-Auto Candidate Signals MVP

Date: 2026-06-06
Status: implemented
Implementation target: Observable Framework

## Objective

Build the first E-Auto candidate signal surface for the current Observable
AmtsScore site. The MVP should make scraper-produced candidate evidence useful
without claiming a final public AmtsScore rating.

## Current Repo Reality

- The live `amtsscore.de` site serves an Observable Framework build.
- The Observable source currently exists in `_src_of_backup/`, which is ignored
  and untracked.
- The tracked `src/` tree is SvelteKit, but that is not the current live source
  of truth.
- Before adding E-Auto content, the repo needs an explicit source-of-truth
  restoration so Observable source is tracked again.

## Deployed Baseline

The current online Observable build is the "previous state" that future
AmtsScore updates must preserve for comparison.

- Build date: 2026-05-20
- Live `prescore.json`: generated 2026-05-15 from AmtsGuide Facts API
- Live topics:
  - `halteverbot`: 11 scored cities
  - `kfz-zulassung`: 20 scored cities
  - `gmbh-gruendung`: 30 scored cities
- Live `halteverbot.json`: scraped 2026-03-29, 570 authority records, 38
  cities
- Live `kfz_enriched.json`: generated 2026-05-15, 20 cities, 9 dimensions

The E-Auto candidate package is a new data family, not a replacement for the
current city/topic prescore data.

## Source Inputs

- `/Users/andx/codex_scraper/output/intake-clusters/eauto/final_audit.json`
- `/Users/andx/codex_scraper/output/intake-clusters/eauto/pipeline_check.json`
- `/Users/andx/codex_scraper/output/intake-clusters/eauto/topic_surface_full_completion.json`
- `/Users/andx/codex_scraper/output/intake-clusters/eauto/web_consumer_contract.json`
- `/Users/andx/codex_scraper/output/intake-clusters/eauto/amtsscore.json`
- `/Users/andx/codex_scraper/output/{topic}/amtsscore/signals.json`

## New E-Auto Baseline

- AmtsScore candidate signal generation date: 2026-06-04
- Topic surface completion date: 2026-06-05
- Candidate-ready topics: 19
- Candidate signals: 133
- Blocked signals: 0
- Topic-surface topics: 20
- Web-buildable embedded surfaces: 12
- Calculator routes ready: 0
- Provider rows used as evidence: false

This should be recorded as the first E-Auto candidate-signal snapshot.

## Implementation Plan

1. Restore Observable Framework as the tracked source target.
2. Move or copy the current Observable source from `_src_of_backup/` into the
   tracked site source location.
3. Update package scripts and dependencies so Observable is the build target.
4. Capture the current deployed data baseline in repo-local history before
   importing new E-Auto data.
5. Add `tools/eauto/import_amtsscore.py`.
6. Validate gate files before importing candidate signals.
7. Emit public-safe normalized data to the Observable data directory, expected
   as `src/data/eauto_prescore.json`.
8. Add the E-Auto history files under `src/data/history/eauto/`.
9. Add an Observable topic page, expected as `src/topics/e-auto.md`.
10. Add navigation and homepage links using candidate-signal wording.
11. Verify with the importer and Observable build.

## MVP Scope Boundary

The plan is intentionally history-first, but the implementation must stay MVP
sized.

MVP must include:

- restore Observable source of truth
- preserve current deployed baseline
- create the E-Auto history model
- import the first E-Auto snapshot
- write current pointer, snapshot, manifest, and baseline diff
- render current E-Auto candidate signal state
- render history/diff scaffolding for the first snapshot
- build and verify

MVP does not need:

- automated monthly scheduler
- full CI pipeline
- multi-snapshot charts with invented history
- deployment automation changes
- advanced filtering or search
- final scoring formula
- public calculator route enablement
- provider-data visualization

Later-work items can be documented, but they should not block the first
history-backed candidate signal page.

## Observable Restoration Strategy

Observable must be restored before E-Auto data changes.

- Treat `_src_of_backup/` as the current live-source candidate because it
  matches the deployed Observable site.
- Replace the tracked SvelteKit `src/` tree with Observable Framework source.
- Keep SvelteKit files only if explicitly archived outside the Observable build
  path. Do not let SvelteKit and Observable both claim `src/`.
- Update `package.json` scripts to Observable commands.
- Add or restore the Observable config/sidebar file if missing.
- Keep `.gitignore` ignoring `_src_of_backup/`; the tracked Observable source
  should live in `src/`, not in the backup directory.
- Verify restored Observable source builds before adding E-Auto.

## Commit Sequence

This should be two logical commits:

1. Restore Observable source of truth.
2. Add E-Auto history model, importer, data, and page.

Each commit should stage only specific files and push immediately after commit.

## History Model Requirement

History is not a follow-up feature. No new E-Auto data should be published or
merged until the history model exists. AmtsScore needs to know both what used
to be and what is current before it changes any data.

The history model should be explicit, versioned, and used in both the importer
and Observable page code. The importer should therefore create append-only
snapshots plus a current pointer:

- `src/data/history/eauto/2026-06-04.json`: first normalized E-Auto snapshot
  keyed by scraper `generated_at`.
- `src/data/eauto_prescore.json`: current public-safe pointer used by the
  Observable page.
- `src/data/history/eauto/index.json`: compact manifest with snapshot date,
  source artifact paths, contract versions, topic count, signal count, blocker
  count, and content hash.
- `src/data/history/eauto/diff-2026-06-04.json`: first diff record. For the
  first snapshot this records `previous_snapshot: null` and establishes the
  baseline.

The model constants should be hard-coded in the implementation, not inferred
from whatever data happens to arrive:

- `history_model_version`
- accepted contract major versions
- snapshot family: `eauto_candidate_signals`
- immutable snapshot fields
- current-pointer fields
- diff event types
- topic groups
- visual rollup fields

## Data Schemas

The importer should write concrete, stable JSON shapes.

### Current Pointer

`src/data/eauto_prescore.json`:

```json
{
  "history_model_version": "1.0",
  "snapshot_family": "eauto_candidate_signals",
  "current_snapshot": "2026-06-04",
  "current_snapshot_path": "history/eauto/2026-06-04.json",
  "latest_diff_path": "history/eauto/diff-2026-06-04.json",
  "summary": {},
  "gates": {},
  "topics": [],
  "visual_rollups": {}
}
```

## Validation Requirements

Add data contract validation before page implementation. The importer should
validate every generated JSON object before writing:

- current pointer shape
- dated snapshot shape
- manifest shape
- diff shape
- required topic fields
- required gate fields
- allowed topic groups
- allowed diff event types
- allowed review statuses

Validation can be implemented as Python assertions or lightweight schema
functions. It should fail fast with readable errors.

## Snapshot Date Rule

The E-Auto snapshot ID should come from the AmtsScore candidate signal
generation date in `amtsscore.json` because that is the data family being
published.

- Snapshot ID: `amtsscore.generated_at`, for example `2026-06-04`.
- Store all other source dates separately in `source_generation_dates`.
- Store the local import timestamp separately as `imported_at`.
- Do not use local import date as the snapshot ID unless source generation date
  is missing. If it is missing, fail unless an explicit override is provided.

## Hash Scope

`content_hash` should be computed from canonical public-safe normalized content.

Include:

- gates
- summary
- topics
- visual rollups
- review status
- public-safe provenance identifiers

Exclude:

- local absolute source paths
- import timestamp
- file write order
- manifest metadata
- comments or planning text

This avoids meaningless diffs when only local paths or import time change.

## Source Path Portability

Scraper paths are local absolute paths. They are useful for provenance in this
workspace but weak as public or cross-machine references.

Store both:

- `source_artifact_paths`: local paths for audit in this workspace
- `source_artifact_ids`: stable identifiers such as
  `intake-clusters/eauto/amtsscore.json` or
  `{topic}/amtsscore/signals.json`

Observable public pages should prefer stable artifact IDs and only expose local
paths when clearly marked as internal provenance.

## Topic Labels

Do not display raw slugs as primary public labels. Add a hard-coded label map
for E-Auto topics.

Examples:

- `e-auto-foerderung`: E-Auto-Förderung
- `wallbox-foerderung`: Wallbox-Förderung
- `kfz-zulassung`: Kfz-Zulassung
- `thg-quote`: THG-Quote
- `kfz-steuer`: Kfz-Steuer
- `e-auto-laden`: E-Auto laden
- `e-kennzeichen`: E-Kennzeichen
- `ladeinfrastruktur`: Ladeinfrastruktur
- `ladesaeule`: Ladesäule
- `ladestation`: Ladestation
- `umweltbonus`: Umweltbonus
- `solaranlage`: Solaranlage

Unknown slugs should fall back to a title-cased slug, but the importer should
report them so the label map can be updated.

## Review Status

Every snapshot and topic should include review status.

Allowed snapshot statuses:

- `candidate`
- `editor_review_required`
- `public_preview_ok`
- `suppressed`

Allowed topic statuses:

- `candidate`
- `buildable_preview`
- `bridge_context`
- `not_ready`
- `provider_only`
- `suppressed`

The first E-Auto snapshot should default to `editor_review_required` at snapshot
level and topic-level statuses derived from the web consumer policy.

## Ownership And Approval

Review status changes need explicit ownership.

- `editor_review_required` can be set by the importer by default.
- `public_preview_ok` requires human approval before publication.
- `suppressed` can be set by an editor or maintainer through overrides.
- The approval actor and approval date should be stored in the manifest or
  override file when status changes are manual.

The importer should not promote a snapshot to `public_preview_ok` by itself.

## Manual Override Policy

The scraper can say a topic is buildable, but AmtsScore may still need to
suppress it editorially.

Add an optional tracked override file:

- `src/data/history/eauto/overrides.json`

It should support:

- suppress topic
- change public label
- change review status
- add editorial note
- force bridge-only display

Overrides must be included in the normalized content hash if they affect public
output.

## Update Cadence

Default cadence for E-Auto candidate-signal imports:

- Run manually for the MVP.
- Move to monthly imports after the first public preview is accepted.
- Allow out-of-cycle imports when the scraper reports a material source or
  policy change.

Every import should produce either a new snapshot, a no-change report, or a
failed-gate report.

## Retention Policy

Keep all public-safe snapshots indefinitely.

- Dated snapshots are append-only audit records.
- Do not delete old snapshots as part of normal maintenance.
- If data size becomes a problem, introduce archive manifests rather than
  deleting history.

## Generated File Policy

Generated files should carry a top-level marker:

```json
{
  "generated_by": "tools/eauto/import_amtsscore.py",
  "do_not_edit_by_hand": true
}
```

Generated files:

- `src/data/eauto_prescore.json`
- `src/data/history/eauto/{date}.json`
- `src/data/history/eauto/diff-{date}.json`
- `src/data/history/eauto/index.json`
- visual rollup files if split out later

Manual files:

- `src/data/history/eauto/overrides.json`
- planning files
- Observable markdown pages

## CI And Build Guards

Add a local validation command before commit. A later CI job should enforce the
same checks.

Required guard checks:

- current pointer references an existing snapshot
- manifest current snapshot matches current pointer
- latest diff file exists
- every manifest snapshot path exists
- generated files validate against importer schema functions
- banned public copy terms are absent
- Observable build passes

## Changelog And Release Notes

Every public data update should have a short markdown release note.

Suggested path:

- `docs/releases/YYYY-MM-DD-eauto-candidate-signals.md`

The note should include:

- snapshot date
- previous snapshot
- current snapshot
- material changes
- known diagnostics
- whether provider evidence remains excluded
- deployment verification result

## Accessibility Requirements

Observable charts should not be the only way to understand the data.

- Every chart should have a short text summary near it.
- Tables should include the same core values shown in charts.
- Use clear German public labels, not only slugs.
- Avoid color-only status communication.

## Data Size Ceiling

The MVP should keep snapshots compact. If generated public-safe data exceeds a
reasonable static-page size, split history into manifest plus dated snapshots
instead of loading every historical snapshot by default.

Initial soft ceiling:

- `src/data/eauto_prescore.json`: under 500 KB
- each dated snapshot: under 1 MB
- history manifest: under 100 KB

If exceeded, Observable should load only manifest and current snapshot on first
render, with older snapshots loaded only for comparison views.

## Failed Import Handoff

If gates fail, the importer must not touch public data files.

Instead write a local report:

- `planning/import_failures/YYYY-MM-DD_eauto_import_failure.md`

The report should include:

- failed gate
- source artifact
- reason
- no files written confirmation
- recommended next action

These failure reports are planning artifacts and should follow planning
directory numbering rules if they become persistent planning files.

## Post-Deploy Rollback

Rollback should have an explicit operational path:

1. Revert the deployment commit, or update `src/data/eauto_prescore.json` to the
   previous `current_snapshot`.
2. Rebuild Observable.
3. Redeploy.
4. Smoke-check `/topics/e-auto` and previous core routes.
5. Add a rollback note to the release note or a follow-up release note.

### Snapshot

`src/data/history/eauto/{date}.json`:

```json
{
  "history_model_version": "1.0",
  "snapshot_family": "eauto_candidate_signals",
  "snapshot_date": "2026-06-04",
  "source_generation_dates": {},
  "source_artifacts": [],
  "contract_versions": {},
  "content_hash": "",
  "gates": {},
  "summary": {},
  "topics": [],
  "visual_rollups": {}
}
```

### Manifest

`src/data/history/eauto/index.json`:

```json
{
  "history_model_version": "1.0",
  "snapshot_family": "eauto_candidate_signals",
  "current_snapshot": "2026-06-04",
  "snapshots": [],
  "latest_diff": "diff-2026-06-04.json"
}
```

### Diff

`src/data/history/eauto/diff-{date}.json`:

```json
{
  "history_model_version": "1.0",
  "snapshot_family": "eauto_candidate_signals",
  "snapshot_date": "2026-06-04",
  "previous_snapshot": null,
  "current_snapshot": "2026-06-04",
  "events": [],
  "summary": {}
}
```

## History Levels

The MVP needs more than one level of history.

1. Provenance history: source artifact paths, contract versions, generation
   dates, gate status, hard blockers, failed checks, provider evidence boundary.
2. Snapshot history: full public-safe normalized snapshot for each import date.
3. Topic history: per-topic readiness, group, tool type, route policy, CTA
   policy, source counts, fact counts, unknown counts, and blocker counts.
4. Signal history: per-topic signal category counts and score scope counts,
   without exposing provider rows as evidence.
5. Diff history: added topics, removed topics, changed topics, count deltas,
   policy changes, blocker changes, and provider-boundary changes.
6. Visual rollup history: compact rows optimized for Observable charts, such as
   `{date, metric, value}` and `{date, topic_slug, field, value}`.

## In-Memory Comparison Model

Observable pages should not reimplement comparison logic ad hoc. Add a small
client-side module or page-local helper that loads the manifest, current
snapshot, previous snapshot, and latest diff into memory, then exposes:

- `current`
- `previous`
- `manifest`
- `latestDiff`
- `topicRows`
- `metricRows`
- `changedTopics`
- `buildableTopics`
- `suppressedTopics`

This keeps table and chart logic consistent. The same normalized fields used
for saving history should be used for display.

## Data Saving Rules

The importer must follow append-only rules:

- Never mutate a dated snapshot.
- Only update `src/data/eauto_prescore.json` as the current pointer.
- Only update `src/data/history/eauto/index.json` by appending or replacing
  manifest metadata for the exact same content hash.
- Write a new dated snapshot only when the normalized public-safe content hash
  changes.
- Write a diff file for every new snapshot.
- Keep provider rows out of official evidence and out of snapshots.
- Store source artifact paths as provenance, not as public evidence by
  themselves.
- Fail fast before writing if gates are invalid.
- If normalized content is unchanged, do not write a new snapshot. Exit cleanly
  with a "no data changes" message.
- If rerunning for the same snapshot date and same content hash, allow manifest
  metadata repair only.
- If rerunning for the same snapshot date with a different content hash, fail
  unless an explicit force flag is provided. Dated snapshots are immutable by
  default.

## Baseline Preservation

Before importing E-Auto, preserve the currently deployed Observable data as the
site baseline:

- `src/data/history/site-baseline/2026-05-20.json`

This baseline should record:

- deployed build date
- deployed data attachment names and hashes where available
- `prescore.json` summary
- `halteverbot.json` summary
- `kfz_enriched.json` summary
- route list from the Observable build metadata where available

This is separate from E-Auto history. It answers "what was online before this
new data family was added."

Baseline source rule:

- Prefer live HTTP fetch for the deployed baseline.
- Also compare against `_src_of_backup/` when available.
- If live and backup summaries differ, record both and mark the baseline
  `mismatch_detected`.
- Do not block E-Auto planning on a mismatch, but do block publication until the
  source-of-truth restoration is resolved.

## Diff Semantics

Material diff events:

- topic added or removed
- topic group changed
- final state changed
- buildable state changed
- route policy changed
- CTA policy changed
- blocker count changed
- provider evidence boundary changed
- official source count changed
- source-backed fact count changed
- unknown count changed

Informational diff events:

- source artifact path changed with identical content hash
- generation timestamp changed with identical normalized content
- public claim wording changed without policy or readiness changes

The page should prioritize material events and keep informational events in a
secondary table.

## Rollback Plan

Rollback should not delete snapshots.

- To roll back, update `src/data/eauto_prescore.json` so `current_snapshot`
  points to an older dated snapshot.
- Add a rollback event to the history manifest.
- Keep the later snapshot and diff files for auditability.
- The Observable page should display the current pointer, not simply the newest
  dated file.

## Visualization Plan

The Observable page should visualize both current state and change over time:

- Current KPI cards: candidate topics, signal count, blocker count, buildable
  surfaces, suppressed routes, provider evidence excluded.
- Timeline chart: candidate signal count, topic count, blocker count, and
  buildable surface count over snapshot dates.
- Topic readiness table: current state with previous-state delta columns.
- Change log table: event type, topic, field, previous value, current value.
- Unknown-count delta chart: topics with the largest change in unknowns.
- Policy-change table: route policy and CTA policy changes.
- Provider-boundary status card: explicit confirmation that provider rows are
  excluded from official evidence.

For the first E-Auto snapshot, the timeline has one point and the change log
should say that the baseline was established. Future imports should show real
deltas.

## Public Copy Gate

Before committing the E-Auto page, scan changed public-facing files for banned
finality language:

- official score
- final score
- final AmtsScore rating
- complete benchmark
- fully verified
- public rating

Allowed wording:

- candidate signals
- preview analysis
- methodology review
- source coverage
- fact coverage
- provider evidence excluded

If banned wording is present, revise the copy before build verification.

## Public Evidence Boundary

Only public-safe normalized fields should be committed to the AmtsScore site.

- Do not commit provider rows.
- Do not commit private scraper internals beyond stable artifact IDs and
  high-level provenance.
- Do not treat Outline text, LLM output, or search snippets as proof unless they
  are backed by source manifests.
- Public pages may describe source and fact coverage, but must not expose
  private operational details as evidence.

## Future Import Flow

Future imports should:

1. Normalize the new scraper package.
2. Compute stable topic-level hashes from public-safe fields.
3. Compare the new snapshot to the latest history snapshot.
4. Record topic additions, removals, state changes, count changes, route-policy
   changes, CTA-policy changes, blocker changes, and provider-boundary changes.
5. Write the new dated snapshot only when the public-safe normalized data
   changes.
6. Update `src/data/eauto_prescore.json` to the latest snapshot.
7. Update the history manifest with previous/current pointers and a short
   change summary.

The Observable page should show the current snapshot and a small "since previous
snapshot" summary once at least two snapshots exist.

## Content Boundaries

- Use labels like "candidate signals", "preview analysis", and "methodology
  review".
- Do not call the output an official score, final AmtsScore rating, or complete
  public evaluation.
- Do not compute a 0-10 E-Auto score in the MVP.
- Do not use provider rows as official evidence.
- Keep bridge-only topics separate from standalone topic claims.
- Keep calculator routes suppressed unless a later policy explicitly enables
  them.

## Observable Page Shape

The first page should show:

- Gate status from final audit and pipeline check.
- Summary metrics for candidate-ready topics, signals, blockers, and provider
  evidence exclusion.
- Buildable AmtsScore-lane topics.
- Bridge or context topics.
- Suppressed, not-ready, and provider-only topics.
- Source coverage, fact coverage, unknown counts, route policy, CTA policy, and
  public claim wording per topic.

## Acceptance Criteria

- Observable source is tracked as the current site source.
- Current deployed Observable data is preserved as a repo-local baseline.
- Importer fails fast on unsupported major contract versions, hard blockers,
  failed pipeline checks, or provider rows used as evidence.
- Importer writes append-only history, current pointer, manifest, and diff
  files before the page consumes the data.
- Derived JSON includes gate summaries, topic readiness, source coverage, fact
  coverage, unknown counts, route policy, CTA policy, and provider boundary.
- The Observable E-Auto page renders useful candidate signal content from local
  data.
- The Observable E-Auto page visualizes current state and change-over-time
  scaffolding from the history model.
- Public page copy makes the non-final status clear.
- Observable build passes and produces the expected E-Auto route.

## Implementation Note

Implemented as two commits:

1. Restore Observable as the tracked source of truth.
2. Add the E-Auto history-first importer, baseline preservation, first
   candidate-signal snapshot, current pointer, diff, manifest, and Observable
   topic page.

## Verification Commands

Exact commands should be confirmed after Observable package restoration, but the
expected verification sequence is:

```bash
python tools/eauto/import_amtsscore.py
pnpm build
test -f dist/topics/e-auto.html
rg -n "official score|final score|final AmtsScore rating|complete benchmark|fully verified|public rating" src/topics src/index.md
```

The copy gate `rg` should return no matches.

## Deployment Verification

Local build is necessary but not sufficient.

After deployment, run smoke checks for:

- published `/topics/e-auto` route returns HTTP 200
- published page contains candidate-signal wording
- published page does not contain banned finality wording
- generated hashed data attachment for `eauto_prescore.json` is present
- previous live routes still return HTTP 200:
  - `/`
  - `/methodology`
  - `/topics/halteverbot`
  - `/topics/kfz-zulassung`

Deployment verification should be reported in the final handoff or release
note.
