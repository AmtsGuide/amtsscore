# E-Auto Candidate Signals

Date: 2026-06-06
Snapshot: 2026-06-04
Status: public preview pending

## Summary

This release adds the first E-Auto candidate-signal snapshot to the Observable
AmtsScore site. It establishes history tracking before publishing the new data
family.

## Baseline

- Previous E-Auto snapshot: none
- Current E-Auto snapshot: 2026-06-04
- Site baseline preserved: 2026-05-20 Observable deployment data

## Material Changes

- Added E-Auto candidate-signal history model.
- Added current pointer, dated snapshot, manifest, and first diff file.
- Added E-Auto Observable topic page.
- Added navigation and homepage links.

## Snapshot Metrics

- Candidate-ready topics: 19
- Candidate signals: 133
- Blocked signals: 0
- Web-buildable embedded surfaces: 12
- Calculator routes ready: 0
- Provider rows used as evidence: false

## Diagnostics

- Final audit: accepted with diagnostics
- Pipeline check: accepted with diagnostics
- Hard blockers: 0
- Failed checks: 0
- Warning checks: 1

## Evidence Boundary

Provider rows remain excluded from AmtsScore evidence. The public page exposes
only normalized candidate-signal, source coverage, fact coverage, unknown-count,
policy, and provenance fields.

## Verification

- Importer run completed.
- No-change importer run completed.
- Observable build completed.
- `dist/topics/e-auto.html` generated.
- Copy gate found no banned finality wording in changed public-facing files.
- Deployment verification remains pending because this change has not been
  deployed in this session.
