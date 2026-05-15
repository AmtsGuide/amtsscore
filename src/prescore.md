---
title: "Pre-AmtsScore: Bürger-Outcome aus AmtsGuide-Daten"
toc: true
---

# Pre-AmtsScore (Vorab-Wertung)

```js
const data = await FileAttachment("./data/prescore.json").json();
```

**Stand:** ${data.generated_at.slice(0,10)}.
**Quelle:** ${data.source}.
**Stadt-Coverage:** ${data.topics.reduce((a,t)=>a+t.n_cities,0)} Datenpunkte über ${data.topics.length} Topics, ${data.city_summary.length} eindeutige Städte.

Die hier gezeigten Punkte sind **Pre-AmtsScore**, nicht der volle AmtsScore.
Sie kommen aus dem **Bürger-Outcome** den AmtsGuide bereits misst:

- **40% Kosten** (Gebühr, Mindestkosten)
- **40% Geschwindigkeit** (Bearbeitungstage, Wartezeit)
- **20% Online-Verfügbarkeit** (i-Kfz, GmbH-Online, etc.)

Linear normalisiert pro Topic. Beste Stadt im Topic = 10, schlechteste = 0.
Fehlende Metriken werden nicht negativ gewertet, sondern aus dem Nenner entfernt.

Der volle AmtsScore (12 Digital-Performance-Dimensionen pro Website) wird
separat gemessen und ergänzt diese Sicht.

## Stadt-Ranking (Durchschnitt über alle Topics)

```js
const summaryFull = data.city_summary.map(r => ({
  Rang: r.rank,
  Stadt: r.city,
  "⌀ Score": r.avg_score,
  Topics: r.topic_count,
}));
```

```js
Inputs.table(summaryFull, {
  rows: 60,
  format: {
    "⌀ Score": (x) => x.toFixed(1),
  },
})
```

Städte mit weniger Topics (`Topics` < 3) sind weniger vergleichbar. der
Durchschnitt basiert auf einer kleineren Stichprobe.

## Pro Topic

```js
const topicChoice = view(Inputs.select(
  data.topics.map(t => t.slug),
  {label: "Topic", format: (s) => data.topics.find(t => t.slug === s).label}
))
```

```js
const topic = data.topics.find(t => t.slug === topicChoice);
```

```js
html`<h3 style="margin-top:1rem">${topic.label} (${topic.n_cities} Städte)</h3>`
```

```js
Inputs.table(topic.cities.map(c => ({
  Rang: c.rank,
  Stadt: c.city,
  Score: c.score,
  Geschwindigkeit: c.speed,
  Kosten: c.cost,
  Online: c.online,
  "Tage (roh)": c.raw.speed_days,
  "Euro (roh)": c.raw.cost_eur,
})), {
  rows: 50,
  format: {
    Score: (x) => x === null ? "—" : x.toFixed(1),
    Geschwindigkeit: (x) => x === null ? "—" : x.toFixed(1),
    Kosten: (x) => x === null ? "—" : x.toFixed(1),
    Online: (x) => x === null ? "—" : x === 10 ? "ja" : "nein",
    "Tage (roh)": (x) => x === null ? "—" : `${x} d`,
    "Euro (roh)": (x) => x === null ? "—" : `${x.toFixed(0)} €`,
  }
})
```

## Was die Daten zeigen

```js
const allCovered = data.city_summary.filter(c => c.topic_count === data.topics.length);
const best = allCovered[0];
const worst = allCovered[allCovered.length - 1];
```

```js
html`
<p><strong>Beste Stadt mit voller Coverage (${data.topics.length} Topics):</strong>
${best.city} — ⌀ ${best.avg_score.toFixed(1)} / 10.</p>
<p><strong>Schwächste Stadt mit voller Coverage:</strong>
${worst.city} — ⌀ ${worst.avg_score.toFixed(1)} / 10.</p>
<p><strong>Spannweite:</strong> ${(best.avg_score - worst.avg_score).toFixed(1)} Punkte
zwischen erster und letzter Stadt im voll-gemessenen Set.</p>
`
```

## Methodik-Kritik (eigene Liste)

Diese Pre-AmtsScore-Vorab-Wertung hat bekannte Schwächen, die der volle
AmtsScore adressieren soll:

- Sie misst **Bürger-Outcome**, nicht **Verwaltungs-Website-Performance**.
  Eine günstige + schnelle KFZ-Zulassung kann mit einer schlechten Website
  einhergehen.
- **Daten-Lücken werden ignoriert**, nicht negativ bewertet. Eine Stadt ohne
  Halteverbots-Daten wird im Topic-Ranking nicht abgewertet.
- **Wartezeit-Strings** werden heuristisch in Tage übersetzt ("mehrere
  Wochen bis zu 10 Wochen" → Mittelwert × 7). Robuste Werte brauchen
  direkte Messung.
- **Aliasing** zwischen Slugs ist manuell gepflegt (`frankfurt` ↔
  `frankfurt-am-main`). Bei neuen Topics möglicherweise nötig nachzupflegen.
- **Topic-Auswahl** ist heute drei. Halteverbot, KFZ-Zulassung, GmbH-Gründung.
  Weitere Topics werden eingespielt, sobald die AmtsGuide-Daten reichen.

## Reproduktion

Code in `tools/prescore/derive.py` im
[öffentlichen Repo](https://github.com/AmtsGuide/amtsscore/tree/main/tools/prescore).
Quelle ist die AmtsGuide Facts API `https://amtsguide.de/api/v1/`.
