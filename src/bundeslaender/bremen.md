---
title: "Bremen: Pre-AmtsScore"
toc: false
---

# Bremen

```js
const d = await FileAttachment("../data/prescore.json").json();
const land = 'Bremen';
const stateSummary = d.state_summary.find(s => s.bundesland === land);
const stateCities = d.city_summary.filter(c => c.bundesland === land);
const stateTopicRows = d.topics.flatMap(t =>
  t.cities.filter(c => c.bundesland === land)
    .map(c => ({topic: t.label, ...c}))
);
```

```js
html`<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:0.75rem;margin:1rem 0">
  <div class="stat-card">
    <div class="stat-label" style="font-size:0.8rem">⌀ Pre-Score</div>
    <div style="font-weight:600">${stateSummary?.avg_score.toFixed(1) ?? "—"} / 10</div>
  </div>
  <div class="stat-card">
    <div class="stat-label" style="font-size:0.8rem">Städte mit Daten</div>
    <div style="font-weight:600">${stateCities.length}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label" style="font-size:0.8rem">Datenpunkte gesamt</div>
    <div style="font-weight:600">${stateSummary?.n_datapoints ?? 0}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label" style="font-size:0.8rem">Bundesländer-Rang</div>
    <div style="font-weight:600">${stateSummary?.rank ?? "—"} / 16</div>
  </div>
</div>`
```

## Städte in Bremen

```js
Inputs.table(stateCities.map(c => ({
  Stadt: c.city,
  "⌀ Score": c.avg_score,
  Topics: c.topic_count,
  "Bundesweiter Rang": c.rank,
  Detail: c.city_slug,
})), {
  rows: 30,
  format: {
    "⌀ Score": (x) => x.toFixed(1),
    Detail: (slug) => htl.html`<a href="/staedte/${slug}">öffnen →</a>`,
  }
})
```

## Topic-Mix in Bremen

```js
const byTopic = {};
for (const r of stateTopicRows) {
  if (r.score === null) continue;
  if (!byTopic[r.topic]) byTopic[r.topic] = [];
  byTopic[r.topic].push(r.score);
}
const topicAvgs = Object.entries(byTopic).map(([topic, scores]) => ({
  Topic: topic,
  "⌀ Score": +(scores.reduce((a,b)=>a+b, 0) / scores.length).toFixed(1),
  Städte: scores.length,
}));
```

```js
Inputs.table(topicAvgs, {rows: 10})
```

## Score-Verteilung

```js
const scoredRows = stateTopicRows.filter(r => r.score !== null);
```

```js
scoredRows.length === 0
  ? html`<p style="opacity:0.7"><em>Keine messbaren Topic-Datenpunkte in diesem Bundesland.</em></p>`
  : Plot.plot({
      width: 700, height: 30 + scoredRows.length * 18,
      marginLeft: 130,
      x: {label: "Score (0-10)", domain: [0, 10], grid: true},
      y: {label: null},
      color: {legend: true},
      marks: [
        Plot.dot(scoredRows, {
          x: "score",
          y: "city",
          fill: "topic",
          r: 5,
        }),
        Plot.ruleX([0])
      ]
    })
```

→ [alle Bundesländer](/bundeslaender/) · [alle Städte](/staedte/) · [Methodik](/methodik)
