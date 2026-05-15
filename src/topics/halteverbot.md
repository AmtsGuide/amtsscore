---
title: Halteverbot: Topic-Daten v0
toc: true
---

# Halteverbot

Erste Auswertung aus dem AmtsGuide-Scraper. **Pre-AmtsScore**. diese Daten sind noch nicht nach der AmtsScore-Methodik gescort. Sie zeigen aber, was wir heute schon messen.

```js
const data = FileAttachment("../../data/halteverbot.json").json();
```

```js
const summary = (await data);
```

## Zusammenfassung

```js
html`<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin:1rem 0">
  <div style="padding:1rem;background:var(--theme-background-b);border:1px solid var(--theme-foreground-faintest);border-radius:8px">
    <div style="color:var(--theme-foreground-muted);font-size:0.85rem">Behörden-Quellen</div>
    <div style="font-size:2rem;font-weight:600">${summary.total_authorities}</div>
  </div>
  <div style="padding:1rem;background:var(--theme-background-b);border:1px solid var(--theme-foreground-faintest);border-radius:8px">
    <div style="color:var(--theme-foreground-muted);font-size:0.85rem">Anbieter im Index</div>
    <div style="font-size:2rem;font-weight:600">${summary.total_suppliers}</div>
  </div>
  <div style="padding:1rem;background:var(--theme-background-b);border:1px solid var(--theme-foreground-faintest);border-radius:8px">
    <div style="color:var(--theme-foreground-muted);font-size:0.85rem">Städte mit Daten</div>
    <div style="font-size:2rem;font-weight:600">${summary.total_cities}</div>
  </div>
  <div style="padding:1rem;background:var(--theme-background-b);border:1px solid var(--theme-foreground-faintest);border-radius:8px">
    <div style="color:var(--theme-foreground-muted);font-size:0.85rem">Anbieter Top-Klasse</div>
    <div style="font-size:2rem;font-weight:600">${summary.supplier_tiers.A}</div>
  </div>
</div>`
```

Stand der Daten: **${summary.scraped_at}**.

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

## Anbieter-Dichte pro Stadt

Anzahl der gefundenen Anbieter, getrennt nach Qualitäts-Klasse (A = strenger Score, B = mittel, C = schwach).

```js
const withSuppliers = summary.cities.filter(c => c.suppliers_count > 0).sort((a,b) => b.suppliers_count - a.suppliers_count);
const stacked = withSuppliers.flatMap(c => [
  {city: c.city, tier: "A", count: c.suppliers_tier_a},
  {city: c.city, tier: "B", count: c.suppliers_tier_b},
  {city: c.city, tier: "C", count: c.suppliers_tier_c}
]).filter(d => d.count > 0);
```

```js
Plot.plot({
  marginLeft: 160,
  width: 800,
  height: 30 + withSuppliers.length * 24,
  x: {label: "Anzahl Anbieter", grid: true},
  y: {label: null, domain: withSuppliers.map(c => c.city)},
  color: {legend: true, domain: ["A", "B", "C"], range: ["#16a34a", "#eab308", "#dc2626"]},
  marks: [
    Plot.barX(stacked, {
      x: "count",
      y: "city",
      fill: "tier"
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
    "suppliers_count",
    "suppliers_tier_a"
  ],
  header: {
    city: "Stadt",
    authorities_count: "Behörden-Quellen",
    processing_days_avg: "⌀ Bearbeitungstage",
    cost_min_avg: "⌀ Mindestgebühr (€)",
    suppliers_count: "Anbieter",
    suppliers_tier_a: "Klasse A"
  },
  sort: "suppliers_count",
  reverse: true,
  rows: 40
})
```

---

## Methodische Anmerkungen

Diese Auswertung ist **Pre-AmtsScore v0**:

- Daten stammen aus dem AmtsGuide-Scraper (Stand März 2026), nicht aus der noch zu implementierenden AmtsScore-Pipeline
- Keine 10-Dimensionen-Bewertung pro Stadt-Website
- Kein Composite-Score 0-10
- Statt dessen: nackte Daten zu Behörden-Wartezeiten, Gebühren und Marktverfügbarkeit von Dienstleistern

Die AmtsScore-Methodik (siehe `/methodology`) misst hingegen die digitale Performance der Stadt-Verwaltungs-Websites selbst. Beide Ebenen sind komplementär:

- **Diese Topic-Daten** sagen: *Wie funktioniert dieser konkrete Behördengang in dieser Stadt?*
- **AmtsScore-Methodik** sagt: *Wie gut macht diese Stadt-Website ihre Arbeit insgesamt?*
