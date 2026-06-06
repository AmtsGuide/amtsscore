# Methodik Route Alignment

Status: implemented

Date: 2026-06-06

## Context

The live site redirects `/methodology` to `/methodik`, but the Observable source still built the methodology page as `/methodology`. This made the public `/methodik` route fail even though the content existed under the English slug.

## Implementation

- Renamed the Observable methodology source page from `src/methodology.md` to `src/methodik.md`.
- Updated the Observable sidebar entry to use `/methodik`.
- Updated internal public links from `/methodology` to `/methodik`.
- Preserved historical baseline data that still records the previous `/methodology` route.

## Verification

- `pnpm build` renders `dist/methodik.html`.
- The build no longer emits `dist/methodology.html`.
- The generated homepage/sidebar link points to `./methodik`.
- The generated Methodik page marks `./methodik` as the active sidebar route.
