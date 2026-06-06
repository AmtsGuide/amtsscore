---
title: "E-Auto: Candidate Signals"
toc: true
---

# E-Auto Candidate Signals

<div class="tag">Preview / Methodology Review</div>

Diese Seite zeigt Candidate Signals aus dem E-Auto-Intake von AmtsGuide. Sie ist
eine Vorschau auf Quellenlage, Faktenabdeckung, Unbekannte und
Provider-Grenze. Sie ist keine veröffentlichte AmtsScore-Wertung und keine
abschließende Bewertung der E-Auto-Themen.

```js
const current = await FileAttachment("../data/eauto_prescore.json").json();
const manifest = await FileAttachment("../data/history/eauto/index.json").json();
const latestDiff = await FileAttachment("../data/history/eauto/diff-2026-06-04.json").json();
const siteBaseline = await FileAttachment("../data/history/site-baseline/2026-05-20.json").json();
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
  baseline_established: "Baseline etabliert",
  bridge: "Kontext",
  bridge_context: "Kontextthema",
  blocked_signal_count: "Blockierte Signals",
  buildable_preview: "Preview bereit",
  complete: "Vollständig",
  core: "AmtsScore-Kern",
  current_snapshot: "Aktueller Snapshot",
  eauto_candidate_signals: "E-Auto Candidate Signals",
  editor_review_required: "Redaktionelle Prüfung offen",
  fact_count: "Fakten",
  light_ready: "Leichtes Tool bereit",
  light_tool_ready: "Leichtes Tool bereit",
  not_ready: "Nicht bereit",
  not_ready_closed: "Nicht bereit",
  not_surfaceable: "Nicht oberflächenreif",
  official_source_count: "Offizielle Quellen",
  provider_only: "Provider-Kontext",
  provider_only_ready: "Provider-Kontext bereit",
  ready: "Bereit",
  signal_count: "Candidate Signals",
  static_lookup: "Statische Auskunft",
  suppress_route: "Route unterdrückt",
  suppressed: "Unterdrückt",
  suppressed_route_count: "Unterdrückte Routen",
  topic_count: "Topics",
  unknown_count: "Unbekannte",
  web_buildable_now_count: "Buildable Surfaces"
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
  .map((t) => ({Topic: t.label, Unbekannte: t.unknown_count, Gruppe: displayLabel(t.group)}))
  .sort((a, b) => b.Unbekannte - a.Unbekannte);
const policyRows = topics.map((t) => ({
  Topic: t.label,
  Gruppe: displayLabel(t.group),
  "Route-Policy": displayLabel(t.route_policy),
  "CTA-Policy": displayLabel(t.cta_policy),
  "Embedded": displayLabel(t.embedded_policy),
}));
```

## Gate Status

Die Gate-Prüfung ist die Import-Sicherung. E-Auto-Daten werden erst angezeigt,
wenn Hard Blocker, fehlgeschlagene Pipeline-Checks und Provider-Evidence als
AmtsScore-Beleg ausgeschlossen sind.

```js
html`<div class="stat-grid">
  ${statCard("Finaler Audit", displayLabel(gates.final_audit_status))}
  ${statCard("Hard Blocker", gates.hard_blocker_count)}
  ${statCard("Pipeline-Fehler", gates.failed_check_count)}
  ${statCard("Provider-Belege", gates.provider_rows_used_as_evidence ? "Genutzt" : "Ausgeschlossen")}
</div>`
```

## Current Snapshot

```js
html`<p>Der aktuelle Snapshot <strong>${current.current_snapshot}</strong> ist die erste
E-Auto-Candidate-Signal-Baseline. Die History-Struktur ist bereits angelegt,
damit spätere Imports sichtbar machen, was sich geändert hat.</p>`
```

```js
html`<div class="stat-grid">
  ${statCard("Candidate Topics", summary.candidate_ready_topic_count)}
  ${statCard("Candidate Signals", summary.signal_count)}
  ${statCard("Blocked Signals", summary.blocked_signal_count)}
  ${statCard("Buildable Surfaces", summary.web_buildable_now_count)}
  ${statCard("Suppressed Routes", summary.suppressed_route_count)}
  ${statCard("Snapshot Review", displayLabel(current.review_status))}
</div>`
```

## Timeline

Mit dem ersten Snapshot hat die Zeitreihe einen Datenpunkt. Sobald ein zweiter
Snapshot importiert wird, zeigen die Linien echte Änderungen der Topic-,
Signal-, Blocker- und Buildable-Surface-Zahlen.

```js
Plot.plot({
  width: 760,
  height: 280,
  marginLeft: 150,
  x: {label: "Snapshot"},
  y: {label: "Wert", grid: true},
  color: {legend: true},
  marks: [
    Plot.dot(metricRows, {x: "date", y: "value", stroke: "metric", r: 5}),
    Plot.line(metricRows, {x: "date", y: "value", stroke: "metric"})
  ]
})
```

## Buildable AmtsScore-Lane Topics

Diese Topics liegen im AmtsScore-Consumer-Lane und können als eingebettete
Preview-Oberflächen beschrieben werden. Eigene Rechner-Routen bleiben laut
Route-Policy unterdrückt.

```js
Inputs.table(buildableTopics.map((t) => ({
  Topic: t.label,
  Gruppe: displayLabel(t.group),
  Tool: displayLabel(t.tool_type),
  Quellen: `${t.official_source_count}/${t.source_count}`,
  Fakten: `${t.source_backed_fact_count}/${t.fact_count}`,
  Unbekannt: t.unknown_count,
  Route: displayLabel(t.route_policy),
  CTA: displayLabel(t.cta_policy),
  Claim: t.public_claim_wording ?? "—",
})), {rows: 20})
```

## Bridge And Context Topics

Bridge-Themen liefern Kontext für den E-Auto-Cluster. Sie werden nicht als
eigenständige Topic-Aussage hochgestuft.

```js
Inputs.table(bridgeTopics.map((t) => ({
  Topic: t.label,
  Status: displayLabel(t.review_status),
  Tool: displayLabel(t.tool_type),
  Quellen: `${t.official_source_count}/${t.source_count}`,
  Fakten: `${t.source_backed_fact_count}/${t.fact_count}`,
  Unbekannt: t.unknown_count,
})), {rows: 20})
```

## Suppressed Or Not Ready

Diese Topics sind aktuell nicht als öffentliche E-Auto-Preview-Oberflächen
geeignet oder gehören in Provider-only-Kontexte. Provider-Daten werden nicht als
AmtsScore-Evidence verwendet.

```js
Inputs.table(suppressedTopics.map((t) => ({
  Topic: t.label,
  Status: displayLabel(t.review_status),
  Gruppe: displayLabel(t.group),
  Tool: displayLabel(t.tool_type),
  Route: displayLabel(t.route_policy),
  CTA: displayLabel(t.cta_policy),
  "Provider Evidence Excluded": yesNo(t.provider_evidence_excluded),
})), {rows: 20})
```

## Unknown Count Baseline

Unbekannte sind ein wichtiger Review-Indikator. Der Chart zeigt die aktuelle
Baseline; spätere Snapshots können hier die stärksten Rückgänge oder Anstiege
sichtbar machen.

```js
Plot.plot({
  width: 760,
  height: 30 + unknownRows.length * 22,
  marginLeft: 190,
  x: {label: "Unknown Count", grid: true},
  y: {label: null},
  marks: [
    Plot.barX(unknownRows, {x: "Unbekannte", y: "Topic", fill: "Gruppe", sort: {y: "x", reverse: true}}),
    Plot.text(unknownRows, {x: "Unbekannte", y: "Topic", text: "Unbekannte", dx: 5, textAnchor: "start", fontSize: 11})
  ]
})
```

## Policy Scaffold

Die Route- und CTA-Policies sind Teil der History. Sie bleiben sichtbar, weil
ein späterer Policy-Wechsel ein materialer Diff-Event ist.

```js
Inputs.table(policyRows, {rows: 25})
```

## Change Log

Für den ersten Snapshot gibt es noch keinen Vorher-Wert. Der Diff hält deshalb
fest, dass die E-Auto-Baseline etabliert wurde.

```js
Inputs.table(latestDiff.events.map((event) => ({
  Typ: displayLabel(event.event_type),
  Topic: event.topic_slug ?? "Cluster",
  Feld: displayLabel(event.field),
  Vorher: displayLabel(event.previous_value),
  Jetzt: displayLabel(event.current_value),
  Schwere: displayLabel(event.severity),
})), {rows: 20})
```

## Provider Boundary

Provider-Zeilen können für Sales- oder Provider-Handoffs relevant sein. Für
AmtsScore-Evidence sind sie in diesem Snapshot ausgeschlossen.

```js
html`<div class="stat-card">
  <div class="stat-label">Provider Evidence Excluded</div>
  <div class="stat-value">${summary.provider_rows_used_as_evidence ? "Nein" : "Ja"}</div>
  <p style="margin:0.5rem 0 0;color:var(--theme-foreground-muted)">Alle Topics melden provider_rows_used_as_evidence=false. Provider-Daten werden nicht in Evidence-Tabellen visualisiert.</p>
</div>`
```

## Site Baseline

Vor der E-Auto-Erweiterung wurde die bestehende Observable-Datenlage als
Site-Baseline gespeichert. Live- und lokale Summaries stimmen im Baseline-Check
überein.

```js
Inputs.table([
  {Datei: "prescore.json", Lokal: siteBaseline.summaries.local.prescore.topic_count + " Topics", Live: siteBaseline.summaries.live.prescore.topic_count + " Topics"},
  {Datei: "halteverbot.json", Lokal: siteBaseline.summaries.local.halteverbot.total_cities + " Städte", Live: siteBaseline.summaries.live.halteverbot.total_cities + " Städte"},
  {Datei: "kfz_enriched.json", Lokal: siteBaseline.summaries.local.kfz_enriched.n_cities + " Städte", Live: siteBaseline.summaries.live.kfz_enriched.n_cities + " Städte"},
], {rows: 5})
```

## Method Notes

```js
html`<ul>
  <li><strong>Snapshot-Familie:</strong> ${displayLabel(current.snapshot_family)}</li>
  <li><strong>History Model:</strong> ${current.history_model_version}</li>
  <li><strong>Current Pointer:</strong> ${current.current_snapshot_path}</li>
  <li><strong>Latest Diff:</strong> ${current.latest_diff_path}</li>
  <li><strong>Manifest-Snapshots:</strong> ${manifest.snapshots.length}</li>
</ul>`
```

Die Seite nutzt den Current Pointer. Ein Rollback kann daher auf einen älteren
Snapshot zeigen, ohne spätere Snapshot-Dateien zu löschen.
