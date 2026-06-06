# AmtsScore-Methodik v0

**Stand:** 2026-05-15 (Entwurf v0.1). Diskussion und Feedback vor v1 sind ausdrücklich erwünscht.

## Zweck dieses Dokuments

Transparente, nachprüfbare Methodik der AmtsScore-Messung. Wer kritisiert, kritisiert konkrete Kriterien und Gewichte, nicht eine Meinung. Diese Offenheit ist die zentrale Verteidigung des Indexes (vgl. Stiftung Warentest, Schufa, Google Lighthouse).

## Grundprinzipien

1. **Nur öffentlich messbare Daten.** Keine Umfragen, keine Selbstauskünfte, keine vertraulichen Quellen. Alle Daten lassen sich von jedem Dritten reproduzieren.
2. **Bürger-Perspektive.** Was zählt, ist was eine Bürgerin auf der Website tatsächlich erreichen kann, nicht was die IT-Abteilung intern verwendet.
3. **Mehrdimensional.** Der AmtsScore ist eine gewichtete Summe aus 10 Teilwerten. Eine Stadt mit perfektem Wert in 9 Dimensionen und 0 in einer hat keinen perfekten AmtsScore.
4. **Reproduzierbar.** Methodik + Daten + Code (später) sind öffentlich. Jeder Wert lässt sich rückgängig nachvollziehen.
5. **Kontinuierlich.** Quartalsweise Messung. Veränderung ist sichtbar.

## Messgegenstand

**Phase v0 (jetzt):** 20 deutsche Großstädte (>200.000 Einwohner). Eine Domain pro Stadt: die offizielle `stadt-X.de` oder vergleichbare Hauptdomain der Stadtverwaltung.

**Phase v1 (Q2/2026):** 50 Städte.
**Phase v2 (Q4/2026):** 100 Städte.
**Phase v3 (Q1/2027):** 401 Bürgerämter Deutschland-weit.

## Die 12 Dimensionen

### Grundlagen: Was Bürger:innen heute brauchen (D1-D10)

| # | Dimension | Was wird gemessen | Werkzeug | Max-Wert |
|---|---|---|---|---|
| 1 | **Online-Termin-Buchung** | Existiert eine Online-Buchung? Welcher Anteil der Dienstleistungen ist online buchbar? | Pattern-Detection (TerminVer / SAGA / Maerker etc.) + Sitemap-Scan | 0-10 |
| 2 | **Anzahl Online-Dienstleistungen** | Wie viele Verwaltungsleistungen sind komplett online erledigbar (OZG-Kategorie 4)? | Sitemap + Page-Pattern (FIM/LeiKa) | 0-10 |
| 3 | **Mobil / Lighthouse-Leistung** | Seitengeschwindigkeit und Mobil-Optimierung auf der Startseite plus drei Dienstleistungs-Seiten | Lighthouse-Leistungswert | 0-10 |
| 4 | **Barrierefreiheit (BITV/WCAG)** | Automatische Prüfung gegen BITV 2.0 / WCAG 2.1 AA | axe-core | 0-10 |
| 5 | **Open-Data-Portal** | Eigenes Open-Data-Portal verfügbar? Anzahl Datasets? Aktualität? | URL-Probe (`/opendata`, `opendata.{stadt}.de`) + GovData-Lookup | 0-10 |
| 6 | **Strukturierte Daten** | Schema.org-Markup auf Dienstleistungs-Seiten (GovernmentService, GovernmentOrganization) | JSON-LD-Parse | 0-10 |
| 7 | **Mehrsprachigkeit** | Verfügbare Sprachen? Englisch? Türkisch? Arabisch? Ukrainisch? | `lang`-Attribute + Sprachwechsel-Detection | 0-10 |
| 8 | **Datenschutz + Sicherheit** | HTTPS überall? Security-Headers? Cookie-Banner DSGVO-konform? Tracker-Anzahl? | HTTP-Header-Scan + Cookie-Audit + Initial-Network-Capture | 0-10 |
| 9 | **Auffindbarkeit / SEO** | Wird die Stadt-Website bei typischen Bürger-Anfragen gefunden? Strukturierte Sitemap? Robots? | Sitemap-Validität + Bing/Google-SERP-Position für Top-10-Anliegen | 0-10 |
| 10 | **Aktualität** | Wann wurden Inhalte zuletzt aktualisiert? Tote Links? | Last-Modified-Header + Linkchecker | 0-10 |

### Zukunft: Was Bürger:innen 2026+ brauchen (D11-D12)

Verwaltungs-Websites bedienen nicht mehr nur Menschen. Sie bedienen auch **KI-Assistenten, Apps, Aggregatoren und Software-Agenten**. Eine Stadt-Website, die für ChatGPT, Perplexity oder Claude unsichtbar ist, wird ihre Bürger:innen ab 2027 nicht mehr erreichen. Diese zwei Dimensionen messen die **Maschinen-Lesbarkeit und KI-Bereitschaft**.

| # | Dimension | Was wird gemessen | Werkzeug | Max-Wert |
|---|---|---|---|---|
| 11 | **Maschinen-Lesbarkeit und KI-Bereitschaft** | `llms.txt` vorhanden? Robots.txt erlaubt KI-Bots (GPTBot, ChatGPT-User, PerplexityBot, ClaudeBot, Google-Extended)? Darstellung ohne JavaScript? Stabile Permalinks? | HTTP-Probe und DOM-Test mit deaktiviertem JS | 0-10 |
| 12 | **Maschinen-Schnittstellen (API + MCP)** | Öffentliche API für Dienst-Abfragen (REST/GraphQL)? OpenAPI/Swagger-Dokumentation? MCP-Server-Endpunkt? | URL-Probe für `/api`, `/.well-known/mcp`, OpenAPI-Erkennung | 0-10 |

**Heute werden fast alle Städte D11 + D12 nahe Null haben.** Das ist Absicht. AmtsScore macht sichtbar, was als nächstes kommt, bevor es zu spät ist.

Siehe Glossar: [Maschinen-Lesbarkeit und KI-Bereitschaft](/glossar/ai-readiness).

## Gewichtung v0

Alle Dimensionen mit Gleichgewicht (12 × 1/12 ≈ 8,33%) für v0. Vorteil: keine implizite Wertung, einfach erklärbar.

**Geplante Anpassung in v1:** Gewichtung nach Bürger-Relevanz. Die Grundlagen-Dimensionen (D1, D2, D4, D8) bekommen höhere Gewichte, weil sie Bürger:innen unmittelbar betreffen. Die Zukunfts-Dimensionen (D11, D12) behalten in v1 noch volles Gewicht, wir wollen den Anpassungsdruck nicht senken. Anpassung wird transparent dokumentiert; v0-Gleichgewicht und v1-relevanzgewichtet werden parallel publiziert, sodass keine Stadt "über Nacht abstürzt" durch Methodik-Änderung.

## Gesamtwert-Berechnung

```text
AmtsScore = Summe aus Gewicht je Dimension mal Teilwert je Dimension
```

Mit `w_i = 1/12 ≈ 0.0833` in v0 (Gleichgewicht).

Ergebnis: 0.0 (komplett analog) bis 10.0 (Spitzenklasse).

## Klassen-Einteilung (für Auszeichnungsphase ab Jahr 2)

| AmtsScore-Bereich | Klasse | Zertifikat-Anrecht |
|---|---|---|
| 9.0-10.0 | **AmtsScore Gold** | Ja |
| 7.5-8.9 | **AmtsScore Silber** | Ja |
| 6.0-7.4 | **AmtsScore Bronze** | Ja |
| 4.0-5.9 | Standard | Nein |
| 0-3.9 | Nachholbedarf | Nein |

## Was bewusst NICHT gemessen wird (v0)

- **Interne IT-Modernität** (z.B. Cloud-Migration, eAkte), nicht von außen messbar
- **Mitarbeiter-Zufriedenheit**: gehört zu Umfragen, nicht zu Web-Messung
- **Politische Ausrichtung**: irrelevant für Bürger-Erfahrung
- **Telefon-Dienst / Vor-Ort-Dienst**: anderes Medium, andere Messung
- **OZG-Einhaltung-Stand laut Selbstauskunft**. Selbstauskünfte sind keine Messung

Diese Punkte können in späteren Phasen (v3+) als separate Indizes folgen, aber AmtsScore v0 ist bewusst **rein Webleistung**.

## Fehlerquellen + Grenzen

Klar zu kommunizieren in jeder Veröffentlichung:

- Stichtag der Messung pro Stadt, manche Verbesserung kann zwischen Messung und Publikation entstehen
- Lighthouse-Wert variabel ±5%. Wir messen 3× und nehmen den Median
- axe-core erkennt ~30% aller BITV/WCAG-Verstöße, der Wert ist eine Untergrenze, kein Vollaudit
- Cookie-Banner-Bewertung ist regelbasiert, komplexe DSGVO-Klauseln werden simplifiziert
- Schema.org-Markup ist freiwillig, fehlendes Markup ≠ schlechter Dienst, aber schlechte Auffindbarkeit für KI-Bots
- 20 Städte = nicht repräsentativ für DE-weite Verwaltungsqualität → in v0 explizit nur Großstadt-Ranking

## Validierung + Fachprüfung (vor v1-Veröffentlichung)

Geplante Schritte vor der ersten öffentlichen v1-Veröffentlichung:

1. **Hochschul-Prüfende:** Hammerschmid (Hertie School) + ein:e BITV-Expert:in der HWR Berlin
2. **Praxis-Prüfende:** 2-3 Stadt-CIOs (Berlin / Hamburg / Köln) prüfen Methodik anonymisiert
3. **Öffentliche Kommentierungsphase:** Methodik-Papier auf amtsscore.de und GitHub, 4 Wochen Kommentare über Änderungsvorschläge
4. **Datenschutz-Audit:** Kurze Prüfung durch datenschutz-cert ob Messmethodik selbst DSGVO-konform (kein Tracking von Bürger:innen während des Scans)

Erst nach 1-4 wird der erste öffentliche AmtsScore-Index publiziert.

## Versionierung

| Version | Datum | Änderungen |
|---|---|---|
| v0.1 | 2026-05-15 | Erster Entwurf, 10 Dimensionen, Gleichgewicht. Vorprüfung. |

Jede zukünftige Version wird hier dokumentiert mit Vergleich zur Vorversion. Methodik-Änderungen sind transparent rückwirkend nachvollziehbar.

## Lizenz

Methodik-Papier: **CC BY 4.0** (Namensnennung). Daten: **CC BY 4.0**. Code (später): **MIT**.

Jeder kann die Methodik adaptieren, aber nur AmtsGuide veröffentlicht den offiziellen AmtsScore-Index.
