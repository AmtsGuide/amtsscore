# Homepage News And Summary

Date: 2026-06-06
Status: implemented
Implementation target: Observable Framework

## Objective

Update the Observable homepage so it keeps the current high-level entry points
and also shows recent additions or changes. The homepage should help a visitor
understand what data exists now and what changed recently.

## Inputs

- `src/data/prescore.json`
- `src/data/eauto_prescore.json`
- `src/data/history/eauto/index.json`
- `docs/releases/2026-06-06-eauto-candidate-signals.md`

## Scope

MVP homepage changes:

- Add data-driven summary cards for existing topic data.
- Add E-Auto candidate-signal summary.
- Add a news/recent changes section.
- Keep public wording clear that E-Auto is a preview and not a rating.
- Keep existing Methodik, Topic-Daten, Leuchttürme, and Über entry points.

Out of scope:

- New data imports.
- Scoring formulas.
- Deployment automation.
- News CMS.

## Acceptance Criteria

- Homepage builds in Observable.
- Recent changes include the E-Auto candidate-signal snapshot.
- Summary cards load from local JSON data.
- Public copy avoids finality wording.

## Implementation Note

Implemented with data-backed Observable homepage summary cards and a static
recent-changes section tied to the E-Auto candidate-signal release and
site-baseline history.
