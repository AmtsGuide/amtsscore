---
title: "Städte: Pre-AmtsScore-Übersicht"
toc: false
---

# Städte

```js
const d = await FileAttachment("../data/prescore.json").json();
```

${d.city_summary.length} Städte mit Pre-AmtsScore-Daten. Klicken Sie eine Stadt für ihre Detailseite.

## Stadt × Topic Matrix

```js
const scoreBySlug = {};
for (const t of d.topics) {
  for (const c of t.cities) {
    if (!scoreBySlug[c.city_slug]) scoreBySlug[c.city_slug] = {};
    scoreBySlug[c.city_slug][t.slug] = c.score;
  }
}
const matrix = d.city_summary.map(c => ({
  Rang: c.rank,
  Stadt: c.city,
  Bundesland: c.bundesland ?? "—",
  Halteverbot: scoreBySlug[c.city_slug]?.["halteverbot"] ?? null,
  KFZ: scoreBySlug[c.city_slug]?.["kfz-zulassung"] ?? null,
  GmbH: scoreBySlug[c.city_slug]?.["gmbh-gruendung"] ?? null,
  "⌀ Score": c.avg_score,
  Topics: c.topic_count,
  Detail: c.city_slug,
}));
```

```js
Inputs.table(matrix, {
  rows: 60,
  format: {
    Halteverbot: (x) => x === null ? "—" : x.toFixed(1),
    KFZ: (x) => x === null ? "—" : x.toFixed(1),
    GmbH: (x) => x === null ? "—" : x.toFixed(1),
    "⌀ Score": (x) => x.toFixed(1),
    Detail: (slug) => htl.html`<a href="/staedte/${slug}">öffnen →</a>`,
  }
})
```

Volle Coverage (3/3 Topics): ${matrix.filter(c => c.Topics === 3).length} Städte.
Teil-Coverage: ${matrix.filter(c => c.Topics < 3).length} Städte.

## Verteilung

```js
Plot.plot({
  width: 800, height: 350,
  marginLeft: 60,
  x: {label: "⌀ Pre-Score (0-10)", grid: true},
  y: {label: "Anzahl Städte"},
  marks: [
    Plot.rectY(d.city_summary, Plot.binX({y: "count"}, {x: "avg_score", thresholds: 20, fill: "#1a3da5"})),
    Plot.ruleY([0])
  ]
})
```

→ [Bundesländer-Übersicht](/bundeslaender/) · [Halteverbot](/topics/halteverbot) · [Methodik](/methodology)
