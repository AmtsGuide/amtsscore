# AmtsScore Methodik v0

**Stand:** 2026-05-15 (v0.1 draft)
**Status:** Pre-launch — Diskussion + Feedback erbeten vor v1 (Q1/2026-Release).

## Zweck dieses Dokuments

Transparente, nachprüfbare Methodik der AmtsScore-Messung. Wer kritisiert, kritisiert konkrete Kriterien und Gewichte — nicht eine Meinung. Diese Offenheit ist die zentrale Verteidigung des Indexes (vgl. Stiftung Warentest, Schufa, Google Lighthouse).

## Grundprinzipien

1. **Nur öffentlich messbare Daten.** Keine Umfragen, keine Selbstauskünfte, keine vertraulichen Quellen. Alle Daten lassen sich von jedem Dritten reproduzieren.
2. **Bürger-Perspektive.** Was zählt, ist was eine Bürgerin auf der Website tatsächlich erreichen kann — nicht was die IT-Abteilung intern verwendet.
3. **Multi-dimensional.** Der AmtsScore ist eine gewichtete Summe von 10 Sub-Scores. Eine Stadt mit perfektem Score in 9 Dimensionen und 0 in einer hat keinen perfekten AmtsScore.
4. **Reproduzierbar.** Methodik + Daten + Code (später) sind öffentlich. Jeder Score lässt sich rückgängig nachvollziehen.
5. **Kontinuierlich.** Quartalsweise Messung. Veränderung ist sichtbar.

## Messgegenstand

**Phase v0 (jetzt):** 20 deutsche Großstädte (>200.000 Einwohner). Eine Domain pro Stadt: die offizielle `stadt-X.de` oder vergleichbare Hauptdomain der Stadtverwaltung.

**Phase v1 (Q2/2026):** 50 Städte.
**Phase v2 (Q4/2026):** 100 Städte.
**Phase v3 (Q1/2027):** 401 Bürgerämter Deutschland-weit.

## Die 10 Dimensionen

| # | Dimension | Was wird gemessen | Werkzeug | Max-Score |
|---|---|---|---|---|
| 1 | **Online-Termin-Buchung** | Existiert eine Online-Buchung? Welcher Anteil der Dienstleistungen ist online buchbar? | Pattern-Detection (TerminVer / SAGA / Maerker etc.) + Sitemap-Scan | 0–10 |
| 2 | **Anzahl Online-Dienstleistungen** | Wie viele Verwaltungsleistungen sind komplett online erledigbar (OZG-Kategorie 4)? | Sitemap + Page-Pattern (FIM/LeiKa) | 0–10 |
| 3 | **Mobile / Lighthouse Performance** | Page-Speed + Mobile-Optimierung auf der Startseite + drei Dienstleistungs-Seiten | Lighthouse (Performance-Score) | 0–10 |
| 4 | **Barrierefreiheit (BITV/WCAG)** | Automatische Prüfung gegen BITV 2.0 / WCAG 2.1 AA | axe-core | 0–10 |
| 5 | **Open-Data-Portal** | Eigenes Open-Data-Portal verfügbar? Anzahl Datasets? Aktualität? | URL-Probe (`/opendata`, `opendata.{stadt}.de`) + GovData-Lookup | 0–10 |
| 6 | **Strukturierte Daten** | Schema.org-Markup auf Dienstleistungs-Seiten (GovernmentService, GovernmentOrganization) | JSON-LD-Parse | 0–10 |
| 7 | **Mehrsprachigkeit** | Verfügbare Sprachen? Englisch? Türkisch? Arabisch? Ukrainisch? | `lang`-Attribute + Sprachwechsel-Detection | 0–10 |
| 8 | **Datenschutz + Sicherheit** | HTTPS überall? Security-Headers? Cookie-Banner DSGVO-konform? Tracker-Anzahl? | HTTP-Header-Scan + Cookie-Audit + Initial-Network-Capture | 0–10 |
| 9 | **Auffindbarkeit / SEO** | Wird die Stadt-Website bei typischen Bürger-Anfragen gefunden? Strukturierte Sitemap? Robots? | Sitemap-Validität + Bing/Google-SERP-Position für Top-10-Anliegen | 0–10 |
| 10 | **Aktualität** | Wann wurden Inhalte zuletzt aktualisiert? Tote Links? | Last-Modified-Header + Linkchecker | 0–10 |

## Gewichtung v0

Alle Dimensionen mit Gleichgewicht (10 × 10%) für v0. Vorteil: keine implizite Wertung, einfach erklärbar.

**Geplante Anpassung in v1:** Gewichtung nach Bürger-Relevanz (Dimensionen 1, 2, 4, 8 bekommen höhere Gewichte). Anpassung wird transparent dokumentiert + es wird historisch beide Versionen (v0-Gleichgewicht + v1-relevanzgewichtet) publiziert, sodass keine Stadt "über Nacht abstürzt" durch Methodik-Änderung.

## Composite-Berechnung

```
AmtsScore = sum(w_i * sub_score_i) for i in 1..10
```

Mit `w_i = 0.1` in v0 (Gleichgewicht).

Ergebnis: 0.0 (komplett analog) bis 10.0 (Spitzenklasse).

## Tier-Einteilung (für Award-Phase ab Year 2)

| AmtsScore-Bereich | Tier | Zertifikat-Anrecht |
|---|---|---|
| 9.0–10.0 | **AmtsScore Gold** | Ja |
| 7.5–8.9 | **AmtsScore Silber** | Ja |
| 6.0–7.4 | **AmtsScore Bronze** | Ja |
| 4.0–5.9 | Standard | Nein |
| 0–3.9 | Nachholbedarf | Nein |

## Was bewusst NICHT gemessen wird (v0)

- **Interne IT-Modernität** (z.B. Cloud-Migration, eAkte) — nicht von außen messbar
- **Mitarbeiter-Zufriedenheit** — gehört zu Umfragen, nicht zu Web-Messung
- **Politische Ausrichtung** — irrelevant für Bürger-Erfahrung
- **Telefon-Service / Vor-Ort-Service** — anderes Medium, andere Messung
- **OZG-Compliance-Status laut Selbstauskunft** — Selbstauskünfte sind keine Messung

Diese Punkte können in späteren Phasen (v3+) als separate Indizes folgen, aber AmtsScore v0 ist bewusst **rein Web-Performance**.

## Fehlerquellen + Grenzen

Klar zu kommunizieren in jeder Veröffentlichung:

- Stichtag der Messung pro Stadt — manche Verbesserung kann zwischen Messung und Publikation entstehen
- Lighthouse-Score variabel ±5% — wir messen 3× und nehmen den Median
- axe-core erkennt ~30% aller BITV/WCAG-Verstöße — der Score ist eine Untergrenze, kein Vollaudit
- Cookie-Banner-Bewertung ist regelbasiert — komplexe DSGVO-Klauseln werden simplifiziert
- Schema.org-Markup ist freiwillig — fehlendes Markup ≠ schlechter Service, aber schlechte Auffindbarkeit für KI-Bots
- 20 Städte = nicht repräsentativ für DE-weite Verwaltungsqualität → in v0 explizit nur Großstadt-Ranking

## Validierung + Peer-Review (vor v1-Release)

Geplante Schritte vor erstem öffentlichen v1-Release:

1. **Hochschul-Reviewer:** Hammerschmid (Hertie School) + ein:e BITV-Expert:in der HWR Berlin
2. **Praxis-Reviewer:** 2–3 Stadt-CIOs (Berlin / Hamburg / Köln) prüfen Methodik anonymisiert
3. **Öffentliche Kommentierungsphase:** Methodik-Paper auf amtsscore.de + GitHub, 4 Wochen Kommentare via Pull Request
4. **Datenschutz-Audit:** Kurze Prüfung durch datenschutz-cert ob Messmethodik selbst DSGVO-konform (kein Tracking von Bürger:innen während des Scans)

Erst nach 1–4 wird der erste öffentliche AmtsScore-Index publiziert.

## Versionierung

| Version | Datum | Änderungen |
|---|---|---|
| v0.1 | 2026-05-15 | Initialer Entwurf, 10 Dimensionen, Gleichgewicht. Pre-Review. |

Jede zukünftige Version wird hier dokumentiert mit Diff zur Vorversion. Methodik-Änderungen sind transparent rückwirkend nachvollziehbar.

## Lizenz

Methodik-Paper: **CC BY 4.0** (Namensnennung). Daten: **CC BY 4.0**. Code (später): **MIT**.

Jeder kann die Methodik adaptieren — aber nur AmtsGuide veröffentlicht den offiziellen AmtsScore-Index.
