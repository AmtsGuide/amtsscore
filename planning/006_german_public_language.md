Status: implemented

# German Public Language Pass

## Context

AmtsScore is a German-language public website. Public-facing pages should not
show English interface labels such as `Candidate Signals`, `Topic`, `Score`,
`Gate Status`, `Snapshot`, or `Provider Evidence`. Internal data fields,
schema keys, code variables, file names, and technical product names can remain
English where changing them would break importers or chart logic.

## Implementation

- Translate public navigation labels to German.
- Translate the E-Auto page copy, headings, metric labels, table headings, and
  status labels to German.
- Translate homepage news and summary cards to German.
- Translate city, state, and topic table labels from `Topic` and `Score` to
  `Thema` and `Wert`.
- Keep internal data identifiers unchanged.

## Verification

- Run a public-copy scan for common English UI terms after the pass.
- Run the Observable build.
- Spot-check the E-Auto and index pages after build or preview.
