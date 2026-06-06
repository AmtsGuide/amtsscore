---
title: "FIM: Föderales Informationsmanagement"
toc: true
---

# FIM: Föderales Informationsmanagement

Das **Föderale Informationsmanagement (FIM)** ist die deutsche Infrastruktur, die Verwaltungsleistungen einheitlich beschreibt, über Bund, Länder und Kommunen hinweg.

## Drei Bausteine

| Baustein | Was es ist |
|---|---|
| **Stammtext** | Standardisierter Beschreibungstext einer Leistung (was sie ist, was sie kostet, wie lange sie dauert) |
| **Datenfeld** | Maschinenlesbare Beschreibung der Antragsfelder (Name, Geburtstag, etc.) |
| **Prozess** | Workflow-Modellierung der Antragsbearbeitung |

FIM verknüpft sich mit [LeiKa](/glossar/leika), jede LeiKa-Leistung hat (idealerweise) einen FIM-Stammtext, Datenfelder und einen Prozess.

## Was FIM löst

Vor FIM: jede Stadt schrieb ihre eigene "Was ist Halteverbot?"-Erklärung. Texte abweichend, Datenfelder anders benannt, Prozesse divers. Bürger:innen verstehen unterschiedliche Versionen. Software-Häuser müssen für jede Stadt neu entwickeln.

Mit FIM: ein Stammtext, eine Datenfeld-Definition, ein referenzierbarer Prozess. Stadt kann sie übernehmen oder lokal überschreiben.

## Realität

FIM ist verfügbar, aber Adoption ist langsam:

- Viele Stadt-Portale verwenden eigene Texte statt FIM-Stammtexte
- Datenfelder werden lokal neu definiert
- Prozess-Modelle werden selten formal hinterlegt

OZG 2.0 verstärkt die FIM-Bindung. Förderbedingung für viele Bundesmittel.

## In AmtsScore-Methodik

**Geplant für v1+:** Dimension "FIM-Adoption". Anteil der Stadt-Leistungs-Seiten, die FIM-Stammtexte verwenden oder per OAuth-Schema-Markup auf FIM-Bausteine verweisen.

## Quellen

- [Föderale IT-Kooperation: FIM-Portal](https://fimportal.de/), offizielle Plattform
- [BMI: FIM-Hintergrund](https://www.bmi.bund.de/DE/themen/moderne-verwaltung/verwaltungsmodernisierung/fim/fim-node.html)
