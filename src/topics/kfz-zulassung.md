---
title: "KFZ-Zulassung: tiefer Stadt-Vergleich"
toc: true
---

# KFZ-Zulassung (Neuzulassung)

```js
const d = await FileAttachment("../data/kfz_enriched.json").json();
```

20 deutsche Großstädte, 9 Dimensionen, keine Kosten-Wertung (Gebühren sind FZV-reguliert und sagen nichts über Service-Qualität).
Stand der Messung: ${d.generated_at.slice(0,10)}.

## Wichtigste Befunde

```js
const dimList = d.dimensions;
const haveSchema = d.cities.filter(c => c.dimensions.schema === 10).length;
const haveLlms = d.cities.filter(c => c.dimensions.llmstxt === 10).length;
const haveEid = d.cities.filter(c => c.dimensions.auth === 10).length;
const haveObs = d.cities.filter(c => c.dimensions.https !== null).length;
```

```js
html`<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:0.75rem;margin:1rem 0">
  <div class="stat-card">
    <div class="stat-label" style="font-size:0.8rem">Schema.org GovernmentService</div>
    <div style="font-size:1.5rem;font-weight:600">${haveSchema} / ${d.n_cities}</div>
    <div class="stat-label" style="font-size:0.8rem">Termin-URL trägt strukturiertes Markup</div>
  </div>
  <div class="stat-card">
    <div class="stat-label" style="font-size:0.8rem">llms.txt</div>
    <div style="font-size:1.5rem;font-weight:600">${haveLlms} / ${d.n_cities}</div>
    <div class="stat-label" style="font-size:0.8rem">Stadt-Domain trägt /llms.txt</div>
  </div>
  <div class="stat-card">
    <div class="stat-label" style="font-size:0.8rem">eID-Anbindung</div>
    <div style="font-size:1.5rem;font-weight:600">${haveEid} / ${d.n_cities}</div>
    <div class="stat-label" style="font-size:0.8rem">Termin-URL erwähnt eID/BundID/Servicekonto</div>
  </div>
  <div class="stat-card">
    <div class="stat-label" style="font-size:0.8rem">i-Kfz Online</div>
    <div style="font-size:1.5rem;font-weight:600">${d.cities.filter(c => c.dimensions.online === 10).length} / ${d.n_cities}</div>
    <div class="stat-label" style="font-size:0.8rem">Bürger kann online zulassen</div>
  </div>
</div>`
```

## Stadt-Ranking (9 Dimensionen, Gleichgewicht)

```js
Inputs.table(d.cities.map(c => ({
  Rang: c.rank,
  Stadt: c.city,
  "⌀": c.composite,
  Wartezeit: c.dimensions.speed,
  "i-Kfz": c.dimensions.online,
  Standorte: c.dimensions.access,
  "Walk-in": c.dimensions.friction,
  eID: c.dimensions.auth,
  "Schema.org": c.dimensions.schema,
  "llms.txt": c.dimensions.llmstxt,
  HTTPS: c.dimensions.https,
  "Presse-Stille": c.dimensions.press,
})), {
  rows: 25,
  format: {
    "⌀": (x) => x === null ? "—" : x.toFixed(1),
    Wartezeit: (x) => x === null ? "—" : x.toFixed(1),
    "i-Kfz": (x) => x === null ? "—" : x.toFixed(0),
    Standorte: (x) => x === null ? "—" : x.toFixed(1),
    "Walk-in": (x) => x === null ? "—" : x.toFixed(0),
    eID: (x) => x === null ? "—" : x.toFixed(0),
    "Schema.org": (x) => x === null ? "—" : x.toFixed(0),
    "llms.txt": (x) => x === null ? "—" : x.toFixed(0),
    HTTPS: (x) => x === null ? "—" : x.toFixed(1),
    "Presse-Stille": (x) => x === null ? "—" : x.toFixed(1),
  }
})
```

## Per Dimension

Alle Dimensionen nebeneinander — jede Stadt × jede Dimension auf einen Blick.

```js
const dimRows = d.dimensions.flatMap(dim =>
  d.cities
    .map(c => ({
      stadt: c.city,
      dimension: dim.label,
      dim_key: dim.key,
      value: c.dimensions[dim.key],
    }))
    .filter(r => r.value !== null)
);
```

```js
Plot.plot({
  width: 1100,
  marginLeft: 110,
  marginRight: 30,
  marginTop: 40,
  x: {domain: [0, 10], grid: true, ticks: 3, label: "Score"},
  y: {label: null},
  fx: {label: null, padding: 0.1},
  facet: {data: dimRows, x: "dimension"},
  marks: [
    Plot.barX(dimRows, {x: "value", y: "stadt", sort: {y: "x", reverse: true}, fill: "#1a3da5"}),
  ]
})
```

## Detailseiten der Termin-URLs

```js
Inputs.table(d.cities.map(c => ({
  Stadt: c.city,
  Behörde: c.authority,
  "Stadt-Domain": c.stadt_domain,
  "Termin-URL": c.source_url,
  Wartezeit: c.raw.wartezeit_label,
  "eID-Signale": (c.raw.eid_evidence ?? []).join(", "),
})), {
  rows: 25,
  format: {
    "Termin-URL": (url) => url ? htl.html`<a href="${url}" target="_blank" rel="noopener">öffnen ↗</a>` : "—",
  }
})
```

## Methodik

**9 Dimensionen, alle gleich gewichtet.** Kosten ist NICHT enthalten, weil
KFZ-Gebühren bundesweit nach FZV reguliert sind und Variationen kein
Qualitäts-Signal sind.

| # | Tier | Dimension | Quelle | Logik |
|---|---|---|---|---|
| 1 | 1 | Wartezeit | AmtsGuide `wartezeit` | weniger Tage = höher |
| 2 | 1 | i-Kfz Online | AmtsGuide `ikfz` | binär 10/0 |
| 3 | 1 | Standorte | AmtsGuide `standorte` count | mehr = höher |
| 4 | 1 | Walk-in möglich | AmtsGuide `terminpflicht` | walk-in = 10, Termin-Pflicht = 5 |
| 5 | 2 | eID-Anbindung | Termin-URL scan | BundID/BerlinID/Servicekonto/AusweisApp erwähnt |
| 6 | 2 | Schema.org GovernmentService | Termin-URL JSON-LD | binär 10/0 |
| 7 | 2 | llms.txt | Stadt-Domain `/llms.txt` | HTTP 200 = 10 |
| 8 | 2 | HTTPS-Hygiene | Mozilla Observatory | A+→10, F→0 |
| 9 | 3 | Presse-Stille | Brave Search "kritik wartezeit" | weniger Treffer = höher |

**Tier 1** = direkt aus AmtsGuide-Daten. **Tier 2** = pro-Stadt Webfetch.
**Tier 3** = externes Signal.

Tools im öffentlichen Repo: [`tools/scan/kfz.py`](https://github.com/AmtsGuide/amtsscore/blob/main/tools/scan/kfz.py).
Reproduzierbar mit `python tools/scan/kfz.py` (Brave API-Key empfohlen).

## Daten-Lücken

```js
const nullSpeed = d.cities.filter(c => c.dimensions.speed === null).length;
const nullObs = d.cities.filter(c => c.dimensions.https === null).length;
const nullPress = d.cities.filter(c => c.dimensions.press === null).length;
html`<ul>
<li>${nullSpeed}/${d.n_cities} Städte ohne maschinenlesbare Wartezeit (qualitative Strings).</li>
<li>${nullObs}/${d.n_cities} Städte ohne Mozilla-Observatory-Score (API-Ausfall im Messzeitraum, kein Stadt-Problem).</li>
<li>${nullPress}/${d.n_cities} Städte ohne Presse-Signal (Brave-API-Quote / Query-Match).</li>
</ul>`
```
