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
const metricRows = current.visual_rollups.metrics;
const unknownRows = topics
  .map((t) => ({Topic: t.label, Unbekannte: t.unknown_count, Gruppe: t.group}))
  .sort((a, b) => b.Unbekannte - a.Unbekannte);
const policyRows = topics.map((t) => ({
  Topic: t.label,
  Gruppe: t.group,
  "Route-Policy": t.route_policy ?? "—",
  "CTA-Policy": t.cta_policy ?? "—",
  "Embedded": t.embedded_policy ?? "—",
}));
```

## Gate Status

Die Gate-Prüfung ist die Import-Sicherung. E-Auto-Daten werden erst angezeigt,
wenn Hard Blocker, fehlgeschlagene Pipeline-Checks und Provider-Evidence als
AmtsScore-Beleg ausgeschlossen sind.

```js
html`<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:0.75rem;margin:1rem 0">
  <div class="stat-card">
    <div class="stat-label">Final Audit</div>
    <div style="font-size:1.35rem;font-weight:650">${gates.final_audit_status}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Hard Blocker</div>
    <div style="font-size:1.35rem;font-weight:650">${gates.hard_blocker_count}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Pipeline Failures</div>
    <div style="font-size:1.35rem;font-weight:650">${gates.failed_check_count}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Provider Evidence</div>
    <div style="font-size:1.35rem;font-weight:650">${gates.provider_rows_used_as_evidence ? "genutzt" : "ausgeschlossen"}</div>
  </div>
</div>`
```

## Current Snapshot

Der aktuelle Snapshot `${current.current_snapshot}` ist die erste
E-Auto-Candidate-Signal-Baseline. Die History-Struktur ist bereits angelegt,
damit spätere Imports sichtbar machen, was sich geändert hat.

```js
html`<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:0.75rem;margin:1rem 0">
  <div class="stat-card">
    <div class="stat-label">Candidate Topics</div>
    <div style="font-size:1.6rem;font-weight:650">${summary.candidate_ready_topic_count}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Candidate Signals</div>
    <div style="font-size:1.6rem;font-weight:650">${summary.signal_count}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Blocked Signals</div>
    <div style="font-size:1.6rem;font-weight:650">${summary.blocked_signal_count}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Buildable Surfaces</div>
    <div style="font-size:1.6rem;font-weight:650">${summary.web_buildable_now_count}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Suppressed Routes</div>
    <div style="font-size:1.6rem;font-weight:650">${summary.suppressed_route_count}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Snapshot Review</div>
    <div style="font-size:1.1rem;font-weight:650">${current.review_status}</div>
  </div>
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
  Gruppe: t.group,
  Tool: t.tool_type ?? "—",
  Quellen: `${t.official_source_count}/${t.source_count}`,
  Fakten: `${t.source_backed_fact_count}/${t.fact_count}`,
  Unbekannt: t.unknown_count,
  Route: t.route_policy ?? "—",
  CTA: t.cta_policy ?? "—",
  Claim: t.public_claim_wording ?? "—",
})), {rows: 20})
```

## Bridge And Context Topics

Bridge-Themen liefern Kontext für den E-Auto-Cluster. Sie werden nicht als
eigenständige Topic-Aussage hochgestuft.

```js
Inputs.table(bridgeTopics.map((t) => ({
  Topic: t.label,
  Status: t.review_status,
  Tool: t.tool_type ?? "—",
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
  Status: t.review_status,
  Gruppe: t.group,
  Tool: t.tool_type ?? "—",
  Route: t.route_policy ?? "—",
  CTA: t.cta_policy ?? "—",
  "Provider Evidence Excluded": t.provider_evidence_excluded ? "ja" : "nein",
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
  Typ: event.event_type,
  Topic: event.topic_slug ?? "Cluster",
  Feld: event.field,
  Vorher: event.previous_value ?? "—",
  Jetzt: event.current_value ?? "—",
  Schwere: event.severity,
})), {rows: 20})
```

## Provider Boundary

Provider-Zeilen können für Sales- oder Provider-Handoffs relevant sein. Für
AmtsScore-Evidence sind sie in diesem Snapshot ausgeschlossen.

```js
html`<div class="stat-card">
  <div class="stat-label">Provider Evidence Excluded</div>
  <div style="font-size:1.5rem;font-weight:650">${summary.provider_rows_used_as_evidence ? "nein" : "ja"}</div>
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

- Snapshot-Familie: `${current.snapshot_family}`
- History Model: `${current.history_model_version}`
- Current Pointer: `${current.current_snapshot_path}`
- Latest Diff: `${current.latest_diff_path}`
- Manifest-Snapshots: `${manifest.snapshots.length}`

Die Seite nutzt den Current Pointer. Ein Rollback kann daher auf einen älteren
Snapshot zeigen, ohne spätere Snapshot-Dateien zu löschen.
