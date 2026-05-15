---
title: "llms.txt: Die kuratierte KI-Karte"
toc: true
---

# llms.txt

**`/llms.txt`** ist eine 2024 vorgeschlagene Standard-Datei für Websites, die KI-Crawlern eine **kuratierte Karte** ihres Inhalts gibt, was wichtig ist, wo es liegt, wie es zu interpretieren ist.

Ähnlich wie `robots.txt` (für Suchmaschinen) und `sitemap.xml` (für Web-Crawler) ist `llms.txt` für **Large Language Models**.

## Format

Eine `llms.txt`-Datei ist reines Markdown am Domain-Root:

```markdown
# Stadt München

> Verwaltungsportal der Landeshauptstadt München

## Dienstleistungen

- [Halteverbot beantragen](/dienstleistung/halteverbot.md): Antragsverfahren, Kosten, Bearbeitungszeit
- [Personalausweis verlängern](/dienstleistung/personalausweis.md): Voraussetzungen, Online-Termin
- [Gewerbe anmelden](/dienstleistung/gewerbeanmeldung.md): Pflichten, Formulare

## Optional

- [Geschichte der Stadt](/ueber/geschichte.md)
- [Veranstaltungskalender](/events.md)
```

## Warum llms.txt für Behörden zählt

Eine Stadt-Website ist groß und chaotisch. Ein KI-Crawler hat keine Geduld, alles zu indexieren. **`llms.txt` sagt: das hier ist wichtig.**

Vorteile:

1. **Präzisere KI-Antworten**. ChatGPT oder Perplexity zitieren die echten Dienstleistungs-Seiten, nicht zufällige Subseiten
2. **Less Halluzination**. die KI hat klar dokumentierte Quellen statt Vermutungen
3. **Stadt-Kontrolle**. die Stadt entscheidet, welche Inhalte für KI relevant sind
4. **Server-Schutz**. KI-Bots crawlen weniger umfassend, wenn `llms.txt` sie zu den richtigen Stellen führt

## Begleitend: Markdown-Versionen einzelner Seiten

Best Practice: jede HTML-Seite hat optional eine `.md`-Version unter gleichem Pfad.

`/dienstleistung/halteverbot` (HTML für Menschen) + `/dienstleistung/halteverbot.md` (Markdown für KI).

Die `.md`-Version enthält nur den semantischen Kern: Überschriften, Absätze, Listen, Tabellen, ohne Navigation, Header, Footer, Cookie-Banner, Sidebars.

## Realität in DE

**Stand 2026: praktisch keine deutsche Behörde hat `/llms.txt`.** Es ist ein neuer Standard. Die ersten Adopter werden 12 Monate Vorsprung haben.

## In AmtsScore-Methodik

Teil von D11 ([Maschinen-Lesbarkeit + KI-Bereitschaft](/glossar/ai-readiness)). Konkret:

- **2 Punkte:** `/llms.txt` vorhanden
- **+2 Punkte:** valide Markdown-Struktur, nicht-leer
- **+3 Punkte:** ≥ 5 verlinkte Dienstleistungen mit eigenen `.md`-Versionen
- **+3 Punkte:** Letzter Update < 90 Tage (gepflegt, nicht 2024-Leiche)

Max: 10 Punkte. Realistischer v0-Score für deutsche Städte: 0.

## Quellen

- [llmstxt.org](https://llmstxt.org/), offizielle Standard-Webseite (Jeremy Howard / Answer.AI)
- [llms.txt von Anthropic](https://docs.anthropic.com/llms.txt). Beispiel-Implementierung
- [llms.txt Hub](https://llmstxt.site/), kuratierte Liste aktiver llms.txt-Implementierungen
