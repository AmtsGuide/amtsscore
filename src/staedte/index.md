---
title: "Städte: Pre-AmtsScore-Übersicht"
toc: false
---

# Städte

```js
const d = await FileAttachment("../data/prescore.json").json();
```

${d.city_summary.length} Städte mit Pre-AmtsScore-Daten. Klicken Sie eine Stadt für ihre Detailseite.

## Ranking nach Coverage + ⌀ Score

```js
Inputs.table(d.city_summary.map(c => ({
  Rang: c.rank,
  Stadt: c.city,
  Bundesland: c.bundesland ?? "—",
  "⌀ Score": c.avg_score,
  Topics: c.topic_count,
  Detail: c.city_slug,
})), {
  rows: 60,
  format: {
    "⌀ Score": (x) => x.toFixed(1),
    Detail: (slug) => htl.html`<a href="/staedte/${slug}">öffnen →</a>`,
  }
})
```

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
