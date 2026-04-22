from __future__ import annotations

import json
import time
from datetime import datetime, timezone

from backend.storage.db import execute, fetch_all, fetch_one


BOOT_TIME = time.time()


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def save_metric(key: str, value: str) -> None:
    execute(
        """
        INSERT INTO system_metrics (metric_key, metric_value, updated_at)
        VALUES (?, ?, ?)
        ON CONFLICT(metric_key) DO UPDATE SET
          metric_value = excluded.metric_value,
          updated_at = excluded.updated_at
        """,
        (key, value, utc_now_iso()),
    )


def update_runtime_metrics() -> None:
    save_metric("uptime_seconds", str(int(time.time() - BOOT_TIME)))


def build_status_snapshot() -> dict[str, object]:
    update_runtime_metrics()
    total_events = fetch_one("SELECT COUNT(*) AS total FROM events") or {"total": 0}
    total_alerts = fetch_one("SELECT COUNT(*) AS total FROM alerts WHERE status != 'resolved'") or {"total": 0}
    critical_alerts = fetch_one("SELECT COUNT(*) AS total FROM alerts WHERE severity = 'critical' AND status != 'resolved'") or {"total": 0}
    rule_hits = fetch_all("SELECT rule_name, total_hits FROM rule_hits ORDER BY total_hits DESC LIMIT 5")
    metrics = fetch_all("SELECT metric_key, metric_value, updated_at FROM system_metrics")

    return {
        "system": "healthy",
        "uptime_seconds": int((fetch_one("SELECT metric_value FROM system_metrics WHERE metric_key = 'uptime_seconds'") or {"metric_value": "0"})["metric_value"]),
        "events_total": int(total_events["total"]),
        "active_alerts": int(total_alerts["total"]),
        "critical_alerts": int(critical_alerts["total"]),
        "rule_hits": rule_hits,
        "metrics": metrics,
    }


def build_overview_snapshot() -> dict[str, object]:
    status = build_status_snapshot()
    severity_breakdown = {
        "critical": int((fetch_one("SELECT COUNT(*) AS total FROM alerts WHERE severity = 'critical' AND status != 'resolved'") or {"total": 0})["total"]),
        "high": int((fetch_one("SELECT COUNT(*) AS total FROM alerts WHERE severity = 'high' AND status != 'resolved'") or {"total": 0})["total"]),
        "medium": int((fetch_one("SELECT COUNT(*) AS total FROM alerts WHERE severity = 'medium' AND status != 'resolved'") or {"total": 0})["total"]),
        "low": int((fetch_one("SELECT COUNT(*) AS total FROM alerts WHERE severity = 'low' AND status != 'resolved'") or {"total": 0})["total"]),
    }
    timeline = fetch_all(
        """
        SELECT substr(created_at, 1, 13) || ':00' AS bucket, COUNT(*) AS total
        FROM events
        GROUP BY bucket
        ORDER BY bucket DESC
        LIMIT 12
        """
    )
    top_sources = fetch_all(
        """
        SELECT source, COUNT(*) AS total
        FROM events
        GROUP BY source
        ORDER BY total DESC, source ASC
        LIMIT 6
        """
    )
    top_cves = fetch_all(
        """
        SELECT cve_id, COUNT(*) AS total, MAX(cve_score) AS score
        FROM alerts
        WHERE cve_id IS NOT NULL AND cve_id != ''
        GROUP BY cve_id
        ORDER BY total DESC, score DESC
        LIMIT 6
        """
    )
    latest_metrics = {
        item["metric_key"]: item["metric_value"]
        for item in status["metrics"]  # type: ignore[index]
    }

    return {
        "status": status,
        "severity_breakdown": severity_breakdown,
        "timeline": list(reversed(timeline)),
        "top_sources": top_sources,
        "top_cves": top_cves,
        "events_per_minute": latest_metrics.get("events_per_minute", "0"),
        "last_ingest_at": latest_metrics.get("last_ingest_at"),
    }


def export_snapshot() -> str:
    return json.dumps(build_status_snapshot(), ensure_ascii=False, indent=2)
