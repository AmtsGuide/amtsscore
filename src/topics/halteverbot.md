---
title: "Halteverbot: Topic-Daten + Pre-AmtsScore"
toc: true
---

# Halteverbot

Erste Auswertung aus dem AmtsGuide-Scraper plus **Pre-AmtsScore** pro Stadt
(40% Kosten + 40% Geschwindigkeit, linear normalisiert).

```js
const data = FileAttachment("../data/halteverbot.json").json();
const prescoreData = FileAttachment("../data/prescore.json").json();
```

```js
const summary = (await data);
const prescore = (await prescoreData).topics.find(t => t.slug === "halteverbot");
```

## Pre-AmtsScore pro Stadt

```js
Inputs.table(prescore.cities.map(c => ({
  Rang: c.rank,
  Stadt: c.city,
  Score: c.score,
  "Tage": c.raw.speed_days,
  "Euro": c.raw.cost_eur,
})), {
  rows: 40,
  format: {
    Score: (x) => x === null ? "—" : x.toFixed(1),
    Tage: (x) => x === null ? "—" : `${x} d`,
    Euro: (x) => x === null ? "—" : `${x.toFixed(0)} €`,
  }
})
```

## Zusammenfassung

```js
html`<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin:1rem 0">
  <div style="padding:1rem;border-radius:8px" class="stat-card">
    <div class="stat-label" style="font-size:0.85rem">Behörden-Quellen</div>
    <div style="font-size:2rem;font-weight:600">${summary.total_authorities}</div>
  </div>
  <div style="padding:1rem;border-radius:8px" class="stat-card">
    <div class="stat-label" style="font-size:0.85rem">Städte mit Daten</div>
    <div style="font-size:2rem;font-weight:600">${summary.total_cities}</div>
  </div>
  <div style="padding:1rem;border-radius:8px" class="stat-card">
    <div class="stat-label" style="font-size:0.85rem">Stand</div>
    <div style="font-size:1.1rem;font-weight:600">${(summary.scraped_at ?? "").slice(0,10) || "—"}</div>
  </div>
</div>`
```

## Was kosten Halteverbots-Anträge im Schnitt?

```js
const withCost = summary.cities.filter(c => c.cost_min_avg != null).sort((a,b) => b.cost_min_avg - a.cost_min_avg);
```

```js
Plot.plot({
  marginLeft: 140,
  width: 800,
  height: 30 + withCost.length * 22,
  x: {label: "Mindestgebühr (€)", grid: true},
  y: {label: null},
  marks: [
    Plot.barX(withCost, {
      x: "cost_min_avg",
      y: "city",
      sort: {y: "x", reverse: true},
      fill: "#3b82f6"
    }),
    Plot.text(withCost, {
      x: "cost_min_avg",
      y: "city",
      text: d => `${d.cost_min_avg.toFixed(2)} €`,
      dx: 5,
      textAnchor: "start",
      fontSize: 11
    })
  ]
})
```

## Wie lange dauert die Bearbeitung?

```js
const withDays = summary.cities.filter(c => c.processing_days_avg != null).sort((a,b) => b.processing_days_avg - a.processing_days_avg);
```

```js
Plot.plot({
  marginLeft: 140,
  width: 800,
  height: 30 + withDays.length * 22,
  x: {label: "Durchschnittliche Bearbeitungstage", grid: true},
  y: {label: null},
  marks: [
    Plot.barX(withDays, {
      x: "processing_days_avg",
      y: "city",
      sort: {y: "x", reverse: true},
      fill: "#ef4444"
    }),
    Plot.text(withDays, {
      x: "processing_days_avg",
      y: "city",
      text: d => `${d.processing_days_avg} Tage`,
      dx: 5,
      textAnchor: "start",
      fontSize: 11
    })
  ]
})
```

## Detail-Tabelle

```js
Inputs.table(summary.cities, {
  columns: [
    "city",
    "authorities_count",
    "processing_days_avg",
    "cost_min_avg",
  ],
  header: {
    city: "Stadt",
    authorities_count: "Behörden-Quellen",
    processing_days_avg: "⌀ Bearbeitungstage",
    cost_min_avg: "⌀ Mindestgebühr (€)",
  },
  sort: "processing_days_avg",
  rows: 40
})
```

---

## Methodische Anmerkungen

Diese Auswertung ist **Pre-AmtsScore v0**:

- Daten stammen aus dem AmtsGuide-Scraper (Stand März 2026), nicht aus der noch zu implementierenden AmtsScore-Pipeline
- Keine 10-Dimensionen-Bewertung pro Stadt-Website
- Kein Composite-Score 0-10
- Statt dessen: nackte Daten zu Behörden-Wartezeiten und Gebühren

Die AmtsScore-Methodik (siehe `/methodology`) misst hingegen die digitale Performance der Stadt-Verwaltungs-Websites selbst. Beide Ebenen sind komplementär:

- **Diese Topic-Daten** sagen: *Wie funktioniert dieser konkrete Behördengang in dieser Stadt?*
- **AmtsScore-Methodik** sagt: *Wie gut macht diese Stadt-Website ihre Arbeit insgesamt?*
