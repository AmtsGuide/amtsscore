---
title: "Leuchttürme: Dienst-Highlights deutscher Verwaltung"
toc: true
---

# Leuchttürme

Während die meisten Stadt-Websites stagnieren, gibt es **einzelne Dienststarts**, die zeigen wie es geht. Eine Stadt mit Gesamtwert 3.2 kann einen einzelnen Dienst mit 9.5 betreiben. Diese **Leuchttürme** sind der einzige praktische Beweis, dass digitale Verwaltung in Deutschland funktioniert, und das wichtigste Lernmaterial für alle anderen.

AmtsScore kuratiert Dienststarts, die bemerkenswert sind: vollständig digital, gut gestaltet, KI-bereit und von Bürger:innen tatsächlich nutzbar.

## Methodik

Jeder Leuchtturm wird nach der **AmtsScore-12-Dimensionen-Methodik** ([siehe Methodik](/methodik)) bewertet, aber **angewendet auf einen einzelnen Dienst**, nicht die ganze Stadt. So entsteht eine zweite Leseebene:

- **Stadt-AmtsScore** = Durchschnitt aller Dienste der Stadt → strukturelle Leistung
- **Dienst-AmtsScore** = einzelner Dienst → was ist konkret gelungen

Ein Dienst-Leuchtturm braucht **Wert ≥ 7.5** in den Grundlagen-Dimensionen (D1-D10) **plus** mindestens 4 von 10 in den Zukunfts-Dimensionen (D11-D12).

## Auswahlkriterien

Ein Dienststart wird als Leuchtturm aufgenommen, wenn:

1. **Vollständig digital**. kein Medienbruch zur Behörde, Antrag bis Bescheid online
2. **Authentifizierung**. eID, BundID oder vergleichbar
3. **Strukturierte Daten**. Schema.org GovernmentService korrekt markiert
4. **Mobil-optimiert**. Lighthouse-Mobilwert ≥ 70
5. **Auffindbarkeit**. Top-3 bei Google/Bing für die typische Bürger-Anfrage
6. **Stabile Permalinks**. keine Sitzungs-IDs, keine Hash-Routen
7. **Pressereife**. die Stadt selbst kommuniziert den Start
8. **Reproduzierbar**. andere Städte könnten den Ansatz übernehmen

Mindestens 6 der 8 Kriterien müssen erfüllt sein.

## Aktuelle Leuchttürme

```js
const specials = await FileAttachment("../../data/specials.json").json();
```

```js
Inputs.table(specials.items, {
  columns: ["service", "stadt", "bundesland", "live_seit", "service_score", "highlight"],
  header: {
    service: "Dienst",
    stadt: "Stadt",
    bundesland: "Bundesland",
    live_seit: "Verfügbar seit",
    service_score: "Dienstwert",
    highlight: "Was zählt"
  },
  sort: "service_score",
  reverse: true,
  rows: 50
})
```

## Detailseiten

```js
html`<div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(280px, 1fr));gap:1rem;margin:1rem 0">
${specials.items.map(s => html`
  <div class="stat-card" style="padding:1.25rem;border-radius:8px">
    <div class="stat-label" style="font-size:0.85rem;margin-bottom:0.25rem">${s.stadt} • ${s.bundesland}</div>
    <div style="font-weight:600;margin-bottom:0.5rem">${s.service}</div>
    <div class="stat-label" style="font-size:0.9rem;margin-bottom:0.75rem">${s.highlight}</div>
    <div><a href="/specials/${s.slug}" style="font-weight:600">Detail →</a></div>
  </div>
`)}
</div>`
```

## Aufnahme vorschlagen

Sie kennen einen Dienststart der hier fehlt? Per Änderungsvorschlag auf [GitHub](https://github.com/AmtsGuide/amtsscore) oder per Mail an `ad@blinktank.de` mit:

- URL des Dienstes
- Stadt + Bundesland
- Wann live gegangen
- Was den Dienst besonders macht

Wir prüfen + bewerten nach den 8 Kriterien.
