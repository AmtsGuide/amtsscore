---
title: Maschinen-Lesbarkeit + KI-Bereitschaft
toc: true
---

# Maschinen-Lesbarkeit + KI-Bereitschaft

Eine Verwaltungs-Website hat 2026 nicht mehr nur menschliche Besucher:innen. Sie wird gelesen von **ChatGPT, Perplexity, Claude, Google AI Overviews, Apps, Aggregatoren, Software-Agenten**. Wenn die Website für diese Konsumenten unsichtbar ist, ist die Stadt für viele Bürger:innen ab 2027 nicht mehr findbar.

## Die fünf KI-Bereitschaft-Kriterien

| # | Kriterium | Frage |
|---|---|---|
| 1 | **`llms.txt`** | Hat die Domain eine `/llms.txt`-Datei mit kuratierten Inhalten für KI-Crawler? |
| 2 | **AI-Bot-Erlaubnis** | Erlaubt `robots.txt` explizit GPTBot, ChatGPT-User, PerplexityBot, ClaudeBot, Google-Extended? |
| 3 | **Non-JS-Rendering** | Funktioniert die Seite vollständig mit deaktiviertem JavaScript? (KI-Bots rendern oft kein JS.) |
| 4 | **Stabile Permalinks** | Sind URLs ohne Session-IDs, Hash-Parameter, Datums-Slugs? Bleiben sie über Jahre stabil? |
| 5 | **Strukturierte Daten** | Schema.org GovernmentService auf jeder Dienstleistungs-Seite (gemessen in D6 separat) |

## Warum jedes Kriterium zählt

### `llms.txt`

[`llms.txt`](/glossar/llms-txt) ist die explizite Karte für KI-Crawler, was sie indexieren sollen, wie sie es interpretieren, welche kanonischen Endpunkte existieren. Ohne `llms.txt` rät die KI; mit `llms.txt` weiß sie.

### AI-Bot-Erlaubnis

Eine zunehmende Zahl von Web-Operatoren blockiert KI-Bots pauschal (User-Agent: GPTBot → Disallow). Für eine Behörde, die ihre Bürger:innen erreichen will, ist das **das Gegenteil von Bürger-Service**.

Modern: `robots.txt` mit expliziter Allow-Liste für die wichtigen AI-Bots:

```
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Google-Extended
Allow: /
```

### Non-JS-Rendering

Viele KI-Bots crawlen ohne JavaScript-Execution (Kosten, Komplexität, Sicherheit). Eine Seite, deren Inhalt erst per JS gerendert wird, ist für sie unsichtbar.

**Test:** Stadt-Website mit deaktiviertem JS aufrufen. Ist die Hauptnavigation noch da? Sind die Dienstleistungs-Listen sichtbar? Funktioniert die Suche?

### Stabile Permalinks

`https://stadt.de/dienstleistung/halteverbot-beantragen` ist stabil. `https://stadt.de/portal.html?id=42&sess=xyz123` ist es nicht. KI-Bots indexieren Permalinks. Session-IDs werden ignoriert oder falsch gecached.

## Realität

**Stand 2026: keine deutsche Stadt-Website erfüllt diese Kriterien vollständig.** Viele blockieren AI-Bots aktiv. Wenige haben `llms.txt`. Non-JS-Rendering ist die Ausnahme bei modernen Single-Page-Apps. Permalinks sind oft URL-Müll.

Das ist der **strategische Punkt** von AmtsScore: wir setzen die Latte für 2027+. Heute scoren alle nahe Null, das ist die Schlagzeile, nicht das Problem.

## In AmtsScore-Methodik (Dimension 11)

D11 misst alle vier dynamischen Kriterien automatisiert. Erwartete v0-Scores: 0-3 von 10 für die meisten Städte. Wer 4+ erreicht, hat aktiv mitgedacht.

## Verwandte Begriffe

- [llms.txt](/glossar/llms-txt), die kuratierte KI-Karte
- [API + MCP](/glossar/api-mcp), die maschinenlesbare Schnittstelle
- [Schema.org](/glossar/schema-org), strukturierte Daten (D6)

## Quellen

- [llms.txt Initiative von Answer.AI](https://llmstxt.org/), der Standard-Vorschlag
- [OpenAI: GPTBot Documentation](https://platform.openai.com/docs/gptbot). User-Agent-Strings + Best Practices
- [Anthropic: Claude bot list](https://docs.anthropic.com/). Bot-User-Agents
- [Perplexity: PerplexityBot](https://docs.perplexity.ai/). Crawl-Verhalten
- [Google: Google-Extended](https://developers.google.com/search/docs/crawling-indexing/overview-google-crawlers), der separate AI-Crawl
