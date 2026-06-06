---
title: "Bundesländer: Pre-AmtsScore-Übersicht"
toc: false
---

# Bundesländer

```js
const d = await FileAttachment("../data/prescore.json").json();
```

Alle 16 Bundesländer, gewichteter Durchschnitt über alle gemessenen Städte und Topics.

## Ranking

```js
Inputs.table(d.state_summary.map(s => {
  const slug = s.bundesland.toLowerCase()
    .replace(/ä/g,"ae").replace(/ö/g,"oe").replace(/ü/g,"ue").replace(/ß/g,"ss")
    .replace(/\s+/g,"-");
  return {
    Rang: s.rank,
    Bundesland: s.bundesland,
    "⌀ Score": s.avg_score,
    Datenpunkte: s.n_datapoints,
    Detail: slug,
  };
}), {
  rows: 16,
  format: {
    "⌀ Score": (x) => x.toFixed(1),
    Detail: (slug) => htl.html`<a href="/bundeslaender/${slug}">öffnen →</a>`,
  }
})
```

## Score-Verteilung

```js
Plot.plot({
  width: 800, height: 30 + d.state_summary.length * 22,
  marginLeft: 180,
  marginRight: 90,
  x: {label: "⌀ Pre-Score (0-10)", domain: [0, 10], grid: true},
  y: {label: null},
  marks: [
    Plot.barX(d.state_summary, {
      x: "avg_score",
      y: "bundesland",
      sort: {y: "x", reverse: true},
      fill: "#1a3da5",
    }),
    Plot.text(d.state_summary, {
      x: "avg_score",
      y: "bundesland",
      text: d => `${d.avg_score.toFixed(1)} (n=${d.n_datapoints})`,
      dx: 5,
      textAnchor: "start",
      fontSize: 11,
    })
  ]
})
```

→ [Städte-Übersicht](/staedte/) · [Methodik](/methodik)
