---
title: "Leipzig: Pre-AmtsScore"
toc: false
---

# Leipzig

```js
const d = await FileAttachment("../data/prescore.json").json();
const slug = 'leipzig';
const cityTopics = d.topics
  .map(t => ({topic: t.label, slug: t.slug, ...t.cities.find(c => c.city_slug === slug)}))
  .filter(t => t.city_slug);
const summary = d.city_summary.find(c => c.city_slug === slug);
const stateSummary = summary ? d.state_summary.find(s => s.bundesland === summary.bundesland) : null;
```

```js
html`<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:0.75rem;margin:1rem 0">
  <div class="stat-card">
    <div class="stat-label" style="font-size:0.8rem">Bundesland</div>
    <div style="font-weight:600">${summary?.bundesland ?? "—"}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label" style="font-size:0.8rem">⌀ Pre-Score</div>
    <div style="font-weight:600">${summary ? summary.avg_score.toFixed(1) + " / 10" : "—"}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label" style="font-size:0.8rem">Topics gemessen</div>
    <div style="font-weight:600">${summary?.topic_count ?? 0} / ${d.topics.length}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label" style="font-size:0.8rem">Bundesweiter Rang</div>
    <div style="font-weight:600">${summary?.rank ?? "—"} / ${d.city_summary.length}</div>
  </div>
</div>`
```

## Score pro Topic

```js
Inputs.table(cityTopics.map(t => ({
  Topic: t.topic,
  Score: t.score,
  "Rang im Topic": t.rank,
  Geschwindigkeit: t.speed,
  Kosten: t.cost,
  Online: t.online,
})), {
  rows: 20,
  format: {
    Score: (x) => x === null ? "—" : x.toFixed(1),
    Geschwindigkeit: (x) => x === null ? "—" : x.toFixed(1),
    Kosten: (x) => x === null ? "—" : x.toFixed(1),
    Online: (x) => x === null ? "—" : x === 10 ? "ja" : "nein",
  }
})
```

## Score-Komponenten

```js
Plot.plot({
  width: 700, height: 30 + cityTopics.length * 60,
  marginLeft: 130,
  x: {label: "Score (0-10)", domain: [0, 10], grid: true},
  y: {label: null},
  marks: [
    Plot.barX(
      cityTopics.flatMap(t => [
        {topic: t.topic, kind: "Geschwindigkeit", value: t.speed},
        {topic: t.topic, kind: "Kosten", value: t.cost},
        {topic: t.topic, kind: "Online", value: t.online},
      ]).filter(d => d.value !== null),
      {x: "value", y: "topic", fy: "topic", fill: "kind", insetTop: 6, insetBottom: 6}
    ),
    Plot.ruleX([0]),
  ],
  fy: {label: null, axis: null},
  color: {legend: true, domain: ["Geschwindigkeit", "Kosten", "Online"], range: ["#1a3da5", "#d97706", "#16a34a"]},
})
```

## Rohwerte

```js
Inputs.table(cityTopics.map(t => ({
  Topic: t.topic,
  "Tage": t.raw.speed_days,
  "Euro": t.raw.cost_eur,
  "Online verfügbar": t.raw.online_available,
})), {
  rows: 20,
  format: {
    "Tage": (x) => x === null ? "—" : `${x} d`,
    "Euro": (x) => x === null ? "—" : `${x.toFixed(0)} €`,
    "Online verfügbar": (x) => x === true ? "ja" : x === false ? "nein" : "—",
  }
})
```

## Im Vergleich

```js
const stateCities = d.city_summary.filter(c => c.bundesland === summary?.bundesland);
```

```js
html`
<p><strong>Im Bundesland (${summary?.bundesland ?? "—"}):</strong>
${stateCities.length} Stadt${stateCities.length === 1 ? "" : "e"} mit Pre-Score-Daten,
Landesdurchschnitt ⌀ ${stateSummary?.avg_score.toFixed(1) ?? "—"}.</p>
<p><strong>Bundesweit:</strong> Stadt-Durchschnitt ${(d.city_summary.reduce((a,c) => a + c.avg_score, 0) / d.city_summary.length).toFixed(1)}.</p>
`
```

```js
const others = stateCities.filter(c => c.city_slug !== slug);
html`${others.length ? html`<p><strong>Andere Städte in ${summary?.bundesland}:</strong> ${others.map(c => html`<a href="/staedte/${c.city_slug}">${c.city}</a>`).reduce((a,b) => html`${a} · ${b}`)}</p>` : ''}`
```

→ [Bundesland-Übersicht](/bundeslaender/sachsen) · [alle Städte](/staedte/) · [Methodik](/methodology)
