---
title: "Berlin: Gaststättenanmeldung 2026"
toc: true
---

# Berlin: Gaststättenanmeldung 2026

```js
const data = await FileAttachment("../data/specials/berlin-gaststaettenanmeldung-2026.json").json();
```

```js
const passIcon = (v) => v === true ? "✅" : v === false ? "❌" : "⏳";
const passLabel = (v) => v === true ? "erfüllt" : v === false ? "nicht erfüllt" : "ausstehend";
const criteria = [
  ["1", "End-to-end digital", "1_end_to_end_digital"],
  ["2", "Authentifizierung (eID / BundID / Servicekonto)", "2_authentifizierung"],
  ["3", "Schema.org GovernmentService", "3_schema_org"],
  ["4", "Lighthouse Mobile Performance ≥ 70", "4_lighthouse_mobile"],
  ["5", "SERP Top-3 für canonical query", "5_serp_top3"],
  ["6", "Stabile Permalinks (keine Session-IDs)", "6_stable_permalink"],
  ["7", "Pressereife / offizielle Kommunikation", "7_pressereife"],
  ["8", "Reproduzierbar für andere Städte", "8_reproduzierbar"],
];
```

```js
html`<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:0.75rem;margin:1rem 0">
  <div class="stat-card">
    <div class="stat-label" style="font-size:0.8rem">Service</div>
    <div style="font-weight:600">${data.service_short}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label" style="font-size:0.8rem">Stadt</div>
    <div style="font-weight:600">${data.stadt}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label" style="font-size:0.8rem">Live seit</div>
    <div style="font-weight:600">${data.live_seit}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label" style="font-size:0.8rem">Score</div>
    <div style="font-weight:600">${data.summary.passed} / ${data.summary.max} ${data.summary.is_leuchtturm ? '⭐' : ''}</div>
  </div>
</div>`
```

**Service-URL:** ${data.url}
**Stand der Messung:** ${data.checked_at.slice(0,10)}.
**Leuchtturm-Status:** ${data.summary.is_leuchtturm ? '⭐ Aufnahme (≥ 6/8 erfüllt)' : `nicht aufgenommen (${data.summary.passed}/8 erfüllt, Schwelle 6)`}.

## 8-Kriterien-Bewertung

```js
function befund(key, c) {
  const ev = c.evidence;
  switch (key) {
    case "1_end_to_end_digital":
      return Array.isArray(ev) && ev.length ? `Signale: ${ev.join(", ")}` : "keine Online-Antrags-Signale";
    case "2_authentifizierung":
      return Array.isArray(ev) && ev.length ? ev.join(", ") : "keine Anbindung sichtbar";
    case "3_schema_org":
      return Array.isArray(ev) && ev.length ? `Typen: ${ev.join(", ")}` : "kein Schema.org-Markup";
    case "4_lighthouse_mobile":
      return typeof ev === "number" ? `Score ${ev}/100` : (c.passes === null ? "Messung ausstehend" : "");
    case "5_serp_top3":
      return ev && ev.position ? `Position ${ev.position} für „${ev.query}"` : "nicht in den Top-10";
    case "6_stable_permalink":
      if (!ev) return "";
      return ev.issues && ev.issues.length ? `Probleme: ${ev.issues.join(", ")}` : "saubere URL, keine Session-IDs";
    case "7_pressereife":
    case "8_reproduzierbar":
      return ev === "pass" ? "verifiziert" : ev === "fail" ? "nicht erfüllt" : "redaktionell ausstehend";
    default:
      return "";
  }
}
```

```js
Inputs.table(
  criteria.map(([n, label, key]) => ({
    "#": n,
    Kriterium: label,
    Status: passIcon(data.checks[key].passes),
    Bewertung: passLabel(data.checks[key].passes),
    Befund: befund(key, data.checks[key]),
  })),
  {rows: 10, layout: "auto", width: {"#": 30, Status: 60, Bewertung: 120}}
)
```

## Was die Daten zeigen

```js
const passed = criteria.filter(([n,l,k]) => data.checks[k].passes === true).map(([n,l,k]) => l);
const failed = criteria.filter(([n,l,k]) => data.checks[k].passes === false).map(([n,l,k]) => l);
const pending = criteria.filter(([n,l,k]) => data.checks[k].passes === null).map(([n,l,k]) => l);
```

```js
html`
${passed.length ? html`<p><strong>Erfüllt:</strong> ${passed.join(' · ')}</p>` : ''}
${failed.length ? html`<p><strong>Nicht erfüllt:</strong> ${failed.join(' · ')}</p>` : ''}
${pending.length ? html`<p><strong>Ausstehend:</strong> ${pending.join(' · ')}</p>` : ''}
`
```

## Methodische Anmerkungen

Die automatischen Checks (1–6) laufen über das Open-Source-Tool im Repo unter
[`tools/leuchtturm/`](https://github.com/AmtsGuide/amtsscore/tree/main/tools/leuchtturm).
Kriterium 1 ist eine Keyword-Heuristik, nutzbar als notwendige Bedingung, nicht als hinreichender Beweis.
Kriterien 7 und 8 sind redaktionell und werden in
`tools/leuchtturm/services.yaml` als `pass` / `fail` / `pending` gepflegt.

## Korrekturen vorschlagen

Falls eine Aussage nicht stimmt oder eine Evidenz fehlt: Pull Request auf
[GitHub](https://github.com/AmtsGuide/amtsscore) öffnen oder Mail an
`ad@blinktank.de`.
