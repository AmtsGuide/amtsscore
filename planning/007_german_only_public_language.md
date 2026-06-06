Status: implemented

# German-Only Public Website Rule

## Decision

AmtsScore is a German-only public website. This is a standing product rule, not
a page-specific copy preference.

## Rule

All public-facing website text must be German:

- navigation labels
- homepage copy
- topic, city, state, glossary, special, and methodology pages
- chart labels
- table labels
- status labels
- metadata titles
- card labels and button/link copy

Allowed exceptions are actual technical names and public product/protocol names,
for example API, MCP, OpenAPI, REST, GraphQL, llms.txt, Schema.org, Lighthouse,
GitHub, Observable, and similar fixed names.

Internal machine identifiers may remain English when they are code variables,
schema fields, imported data keys, file names, or stable machine values. They
must not leak as visible page text.

## Implementation Note

The rule is now recorded in `AGENTS.md` so future agents have a persistent
repository-level memory note. This complements the earlier German public copy
pass in `planning/006_german_public_language.md`.
