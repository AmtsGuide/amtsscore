---
title: "Städte: AmtsScore-Vorabwert-Übersicht"
toc: false
---

# Städte

```js
const d = await FileAttachment("../data/prescore.json").json();
```

${d.city_summary.length} Städte mit AmtsScore-Vorabwert-Daten. Klicken Sie eine Stadt für ihre Detailseite.

## Stadt-Themen-Matrix

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
  "⌀ Wert": c.avg_score,
  Themen: c.topic_count,
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
    "⌀ Wert": (x) => x.toFixed(1),
    Detail: (slug) => htl.html`<a href="/staedte/${slug}">öffnen →</a>`,
  }
})
```

Vollständige Abdeckung (3/3 Themen): ${matrix.filter(c => c.Themen === 3).length} Städte.
Teilabdeckung: ${matrix.filter(c => c.Themen < 3).length} Städte.

## Verteilung

```js
Plot.plot({
  width: 800, height: 350,
  marginLeft: 60,
  x: {label: "⌀ Vorabwert (0-10)", grid: true},
  y: {label: "Anzahl Städte"},
  marks: [
    Plot.rectY(d.city_summary, Plot.binX({y: "count"}, {x: "avg_score", thresholds: 20, fill: "#1a3da5"})),
    Plot.ruleY([0])
  ]
})
```

→ [Bundesländer-Übersicht](/bundeslaender/) · [Halteverbot](/topics/halteverbot) · [Methodik](/methodik)
