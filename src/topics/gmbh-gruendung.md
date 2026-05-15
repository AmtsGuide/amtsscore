---
title: "GmbH-Gründung: Topic-Daten + Pre-AmtsScore"
toc: true
---

# GmbH-Gründung (Mustervertrag, 1 Gesellschafter)

Pre-AmtsScore pro Stadt:
**40% Kosten** (Gewerbeamt + Notar + HR-Eintrag, ohne Stammkapital)
+ **40% Geschwindigkeit** (Bearbeitungszeit)
+ **20% Online-Verfügbarkeit**, linear normalisiert.

```js
const prescore = (await FileAttachment("../data/prescore.json").json())
  .topics.find(t => t.slug === "gmbh-gruendung");
```

## Pro Stadt

```js
Inputs.table(prescore.cities.map(c => ({
  Rang: c.rank,
  Stadt: c.city,
  Score: c.score,
  "Tage": c.raw.speed_days,
  "Kosten ab": c.raw.cost_eur,
  "Online": c.raw.online_available,
})), {
  rows: 50,
  format: {
    Score: (x) => x === null ? "—" : x.toFixed(1),
    "Tage": (x) => x === null ? "—" : `${x} d`,
    "Kosten ab": (x) => x === null ? "—" : `${x.toFixed(0)} €`,
    "Online": (x) => x ? "ja" : "nein",
  }
})
```

## Kosten-Verteilung

```js
const withCost = prescore.cities.filter(c => c.raw.cost_eur != null)
  .sort((a,b) => a.raw.cost_eur - b.raw.cost_eur);
```

```js
Plot.plot({
  marginLeft: 140,
  width: 800,
  height: 30 + withCost.length * 20,
  x: {label: "Mindest-Gründungskosten (€)", grid: true},
  y: {label: null},
  marks: [
    Plot.barX(withCost, {
      x: d => d.raw.cost_eur,
      y: "city",
      sort: {y: "x"},
      fill: "#1a3da5"
    }),
    Plot.text(withCost, {
      x: d => d.raw.cost_eur,
      y: "city",
      text: d => `${d.raw.cost_eur.toFixed(0)} €`,
      dx: 5,
      textAnchor: "start",
      fontSize: 11
    })
  ]
})
```

## Methodik

Daten aus der [AmtsGuide Facts API](https://amtsguide.de/api/v1/calculator/gmbh/results),
Variante `gesellschaftsvertrag=muster`, 1 Gesellschafter.

Kosten = Gewerbeamt + Notar (min) + Handelsregister-Eintrag. Stammkapital
(25.000 € gesetzlich) und jährliche IHK-Beiträge sind ausgeschlossen.

Pre-Wertung misst Bürger-Outcome, nicht die digitale Performance der
Verwaltungs-Website.
