#!/usr/bin/env python3
"""Generate per-city and per-state Pre-AmtsScore pages from prescore.json.

Each page is a thin Observable Markdown file that reads prescore.json
client-side, filters to the relevant slug, and renders the per-place view.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "src" / "data" / "prescore.json"
CITY_DIR = ROOT / "src" / "staedte"
STATE_DIR = ROOT / "src" / "bundeslaender"

CITY_TEMPLATE = """---
title: "{display}: Pre-AmtsScore"
toc: false
---

# {display}

```js
const d = await FileAttachment("../data/prescore.json").json();
const slug = {slug!r};
const cityTopics = d.topics
  .map(t => ({{topic: t.label, slug: t.slug, ...t.cities.find(c => c.city_slug === slug)}}))
  .filter(t => t.city_slug);
const summary = d.city_summary.find(c => c.city_slug === slug);
const stateSummary = summary ? d.state_summary.find(s => s.bundesland === summary.bundesland) : null;
```

```js
html`<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:0.75rem;margin:1rem 0">
  <div class="stat-card">
    <div class="stat-label" style="font-size:0.8rem">Bundesland</div>
    <div style="font-weight:600">${{summary?.bundesland ?? "—"}}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label" style="font-size:0.8rem">⌀ Pre-Score</div>
    <div style="font-weight:600">${{summary ? summary.avg_score.toFixed(1) + " / 10" : "—"}}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label" style="font-size:0.8rem">Topics gemessen</div>
    <div style="font-weight:600">${{summary?.topic_count ?? 0}} / ${{d.topics.length}}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label" style="font-size:0.8rem">Bundesweiter Rang</div>
    <div style="font-weight:600">${{summary?.rank ?? "—"}} / ${{d.city_summary.length}}</div>
  </div>
</div>`
```

## Score pro Topic

```js
Inputs.table(cityTopics.map(t => ({{
  Topic: t.topic,
  Score: t.score,
  "Rang im Topic": t.rank,
  Geschwindigkeit: t.speed,
  Kosten: t.cost,
  Online: t.online,
}})), {{
  rows: 20,
  format: {{
    Score: (x) => x === null ? "—" : x.toFixed(1),
    Geschwindigkeit: (x) => x === null ? "—" : x.toFixed(1),
    Kosten: (x) => x === null ? "—" : x.toFixed(1),
    Online: (x) => x === null ? "—" : x === 10 ? "ja" : "nein",
  }}
}})
```

## Score-Komponenten

```js
Plot.plot({{
  width: 700, height: 30 + cityTopics.length * 60,
  marginLeft: 130,
  x: {{label: "Score (0-10)", domain: [0, 10], grid: true}},
  y: {{label: null}},
  marks: [
    Plot.barX(
      cityTopics.flatMap(t => [
        {{topic: t.topic, kind: "Geschwindigkeit", value: t.speed}},
        {{topic: t.topic, kind: "Kosten", value: t.cost}},
        {{topic: t.topic, kind: "Online", value: t.online}},
      ]).filter(d => d.value !== null),
      {{x: "value", y: "topic", fy: "topic", fill: "kind", insetTop: 6, insetBottom: 6}}
    ),
    Plot.ruleX([0]),
  ],
  fy: {{label: null, axis: null}},
  color: {{legend: true, domain: ["Geschwindigkeit", "Kosten", "Online"], range: ["#1a3da5", "#d97706", "#16a34a"]}},
}})
```

## Rohwerte

```js
Inputs.table(cityTopics.map(t => ({{
  Topic: t.topic,
  "Tage": t.raw.speed_days,
  "Euro": t.raw.cost_eur,
  "Online verfügbar": t.raw.online_available,
}})), {{
  rows: 20,
  format: {{
    "Tage": (x) => x === null ? "—" : `${{x}} d`,
    "Euro": (x) => x === null ? "—" : `${{x.toFixed(0)}} €`,
    "Online verfügbar": (x) => x === true ? "ja" : x === false ? "nein" : "—",
  }}
}})
```

## Im Vergleich

```js
const stateCities = d.city_summary.filter(c => c.bundesland === summary?.bundesland);
```

```js
html`
<p><strong>Im Bundesland (${{summary?.bundesland ?? "—"}}):</strong>
${{stateCities.length}} Stadt${{stateCities.length === 1 ? "" : "e"}} mit Pre-Score-Daten,
Landesdurchschnitt ⌀ ${{stateSummary?.avg_score.toFixed(1) ?? "—"}}.</p>
<p><strong>Bundesweit:</strong> Stadt-Durchschnitt ${{(d.city_summary.reduce((a,c) => a + c.avg_score, 0) / d.city_summary.length).toFixed(1)}}.</p>
`
```

```js
const others = stateCities.filter(c => c.city_slug !== slug);
html`${{others.length ? html`<p><strong>Andere Städte in ${{summary?.bundesland}}:</strong> ${{others.map(c => html`<a href="/staedte/${{c.city_slug}}">${{c.city}}</a>`).reduce((a,b) => html`${{a}} · ${{b}}`)}}</p>` : ''}}`
```

→ [Bundesland-Übersicht](/bundeslaender/{state_slug}) · [alle Städte](/staedte/) · [Methodik](/methodology)
"""


STATE_TEMPLATE = """---
title: "{display}: Pre-AmtsScore"
toc: false
---

# {display}

```js
const d = await FileAttachment("../data/prescore.json").json();
const land = {display!r};
const stateSummary = d.state_summary.find(s => s.bundesland === land);
const stateCities = d.city_summary.filter(c => c.bundesland === land);
const stateTopicRows = d.topics.flatMap(t =>
  t.cities.filter(c => c.bundesland === land)
    .map(c => ({{topic: t.label, ...c}}))
);
```

```js
html`<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:0.75rem;margin:1rem 0">
  <div class="stat-card">
    <div class="stat-label" style="font-size:0.8rem">⌀ Pre-Score</div>
    <div style="font-weight:600">${{stateSummary?.avg_score.toFixed(1) ?? "—"}} / 10</div>
  </div>
  <div class="stat-card">
    <div class="stat-label" style="font-size:0.8rem">Städte mit Daten</div>
    <div style="font-weight:600">${{stateCities.length}}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label" style="font-size:0.8rem">Datenpunkte gesamt</div>
    <div style="font-weight:600">${{stateSummary?.n_datapoints ?? 0}}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label" style="font-size:0.8rem">Bundesländer-Rang</div>
    <div style="font-weight:600">${{stateSummary?.rank ?? "—"}} / 16</div>
  </div>
</div>`
```

## Städte in {display}

```js
Inputs.table(stateCities.map(c => ({{
  Stadt: c.city,
  "⌀ Score": c.avg_score,
  Topics: c.topic_count,
  "Bundesweiter Rang": c.rank,
  Detail: c.city_slug,
}})), {{
  rows: 30,
  format: {{
    "⌀ Score": (x) => x.toFixed(1),
    Detail: (slug) => htl.html`<a href="/staedte/${{slug}}">öffnen →</a>`,
  }}
}})
```

## Topic-Mix in {display}

```js
const byTopic = {{}};
for (const r of stateTopicRows) {{
  if (r.score === null) continue;
  if (!byTopic[r.topic]) byTopic[r.topic] = [];
  byTopic[r.topic].push(r.score);
}}
const topicAvgs = Object.entries(byTopic).map(([topic, scores]) => ({{
  Topic: topic,
  "⌀ Score": +(scores.reduce((a,b)=>a+b, 0) / scores.length).toFixed(1),
  Städte: scores.length,
}}));
```

```js
Inputs.table(topicAvgs, {{rows: 10}})
```

## Score-Verteilung

```js
Plot.plot({{
  width: 700, height: 30 + stateTopicRows.length * 18,
  marginLeft: 130,
  x: {{label: "Score (0-10)", domain: [0, 10], grid: true}},
  y: {{label: null}},
  color: {{legend: true}},
  marks: [
    Plot.dot(stateTopicRows.filter(r => r.score !== null), {{
      x: "score",
      y: "city",
      fill: "topic",
      r: 5,
    }}),
    Plot.ruleX([0])
  ]
}})
```

→ [alle Bundesländer](/bundeslaender/) · [alle Städte](/staedte/) · [Methodik](/methodology)
"""


def slugify_state(name: str) -> str:
    return (name.lower()
            .replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")
            .replace("ß", "ss").replace(" ", "-").replace("-", "-"))


def main():
    d = json.loads(DATA.read_text())

    CITY_DIR.mkdir(parents=True, exist_ok=True)
    STATE_DIR.mkdir(parents=True, exist_ok=True)

    n_city = 0
    for c in d["city_summary"]:
        slug = c["city_slug"]
        state_slug = slugify_state(c["bundesland"]) if c["bundesland"] else ""
        page = CITY_TEMPLATE.format(display=c["city"], slug=slug, state_slug=state_slug)
        (CITY_DIR / f"{slug}.md").write_text(page)
        n_city += 1

    n_state = 0
    for s in d["state_summary"]:
        state_slug = slugify_state(s["bundesland"])
        page = STATE_TEMPLATE.format(display=s["bundesland"])
        (STATE_DIR / f"{state_slug}.md").write_text(page)
        n_state += 1

    print(f"wrote {n_city} city pages, {n_state} state pages")


if __name__ == "__main__":
    main()
