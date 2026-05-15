# AmtsScore

**Status:** v0 / Pre-Launch. Methodik in öffentlicher Kommentierungsphase.

Continuous data-driven measurement of digital performance of German Verwaltungs-Websites. Quartalsweise, methodisch offen, reproduzierbar.

🌐 Live: [amtsscore.de](https://amtsscore.de)

## Was AmtsScore ist

Eine Initiative der **AmtsGuide GmbH** (German Innovation Award Winner 2026, Kategorie B2C E-Business). AmtsScore misst die digitale Performance einzelner deutscher Stadt-Websites mit einem reproduzierbaren 10-Dimensionen-Composite-Score (0–10).

## Was hier im Repo ist

| Pfad | Inhalt |
|---|---|
| `docs/methodology.md` | Methodik-Paper v0.1 (10 Dimensionen, Gewichtungen, Validierungsplan) |
| `src/` | Observable Framework Site-Source (Markdown + Charts) |
| `data/` | Aggregierte Daten-Outputs pro Quartal (JSON) |
| `LICENSE-CONTENT` | Methodik + Daten: CC BY 4.0 |
| `LICENSE-CODE` | Site-Code: MIT |
| `CONTRIBUTING.md` | Wie man Methodik-Vorschläge oder Daten-Korrekturen einreicht |

## Was hier NICHT im Repo ist

Der Scraper selbst ist nicht öffentlich. Er produziert die JSON-Dateien in `data/`. Der Output ist reproduzierbar (Methodik öffentlich), die Implementierung ist Betriebsgeheimnis.

## Site lokal bauen

```bash
pnpm install
pnpm build
npx serve dist
```

Voraussetzung: **Node 22 LTS** (Node 25+ hat Build-Issues mit Observable Framework Dependencies).

## Lizenz

- **Methodik + Daten:** Creative Commons Attribution 4.0 (`LICENSE-CONTENT`)
- **Site-Code:** MIT (`LICENSE-CODE`)
- **Marke "AmtsScore":** DPMA-Wortmarke (Anmeldung 2026-05-15)

## Kontakt

ad@blinktank.de
