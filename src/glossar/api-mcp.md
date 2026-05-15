---
title: "API + MCP: Maschinen-Schnittstellen für Behörden"
toc: true
---

# API + MCP: Maschinen-Schnittstellen

Eine Stadt-Website mit reiner HTML-Oberfläche ist nur für Menschen verständlich. Eine moderne Verwaltung bietet zusätzlich **maschinenlesbare Schnittstellen**. APIs (REST, GraphQL) und langfristig **MCP-Endpunkte** (Model Context Protocol).

## REST-/GraphQL-APIs für Bürger-Services

Ein Beispiel, wie eine Stadt-API aussehen *könnte*:

```http
GET /api/v1/dienstleistungen?stadt=berlin&thema=halteverbot
```

```json
{
  "dienstleistungen": [{
    "leika_id": "99064001000000",
    "name": "Halteverbotszone beantragen",
    "kosten_min_eur": 21,
    "bearbeitung_werktage": 14,
    "online_buchbar": true,
    "termin_endpoint": "https://service.berlin.de/termin/...",
    "schema_org": {"@type": "GovernmentService", "...": "..."}
  }]
}
```

**Was das ermöglicht:**

- Aggregator-Apps (wie AmtsGuide) können Bürger:innen direkt zur richtigen Stadt-Leistung lotsen
- KI-Agenten können Halteverbote im Auftrag von Bürgern beantragen
- Drittanbieter (Anwälte, Beratungen) können integrierte Tools bauen
- Datenjournalismus kann fundierte Vergleiche ziehen

## OpenAPI / Swagger-Dokumentation

Eine API ohne Dokumentation ist eine Black-Box. **OpenAPI 3.x** (früher Swagger) ist der Standard:

- Maschinenlesbare API-Beschreibung
- Auto-generierte Client-SDKs in jeder Sprache
- Interaktive Dokumentations-UI (Swagger UI, ReDoc)
- Aufrufbar unter konventionellem Pfad wie `/openapi.json`, `/api/docs`, `/.well-known/openapi`

## MCP: Model Context Protocol

**MCP** ist der **2024 von Anthropic veröffentlichte Standard** für die Kommunikation zwischen KI-Modellen und externen Diensten. Statt jede KI mit jedem Service einzeln zu integrieren, bietet ein Service einen **MCP-Server** an, und JEDE MCP-kompatible KI (Claude, ChatGPT, etc.) kann ihn nutzen.

**Eine Stadt mit MCP-Server würde z.B. anbieten:**

| MCP-Tool | Was es kann |
|---|---|
| `list_services(thema)` | Alle Dienstleistungen zum Thema |
| `get_service_details(leika_id)` | Kosten, Bearbeitungszeit, Voraussetzungen |
| `book_termin(leika_id, datum)` | Termin reservieren (mit eID-Authentifizierung) |
| `check_status(antrag_id)` | Bearbeitungsstand abrufen |

Bürger:in fragt ChatGPT: *"Buch mir einen Termin für Personalausweis in Berlin nächste Woche"*. ChatGPT redet über MCP mit dem Berlin-Server, sucht freie Slots, bucht.

**Stand 2026:** keine deutsche Behörde betreibt einen produktiven MCP-Server. Aber das wird sich ändern.

## Bestehende, schwache Vorbilder

Es gibt heute schon Ansätze:

- **govdata.de API**. Open-Data-Discovery, aber keine transaktionalen Operationen
- **Bundesportal API** (in Entwicklung), soll OZG-Leistungen aggregieren
- **Berlin Open API** (in Pilotphase), manche Dienste experimentell verfügbar
- **München OpenAPI** für Verkehr / Wetter, nicht für Verwaltungs-Transaktionen

## In AmtsScore-Methodik (Dimension 12)

D12 misst pro Stadt:

| Kriterium | Punkte |
|---|---|
| Öffentliche REST-API für Service-Discovery | 3 |
| OpenAPI-Dokumentation auffindbar | 2 |
| Transaktionale Endpunkte (Termin buchen, etc.) | 3 |
| MCP-Server-Endpunkt unter `/.well-known/mcp` | 2 |

Max: 10. Realistischer v0-Score für deutsche Städte: **0-2**.

Die ersten Städte, die transaktionale APIs anbieten, werden in der KI-Ära den massiven Vorsprung haben. AmtsScore macht diese Lücke heute schon sichtbar.

## Verwandte Begriffe

- [Maschinen-Lesbarkeit + KI-Bereitschaft](/glossar/ai-readiness), der breitere Kontext
- [llms.txt](/glossar/llms-txt), die Karte für KI-Crawler
- [Schema.org](/glossar/schema-org), strukturierte Daten

## Quellen

- [Model Context Protocol Specification (Anthropic, 2024)](https://modelcontextprotocol.io/)
- [OpenAPI 3.x Spec](https://swagger.io/specification/), der API-Beschreibungs-Standard
- [GovTech Best Practices: Public API Design](https://www.gov.uk/service-manual/design/design-an-api)
