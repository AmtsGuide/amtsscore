Status: implemented

# Full-Width Black Warning Bar

## Decision

The pre-alpha warning must use the site design system as a full-width black top
bar. It should not appear as a red block constrained to the content/header
column.

## Implementation

- Keep the global warning markup in the Observable header.
- Update `.amtsscore-alpha-banner` to span `100vw` and break out of the
  Observable header content width using viewport-relative margins.
- Use a black background, light text, compact typography, and a subtle bottom
  border.

## Verification

- Build the Observable site.
- Confirm generated pages include the warning bar markup and updated CSS.
