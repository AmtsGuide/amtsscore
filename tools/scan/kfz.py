#!/usr/bin/env python3
"""KFZ-Zulassung deep scan, all tiers (no Lighthouse).

Pulls per-city KFZ data from AmtsGuide, then fetches each city's Termin-URL +
Stadt-Domain for site-level signals, then queries Brave Search for press-pain.

Output: src/data/kfz_enriched.json

Dimensions (0-10 each, equal-weighted composite):
  D-speed     Wartezeit (lower days = higher score)
  D-online    i-Kfz available (10 if yes, else 0)
  D-access    Standorte count (more standorte = higher)
  D-friction  Terminpflicht (10 if walk-in possible, 0 if appointment-only)
  D-auth      eID/BundID/BerlinID etc. on Termin-URL page
  D-schema    Schema.org GovernmentService markup on Termin-URL
  D-llmstxt   /llms.txt at Stadt-Domain (D11 proxy)
  D-https     Mozilla Observatory grade (A+→10, F→0)
  D-press     Brave Search press-pain mentions (inverse: fewer = better)
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent.parent
OUT = ROOT / "src" / "data" / "kfz_enriched.json"
UA = "Mozilla/5.0 (compatible; AmtsScore/0.1; +https://amtsscore.de)"

# Stadt slug -> main domain for llms.txt + Mozilla Observatory probes.
STADT_DOMAIN = {
    "berlin": "berlin.de", "hamburg": "hamburg.de", "muenchen": "muenchen.de",
    "koeln": "stadt-koeln.de", "frankfurt-am-main": "frankfurt.de",
    "stuttgart": "stuttgart.de", "duesseldorf": "duesseldorf.de",
    "leipzig": "leipzig.de", "dortmund": "dortmund.de", "essen": "essen.de",
    "bremen": "bremen.de", "dresden": "dresden.de", "hannover": "hannover.de",
    "bielefeld": "bielefeld.de", "bochum": "bochum.de", "bonn": "bonn.de",
    "duisburg": "duisburg.de", "muenster": "stadt-muenster.de",
    "nuernberg": "nuernberg.de", "wuppertal": "wuppertal.de",
}

OBS_GRADE_SCORE = {
    "A+": 10.0, "A": 9.0, "A-": 8.5,
    "B+": 7.5, "B": 7.0, "B-": 6.5,
    "C+": 5.5, "C": 5.0, "C-": 4.5,
    "D+": 3.5, "D": 3.0, "D-": 2.5,
    "F": 0.0,
}


def fetch_json(url, params=None, headers=None, timeout=30):
    r = requests.get(url, params=params,
                     headers={"User-Agent": UA, **(headers or {})},
                     timeout=timeout)
    r.raise_for_status()
    return r.json()


def fetch_text(url, timeout=20):
    r = requests.get(url, headers={"User-Agent": UA},
                     timeout=timeout, allow_redirects=True)
    r.raise_for_status()
    return r.text


def normalize(values, invert=False):
    present = [(i, v) for i, v in enumerate(values) if v is not None]
    if len(present) < 2:
        return {i: None for i in range(len(values))}
    vmin = min(v for _, v in present)
    vmax = max(v for _, v in present)
    span = vmax - vmin
    out = {i: None for i in range(len(values))}
    for i, v in present:
        if span == 0:
            out[i] = 10.0
        else:
            frac = (v - vmin) / span
            out[i] = round(10 * (1 - frac if invert else frac), 1)
    return out


def parse_days(text):
    if not text:
        return None
    s = str(text).lower()
    if "sofort" in s or "selben tag" in s:
        return 1
    if re.search(r"\bminuten?\b|\bmin\b", s):
        return 0
    m = re.search(r"(\d+)\s*(?:[-–]|bis(?:\s+zu)?)\s*(\d+)\s*(werktag|tage?|wochen?)", s)
    if m:
        a, b, u = int(m.group(1)), int(m.group(2)), m.group(3)
        avg = (a + b) / 2
        return int(avg * 7) if u.startswith("woche") else int(avg)
    m = re.search(r"(\d+)\s*(werktag|tage?|wochen?)", s)
    if m:
        n, u = int(m.group(1)), m.group(2)
        return n * 7 if u.startswith("woche") else n
    if "mehrere wochen" in s:
        return 21
    if "mehrere tage bis wochen" in s:
        return 14
    if "wenige tage" in s:
        return 3
    return None


# --- Tier 2 fetchers -----------------------------------------------------


def check_eid_buttons(html: str) -> tuple[bool, list[str]]:
    found = []
    for name, pat in [
        ("BundID", r"\bBundID\b"),
        ("BUND-ID", r"\bBUND[-\s]ID\b"),
        ("eID", r"\beID(?:\b|-Funktion|-Karte|-Service)"),
        ("Servicekonto", r"\bServicekonto\b"),
        ("BerlinID", r"\bBerlin[-]?ID\b"),
        ("BayernID", r"\bBayern[-]?ID\b"),
        ("NRW-Konto", r"\bNRW[-\s]?Konto\b"),
        ("Mein Unternehmenskonto", r"Mein\s+Unternehmenskonto"),
        ("AusweisApp", r"AusweisApp"),
    ]:
        if re.search(pat, html):
            found.append(name)
    return bool(found), found


def check_schema_org(html: str) -> tuple[bool, list[str]]:
    blocks = re.findall(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html, re.DOTALL | re.IGNORECASE,
    )
    types = []
    for b in blocks:
        try:
            data = json.loads(b.strip())
        except json.JSONDecodeError:
            continue
        for node in _flatten(data):
            t = node.get("@type")
            if isinstance(t, list):
                types.extend(t)
            elif isinstance(t, str):
                types.append(t)
    target = {"GovernmentService", "Service", "CivicStructure"}
    return bool(set(types) & target), sorted(set(types))


def _flatten(data):
    if isinstance(data, dict):
        yield data
        for v in data.values():
            yield from _flatten(v)
    elif isinstance(data, list):
        for v in data:
            yield from _flatten(v)


def check_llms_txt(domain: str) -> bool:
    try:
        r = requests.head(f"https://{domain}/llms.txt",
                          headers={"User-Agent": UA},
                          timeout=10, allow_redirects=True)
        return r.status_code == 200
    except Exception:
        return False


def mozilla_observatory(domain: str) -> tuple[str | None, int | None]:
    """Run a fresh scan + read result. Cached server-side, fast on repeat."""
    api = "https://http-observatory.security.mozilla.org/api/v1/analyze"
    try:
        requests.post(api, params={"host": domain, "hidden": "true"},
                      headers={"User-Agent": UA}, timeout=15)
        time.sleep(2)
        for _ in range(12):
            j = fetch_json(api, params={"host": domain}, timeout=15)
            state = j.get("state")
            if state == "FINISHED":
                return j.get("grade"), j.get("score")
            if state in {"FAILED", "ABORTED"}:
                return None, None
            time.sleep(5)
    except Exception as e:
        print(f"  ! observatory error for {domain}: {e}", file=sys.stderr)
    return None, None


# --- Tier 3: Brave Search press-pain ------------------------------------


def brave_press_pain(query: str) -> int | None:
    key = os.environ.get("BRAVE_API_KEY")
    if not key:
        return None
    try:
        r = requests.get(
            "https://api.search.brave.com/res/v1/web/search",
            params={"q": query, "country": "DE", "search_lang": "de", "count": 20},
            headers={"X-Subscription-Token": key, "Accept": "application/json"},
            timeout=20,
        )
        r.raise_for_status()
        return len(r.json().get("web", {}).get("results", []))
    except Exception as e:
        print(f"  ! brave error: {e}", file=sys.stderr)
        return None


# --- main ---------------------------------------------------------------


def main():
    print("== KFZ deep scan ==", file=sys.stderr)

    kfz = fetch_json("https://amtsguide.de/api/v1/calculator/kfz/results/")
    rows_in = [r for r in kfz["data"]["results"]
               if r["vorgang"] == "neuzulassung"]
    rows_by_slug = {r["citySlug"]: r for r in rows_in}

    cities = []
    for slug, r in rows_by_slug.items():
        print(f"  -> {slug}", file=sys.stderr)
        termin_url = (r.get("links") or {}).get("termin")
        stadt_domain = STADT_DOMAIN.get(slug)

        # Tier 1
        speed_raw = parse_days(r.get("wartezeit"))
        online = bool(r.get("ikfz"))
        standorte = len(r.get("standorte") or [])
        walk_in = not bool(r.get("terminpflicht"))

        # Tier 2
        has_eid, eid_evidence = False, []
        has_schema, schema_types = False, []
        if termin_url:
            try:
                html = fetch_text(termin_url)
                has_eid, eid_evidence = check_eid_buttons(html)
                has_schema, schema_types = check_schema_org(html)
            except Exception as e:
                print(f"    ! fetch {termin_url}: {e}", file=sys.stderr)

        has_llms = check_llms_txt(stadt_domain) if stadt_domain else False
        obs_grade, obs_score = (mozilla_observatory(stadt_domain)
                                if stadt_domain else (None, None))

        # Tier 3
        press_pain_count = brave_press_pain(
            f"{r['cityName']} KFZ-Zulassung wartezeit kritik"
        )

        cities.append({
            "slug": slug,
            "city": r["cityName"],
            "authority": r.get("behoerde"),
            "source_url": termin_url,
            "stadt_domain": stadt_domain,
            "raw": {
                "wartezeit_label": r.get("wartezeit"),
                "speed_days": speed_raw,
                "ikfz": online,
                "standorte_count": standorte,
                "terminpflicht": r.get("terminpflicht"),
                "eid_evidence": eid_evidence,
                "schema_types": schema_types,
                "llms_txt": has_llms,
                "observatory_grade": obs_grade,
                "observatory_score": obs_score,
                "press_pain_results": press_pain_count,
            },
            "_speed_raw": speed_raw,
            "_online_raw": online,
            "_standorte_raw": standorte,
            "_walk_in_raw": walk_in,
            "_eid_raw": has_eid,
            "_schema_raw": has_schema,
            "_llms_raw": has_llms,
            "_obs_raw": obs_score,
            "_press_raw": press_pain_count,
        })
        time.sleep(0.5)

    # normalize dimensions
    speed_n = normalize([c["_speed_raw"] for c in cities], invert=True)
    standorte_n = normalize([c["_standorte_raw"] for c in cities], invert=False)
    obs_n_raw = [c["_obs_raw"] for c in cities]
    obs_n = normalize(obs_n_raw, invert=False) if any(v is not None for v in obs_n_raw) else {i: None for i in range(len(cities))}
    press_n = normalize([c["_press_raw"] for c in cities], invert=True)

    for i, c in enumerate(cities):
        dims = {
            "speed":     speed_n[i],
            "online":    10.0 if c["_online_raw"] else 0.0,
            "access":    standorte_n[i],
            "friction":  10.0 if c["_walk_in_raw"] else 5.0,
            "auth":      10.0 if c["_eid_raw"] else 0.0,
            "schema":    10.0 if c["_schema_raw"] else 0.0,
            "llmstxt":   10.0 if c["_llms_raw"] else 0.0,
            "https":     OBS_GRADE_SCORE.get(c["raw"]["observatory_grade"]) if c["raw"]["observatory_grade"] else None,
            "press":     press_n[i],
        }
        present = [v for v in dims.values() if v is not None]
        c["dimensions"] = dims
        c["composite"] = round(sum(present) / len(present), 1) if present else None
        # strip internal _raw fields
        for k in [k for k in c if k.startswith("_")]:
            del c[k]

    cities.sort(key=lambda x: (x["composite"] is None, -(x["composite"] or 0)))
    for i, c in enumerate(cities, start=1):
        c["rank"] = i if c["composite"] is not None else None

    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "topic": "kfz-zulassung",
        "topic_label": "KFZ-Zulassung (Neuzulassung)",
        "n_cities": len(cities),
        "dimensions": [
            {"key": "speed",    "label": "Wartezeit",       "tier": 1, "invert": True},
            {"key": "online",   "label": "i-Kfz Online",    "tier": 1, "invert": False},
            {"key": "access",   "label": "Standorte",       "tier": 1, "invert": False},
            {"key": "friction", "label": "Walk-in möglich", "tier": 1, "invert": False},
            {"key": "auth",     "label": "eID-Anbindung",   "tier": 2, "invert": False},
            {"key": "schema",   "label": "Schema.org",      "tier": 2, "invert": False},
            {"key": "llmstxt",  "label": "llms.txt",        "tier": 2, "invert": False},
            {"key": "https",    "label": "HTTPS-Hygiene",   "tier": 2, "invert": False},
            {"key": "press",    "label": "Presse-Stille",   "tier": 3, "invert": True},
        ],
        "cities": cities,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"wrote {OUT.relative_to(ROOT)}: "
          f"{len(cities)} cities, 9 dimensions", file=sys.stderr)


if __name__ == "__main__":
    main()
