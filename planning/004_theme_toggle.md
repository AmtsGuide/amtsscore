# Theme Toggle

Status: implemented

Date: 2026-06-06

## Context

The Observable site already shipped light and dark theme tokens through Observable's theme CSS, but there was no user-facing control. The site also had separate light and dark logo assets, so a manual mode needs to switch both theme variables and the logo.

## Implementation

- Added a global light/dark toggle in the Observable header.
- Persisted the selected theme in `localStorage` under `amtsscore-theme`.
- Applied the saved theme before page paint through the configured head script.
- Added explicit global stylesheet configuration for `src/style.css`.
- Added `data-theme` CSS variable overrides so manual choice wins over system preference.
- Switched between `logo-light.svg` and `logo-dark.svg` based on the active theme.

## Verification

- `pnpm build` passes and validates all Observable links.
- Browser interaction check confirms dark mode applies, stores `dark`, swaps to the dark logo, and persists after reload.
- Browser interaction check confirms a second click stores `light`, restores the light theme, and swaps back to the light logo.
- Browser media check confirms system dark mode applies when no manual preference is saved.
