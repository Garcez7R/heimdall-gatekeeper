from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

import requests

from backend.core.config import load_config
from backend.storage.db import execute, fetch_one


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def cached_lookup(cve_id: str) -> dict[str, Any] | None:
    row = fetch_one("SELECT * FROM cve_cache WHERE cve_id = ?", (cve_id,))
    if not row:
        return None
    updated_at = datetime.fromisoformat(row["updated_at"])
    if updated_at >= datetime.now(timezone.utc) - timedelta(hours=12):
        return row
    return None


def fetch_cve_details(cve_id: str) -> dict[str, Any] | None:
    config = load_config()
    if not config.get("threat_intel", {}).get("enabled", True):
        return None

    cached = cached_lookup(cve_id)
    if cached:
        return cached

    try:
        response = requests.get(
            "https://services.nvd.nist.gov/rest/json/cves/2.0",
            params={"cveId": cve_id},
            timeout=8,
        )
        response.raise_for_status()
        body = response.json()
        vulnerabilities = body.get("vulnerabilities", [])
        if not vulnerabilities:
            return None
        cve = vulnerabilities[0].get("cve", {})
        metrics = cve.get("metrics", {})
        cvss_block = (
            metrics.get("cvssMetricV31", [{}])[0]
            or metrics.get("cvssMetricV30", [{}])[0]
            or metrics.get("cvssMetricV2", [{}])[0]
        )
        score = cvss_block.get("cvssData", {}).get("baseScore")
        severity = cvss_block.get("cvssData", {}).get("baseSeverity")
        descriptions = cve.get("descriptions", [])
        summary = next((item.get("value") for item in descriptions if item.get("lang") == "en"), "")

        execute(
            """
            INSERT INTO cve_cache (cve_id, score, severity, summary, payload, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(cve_id) DO UPDATE SET
              score = excluded.score,
              severity = excluded.severity,
              summary = excluded.summary,
              payload = excluded.payload,
              updated_at = excluded.updated_at
            """,
            (cve_id, score, severity, summary, response.text, utc_now_iso()),
        )
        return fetch_one("SELECT * FROM cve_cache WHERE cve_id = ?", (cve_id,))
    except requests.RequestException:
        return None
