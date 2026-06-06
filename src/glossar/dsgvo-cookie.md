---
title: "DSGVO + Cookies: Datenschutz auf Behörden-Websites"
toc: true
---

# DSGVO + Cookie-Banner

Verwaltungs-Websites müssen die **EU-Datenschutz-Grundverordnung (DSGVO)** einhalten, strenger als kommerzielle Sites, weil Bürger:innen oft keine Wahl haben, ob sie die Behörde nutzen.

## Kernpflichten

| Pflicht | Was das bedeutet |
|---|---|
| **Datenminimierung** | Nur Daten erheben, die wirklich gebraucht werden |
| **Zweckbindung** | Daten dürfen nur für den deklarierten Zweck verwendet werden |
| **Transparenz** | Datenschutzerklärung muss zugänglich + verständlich sein |
| **Einwilligung** | Vor jedem Tracking explizite, informierte Zustimmung |
| **Recht auf Auskunft + Löschung** | Bürger können ihre Daten einsehen und löschen lassen |

## Cookie-Banner-Standards (TTDSG + DSGVO)

Seit dem Telekommunikation-Telemedien-Datenschutz-Gesetz (**TTDSG**, 2021) ist klar:

- **Nicht-essenzielle Cookies** brauchen explizite Einwilligung VOR dem Setzen
- "Weiter surfen = Zustimmung" ist illegal
- "Alle akzeptieren" und "Alle ablehnen" müssen **gleichwertig** prominent sein
- Pre-checked Boxen sind illegal
- Cookie-Wand (Dark Pattern: man muss zustimmen, um die Seite zu sehen) ist umstritten

## Wichtige Abgrenzung: Verwaltungsprozesse sind nicht DSGVO-relevant

Die DSGVO schützt **personenbezogene Daten der Bürger:innen**. Namen, Adressen, Geburtsdaten, Anliegen. Sie schützt **nicht** Informationen über **die Verwaltungsprozesse selbst**.

Konkret nicht DSGVO-relevant sind zum Beispiel:

- Was kostet ein Halteverbot in München?
- Wie lange dauert die Bearbeitung eines Personalausweises in Hamburg?
- Welche Unterlagen werden für eine Gewerbeanmeldung in Köln gebraucht?
- Wann hat das Bürgeramt Mitte geöffnet?
- Welche Online-Dienste bietet Stadt X an?
- Wer bietet als Privatdienstleister Halteverbot-Anträge an?

Diese Informationen sind **öffentliche Verwaltungsdaten**. Sie betreffen kein einziges Individuum. Sie unterliegen weder DSGVO noch BDSG.

### Die Konsequenz: diese Daten müssen frei zugänglich sein

Weil sie öffentlich sind, **dürfen und sollten** sie von beliebigen Dritten verarbeitet werden:

- Aggregatoren wie AmtsGuide
- Suchmaschinen (Google, Bing, Brave, DuckDuckGo)
- KI-Assistenten (ChatGPT, Perplexity, Claude, Google AI Overviews)
- Statistik-Plattformen
- US-amerikanische Datenfirmen
- Chinesische, indische, brasilianische Plattformen, wer auch immer

Es gibt keinen rechtlichen Grund, diese Daten nicht maschinenlesbar bereitzustellen.

## In AmtsScore-Methodik (Dimension 8)

AmtsScore prüft pro Stadt-Website:

- **HTTPS überall**. Stadt-Website lädt komplett über TLS
- **Security-Headers**. HSTS, X-Frame-Options, Referrer-Policy, etc.
- **Cookie-Banner-Detection**: wird die Einwilligung korrekt eingeholt?
- **Tracker-Anzahl**: wie viele externe Domains laden beim ersten Seitenaufruf (ohne Einwilligung)?

Das gibt einen guten Indikator, aber ersetzt nicht eine vollständige Datenschutz-Prüfung.

## Quellen

- [Bundesbeauftragte für den Datenschutz](https://www.bfdi.bund.de/)
- [TTDSG Volltext](https://www.gesetze-im-internet.de/ttdsg/)
- [EU-DSGVO Volltext](https://gdpr-info.eu/)
- [WebKoll / SecurityHeaders.com / Mozilla Observatory](https://observatory.mozilla.org/), automatisierte Header-Prüfung
