---
title: "E-Auto: Kandidatensignale"
toc: true
---

# E-Auto Kandidatensignale

<div class="tag">Vorschau / Methodenprüfung</div>

Diese Seite zeigt Kandidatensignale aus dem E-Auto-Intake von AmtsGuide. Sie ist
eine Vorschau auf Quellenlage, Faktenabdeckung, Unbekannte und
Anbietergrenze. Sie ist keine veröffentlichte AmtsScore-Wertung und keine
abschließende Bewertung der E-Auto-Themen.

```js
const current = await FileAttachment("../data/eauto_prescore.json").json();
const manifest = await FileAttachment("../data/history/eauto/index.json").json();
const latestDiff = await FileAttachment("../data/history/eauto/diff-2026-06-04.json").json();
const siteAusgangsstand = await FileAttachment("../data/history/site-baseline/2026-05-20.json").json();
```

```js
const topics = current.topics;
const summary = current.summary;
const gates = current.gates;
const buildableTopics = topics.filter((t) => t.review_status === "buildable_preview");
const bridgeTopics = topics.filter((t) => t.review_status === "bridge_context");
const suppressedTopics = topics.filter((t) => ["not_ready", "provider_only", "suppressed"].includes(t.review_status));
const labelMap = new Map(Object.entries({
  accepted: "Akzeptiert",
  accepted_with_diagnostics: "Akzeptiert mit Hinweisen",
  allow_cta: "CTA erlaubt",
  allow_embedded: "Einbettung erlaubt",
  baseline_established: "Ausgangsstand etabliert",
  bridge: "Kontext",
  bridge_context: "Kontextthema",
  blocked_signal_count: "Blockierte Signale",
  buildable_preview: "Vorschau bereit",
  complete: "Vollständig",
  core: "AmtsScore-Kern",
  current_snapshot: "Aktueller Datenstand",
  eauto_candidate_signals: "E-Auto Kandidatensignale",
  editor_review_required: "Redaktionelle Prüfung offen",
  fact_count: "Fakten",
  light_ready: "Leichtes Werkzeug bereit",
  light_tool_ready: "Leichtes Werkzeug bereit",
  not_ready: "Nicht bereit",
  not_ready_closed: "Nicht bereit",
  not_surfaceable: "Nicht oberflächenreif",
  official_source_count: "Offizielle Quellen",
  provider_only: "Anbieterkontext",
  provider_only_ready: "Anbieterkontext bereit",
  ready: "Bereit",
  signal_count: "Kandidatensignale",
  static_lookup: "Statische Auskunft",
  suppress_route: "Seite unterdrückt",
  suppressed: "Unterdrückt",
  suppressed_route_count: "Unterdrückte Seiten",
  topic_count: "Themen",
  unknown_count: "Unbekannte",
  web_buildable_now_count: "Darstellbare Flächen"
}));
const displayLabel = (value) => {
  if (value == null || value === "") return "—";
  if (typeof value === "boolean") return value ? "Ja" : "Nein";
  const text = String(value);
  return labelMap.get(text) ?? text.replace(/[_-]+/g, " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
};
const yesNo = (value) => value ? "Ja" : "Nein";
const statCard = (label, value, tone = "") => {
  const valueText = String(value ?? "");
  const longValueClass = valueText.length > 11 ? " stat-value--long" : "";
  return html`<div class="stat-card ${tone}">
  <div class="stat-label">${label}</div>
  <div class="stat-value${longValueClass}">${value}</div>
</div>`;
};
const metricRows = current.visual_rollups.metrics.map((row) => ({
  ...row,
  metric: displayLabel(row.metric)
}));
const unknownRows = topics
  .map((t) => ({Thema: t.label, Unbekannte: t.unknown_count, Gruppe: displayLabel(t.group)}))
  .sort((a, b) => b.Unbekannte - a.Unbekannte);
const policyRows = topics.map((t) => ({
  Thema: t.label,
  Gruppe: displayLabel(t.group),
  "Seitenregel": displayLabel(t.route_policy),
  "Handlungsregel": displayLabel(t.cta_policy),
  "Einbettung": displayLabel(t.embedded_policy),
}));
```

## Prüfstatus

Die Sicherheitsprüfung ist die Import-Sicherung. E-Auto-Daten werden erst angezeigt,
wenn harte Sperren, fehlgeschlagene Verarbeitungsprüfungen und Anbieter-Belege als
AmtsScore-Belege ausgeschlossen sind.

```js
html`<div class="stat-grid">
  ${statCard("Abschlussprüfung", displayLabel(gates.final_audit_status))}
  ${statCard("Harte Sperren", gates.hard_blocker_count)}
  ${statCard("Verarbeitungsfehler", gates.failed_check_count)}
  ${statCard("Anbieter-Belege", gates.provider_rows_used_as_evidence ? "Genutzt" : "Ausgeschlossen")}
</div>`
```

## Aktueller Datenstand

```js
html`<p>Der aktuelle Datenstand <strong>${current.current_snapshot}</strong> ist die erste
Ausgangslage für E-Auto-Kandidatensignale. Die Historienstruktur ist bereits angelegt,
damit spätere Imports sichtbar machen, was sich geändert hat.</p>`
```

```js
html`<div class="stat-grid">
  ${statCard("Kandidatenthemen", summary.candidate_ready_topic_count)}
  ${statCard("Kandidatensignale", summary.signal_count)}
  ${statCard("Blockierte Signale", summary.blocked_signal_count)}
  ${statCard("Darstellbare Flächen", summary.web_buildable_now_count)}
  ${statCard("Unterdrückte Seiten", summary.suppressed_route_count)}
  ${statCard("Prüfung des Datenstands", displayLabel(current.review_status))}
</div>`
```

## Zeitverlauf

Mit dem ersten Datenstand hat die Zeitreihe einen Datenpunkt. Sobald ein zweiter
Datenstand importiert wird, zeigen die Linien echte Änderungen der Themen,
Signale, Sperren und darstellbaren Flächen.

```js
Plot.plot({
  width: 760,
  height: 280,
  marginLeft: 150,
  x: {label: "Datenstand"},
  y: {label: "Wert", grid: true},
  color: {legend: true},
  marks: [
    Plot.dot(metricRows, {x: "date", y: "value", stroke: "metric", r: 5}),
    Plot.line(metricRows, {x: "date", y: "value", stroke: "metric"})
  ]
})
```

## Darstellbare AmtsScore-Themen

Diese Themen liegen auf der AmtsScore-Nutzungsebene und können als eingebettete
Vorschauflächen beschrieben werden. Eigene Rechner-Seiten bleiben laut
Seitenregel unterdrückt.

```js
Inputs.table(buildableTopics.map((t) => ({
  Thema: t.label,
  Gruppe: displayLabel(t.group),
  Werkzeug: displayLabel(t.tool_type),
  Quellen: `${t.official_source_count}/${t.source_count}`,
  Fakten: `${t.source_backed_fact_count}/${t.fact_count}`,
  Unbekannt: t.unknown_count,
  Seite: displayLabel(t.route_policy),
  CTA: displayLabel(t.cta_policy),
  Aussage: t.public_claim_wording ?? "—",
})), {rows: 20})
```

## Brücken- und Kontextthemen

Brückenthemen liefern Kontext für den E-Auto-Cluster. Sie werden nicht als
eigenständige Themenaussage hochgestuft.

```js
Inputs.table(bridgeTopics.map((t) => ({
  Thema: t.label,
  Stand: displayLabel(t.review_status),
  Werkzeug: displayLabel(t.tool_type),
  Quellen: `${t.official_source_count}/${t.source_count}`,
  Fakten: `${t.source_backed_fact_count}/${t.fact_count}`,
  Unbekannt: t.unknown_count,
})), {rows: 20})
```

## Unterdrückt oder nicht bereit

Diese Themen sind aktuell nicht als öffentliche E-Auto-Vorschauflächen
geeignet oder gehören in reine Anbieterkontexte. Anbieterdaten werden nicht als
AmtsScore-Belege verwendet.

```js
Inputs.table(suppressedTopics.map((t) => ({
  Thema: t.label,
  Stand: displayLabel(t.review_status),
  Gruppe: displayLabel(t.group),
  Werkzeug: displayLabel(t.tool_type),
  Seite: displayLabel(t.route_policy),
  CTA: displayLabel(t.cta_policy),
  "Anbieter-Belege ausgeschlossen": yesNo(t.provider_evidence_excluded),
})), {rows: 20})
```

## Ausgangswert der Unbekannten

Unbekannte sind ein wichtiger Prüfhinweis. Die Grafik zeigt den aktuellen
Ausgangsstand; spätere Datenstände können hier die stärksten Rückgänge oder Anstiege
sichtbar machen.

```js
Plot.plot({
  width: 760,
  height: 30 + unknownRows.length * 22,
  marginLeft: 190,
  x: {label: "Unbekannte", grid: true},
  y: {label: null},
  marks: [
    Plot.barX(unknownRows, {x: "Unbekannte", y: "Thema", fill: "Gruppe", sort: {y: "x", reverse: true}}),
    Plot.text(unknownRows, {x: "Unbekannte", y: "Thema", text: "Unbekannte", dx: 5, textAnchor: "start", fontSize: 11})
  ]
})
```

## Regelgerüst

Die Seiten- und Handlungsregeln sind Teil der Historie. Sie bleiben sichtbar, weil
ein späterer Regelwechsel ein wesentliches Vergleichsereignis ist.

```js
Inputs.table(policyRows, {rows: 25})
```

## Änderungsprotokoll

Für den ersten Datenstand gibt es noch keinen Vorher-Wert. Der Vergleich hält deshalb
fest, dass der E-Auto-Ausgangsstand etabliert wurde.

```js
Inputs.table(latestDiff.events.map((event) => ({
  Typ: displayLabel(event.event_type),
  Thema: event.topic_slug ?? "Cluster",
  Feld: displayLabel(event.field),
  Vorher: displayLabel(event.previous_value),
  Jetzt: displayLabel(event.current_value),
  Schwere: displayLabel(event.severity),
})), {rows: 20})
```

## Anbietergrenze

Anbieter-Zeilen können für Vertriebs- oder Anbieterübergaben relevant sein. Für
AmtsScore-Belege sind sie in diesem Datenstand ausgeschlossen.

```js
html`<div class="stat-card">
  <div class="stat-label">Anbieter-Belege ausgeschlossen</div>
  <div class="stat-value">${summary.provider_rows_used_as_evidence ? "Nein" : "Ja"}</div>
  <p style="margin:0.5rem 0 0;color:var(--theme-foreground-muted)">Alle Themen melden, dass Anbieterzeilen nicht als Belege genutzt werden. Anbieterdaten werden nicht in Belegtabellen visualisiert.</p>
</div>`
```

## Website-Ausgangsstand

Vor der E-Auto-Erweiterung wurde die bestehende Observable-Datenlage als
Website-Ausgangsstand gespeichert. Live- und lokale Zusammenfassungen stimmen im Ausgangsstand-Check
überein.

```js
Inputs.table([
  {Datei: "prescore.json", Lokal: siteAusgangsstand.summaries.local.prescore.topic_count + " Themen", Live: siteAusgangsstand.summaries.live.prescore.topic_count + " Themen"},
  {Datei: "halteverbot.json", Lokal: siteAusgangsstand.summaries.local.halteverbot.total_cities + " Städte", Live: siteAusgangsstand.summaries.live.halteverbot.total_cities + " Städte"},
  {Datei: "kfz_enriched.json", Lokal: siteAusgangsstand.summaries.local.kfz_enriched.n_cities + " Städte", Live: siteAusgangsstand.summaries.live.kfz_enriched.n_cities + " Städte"},
], {rows: 5})
```

## Methodische Hinweise

```js
html`<ul>
  <li><strong>Datenstand-Familie:</strong> ${displayLabel(current.snapshot_family)}</li>
  <li><strong>Historienmodell:</strong> ${current.history_model_version}</li>
  <li><strong>Aktueller Zeiger:</strong> ${current.current_snapshot_path}</li>
  <li><strong>Letzter Vergleich:</strong> ${current.latest_diff_path}</li>
  <li><strong>Manifest-Datenstände:</strong> ${manifest.snapshots.length}</li>
</ul>`
```

Die Seite nutzt den aktuellen Zeiger. Eine Rückkehr kann daher auf einen älteren
Datenstand zeigen, ohne spätere Datenstand-Dateien zu löschen.
