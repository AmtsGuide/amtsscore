---
title: "Leuchttürme: Service-Highlights deutscher Verwaltung"
toc: true
---

# Leuchttürme

Während die meisten Stadt-Websites stagnieren, gibt es **einzelne Service-Launches**, die zeigen wie es geht. Eine Stadt mit Gesamt-Score 3.2 kann einen einzelnen Service mit 9.5 betreiben. Diese **Leuchttürme** sind der einzige praktische Beweis, dass digitale Verwaltung in Deutschland funktioniert, und das wichtigste Lernmaterial für alle anderen.

AmtsScore kuratiert Service-Launches, die bemerkenswert sind: end-to-end-digital, gut gestaltet, KI-bereit, von Bürger:innen tatsächlich nutzbar.

## Methodik

Jeder Leuchtturm wird nach der **AmtsScore-12-Dimensionen-Methodik** ([siehe Methodik](/methodik)) bewertet, aber **angewendet auf einen einzelnen Service**, nicht die ganze Stadt. So entsteht ein zweiter Lese-Layer:

- **Stadt-AmtsScore** = Durchschnitt aller Dienste der Stadt → strukturelle Performance
- **Service-AmtsScore** = einzelner Dienst → was ist konkret gelungen

Ein Service-Leuchtturm braucht **Score ≥ 7.5** in den Grundlagen-Dimensionen (D1-D10) **plus** mindestens 4 von 10 in den Zukunfts-Dimensionen (D11-D12).

## Auswahlkriterien

Ein Service-Launch wird als Leuchtturm aufgenommen, wenn:

1. **End-to-end digital**. kein Medienbruch zur Behörde, Antrag bis Bescheid online
2. **Authentifizierung**. eID, BundID oder vergleichbar
3. **Strukturierte Daten**. Schema.org GovernmentService korrekt markiert
4. **Mobile-optimiert**. Lighthouse Mobile-Score ≥ 70
5. **Auffindbarkeit**. Top-3 bei Google/Bing für die typische Bürger-Anfrage
6. **Stabile Permalinks**. keine Session-IDs, keine Hash-Routes
7. **Pressereife**. die Stadt selbst kommuniziert den Launch
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
    service: "Service",
    stadt: "Stadt",
    bundesland: "Bundesland",
    live_seit: "Live seit",
    service_score: "Service-Score",
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

Sie kennen einen Service-Launch der hier fehlt? Per Pull Request auf [GitHub](https://github.com/AmtsGuide/amtsscore) oder per Mail an `ad@blinktank.de` mit:

- URL des Services
- Stadt + Bundesland
- Wann live gegangen
- Was den Service besonders macht

Wir prüfen + bewerten nach den 8 Kriterien.
