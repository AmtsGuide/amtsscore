# AGENTS.md

Standing rules for work in this repository.

## Public Language

- AmtsScore is a German-only public website.
- All public-facing website text, navigation labels, chart labels, table labels,
  buttons, headings, metadata titles, and visible status labels must be German.
- Do not introduce English public copy such as `Preview`, `Candidate Signals`,
  `Score`, `Topic`, `Coverage`, `Review`, `Status`, or `Provider Evidence`.
- Technical protocol/product names may remain unchanged where they are the
  actual names, for example API, MCP, OpenAPI, REST, GraphQL, llms.txt,
  Schema.org, Lighthouse, GitHub, and Observable.
- Internal implementation identifiers may remain English when they are schema
  fields, code variables, file names, imported data keys, or stable machine
  values.

## Repository Discipline

- One logical unit = one commit. Push immediately after commit.
- Never use `git add .` or `git add -A`. Stage specific files.
- Internal artifacts such as code, comments, planning, and handoffs are written
  in English unless they are public-facing website copy.
- Planning files live under `planning/` and use consecutive numbering.
- Do not overwrite unrelated user changes.
