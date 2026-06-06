Status: implemented

# Pre-Alpha Data Warning Bar

## Decision

AmtsScore must show a persistent site-wide warning that the current public data
is KI-generated pre-alpha data and can be wrong, incomplete, or misleading.

## Implementation

- Add a global warning banner above the normal Observable header.
- Keep the copy public-facing and German-only.
- Make the warning visible on every page without relying on route-specific page
  content.

## Public Copy

`Pre-Alpha: Diese Website zeigt KI-generierte Vorabdaten. Die Daten können
falsch, unvollständig oder irreführend sein und sind nicht für Entscheidungen
geeignet.`

## Verification

- Build the Observable site.
- Confirm the warning appears in the generated homepage and E-Auto page.
