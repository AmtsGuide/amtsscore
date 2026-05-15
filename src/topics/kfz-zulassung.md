---
title: "KFZ-Zulassung: Topic-Daten + Pre-AmtsScore"
toc: true
---

# KFZ-Zulassung (Neuzulassung)

Pre-AmtsScore pro Stadt aus AmtsGuide-Daten:
**40% Kosten** (Gebühr) + **40% Geschwindigkeit** (Wartezeit)
+ **20% Online-Verfügbarkeit** (i-Kfz), linear normalisiert.

```js
const prescore = (await FileAttachment("../../data/prescore.json").json())
  .topics.find(t => t.slug === "kfz-zulassung");
```

## Pro Stadt

```js
Inputs.table(prescore.cities.map(c => ({
  Rang: c.rank,
  Stadt: c.city,
  Score: c.score,
  "Tage Wartezeit": c.raw.speed_days,
  "Gebühr": c.raw.cost_eur,
  "i-Kfz": c.raw.online_available,
})), {
  rows: 30,
  format: {
    Score: (x) => x === null ? "—" : x.toFixed(1),
    "Tage Wartezeit": (x) => x === null ? "—" : `${x} d`,
    "Gebühr": (x) => x === null ? "—" : `${x.toFixed(2)} €`,
    "i-Kfz": (x) => x ? "ja" : "nein",
  }
})
```

## Verteilung Wartezeit

```js
const withWait = prescore.cities.filter(c => c.raw.speed_days != null)
  .sort((a,b) => b.raw.speed_days - a.raw.speed_days);
```

```js
Plot.plot({
  marginLeft: 140,
  width: 800,
  height: 30 + withWait.length * 22,
  x: {label: "Wartezeit (Tage)", grid: true},
  y: {label: null},
  marks: [
    Plot.barX(withWait, {
      x: d => d.raw.speed_days,
      y: "city",
      sort: {y: "x", reverse: true},
      fill: "#1a3da5"
    }),
    Plot.text(withWait, {
      x: d => d.raw.speed_days,
      y: "city",
      text: d => `${d.raw.speed_days} d`,
      dx: 5,
      textAnchor: "start",
      fontSize: 11
    })
  ]
})
```

## Methodik

Daten aus der [AmtsGuide Facts API](https://amtsguide.de/api/v1/calculator/kfz/results),
Vorgang `neuzulassung`. Wartezeit-Strings ("mehrere Wochen bis zu 10 Wochen")
werden heuristisch in Tage übersetzt, vgl.
`tools/prescore/derive.py::parse_days`.

Diese Pre-Wertung misst Bürger-Outcome (was kostet es, wie lange dauert es).
Sie ersetzt nicht die AmtsScore-Website-Bewertung der zuständigen Behörde,
ergänzt sie aber.
