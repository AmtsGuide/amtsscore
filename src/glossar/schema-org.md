---
title: "Schema.org: Strukturierte Daten für die Verwaltung"
toc: true
---

# Schema.org

**Schema.org** ist ein offener, von Google, Microsoft, Yahoo + Yandex getragener Standard für strukturierte Daten auf Web-Seiten. Wenn eine Stadt-Website ihre Halteverbots-Antrags-Seite mit Schema.org markiert, können Suchmaschinen und KI-Assistenten (ChatGPT, Perplexity, Google AI) sie eindeutig erkennen.

## Wie es technisch aussieht

JSON-LD-Block im HTML-Head:

```json
{
  "@context": "https://schema.org",
  "@type": "GovernmentService",
  "name": "Halteverbotszone beantragen",
  "provider": {
    "@type": "GovernmentOrganization",
    "name": "Bürgeramt Mitte, Berlin",
    "address": "..."
  },
  "areaServed": "Berlin Mitte",
  "audience": {"@type": "Audience", "audienceType": "Bürger:innen"},
  "estimatedCost": {"@type": "MonetaryAmount", "value": "21", "currency": "EUR"},
  "termsOfService": "https://...",
  "url": "https://service.berlin.de/dienstleistung/325649/"
}
```

## Relevante Schema.org-Typen für Verwaltung

| Typ | Was beschreibt es |
|---|---|
| **GovernmentService** | Eine Verwaltungsdienstleistung |
| **GovernmentOrganization** | Die Behörde |
| **GovernmentBuilding** | Physisches Bürgeramt-Gebäude |
| **OpeningHoursSpecification** | Öffnungszeiten |
| **Service** (generisch) | Wenn GovernmentService zu eng |
| **FAQPage** | Häufige Bürger-Fragen |
| **ContactPoint** | Telefon, E-Mail, Adresse |

## Warum es zählt

- **Google Rich Results**: bessere Darstellung in der Google-Suche (Termin direkt im SERP-Card)
- **KI-Assistenten**. ChatGPT, Perplexity, Google AI können Stadt-Info zuverlässig zitieren
- **Voice-Assistenten**. "Alexa, wie viel kostet ein Halteverbot in Berlin?"
- **Bundesportal-Integration**: strukturierte Daten lassen sich automatisch aggregieren

## Realität

Die meisten Stadt-Websites haben **kein** Schema.org-Markup. Wenn überhaupt, dann oberflächlich (`@type: WebSite`) und nicht auf den eigentlichen Dienstleistungs-Seiten.

## In AmtsScore-Methodik (Dimension 6)

AmtsScore prüft pro Stadt:

- **JSON-LD vorhanden**. Boolean
- **Schema-Typen gefunden**. Welche der relevanten Typen sind im Einsatz?
- **Anzahl Seiten mit Schema**. Tiefe der Markierung

## Quellen

- [schema.org/GovernmentService](https://schema.org/GovernmentService). Typdefinition
- [Google Rich Results Test](https://search.google.com/test/rich-results). Validierung
- [Schema.org Vollindex](https://schema.org/docs/full.html), alle Typen
