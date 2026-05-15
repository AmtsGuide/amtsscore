#!/usr/bin/env python3
"""AmtsScore Leuchtturm checker.

Runs the 8 Leuchtturm criteria against a single service URL and writes
src/data/specials/<slug>.json.

Usage:
  python tools/leuchtturm/check.py --slug berlin-gaststaettenanmeldung-2026
  python tools/leuchtturm/check.py --all

Env (optional, improves checks 4 + 5):
  BRAVE_API_KEY            for SERP top-3 check (criterion 5)
  GOOGLE_PAGESPEED_API_KEY for Lighthouse mobile score (criterion 4)
                           Optional. PSI works without a key at low volume.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.parse
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path

import requests
import yaml

ROOT = Path(__file__).resolve().parent.parent.parent
REGISTRY = Path(__file__).parent / "services.yaml"
OUTPUT_DIR = ROOT / "src" / "data" / "specials"
UA = "Mozilla/5.0 (compatible; AmtsScore/0.1; +https://amtsscore.de)"


@dataclass
class CheckResult:
    passes: bool | None
    evidence: object = None
    note: str = ""

    def as_dict(self) -> dict:
        return {"passes": self.passes, "evidence": self.evidence, "note": self.note}


def fetch(url: str, timeout: int = 20) -> tuple[requests.Response, str]:
    r = requests.get(url, headers={"User-Agent": UA}, timeout=timeout, allow_redirects=True)
    r.raise_for_status()
    return r, r.text


def check_end_to_end_digital(html: str, base_url: str) -> CheckResult:
    """Criterion 1: end-to-end digital. Look for online application affordances."""
    signals = [
        r"online[\s-]?antrag",
        r"online beantragen",
        r"antrag(?:\s+stellen)?\s+online",
        r"formularserver",
        r"antragsmanagement",
        r"ego[-_]portal",
        r"servicekonto",
        r"jetzt online",
        r"online[-\s]?dienst",
    ]
    found = []
    for s in signals:
        m = re.search(s, html, re.IGNORECASE)
        if m:
            found.append(m.group(0).lower().strip())
    found = sorted(set(found))
    return CheckResult(passes=bool(found), evidence=found,
                       note="signal heuristic; manual verify needed for true e2e")


def check_authentifizierung(html: str) -> CheckResult:
    """Criterion 2: federated identity (eID / BundID / Servicekonto)."""
    patterns = {
        "BundID": r"\bBundID\b",
        "BUND-ID": r"\bBUND[-\s]ID\b",
        "eID": r"\beID(?:\b|-Funktion|-Karte|-Service)",
        "Servicekonto": r"\bServicekonto\b",
        "BerlinID": r"\bBerlin[-]?ID\b",
        "BayernID": r"\bBayern[-]?ID\b",
        "NRW-Konto": r"\bNRW[-\s]?Konto\b",
        "Nutzerkonto Bund": r"Nutzerkonto\s+Bund",
        "Mein Unternehmenskonto": r"Mein\s+Unternehmenskonto",
    }
    found = []
    for name, pat in patterns.items():
        if re.search(pat, html):
            found.append(name)
    return CheckResult(passes=bool(found), evidence=found)


def check_schema_org(html: str) -> CheckResult:
    """Criterion 3: Schema.org GovernmentService / Service markup."""
    blocks = re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
                        html, re.DOTALL | re.IGNORECASE)
    types_found = []
    for b in blocks:
        try:
            data = json.loads(b.strip())
        except json.JSONDecodeError:
            continue
        for node in _flatten(data):
            t = node.get("@type")
            if isinstance(t, list):
                types_found.extend(t)
            elif isinstance(t, str):
                types_found.append(t)
    types_found = sorted(set(types_found))
    target = {"GovernmentService", "Service", "CivicStructure"}
    return CheckResult(passes=bool(set(types_found) & target),
                       evidence=types_found,
                       note=f"{len(blocks)} JSON-LD blocks parsed")


def _flatten(data):
    if isinstance(data, dict):
        yield data
        for v in data.values():
            yield from _flatten(v)
    elif isinstance(data, list):
        for v in data:
            yield from _flatten(v)


def check_lighthouse_mobile(url: str) -> CheckResult:
    """Criterion 4: PageSpeed Insights mobile performance ≥ 70."""
    api = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    params = {
        "url": url,
        "strategy": "mobile",
        "category": "PERFORMANCE",
    }
    key = os.environ.get("GOOGLE_PAGESPEED_API_KEY")
    if key:
        params["key"] = key
    try:
        r = requests.get(api, params=params, timeout=60)
        r.raise_for_status()
        data = r.json()
        score = data["lighthouseResult"]["categories"]["performance"]["score"]
        score_pct = round(score * 100)
        return CheckResult(passes=score_pct >= 70, evidence=score_pct,
                           note="PSI mobile performance score (0-100)")
    except Exception as e:
        return CheckResult(passes=None, evidence=None, note=f"PSI error: {e}")


def check_serp(query: str, target_domain: str) -> CheckResult:
    """Criterion 5: Top-3 SERP position via Brave Search API."""
    key = os.environ.get("BRAVE_API_KEY")
    if not key:
        return CheckResult(passes=None, evidence=None, note="BRAVE_API_KEY missing")
    try:
        r = requests.get(
            "https://api.search.brave.com/res/v1/web/search",
            params={"q": query, "country": "DE", "search_lang": "de"},
            headers={"X-Subscription-Token": key, "Accept": "application/json"},
            timeout=20,
        )
        r.raise_for_status()
        results = r.json().get("web", {}).get("results", [])
        position = None
        for i, res in enumerate(results[:10], start=1):
            host = urllib.parse.urlparse(res.get("url", "")).hostname or ""
            if target_domain.lower() in host.lower():
                position = i
                break
        return CheckResult(
            passes=position is not None and position <= 3,
            evidence={"position": position, "query": query, "domain": target_domain},
            note="Brave Search top-10",
        )
    except Exception as e:
        return CheckResult(passes=None, evidence=None, note=f"Brave error: {e}")


def check_stable_permalink(url: str, response_url: str) -> CheckResult:
    """Criterion 6: no session IDs, no hash routes, redirect to canonical form."""
    issues = []
    parsed = urllib.parse.urlparse(response_url)
    if ";jsessionid=" in response_url.lower():
        issues.append("jsessionid")
    qs = urllib.parse.parse_qs(parsed.query)
    for bad in ("sid", "session", "phpsessid", "asp.net_sessionid"):
        if bad in {k.lower() for k in qs}:
            issues.append(bad)
    if "#/" in response_url or "#!" in response_url:
        issues.append("hash-route")
    if url != response_url and parsed.path != urllib.parse.urlparse(url).path:
        issues.append(f"redirected: {url} -> {response_url}")
    return CheckResult(passes=not issues, evidence={"final_url": response_url, "issues": issues})


def run_one(svc: dict) -> dict:
    print(f"  -> fetching {svc['url']}", file=sys.stderr)
    r, html = fetch(svc["url"])

    target_domain = urllib.parse.urlparse(svc["url"]).hostname

    checks = {
        "1_end_to_end_digital": check_end_to_end_digital(html, svc["url"]).as_dict(),
        "2_authentifizierung": check_authentifizierung(html).as_dict(),
        "3_schema_org": check_schema_org(html).as_dict(),
        "4_lighthouse_mobile": check_lighthouse_mobile(svc["url"]).as_dict(),
        "5_serp_top3": check_serp(svc["serp_query"], target_domain).as_dict(),
        "6_stable_permalink": check_stable_permalink(svc["url"], r.url).as_dict(),
        "7_pressereife": {"passes": svc.get("pressereife") == "pass",
                          "evidence": svc.get("pressereife", "pending"),
                          "note": "manual"},
        "8_reproduzierbar": {"passes": svc.get("reproduzierbar") == "pass",
                             "evidence": svc.get("reproduzierbar", "pending"),
                             "note": "manual"},
    }

    passed = sum(1 for c in checks.values() if c["passes"] is True)
    return {
        "slug": svc["slug"],
        "stadt": svc["stadt"],
        "bundesland": svc["bundesland"],
        "service": svc["service"],
        "service_short": svc.get("service_short", svc["service"]),
        "url": svc["url"],
        "live_seit": svc["live_seit"],
        "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "checks": checks,
        "summary": {"passed": passed, "max": 8, "threshold": 6,
                    "is_leuchtturm": passed >= 6},
    }


def load_services() -> list[dict]:
    return yaml.safe_load(REGISTRY.read_text())["services"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", help="single service slug")
    ap.add_argument("--all", action="store_true", help="run all services in services.yaml")
    args = ap.parse_args()

    services = load_services()
    if args.all:
        targets = services
    elif args.slug:
        targets = [s for s in services if s["slug"] == args.slug]
        if not targets:
            sys.exit(f"slug not found in services.yaml: {args.slug}")
    else:
        ap.print_help()
        sys.exit(2)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for svc in targets:
        print(f"== {svc['slug']} ==", file=sys.stderr)
        result = run_one(svc)
        out = OUTPUT_DIR / f"{svc['slug']}.json"
        out.write_text(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"   wrote {out.relative_to(ROOT)} "
              f"({result['summary']['passed']}/8 passed)", file=sys.stderr)
        time.sleep(1)


if __name__ == "__main__":
    main()
