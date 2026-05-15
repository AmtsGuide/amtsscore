#!/usr/bin/env python3
"""Pre-AmtsScore deriver.

Reuses existing AmtsGuide Facts API data to score cities on Bürger-outcome
quality per topic. This is NOT the full AmtsScore (12 digital-performance
dimensions) but a useful precursor that says: how good is this Behördengang
for the citizen in this city today, based on cost / processing time / online
availability?

Score formula per (topic, city), 0-10:
  - cost component (40%): linear normalization, cheapest in topic = 10
  - speed component (40%): linear normalization, fastest in topic = 10
  - online component (20%): 10 if online-available, 0 if not, omitted if unknown

A topic with only cost data gets cost-weighted average. Missing metrics are
omitted from the topic's denominator, not penalized.

Output: src/data/prescore.json + per-topic JSON files.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUT = ROOT / "src" / "data" / "prescore.json"
API = "https://amtsguide.de/api/v1"
UA = "Mozilla/5.0 (compatible; AmtsScore/0.1)"

SLUG_ALIAS = {
    "frankfurt": "frankfurt-am-main",
    "halle": "halle-saale",
    "muelheim": "muelheim-an-der-ruhr",
}

CITY_DISPLAY = {
    "frankfurt-am-main": "Frankfurt am Main",
    "muenchen": "München",
    "koeln": "Köln",
    "duesseldorf": "Düsseldorf",
    "nuernberg": "Nürnberg",
    "muenster": "Münster",
    "saarbruecken": "Saarbrücken",
    "halle-saale": "Halle (Saale)",
    "muelheim-an-der-ruhr": "Mülheim an der Ruhr",
    "moenchengladbach": "Mönchengladbach",
}

# city slug -> Bundesland.
BUNDESLAND = {
    # Berlin / Hamburg / Bremen are city-states
    "berlin": "Berlin",
    "hamburg": "Hamburg",
    "bremen": "Bremen", "bremerhaven": "Bremen",
    # Bayern
    "muenchen": "Bayern", "nuernberg": "Bayern", "augsburg": "Bayern",
    "wuerzburg": "Bayern", "regensburg": "Bayern", "ingolstadt": "Bayern",
    "fuerth": "Bayern", "erlangen": "Bayern",
    # Baden-Württemberg
    "stuttgart": "Baden-Württemberg", "karlsruhe": "Baden-Württemberg",
    "mannheim": "Baden-Württemberg", "heidelberg": "Baden-Württemberg",
    "freiburg": "Baden-Württemberg", "ulm": "Baden-Württemberg",
    "heilbronn": "Baden-Württemberg", "pforzheim": "Baden-Württemberg",
    # Hessen
    "frankfurt-am-main": "Hessen", "wiesbaden": "Hessen",
    "kassel": "Hessen", "darmstadt": "Hessen", "offenbach": "Hessen",
    # NRW
    "koeln": "Nordrhein-Westfalen", "duesseldorf": "Nordrhein-Westfalen",
    "dortmund": "Nordrhein-Westfalen", "essen": "Nordrhein-Westfalen",
    "duisburg": "Nordrhein-Westfalen", "bochum": "Nordrhein-Westfalen",
    "wuppertal": "Nordrhein-Westfalen", "muenster": "Nordrhein-Westfalen",
    "bielefeld": "Nordrhein-Westfalen", "bonn": "Nordrhein-Westfalen",
    "gelsenkirchen": "Nordrhein-Westfalen", "krefeld": "Nordrhein-Westfalen",
    "aachen": "Nordrhein-Westfalen", "leverkusen": "Nordrhein-Westfalen",
    "oberhausen": "Nordrhein-Westfalen", "hagen": "Nordrhein-Westfalen",
    "moenchengladbach": "Nordrhein-Westfalen",
    "neuss": "Nordrhein-Westfalen", "paderborn": "Nordrhein-Westfalen",
    "recklinghausen": "Nordrhein-Westfalen", "solingen": "Nordrhein-Westfalen",
    "herne": "Nordrhein-Westfalen", "muelheim-an-der-ruhr": "Nordrhein-Westfalen",
    "siegen": "Nordrhein-Westfalen",
    # Sachsen
    "leipzig": "Sachsen", "dresden": "Sachsen", "chemnitz": "Sachsen",
    # Sachsen-Anhalt
    "magdeburg": "Sachsen-Anhalt", "halle-saale": "Sachsen-Anhalt",
    # Thüringen
    "erfurt": "Thüringen", "jena": "Thüringen",
    # Mecklenburg-Vorpommern
    "rostock": "Mecklenburg-Vorpommern", "schwerin": "Mecklenburg-Vorpommern",
    # Schleswig-Holstein
    "kiel": "Schleswig-Holstein", "luebeck": "Schleswig-Holstein",
    # Niedersachsen
    "hannover": "Niedersachsen", "braunschweig": "Niedersachsen",
    "oldenburg": "Niedersachsen", "osnabrueck": "Niedersachsen",
    "wolfsburg": "Niedersachsen", "goettingen": "Niedersachsen",
    # Rheinland-Pfalz
    "mainz": "Rheinland-Pfalz", "ludwigshafen": "Rheinland-Pfalz",
    "koblenz": "Rheinland-Pfalz", "trier": "Rheinland-Pfalz",
    # Saarland
    "saarbruecken": "Saarland",
    # Brandenburg
    "potsdam": "Brandenburg", "cottbus": "Brandenburg",
}


def canon_slug(slug: str) -> str:
    return SLUG_ALIAS.get(slug, slug)


def fetch(path: str) -> dict:
    r = requests.get(f"{API}{path}", headers={"User-Agent": UA}, timeout=30)
    r.raise_for_status()
    return r.json()["data"]


def parse_days(text: str | None) -> int | None:
    if not text:
        return None
    if isinstance(text, (int, float)):
        return int(text)
    s = str(text).lower()
    # "etwa 14 Tage", "5-10 Tage", "mehrere Wochen bis zu 10 Wochen"
    m = re.search(r"(\d+)\s*[-–bis]+\s*(\d+)\s*(tage?|wochen?)", s)
    if m:
        a, b, unit = int(m.group(1)), int(m.group(2)), m.group(3)
        avg = (a + b) / 2
        return int(avg * 7) if unit.startswith("woche") else int(avg)
    m = re.search(r"(\d+)\s*(tage?|wochen?)", s)
    if m:
        n, unit = int(m.group(1)), m.group(2)
        return n * 7 if unit.startswith("woche") else n
    return None


def parse_eur(text) -> float | None:
    if text is None:
        return None
    if isinstance(text, (int, float)):
        return float(text)
    s = str(text).replace(".", "").replace(",", ".")
    m = re.search(r"(\d+(?:\.\d+)?)", s)
    return float(m.group(1)) if m else None


def normalize(values: list[float | None], invert: bool = True) -> dict[int, float | None]:
    """Linear 0-10 normalization. invert=True → lower input = higher score."""
    present = [(i, v) for i, v in enumerate(values) if v is not None]
    if len(present) < 2:
        return {i: None for i in range(len(values))}
    vmin = min(v for _, v in present)
    vmax = max(v for _, v in present)
    span = vmax - vmin
    out: dict[int, float | None] = {i: None for i in range(len(values))}
    for i, v in present:
        if span == 0:
            out[i] = 10.0
        else:
            frac = (v - vmin) / span
            out[i] = round(10 * (1 - frac if invert else frac), 1)
    return out


def gather_halteverbot() -> list[dict]:
    data = fetch("/calculator/halteverbot/")
    rows = []
    for slug, loc in data["locations"].items():
        rows.append({
            "city_slug": slug,
            "city": loc["name"],
            "_speed_raw": loc.get("processing_days"),
            "_cost_raw": loc.get("cost_min"),
            "_online_raw": None,
        })
    return rows


def gather_kfz() -> list[dict]:
    data = fetch("/calculator/kfz/results/")
    by_city: dict[str, dict] = {}
    for r in data["results"]:
        if r["vorgang"] != "neuzulassung":
            continue
        slug = r["citySlug"]
        if slug in by_city:
            continue
        gebuehr_amt = parse_eur(r.get("gebuehr", {}).get("amt"))
        gebuehr_online = parse_eur(r.get("gebuehr", {}).get("online"))
        cost = gebuehr_online or gebuehr_amt
        by_city[slug] = {
            "city_slug": slug,
            "city": r["cityName"],
            "_speed_raw": parse_days(r.get("wartezeit")),
            "_cost_raw": cost,
            "_online_raw": bool(r.get("ikfz")),
        }
    return list(by_city.values())


def gather_gmbh() -> list[dict]:
    data = fetch("/calculator/gmbh/results/")
    by_city: dict[str, dict] = {}
    for r in data["results"]:
        if r["gesellschaftsvertrag"] != "muster":
            continue
        slug = r["citySlug"]
        if slug in by_city:
            continue
        by_city[slug] = {
            "city_slug": slug,
            "city": slug.title(),
            "_speed_raw": parse_days(r.get("processingTime")),
            "_cost_raw": r.get("totalMin"),
            "_online_raw": bool(r.get("onlineAvailable")),
        }
    return list(by_city.values())


def score_topic(slug: str, label: str, rows: list[dict]) -> dict:
    speed_norm = normalize([r["_speed_raw"] for r in rows], invert=True)
    cost_norm = normalize([r["_cost_raw"] for r in rows], invert=True)

    scored = []
    for i, r in enumerate(rows):
        s = speed_norm[i]
        c = cost_norm[i]
        o = (10.0 if r["_online_raw"] else 0.0) if r["_online_raw"] is not None else None

        weights = []
        comps = []
        if s is not None:
            weights.append(0.4)
            comps.append(0.4 * s)
        if c is not None:
            weights.append(0.4)
            comps.append(0.4 * c)
        if o is not None:
            weights.append(0.2)
            comps.append(0.2 * o)

        if not weights:
            total = None
        else:
            total = round(sum(comps) / sum(weights), 1)

        scored.append({
            "city": r["city"],
            "city_slug": r["city_slug"],
            "bundesland": BUNDESLAND.get(r["city_slug"]),
            "score": total,
            "speed": s,
            "cost": c,
            "online": o,
            "raw": {
                "speed_days": r["_speed_raw"],
                "cost_eur": r["_cost_raw"],
                "online_available": r["_online_raw"],
            },
        })

    scored.sort(key=lambda x: (x["score"] is None, -(x["score"] or 0)))
    for i, row in enumerate(scored, start=1):
        row["rank"] = i if row["score"] is not None else None
    return {"slug": slug, "label": label, "n_cities": len(scored), "cities": scored}


def main():
    topics = [
        ("halteverbot", "Halteverbot", gather_halteverbot),
        ("kfz-zulassung", "KFZ-Zulassung (Neuzulassung)", gather_kfz),
        ("gmbh-gruendung", "GmbH-Gründung (Mustervertrag)", gather_gmbh),
    ]

    all_topics = []
    by_slug: dict[str, dict] = {}  # canonical slug -> {scores: [..], display: str}

    for slug, label, fn in topics:
        print(f"  -> {slug}", file=sys.stderr)
        rows = fn()
        for r in rows:
            r["city_slug"] = canon_slug(r["city_slug"])
            r["city"] = CITY_DISPLAY.get(r["city_slug"], r["city"])
        scored = score_topic(slug, label, rows)
        all_topics.append(scored)
        for c in scored["cities"]:
            if c["score"] is None:
                continue
            entry = by_slug.setdefault(c["city_slug"],
                                       {"display": c["city"], "scores": []})
            entry["scores"].append(c["score"])

    summary = [
        {"city": v["display"], "city_slug": k,
         "bundesland": BUNDESLAND.get(k),
         "topic_count": len(v["scores"]),
         "avg_score": round(sum(v["scores"]) / len(v["scores"]), 1)}
        for k, v in by_slug.items()
    ]
    summary.sort(key=lambda x: (-x["topic_count"], -x["avg_score"]))
    for i, row in enumerate(summary, start=1):
        row["rank"] = i

    by_state: dict[str, list[float]] = {}
    for t in all_topics:
        for c in t["cities"]:
            if c["score"] is None or not c.get("bundesland"):
                continue
            by_state.setdefault(c["bundesland"], []).append(c["score"])
    state_summary = [
        {"bundesland": st, "n_datapoints": len(scs),
         "avg_score": round(sum(scs) / len(scs), 1)}
        for st, scs in by_state.items()
    ]
    state_summary.sort(key=lambda x: -x["avg_score"])
    for i, row in enumerate(state_summary, start=1):
        row["rank"] = i

    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": "AmtsGuide Facts API",
        "topics": all_topics,
        "city_summary": summary,
        "state_summary": state_summary,
        "method": "Bürger-Outcome-Pre-Score: 40% cost + 40% speed + 20% online availability, linear normalization per topic.",
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"wrote {OUTPUT.relative_to(ROOT)}: "
          f"{len(all_topics)} topics, {len(summary)} cities", file=sys.stderr)


if __name__ == "__main__":
    main()
