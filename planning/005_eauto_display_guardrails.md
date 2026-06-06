# E-Auto Display Guardrails

Status: implemented

Date: 2026-06-06

## Context

The E-Auto Candidate Signals page exposed internal machine labels such as `accepted_with_diagnostics` and `editor_review_required` in public cards. Long status values could also overflow or wrap badly in metric cards.

## Implementation

- Added a display-label mapping on the E-Auto page for statuses, policies, groups, metrics, and review labels.
- Replaced raw machine labels in cards, tables, chart legends, and method notes with readable display text.
- Fixed a Markdown interpolation issue that rendered `${current.current_snapshot}` literally.
- Added reusable `.stat-grid`, `.stat-value`, and `.stat-value--long` styles.
- Added container-aware sizing, stable min widths, and emergency wrapping to `.stat-card` so long values do not escape card boundaries.

## Verification

- `pnpm build` passes and validates all Observable links.
- Desktop rendered check confirms no raw machine labels in visible E-Auto page text.
- Desktop and mobile rendered checks confirm no stat-card text overflow.
- Desktop and mobile screenshots confirm the first E-Auto card section wraps cleanly.
