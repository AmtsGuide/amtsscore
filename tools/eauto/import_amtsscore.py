#!/usr/bin/env python3
"""Import E-Auto AmtsScore candidate signals into Observable data history."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SCRAPER_OUTPUT = Path("/Users/andx/codex_scraper/output")
CLUSTER_ROOT = SCRAPER_OUTPUT / "intake-clusters" / "eauto"

GENERATED_BY = "tools/eauto/import_amtsscore.py"
HISTORY_MODEL_VERSION = "1.0"
SNAPSHOT_FAMILY = "eauto_candidate_signals"
ACCEPTED_CONTRACT_MAJOR_VERSIONS = {"1"}
SNAPSHOT_REVIEW_STATUS = "editor_review_required"

DIFF_EVENT_TYPES = {
    "baseline_established",
    "topic_added",
    "topic_removed",
    "topic_group_changed",
    "topic_status_changed",
    "buildable_state_changed",
    "route_policy_changed",
    "cta_policy_changed",
    "blocker_count_changed",
    "provider_boundary_changed",
    "official_source_count_changed",
    "source_backed_fact_count_changed",
    "unknown_count_changed",
    "informational_change",
}

TOPIC_GROUPS = {
    "core",
    "bridge",
    "not_surfaceable",
    "provider_only",
    "suppressed",
}

VISUAL_ROLLUP_FIELDS = {
    "candidate_ready_topic_count",
    "signal_count",
    "blocked_signal_count",
    "web_buildable_now_count",
    "suppressed_route_count",
}

TOPIC_LABELS = {
    "e-auto-foerderung": "E-Auto-Förderung",
    "wallbox-foerderung": "Wallbox-Förderung",
    "kfz-zulassung": "Kfz-Zulassung",
    "thg-quote": "THG-Quote",
    "kfz-steuer": "Kfz-Steuer",
    "e-auto-laden": "E-Auto laden",
    "wallbox-installation": "Wallbox-Installation",
    "ladestation": "Ladestation",
    "ladesaeule": "Ladesäule",
    "ladeinfrastruktur": "Ladeinfrastruktur",
    "e-kennzeichen": "E-Kennzeichen",
    "umweltbonus": "Umweltbonus",
    "pv-wallbox": "PV-Wallbox",
    "solarstrom-auto-laden": "Solarstrom fürs Auto",
    "solaranlage": "Solaranlage",
    "energieberater": "Energieberater",
    "solarteur": "Solarteur",
    "e-auto-versicherung": "E-Auto-Versicherung",
    "gebrauchtwagen-eauto-foerderung": "Gebrauchtwagen-E-Auto-Förderung",
    "supplier-pool-e-autohaendler": "E-Auto-Händler-Pool",
}

LIVE_DATA_URLS = {
    "prescore": "https://amtsscore.de/_file/data/prescore.3200aa04.json",
    "halteverbot": "https://amtsscore.de/_file/data/halteverbot.c734c525.json",
    "kfz_enriched": "https://amtsscore.de/_file/data/kfz_enriched.692592bc.json",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: dict[str, Any], *, force: bool = False) -> None:
    if path.exists() and not force:
        raise RuntimeError(f"Refusing to overwrite immutable file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def rewrite_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def canonical_hash(data: Any) -> str:
    blob = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def require_contract(doc: dict[str, Any], path: Path) -> None:
    version = str(doc.get("contract_version", ""))
    major = version.split(".", 1)[0]
    if major not in ACCEPTED_CONTRACT_MAJOR_VERSIONS:
        raise RuntimeError(f"Unsupported contract_version {version!r} in {path}")


def artifact_id(path: Path) -> str:
    try:
        return str(path.relative_to(SCRAPER_OUTPUT))
    except ValueError:
        return path.name


def fetch_live_json(url: str) -> dict[str, Any] | None:
    try:
        with urllib.request.urlopen(url, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None


def summarize_prescore(doc: dict[str, Any]) -> dict[str, Any]:
    return {
        "generated_at": doc.get("generated_at"),
        "source": doc.get("source"),
        "topic_count": len(doc.get("topics", [])),
        "topics": [
            {
                "slug": topic.get("slug"),
                "label": topic.get("label"),
                "n_cities": topic.get("n_cities"),
            }
            for topic in doc.get("topics", [])
        ],
    }


def summarize_halteverbot(doc: dict[str, Any]) -> dict[str, Any]:
    return {
        "scraped_at": doc.get("scraped_at"),
        "total_authorities": doc.get("total_authorities"),
        "total_cities": doc.get("total_cities"),
        "city_count": len(doc.get("cities", [])),
    }


def summarize_kfz(doc: dict[str, Any]) -> dict[str, Any]:
    return {
        "generated_at": doc.get("generated_at"),
        "topic": doc.get("topic"),
        "topic_label": doc.get("topic_label"),
        "n_cities": doc.get("n_cities"),
        "dimensions": [d.get("key") for d in doc.get("dimensions", [])],
    }


def build_site_baseline() -> dict[str, Any]:
    local_sources = {
        "prescore": ROOT / "src" / "data" / "prescore.json",
        "halteverbot": ROOT / "src" / "data" / "halteverbot.json",
        "kfz_enriched": ROOT / "src" / "data" / "kfz_enriched.json",
    }
    local_docs = {key: load_json(path) for key, path in local_sources.items()}
    live_docs = {key: fetch_live_json(url) for key, url in LIVE_DATA_URLS.items()}

    summaries = {
        "local": {
            "prescore": summarize_prescore(local_docs["prescore"]),
            "halteverbot": summarize_halteverbot(local_docs["halteverbot"]),
            "kfz_enriched": summarize_kfz(local_docs["kfz_enriched"]),
        },
        "live": {},
    }

    for key, doc in live_docs.items():
        if doc is None:
            summaries["live"][key] = {"fetch_status": "unavailable"}
        elif key == "prescore":
            summaries["live"][key] = summarize_prescore(doc)
        elif key == "halteverbot":
            summaries["live"][key] = summarize_halteverbot(doc)
        elif key == "kfz_enriched":
            summaries["live"][key] = summarize_kfz(doc)

    mismatch = any(
        summaries["live"].get(key, {}).get("fetch_status") != "unavailable"
        and summaries["live"].get(key) != summaries["local"].get(key)
        for key in summaries["local"]
    )

    route_sources = sorted(
        str(path.relative_to(ROOT / "src")).removesuffix(".md")
        for path in (ROOT / "src").glob("**/*.md")
    )

    return {
        "history_model_version": HISTORY_MODEL_VERSION,
        "snapshot_family": "site_baseline",
        "baseline_date": "2026-05-20",
        "generated_by": GENERATED_BY,
        "do_not_edit_by_hand": True,
        "deployed_build_date": "2026-05-20",
        "live_data_urls": LIVE_DATA_URLS,
        "backup_source": "_src_of_backup",
        "mismatch_detected": mismatch,
        "summaries": summaries,
        "routes_from_source": route_sources,
    }


def get_signal(signals: dict[str, Any], key: str) -> dict[str, Any] | None:
    for signal in signals.get("signals", []):
        if signal.get("key") == key:
            return signal
    return None


def topic_group(surface: dict[str, Any], web: dict[str, Any] | None) -> str:
    lanes = set(surface.get("consumer_lanes") or [])
    final_state = surface.get("final_state")
    if "provider_sales" in lanes or final_state == "provider_only_ready":
        return "provider_only"
    if surface.get("scope") == "cluster_bridge" or surface.get("scope_claim") == "cluster_bridge":
        return "bridge"
    if "amtsscore" in lanes and web and web.get("embedded_policy") == "allow_embedded":
        return "core"
    if final_state in {"not_ready_closed", "bridge_only_closed"}:
        return "not_surfaceable"
    return "suppressed"


def review_status_for(group: str, surface: dict[str, Any], web: dict[str, Any] | None) -> str:
    if group == "core" and web and web.get("embedded_tool_status") == "ready":
        return "buildable_preview"
    if group == "bridge":
        return "bridge_context"
    if group == "provider_only":
        return "provider_only"
    if group == "not_surfaceable":
        return "not_ready"
    return "suppressed"


def normalize_topic(
    surface: dict[str, Any],
    web: dict[str, Any] | None,
    signal_doc: dict[str, Any] | None,
) -> dict[str, Any]:
    slug = surface["topic_slug"]
    group = topic_group(surface, web)
    source_quality = get_signal(signal_doc or {}, "source_manifest_coverage") or {}
    fact_quality = get_signal(signal_doc or {}, "fact_map_coverage") or {}
    provider_boundary = get_signal(signal_doc or {}, "provider_evidence_separation") or {}
    calculator = get_signal(signal_doc or {}, "calculator_surface") or {}
    source_value = source_quality.get("value") or {}
    fact_value = fact_quality.get("value") or {}
    provider_value = provider_boundary.get("value") or {}
    calculator_value = calculator.get("value") or {}
    signal_summary = (signal_doc or {}).get("summary") or {}

    route_policy = (
        web.get("route_policy")
        if web
        else (surface.get("web_build_policy") or {}).get("route_policy")
    )
    cta_policy = (
        web.get("cta_policy")
        if web
        else (surface.get("web_build_policy") or {}).get("cta_policy")
    )
    embedded_policy = (
        web.get("embedded_policy")
        if web
        else (surface.get("web_build_policy") or {}).get("embedded_policy")
    )

    return {
        "topic_slug": slug,
        "label": TOPIC_LABELS.get(slug, slug.replace("-", " ").title()),
        "group": group,
        "review_status": review_status_for(group, surface, web),
        "consumer_lanes": surface.get("consumer_lanes") or [],
        "final_state": surface.get("final_state"),
        "standalone_status": surface.get("standalone_status"),
        "tool_type": surface.get("tool_type"),
        "tool_status": surface.get("tool_status"),
        "calculator_status": surface.get("calculator_status"),
        "embedded_policy": embedded_policy,
        "route_policy": route_policy,
        "cta_policy": cta_policy,
        "can_show_tool_cta": bool(web.get("can_show_tool_cta")) if web else False,
        "web_buildable_now": bool(
            (surface.get("human_review_boundary") or {}).get("web_buildable_now")
        ),
        "public_claim_wording": (
            web.get("public_claim_wording")
            if web
            else surface.get("public_claim_wording")
        ),
        "source_note_required": bool(web.get("source_note_required")) if web else True,
        "signal_count": signal_summary.get("signal_count", 0),
        "blocked_signal_count": signal_summary.get("blocked_signal_count", 0),
        "signal_category_counts": signal_summary.get("by_category") or {},
        "score_scope_counts": score_scope_counts(signal_doc or {}),
        "official_source_count": source_value.get("official_source_count", 0),
        "source_count": source_value.get("source_count", 0),
        "fact_count": fact_value.get("fact_count", 0),
        "official_fact_count": fact_value.get("official_fact_count", 0),
        "source_backed_fact_count": fact_value.get("source_backed_fact_count", 0),
        "unknown_count": fact_value.get("unknown_count", 0),
        "has_calculator_surface": bool(calculator_value.get("has_calculator_surface")),
        "calculator_input_count": calculator_value.get("input_count", 0),
        "calculator_unknown_input_count": calculator_value.get("unknown_input_count", 0),
        "provider_rows_available": bool(provider_value.get("provider_rows_available")),
        "provider_rows_used_as_evidence": bool(
            provider_value.get("provider_rows_used_as_evidence")
        ),
        "provider_evidence_excluded": not bool(
            provider_value.get("provider_rows_used_as_evidence")
        ),
        "blocking_issues": surface.get("blocking_issues") or [],
        "source_artifact_ids": {
            "writer_bundle": artifact_id(Path(surface["writer_bundle_path"]))
            if surface.get("writer_bundle_path")
            else None,
            "source_manifest": artifact_id(Path(surface["source_manifest_path"]))
            if surface.get("source_manifest_path")
            else None,
            "tool_bundle": artifact_id(Path(surface["tool_bundle_path"]))
            if surface.get("tool_bundle_path")
            else None,
            "unknown_state_map": artifact_id(Path(surface["unknown_state_map_path"]))
            if surface.get("unknown_state_map_path")
            else None,
            "signals": f"{slug}/amtsscore/signals.json",
        },
        "source_artifact_paths": {
            "writer_bundle": surface.get("writer_bundle_path"),
            "source_manifest": surface.get("source_manifest_path"),
            "tool_bundle": surface.get("tool_bundle_path"),
            "unknown_state_map": surface.get("unknown_state_map_path"),
            "signals": str(SCRAPER_OUTPUT / slug / "amtsscore" / "signals.json"),
        },
    }


def score_scope_counts(signal_doc: dict[str, Any]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for signal in signal_doc.get("signals", []):
        scope = signal.get("score_scope") or "unknown"
        counts[scope] = counts.get(scope, 0) + 1
    return counts


def build_visual_rollups(snapshot_date: str, summary: dict[str, Any], topics: list[dict[str, Any]]) -> dict[str, Any]:
    metrics = [
        {
            "date": snapshot_date,
            "metric": "candidate_ready_topic_count",
            "value": summary.get("candidate_ready_topic_count", 0),
        },
        {
            "date": snapshot_date,
            "metric": "signal_count",
            "value": summary.get("signal_count", 0),
        },
        {
            "date": snapshot_date,
            "metric": "blocked_signal_count",
            "value": summary.get("blocked_signal_count", 0),
        },
        {
            "date": snapshot_date,
            "metric": "web_buildable_now_count",
            "value": summary.get("web_buildable_now_count", 0),
        },
        {
            "date": snapshot_date,
            "metric": "suppressed_route_count",
            "value": summary.get("suppressed_route_count", 0),
        },
    ]
    topic_metrics = []
    for topic in topics:
        for field in [
            "official_source_count",
            "source_count",
            "fact_count",
            "source_backed_fact_count",
            "unknown_count",
            "signal_count",
            "blocked_signal_count",
        ]:
            topic_metrics.append(
                {
                    "date": snapshot_date,
                    "topic_slug": topic["topic_slug"],
                    "label": topic["label"],
                    "field": field,
                    "value": topic.get(field, 0),
                }
            )
    return {"metrics": metrics, "topic_metrics": topic_metrics}


def normalize(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    paths = {
        "final_audit": CLUSTER_ROOT / "final_audit.json",
        "pipeline_check": CLUSTER_ROOT / "pipeline_check.json",
        "topic_surface": CLUSTER_ROOT / "topic_surface_full_completion.json",
        "web_consumer": CLUSTER_ROOT / "web_consumer_contract.json",
        "amtsscore": CLUSTER_ROOT / "amtsscore.json",
    }
    docs = {key: load_json(path) for key, path in paths.items()}
    for key, doc in docs.items():
        require_contract(doc, paths[key])

    final_summary = docs["final_audit"].get("summary") or {}
    pipeline_summary = docs["pipeline_check"].get("summary") or {}
    web_summary = docs["web_consumer"].get("summary") or {}
    amtsscore_summary = docs["amtsscore"].get("summary") or {}
    surface_summary = docs["topic_surface"].get("summary") or {}

    if final_summary.get("hard_blocker_count", 0) > 0:
        raise RuntimeError("Final audit has hard blockers")
    if pipeline_summary.get("failed_check_count", 0) > 0:
        raise RuntimeError("Pipeline check has failed checks")
    if web_summary.get("provider_rows_used_as_evidence"):
        raise RuntimeError("Web consumer contract uses provider rows as evidence")
    if amtsscore_summary.get("provider_rows_used_as_evidence"):
        raise RuntimeError("AmtsScore package uses provider rows as evidence")

    snapshot_date = docs["amtsscore"].get("generated_at")
    if not snapshot_date:
        raise RuntimeError("Missing amtsscore.generated_at; cannot derive snapshot ID")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", snapshot_date):
        raise RuntimeError(f"Unexpected snapshot date format: {snapshot_date!r}")

    web_by_slug = {topic["topic_slug"]: topic for topic in docs["web_consumer"].get("topics", [])}
    signal_by_slug: dict[str, dict[str, Any]] = {}
    for topic in docs["amtsscore"].get("topics", []):
        slug = topic["topic"]
        signal_path = SCRAPER_OUTPUT / slug / "amtsscore" / "signals.json"
        signal_doc = load_json(signal_path)
        require_contract(signal_doc, signal_path)
        if (signal_doc.get("summary") or {}).get("provider_rows_used_as_evidence"):
            raise RuntimeError(f"Signal file uses provider rows as evidence: {signal_path}")
        signal_by_slug[slug] = signal_doc

    topics = [
        normalize_topic(surface, web_by_slug.get(surface["topic_slug"]), signal_by_slug.get(surface["topic_slug"]))
        for surface in docs["topic_surface"].get("topics", [])
    ]
    topics.sort(key=lambda t: (group_order(t["group"]), t["label"]))

    if any(topic["provider_rows_used_as_evidence"] for topic in topics):
        raise RuntimeError("A normalized topic uses provider rows as evidence")

    summary = {
        "topic_count": surface_summary.get("topic_count", 0),
        "candidate_ready_topic_count": amtsscore_summary.get("candidate_ready_topic_count", 0),
        "signal_count": amtsscore_summary.get("signal_count", 0),
        "blocked_signal_count": amtsscore_summary.get("blocked_signal_count", 0),
        "web_buildable_now_count": surface_summary.get("web_buildable_now_count", 0),
        "embedded_buildable_count": web_summary.get("embedded_buildable_count", 0),
        "suppressed_route_count": web_summary.get("suppressed_route_count", 0),
        "suppressed_cta_count": web_summary.get("suppressed_cta_count", 0),
        "calculator_route_ready_count": web_summary.get("calculator_route_ready_count", 0),
        "provider_rows_used_as_evidence": False,
        "topic_groups": count_by(topics, "group"),
        "review_statuses": count_by(topics, "review_status"),
    }
    gates = {
        "final_audit_status": docs["final_audit"].get("status"),
        "pipeline_status": docs["pipeline_check"].get("status"),
        "topic_surface_status": docs["topic_surface"].get("status"),
        "web_consumer_status": docs["web_consumer"].get("status"),
        "hard_blocker_count": final_summary.get("hard_blocker_count", 0),
        "failed_check_count": pipeline_summary.get("failed_check_count", 0),
        "warning_check_count": pipeline_summary.get("warning_check_count", 0),
        "blocked_signal_count": amtsscore_summary.get("blocked_signal_count", 0),
        "provider_rows_used_as_evidence": False,
    }
    visual_rollups = build_visual_rollups(snapshot_date, summary, topics)

    hash_payload = {
        "history_model_version": HISTORY_MODEL_VERSION,
        "snapshot_family": SNAPSHOT_FAMILY,
        "snapshot_date": snapshot_date,
        "review_status": SNAPSHOT_REVIEW_STATUS,
        "gates": gates,
        "summary": summary,
        "topics": strip_volatile_topic_fields(topics),
        "visual_rollups": visual_rollups,
    }
    content_hash = canonical_hash(hash_payload)

    source_artifacts = [
        {"id": artifact_id(path), "path": str(path)}
        for path in paths.values()
    ]
    source_artifacts.extend(
        {
            "id": f"{slug}/amtsscore/signals.json",
            "path": str(SCRAPER_OUTPUT / slug / "amtsscore" / "signals.json"),
        }
        for slug in sorted(signal_by_slug)
    )

    base = {
        "history_model_version": HISTORY_MODEL_VERSION,
        "snapshot_family": SNAPSHOT_FAMILY,
        "generated_by": GENERATED_BY,
        "do_not_edit_by_hand": True,
    }
    snapshot = {
        **base,
        "snapshot_date": snapshot_date,
        "review_status": SNAPSHOT_REVIEW_STATUS,
        "imported_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source_generation_dates": {
            "amtsscore": docs["amtsscore"].get("generated_at"),
            "topic_surface": docs["topic_surface"].get("generated_at"),
            "web_consumer": docs["web_consumer"].get("generated_at"),
            "pipeline_check": docs["pipeline_check"].get("generated_at"),
            "final_audit": docs["final_audit"].get("generated_at"),
        },
        "source_artifacts": source_artifacts,
        "contract_versions": {
            key: doc.get("contract_version")
            for key, doc in docs.items()
        },
        "content_hash": content_hash,
        "gates": gates,
        "summary": summary,
        "topics": topics,
        "visual_rollups": visual_rollups,
    }
    current_pointer = {
        **base,
        "current_snapshot": snapshot_date,
        "current_snapshot_path": f"history/eauto/{snapshot_date}.json",
        "latest_diff_path": f"history/eauto/diff-{snapshot_date}.json",
        "review_status": SNAPSHOT_REVIEW_STATUS,
        "content_hash": content_hash,
        "summary": summary,
        "gates": gates,
        "topics": topics,
        "visual_rollups": visual_rollups,
    }
    return snapshot, current_pointer, docs, paths


def strip_volatile_topic_fields(topics: list[dict[str, Any]]) -> list[dict[str, Any]]:
    stripped = []
    for topic in topics:
        item = dict(topic)
        item.pop("source_artifact_paths", None)
        stripped.append(item)
    return stripped


def group_order(group: str) -> int:
    return {
        "core": 0,
        "bridge": 1,
        "not_surfaceable": 2,
        "provider_only": 3,
        "suppressed": 4,
    }.get(group, 9)


def count_by(rows: list[dict[str, Any]], field: str) -> dict[str, int]:
    out: dict[str, int] = {}
    for row in rows:
        key = row.get(field) or "unknown"
        out[key] = out.get(key, 0) + 1
    return out


def validate_snapshot(snapshot: dict[str, Any]) -> None:
    require_keys(
        snapshot,
        [
            "history_model_version",
            "snapshot_family",
            "snapshot_date",
            "review_status",
            "source_generation_dates",
            "source_artifacts",
            "contract_versions",
            "content_hash",
            "gates",
            "summary",
            "topics",
            "visual_rollups",
        ],
        "snapshot",
    )
    if snapshot["snapshot_family"] != SNAPSHOT_FAMILY:
        raise RuntimeError("Invalid snapshot family")
    for topic in snapshot["topics"]:
        validate_topic(topic)


def validate_pointer(pointer: dict[str, Any]) -> None:
    require_keys(
        pointer,
        [
            "history_model_version",
            "snapshot_family",
            "current_snapshot",
            "current_snapshot_path",
            "latest_diff_path",
            "summary",
            "gates",
            "topics",
            "visual_rollups",
        ],
        "current pointer",
    )


def validate_manifest(manifest: dict[str, Any]) -> None:
    require_keys(
        manifest,
        ["history_model_version", "snapshot_family", "current_snapshot", "snapshots", "latest_diff"],
        "manifest",
    )


def validate_diff(diff: dict[str, Any]) -> None:
    require_keys(
        diff,
        [
            "history_model_version",
            "snapshot_family",
            "snapshot_date",
            "previous_snapshot",
            "current_snapshot",
            "events",
            "summary",
        ],
        "diff",
    )
    for event in diff["events"]:
        if event.get("event_type") not in DIFF_EVENT_TYPES:
            raise RuntimeError(f"Invalid diff event type: {event.get('event_type')}")


def validate_topic(topic: dict[str, Any]) -> None:
    require_keys(
        topic,
        [
            "topic_slug",
            "label",
            "group",
            "review_status",
            "signal_count",
            "blocked_signal_count",
            "official_source_count",
            "source_count",
            "fact_count",
            "official_fact_count",
            "source_backed_fact_count",
            "unknown_count",
            "provider_evidence_excluded",
        ],
        "topic",
    )
    if topic["group"] not in TOPIC_GROUPS:
        raise RuntimeError(f"Invalid topic group: {topic['group']}")


def require_keys(doc: dict[str, Any], keys: list[str], label: str) -> None:
    missing = [key for key in keys if key not in doc]
    if missing:
        raise RuntimeError(f"{label} missing keys: {', '.join(missing)}")


def build_diff(snapshot: dict[str, Any], previous: dict[str, Any] | None) -> dict[str, Any]:
    date = snapshot["snapshot_date"]
    if previous is None:
        events = [
            {
                "event_type": "baseline_established",
                "severity": "material",
                "topic_slug": None,
                "field": "snapshot",
                "previous_value": None,
                "current_value": date,
                "note": "First E-Auto candidate-signal snapshot established.",
            }
        ]
    else:
        events = diff_topics(previous, snapshot)

    return {
        "history_model_version": HISTORY_MODEL_VERSION,
        "snapshot_family": SNAPSHOT_FAMILY,
        "generated_by": GENERATED_BY,
        "do_not_edit_by_hand": True,
        "snapshot_date": date,
        "previous_snapshot": previous["snapshot_date"] if previous else None,
        "current_snapshot": date,
        "events": events,
        "summary": {
            "event_count": len(events),
            "material_event_count": sum(1 for e in events if e.get("severity") == "material"),
            "informational_event_count": sum(1 for e in events if e.get("severity") == "informational"),
        },
    }


def diff_topics(previous: dict[str, Any], current: dict[str, Any]) -> list[dict[str, Any]]:
    events = []
    prev_topics = {t["topic_slug"]: t for t in previous.get("topics", [])}
    curr_topics = {t["topic_slug"]: t for t in current.get("topics", [])}
    for slug in sorted(set(curr_topics) - set(prev_topics)):
        events.append(diff_event("topic_added", slug, "topic", None, curr_topics[slug]["label"]))
    for slug in sorted(set(prev_topics) - set(curr_topics)):
        events.append(diff_event("topic_removed", slug, "topic", prev_topics[slug]["label"], None))
    field_events = {
        "group": "topic_group_changed",
        "review_status": "topic_status_changed",
        "web_buildable_now": "buildable_state_changed",
        "route_policy": "route_policy_changed",
        "cta_policy": "cta_policy_changed",
        "blocked_signal_count": "blocker_count_changed",
        "provider_evidence_excluded": "provider_boundary_changed",
        "official_source_count": "official_source_count_changed",
        "source_backed_fact_count": "source_backed_fact_count_changed",
        "unknown_count": "unknown_count_changed",
    }
    for slug in sorted(set(curr_topics) & set(prev_topics)):
        prev = prev_topics[slug]
        curr = curr_topics[slug]
        for field, event_type in field_events.items():
            if prev.get(field) != curr.get(field):
                events.append(diff_event(event_type, slug, field, prev.get(field), curr.get(field)))
    return events


def diff_event(event_type: str, slug: str | None, field: str, previous: Any, current: Any) -> dict[str, Any]:
    return {
        "event_type": event_type,
        "severity": "material",
        "topic_slug": slug,
        "field": field,
        "previous_value": previous,
        "current_value": current,
    }


def load_previous_snapshot(manifest_path: Path) -> dict[str, Any] | None:
    if not manifest_path.exists():
        return None
    manifest = load_json(manifest_path)
    current = manifest.get("current_snapshot")
    if not current:
        return None
    path = ROOT / "src" / "data" / "history" / "eauto" / f"{current}.json"
    if not path.exists():
        return None
    return load_json(path)


def build_manifest(snapshot: dict[str, Any], diff: dict[str, Any], previous_manifest: dict[str, Any] | None) -> dict[str, Any]:
    entry = {
        "snapshot": snapshot["snapshot_date"],
        "path": f"{snapshot['snapshot_date']}.json",
        "diff_path": f"diff-{snapshot['snapshot_date']}.json",
        "content_hash": snapshot["content_hash"],
        "review_status": snapshot["review_status"],
        "summary": snapshot["summary"],
        "source_generation_dates": snapshot["source_generation_dates"],
    }
    snapshots = []
    if previous_manifest:
        snapshots = [s for s in previous_manifest.get("snapshots", []) if s.get("snapshot") != entry["snapshot"]]
    snapshots.append(entry)
    snapshots.sort(key=lambda s: s["snapshot"])
    return {
        "history_model_version": HISTORY_MODEL_VERSION,
        "snapshot_family": SNAPSHOT_FAMILY,
        "generated_by": GENERATED_BY,
        "do_not_edit_by_hand": True,
        "current_snapshot": snapshot["snapshot_date"],
        "snapshots": snapshots,
        "latest_diff": f"diff-{snapshot['snapshot_date']}.json",
        "rollback_events": (previous_manifest or {}).get("rollback_events", []),
        "latest_diff_summary": diff["summary"],
    }


def same_content_existing(snapshot: dict[str, Any], snapshot_path: Path) -> bool:
    if not snapshot_path.exists():
        return False
    existing = load_json(snapshot_path)
    return existing.get("content_hash") == snapshot.get("content_hash")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="overwrite an existing dated snapshot")
    args = parser.parse_args()

    try:
        snapshot, pointer, _docs, _paths = normalize(args)
        validate_snapshot(snapshot)
        validate_pointer(pointer)

        data_dir = ROOT / "src" / "data"
        history_dir = data_dir / "history" / "eauto"
        baseline_path = data_dir / "history" / "site-baseline" / "2026-05-20.json"
        snapshot_path = history_dir / f"{snapshot['snapshot_date']}.json"
        diff_path = history_dir / f"diff-{snapshot['snapshot_date']}.json"
        manifest_path = history_dir / "index.json"
        pointer_path = data_dir / "eauto_prescore.json"

        previous_snapshot = load_previous_snapshot(manifest_path)
        previous_manifest = load_json(manifest_path) if manifest_path.exists() else None

        if snapshot_path.exists() and not args.force:
            if same_content_existing(snapshot, snapshot_path):
                print(f"no data changes: {snapshot_path.relative_to(ROOT)}")
                if not pointer_path.exists():
                    rewrite_json(pointer_path, pointer)
                return 0
            raise RuntimeError(f"Snapshot exists with different content hash: {snapshot_path}")

        baseline = build_site_baseline()
        diff = build_diff(snapshot, previous_snapshot)
        manifest = build_manifest(snapshot, diff, previous_manifest)
        validate_diff(diff)
        validate_manifest(manifest)

        if not baseline_path.exists():
            write_json(baseline_path, baseline)
        write_json(snapshot_path, snapshot, force=args.force)
        write_json(diff_path, diff, force=args.force)
        rewrite_json(manifest_path, manifest)
        rewrite_json(pointer_path, pointer)
        print(f"wrote {pointer_path.relative_to(ROOT)}")
        print(f"wrote {snapshot_path.relative_to(ROOT)}")
        return 0
    except Exception as exc:
        write_failure_report(exc)
        print(f"error: {exc}", file=sys.stderr)
        return 1


def write_failure_report(exc: Exception) -> None:
    failures_dir = ROOT / "planning" / "import_failures"
    failures_dir.mkdir(parents=True, exist_ok=True)
    existing = sorted(failures_dir.glob("[0-9][0-9][0-9]_*.md"))
    next_num = int(existing[-1].name[:3]) + 1 if existing else 1
    path = failures_dir / f"{next_num:03d}_eauto_import_failure.md"
    body = (
        "# E-Auto Import Failure\n\n"
        f"Date: {datetime.now(timezone.utc).date().isoformat()}\n"
        f"Source: `{CLUSTER_ROOT}`\n\n"
        "## Reason\n\n"
        f"{exc}\n\n"
        "## Write Status\n\n"
        "No public data files should be considered valid from this failed run.\n"
    )
    path.write_text(body, encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
