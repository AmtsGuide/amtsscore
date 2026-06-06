---
title: AmtsScore
toc: false
---

<style>
.hero {
  background: var(--theme-background-alt);
  color: var(--theme-foreground);
  padding: 4rem 2rem;
  border-radius: 12px;
  margin-bottom: 2rem;
  border: 1px solid var(--theme-foreground-faintest);
}
.hero h1 { font-size: 3rem; margin: 0 0 1rem 0; color: var(--theme-foreground); }
.hero p { font-size: 1.25rem; margin: 0; max-width: 60ch; color: var(--theme-foreground-muted); }
.tag {
  display: inline-block;
  background: var(--theme-foreground-faintest);
  color: var(--theme-foreground-muted);
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-size: 0.85rem;
  margin-bottom: 1rem;
}
.cta-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
  margin: 2rem 0;
}
/* .cta-card colors defined globally in style.css (use theme vars) */
.cta-card { padding: 1.5rem; }
.cta-card h3 { margin-top: 0; color: inherit; }
.cta-card p { color: var(--theme-foreground-muted); }
.cta-card a { color: var(--theme-foreground-focus); font-weight: 600; }
.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 0.75rem;
  margin: 1.25rem 0 2rem;
}
.summary-card {
  border: 1px solid var(--theme-foreground-faintest);
  border-radius: 8px;
  padding: 1rem;
  background: var(--theme-background);
}
.summary-label {
  color: var(--theme-foreground-muted);
  font-size: 0.8rem;
  margin-bottom: 0.35rem;
}
.summary-value {
  font-size: 1.7rem;
  line-height: 1;
  font-weight: 700;
}
.news-list {
  display: grid;
  gap: 0.75rem;
  margin: 1rem 0 2rem;
}
.news-item {
  border-left: 3px solid var(--theme-foreground-focus);
  padding: 0.75rem 1rem;
  background: var(--theme-background-alt);
}
.news-item h3 {
  margin: 0 0 0.35rem;
  font-size: 1rem;
}
.news-item p {
  margin: 0;
  color: var(--theme-foreground-muted);
}
</style>

```js
const prescore = await FileAttachment("data/prescore.json").json();
const eauto = await FileAttachment("data/eauto_prescore.json").json();
const eautoHistory = await FileAttachment("data/history/eauto/index.json").json();
const prescoreTopicCount = prescore.topics.length;
const prescoreCityCount = prescore.city_summary.length;
const prescoreStateCount = prescore.state_summary.length;
const eautoSummary = eauto.summary;
```

<div class="hero">
  <div class="tag">v0 / Pre-Launch</div>
  <h1>Wie digital ist die deutsche Verwaltung wirklich?</h1>
  <p>AmtsScore misst die digitale Performance deutscher Verwaltungs-Websites. Quartalsweise, datenbasiert, methodisch offen.</p>
</div>

## Status

AmtsScore befindet sich in **öffentlicher Methodik-Kommentierung**. Die [Methodik v0.1](/methodology) liegt zur Diskussion vor. Erste vollständige Messung der 20 deutschen Großstädte erwartet **Q3/2026**.

In der Zwischenzeit zeigen wir aus bestehenden AmtsGuide-Daten erste **Topic-Auswertungen**. Behördengang-Daten pro Stadt, ohne AmtsScore-Bewertung.

## Aktueller Stand

```js
html`<div class="summary-grid">
  <div class="summary-card">
    <div class="summary-label">Topic-Auswertungen</div>
    <div class="summary-value">${prescoreTopicCount}</div>
    <p style="margin:0.5rem 0 0;color:var(--theme-foreground-muted)">Halteverbot, Kfz-Zulassung, GmbH-Gründung</p>
  </div>
  <div class="summary-card">
    <div class="summary-label">Städte mit Pre-Score-Daten</div>
    <div class="summary-value">${prescoreCityCount}</div>
    <p style="margin:0.5rem 0 0;color:var(--theme-foreground-muted)">${prescoreStateCount} Bundesländer abgedeckt</p>
  </div>
  <div class="summary-card">
    <div class="summary-label">E-Auto Candidate Topics</div>
    <div class="summary-value">${eautoSummary.candidate_ready_topic_count}</div>
    <p style="margin:0.5rem 0 0;color:var(--theme-foreground-muted)">${eautoSummary.signal_count} Candidate Signals</p>
  </div>
  <div class="summary-card">
    <div class="summary-label">E-Auto Preview Surfaces</div>
    <div class="summary-value">${eautoSummary.web_buildable_now_count}</div>
    <p style="margin:0.5rem 0 0;color:var(--theme-foreground-muted)">Provider Evidence ausgeschlossen</p>
  </div>
</div>`
```

## Neueste Änderungen

<div class="news-list">
  <div class="news-item">
    <h3>2026-06-06 · E-Auto Candidate Signals ergänzt</h3>
    <p>Neue Preview-Seite für E-Auto: Candidate Signals, Source Coverage, Fact Coverage, Unknown Counts und Provider-Grenze im Methodology Review.</p>
  </div>
  <div class="news-item">
    <h3>2026-06-04 · Erste E-Auto-History-Baseline</h3>
    <p>Der erste Snapshot enthält 19 candidate-ready Topics, 133 Candidate Signals, 0 blocked Signals und 12 buildable Preview Surfaces.</p>
  </div>
  <div class="news-item">
    <h3>2026-05-20 · Observable-Datenstand gesichert</h3>
    <p>Die bestehende AmtsScore-Datenlage wurde als Baseline festgehalten, damit spätere Änderungen gegen den vorherigen Stand vergleichbar bleiben.</p>
  </div>
</div>

<div class="cta-grid">
  <div class="cta-card">
    <h3>Methodik</h3>
    <p>Die 10 Dimensionen, mit denen AmtsScore misst. Öffentlich, reproduzierbar, in Kommentierung.</p>
    <p><a href="/methodology">Methodik v0.1 →</a></p>
  </div>
  <div class="cta-card">
    <h3>Topic-Daten</h3>
    <p>Pre-AmtsScore-Auswertung: was kostet ein Halteverbot wo? Wie lange dauert die Bearbeitung? Wie schneiden Städte im Vergleich ab?</p>
    <p><a href="/topics/halteverbot">Halteverbot-Topographie →</a></p>
  </div>
  <div class="cta-card">
    <h3>E-Auto Candidate Signals</h3>
    <p>Preview der E-Auto-Quellenlage: Candidate Signals, Abdeckung, Unbekannte und Provider-Grenze im Methodology Review.</p>
    <p><a href="/topics/e-auto">E-Auto-Preview →</a></p>
  </div>
  <div class="cta-card">
    <h3>Leuchttürme</h3>
    <p>Service-Launches, die zeigen wie es geht. Berlin Gaststätten 2026, mehr in Recherche.</p>
    <p><a href="/specials/">Leuchttürme →</a></p>
  </div>
  <div class="cta-card">
    <h3>Über AmtsScore</h3>
    <p>Eine Initiative von AmtsGuide, German Innovation Award Winner 2026 (B2C E-Business).</p>
    <p><a href="/ueber">Mehr →</a></p>
  </div>
</div>

## Was unterscheidet AmtsScore?

Andere Reports messen *Themen* (Trendradar, ThemenRadar) oder *Bürger-Befindlichkeit* (eGovernment Monitor). Niemand misst kontinuierlich, was tatsächlich auf den Verwaltungs-Websites passiert. **AmtsScore schließt diese Lücke.**

- **Datengetrieben**: kein Survey, keine Selbstauskunft
- **Reproduzierbar**. Methodik öffentlich, Daten downloadbar (CC BY 4.0)
- **Quartalsweise**. Veränderung wird sichtbar
- **Bürger-Perspektive**: was sieht die Bürger:in, nicht was meldet die IT
