from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from backend.core.metrics import save_metric
from backend.core.models import AlertPayload, EventPayload
from backend.core.rules_engine import load_rules
from backend.storage.db import execute, fetch_all, fetch_one
from backend.threat_intel.nvd import fetch_cve_details


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_event(payload: dict[str, Any]) -> EventPayload:
    source = str(payload.get("source", "unknown")).strip() or "unknown"
    event_type = str(payload.get("event_type", payload.get("type", "generic"))).strip() or "generic"
    title = str(payload.get("title", event_type.replace("_", " ").title())).strip() or "Generic event"
    message = str(payload.get("message", payload.get("description", "No message provided"))).strip()
    severity = str(payload.get("severity", "low")).lower()
    ip_address = payload.get("ip_address")
    cve_id = payload.get("cve_id")
    tags = payload.get("tags", [])
    if not isinstance(tags, list):
        tags = [str(tags)]

    return EventPayload(
        source=source,
        event_type=event_type,
        title=title,
        message=message,
        severity=severity,
        ip_address=str(ip_address) if ip_address else None,
        cve_id=str(cve_id) if cve_id else None,
        tags=[str(item) for item in tags],
        raw_payload=payload,
    )


def persist_event(event: EventPayload) -> int:
    event_id = execute(
        """
        INSERT INTO events (
          source, event_type, severity, title, message, raw_payload,
          ip_address, cve_id, cve_score, status, tags, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            event.source,
            event.event_type,
            event.severity,
            event.title,
            event.message,
            json.dumps(event.raw_payload, ensure_ascii=False),
            event.ip_address,
            event.cve_id,
            None,
            "new",
            ",".join(event.tags),
            event.created_at,
            event.created_at,
        ),
    )
    return event_id


def persist_alert(alert: AlertPayload) -> int:
    return execute(
        """
        INSERT INTO alerts (
          rule_name, severity, title, message, source, event_id, ip_address,
          cve_id, cve_score, mitre_tag, status, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            alert.rule_name,
            alert.severity,
            alert.title,
            alert.message,
            alert.source,
            alert.event_id,
            alert.ip_address,
            alert.cve_id,
            alert.cve_score,
            alert.mitre_tag,
            "active",
            alert.created_at,
            alert.created_at,
        ),
    )


def bump_rule_hit(rule_name: str) -> None:
    current = fetch_one("SELECT total_hits FROM rule_hits WHERE rule_name = ?", (rule_name,))
    total = int(current["total_hits"]) + 1 if current else 1
    execute(
        """
        INSERT INTO rule_hits (rule_name, total_hits, updated_at)
        VALUES (?, ?, ?)
        ON CONFLICT(rule_name) DO UPDATE SET
          total_hits = excluded.total_hits,
          updated_at = excluded.updated_at
        """,
        (rule_name, total, utc_now_iso()),
    )


def evaluate_event(event_id: int, event: EventPayload) -> list[int]:
    alerts: list[int] = []
    cve_details = fetch_cve_details(event.cve_id) if event.cve_id else None
    for rule in load_rules():
        if not rule.matches(event.__dict__):
            continue
        bump_rule_hit(rule.name)
        alert_id = persist_alert(
            AlertPayload(
                rule_name=rule.name,
                severity=rule.severity,
                title=rule.title,
                message=f"{rule.description} | {event.message}",
                source=event.source,
                event_id=event_id,
                ip_address=event.ip_address,
                cve_id=event.cve_id,
                cve_score=float(cve_details["score"]) if cve_details and cve_details.get("score") is not None else None,
                mitre_tag=rule.mitre_tag,
            )
        )
        alerts.append(alert_id)
    return alerts


def ingest_event(payload: dict[str, Any]) -> dict[str, Any]:
    event = normalize_event(payload)
    event_id = persist_event(event)
    alert_ids = evaluate_event(event_id, event)
    save_metric("last_ingest_at", utc_now_iso())
    return {"event_id": event_id, "alert_ids": alert_ids}


def list_events(limit: int = 100, search: str = "", severity: str = "") -> list[dict[str, Any]]:
    query = "SELECT * FROM events WHERE 1=1"
    params: list[Any] = []
    if search:
        query += " AND (title LIKE ? OR message LIKE ? OR source LIKE ?)"
        like = f"%{search}%"
        params.extend([like, like, like])
    if severity:
        query += " AND severity = ?"
        params.append(severity)
    query += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)
    return fetch_all(query, tuple(params))


def list_alerts(limit: int = 100, status: str = "") -> list[dict[str, Any]]:
    query = "SELECT * FROM alerts WHERE 1=1"
    params: list[Any] = []
    if status:
        query += " AND status = ?"
        params.append(status)
    query += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)
    return fetch_all(query, tuple(params))


def update_alert_status(alert_id: int, status: str, actor: str) -> None:
    field = "acknowledged_by" if status == "acknowledged" else "resolved_by"
    execute(
        f"UPDATE alerts SET status = ?, {field} = ?, updated_at = ? WHERE id = ?",
        (status, actor, utc_now_iso(), alert_id),
    )
