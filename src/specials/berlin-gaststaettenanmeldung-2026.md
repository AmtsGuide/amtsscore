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
  ["1", "Vollständig digital", "1_end_to_end_digital"],
  ["2", "Authentifizierung (eID / BundID / Servicekonto)", "2_authentifizierung"],
  ["3", "Schema.org GovernmentService", "3_schema_org"],
  ["4", "Lighthouse-Mobilleistung ≥ 70", "4_lighthouse_mobile"],
  ["5", "Top-3 in Suchergebnissen für die kanonische Suchanfrage", "5_serp_top3"],
  ["6", "Stabile Permalinks (keine Sitzungs-IDs)", "6_stable_permalink"],
  ["7", "Pressereife / offizielle Kommunikation", "7_pressereife"],
  ["8", "Reproduzierbar für andere Städte", "8_reproduzierbar"],
];
```

```js
html`<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:0.75rem;margin:1rem 0">
  <div class="stat-card">
    <div class="stat-label" style="font-size:0.8rem">Dienst</div>
    <div style="font-weight:600">${data.service_short}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label" style="font-size:0.8rem">Stadt</div>
    <div style="font-weight:600">${data.stadt}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label" style="font-size:0.8rem">Verfügbar seit</div>
    <div style="font-weight:600">${data.live_seit}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label" style="font-size:0.8rem">Wert</div>
    <div style="font-weight:600">${data.summary.passed} / ${data.summary.max} ${data.summary.is_leuchtturm ? '⭐' : ''}</div>
  </div>
</div>`
```

**Dienst-URL:** ${data.url}
**Stand der Messung:** ${data.checked_at.slice(0,10)}.
**Leuchtturm-Stand:** ${data.summary.is_leuchtturm ? '⭐ Aufnahme (≥ 6/8 erfüllt)' : `nicht aufgenommen (${data.summary.passed}/8 erfüllt, Schwelle 6)`}.

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
      return Array.isArray(ev) && ev.length ? `Typen: ${ev.join(", ")}` : "keine Schema.org-Auszeichnung";
    case "4_lighthouse_mobile":
      return typeof ev === "number" ? `Wert ${ev}/100` : (c.passes === null ? "Messung ausstehend" : "");
    case "5_serp_top3":
      return ev && ev.position ? `Position ${ev.position} für „${ev.query}"` : "nicht unter den ersten 10";
    case "6_stable_permalink":
      if (!ev) return "";
      return ev.issues && ev.issues.length ? `Probleme: ${ev.issues.join(", ")}` : "saubere URL, keine Sitzungs-IDs";
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
    Stand: passIcon(data.checks[key].passes),
    Bewertung: passLabel(data.checks[key].passes),
    Befund: befund(key, data.checks[key]),
  })),
  {rows: 10, layout: "auto", width: {"#": 30, Stand: 60, Bewertung: 120}}
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

Die automatischen Prüfungen (1–6) laufen über das quelloffene Werkzeug im Repo unter
[`tools/leuchtturm/`](https://github.com/AmtsGuide/amtsscore/tree/main/tools/leuchtturm).
Kriterium 1 ist eine Keyword-Heuristik, nutzbar als notwendige Bedingung, nicht als hinreichender Beweis.
Kriterien 7 und 8 sind redaktionell und werden in
`tools/leuchtturm/services.yaml` als `pass` / `fail` / `pending` gepflegt.

## Korrekturen vorschlagen

Falls eine Aussage nicht stimmt oder eine Evidenz fehlt: Änderungsvorschlag auf
[GitHub](https://github.com/AmtsGuide/amtsscore) öffnen oder Mail an
`ad@blinktank.de`.
