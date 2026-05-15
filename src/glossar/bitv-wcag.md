---
title: BITV / WCAG: Barrierefreiheit
toc: true
---

# BITV 2.0 / WCAG 2.1: Barrierefreiheit

**BITV 2.0** (Barrierefreie-Informationstechnik-Verordnung) ist die deutsche Umsetzung der EU-Richtlinie 2016/2102 zur Barrierefreiheit öffentlicher Websites. Sie verweist im Wesentlichen auf den internationalen Standard **WCAG 2.1 Stufe AA**.

## Wer ist verpflichtet

Alle deutschen öffentlichen Stellen. Bund, Länder, Kommunen, ÖPNV, Universitäten, Sozialversicherungsträger. Stichtag: **23. September 2018** (neue Seiten) bzw. **23. September 2020** (bestehende Seiten).

Praktisch: **Stadt-Websites müssen seit 2020 barrierefrei sein.**

## Was BITV/WCAG verlangt (Auszug)

| Bereich | Beispiel |
|---|---|
| **Textalternative** | Jedes Bild braucht `alt`-Text |
| **Kontrast** | Mindestens 4.5:1 für normalen Text, 3:1 für große Schrift |
| **Tastatur-Navigation** | Alle Funktionen ohne Maus erreichbar |
| **Heading-Struktur** | h1, h2, h3 in korrekter Hierarchie |
| **Formular-Labels** | Jedes Eingabefeld mit zugehörigem `<label>` |
| **ARIA-Roles** | Dynamische Komponenten korrekt für Screenreader markiert |
| **Sprachattribut** | `lang="de"` im `<html>`-Tag |
| **Zoom auf 200%** | Inhalt bleibt nutzbar |

## Erklärung zur Barrierefreiheit

Jede Stadt-Website MUSS eine "Erklärung zur Barrierefreiheit" haben, eine Seite, die transparent dokumentiert: Was ist konform? Was nicht? Wann wird es behoben? Wo melden Bürger:innen Probleme?

Fehlt diese Erklärung → klare BITV-Verletzung.

## Automatisierte Tests

**axe-core** (Deque Systems) ist der De-facto-Standard für automatisierte WCAG-Prüfung. Erkennt ca. **30% aller WCAG-Verstöße** automatisch. Rest braucht manuelle Prüfung.

Andere Werkzeuge: WAVE (WebAIM), Lighthouse-Accessibility, Pa11y.

## In AmtsScore-Methodik (Dimension 4)

AmtsScore misst Barrierefreiheit auf 4 Stadt-Seiten (Startseite + 3 Dienstleistungs-Seiten):

- Anzahl axe-core-Verstöße
- WCAG-AA-Compliance-Quote
- Vorhandensein der Barrierefreiheits-Erklärung

Ergebnis ist eine **Untergrenze** (das was Maschinen erkennen). Volle manuelle Prüfung ist nicht skalierbar; AmtsScore identifiziert die schlechtesten Performer für gezielte tiefere Audits.

## Quellen

- [BITV 2.0 Volltext (gesetze-im-internet.de)](https://www.gesetze-im-internet.de/bitv_2_0/)
- [WCAG 2.1 (W3C)](https://www.w3.org/TR/WCAG21/)
- [axe-core (GitHub)](https://github.com/dequelabs/axe-core)
- [Überwachungsstelle des Bundes für Barrierefreiheit von Informationstechnik (BFIT-Bund)](https://www.bfit-bund.de/)
