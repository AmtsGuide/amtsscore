---
title: DSGVO + Cookies — Datenschutz auf Behörden-Websites
toc: true
---

# DSGVO + Cookie-Banner

Verwaltungs-Websites müssen die **EU-Datenschutz-Grundverordnung (DSGVO)** einhalten — strenger als kommerzielle Sites, weil Bürger:innen oft keine Wahl haben, ob sie die Behörde nutzen.

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

## Häufige Verletzungen auf Stadt-Websites

- Google Analytics ohne Einwilligung geladen
- Maps (Google, OpenStreetMap-Variants) lädt Tracker ohne Banner
- YouTube-Embeds laden auf Seitenaufruf, nicht erst auf Klick
- Cookie-Banner ohne "Alle ablehnen"-Option
- Externe Schriftarten (Google Fonts) laden ohne Hinweis (Server-IP-Übertragung)

## In AmtsScore-Methodik (Dimension 8)

AmtsScore prüft pro Stadt-Website:

- **HTTPS überall** — Stadt-Website lädt komplett über TLS
- **Security-Headers** — HSTS, X-Frame-Options, Referrer-Policy, etc.
- **Cookie-Banner-Detection** — wird die Einwilligung korrekt eingeholt?
- **Tracker-Anzahl** — wie viele externe Domains laden beim ersten Seitenaufruf (ohne Einwilligung)?

Das gibt einen guten Indikator, aber ersetzt nicht eine vollständige Datenschutz-Prüfung.

## Quellen

- [Bundesbeauftragte für den Datenschutz](https://www.bfdi.bund.de/)
- [TTDSG Volltext](https://www.gesetze-im-internet.de/ttdsg/)
- [EU-DSGVO Volltext](https://gdpr-info.eu/)
- [WebKoll / SecurityHeaders.com / Mozilla Observatory](https://observatory.mozilla.org/) — automatisierte Header-Prüfung
