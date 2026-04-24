"""Webhook storage and persistence layer (PHASE 3)."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from backend.storage.db import execute, fetch_all, fetch_one


def utc_now_iso() -> str:
    """Get current UTC time in ISO format."""
    return datetime.now(timezone.utc).isoformat()


def create_webhook(
    webhook_id: str,
    name: str,
    url: str,
    platform: str,
    severity_filter: str = "low",
    active: bool = True,
) -> dict[str, Any]:
    """Create a new webhook in persistent storage."""
    now = utc_now_iso()
    execute(
        """
        INSERT INTO webhooks (id, name, url, platform, severity_filter, active, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (webhook_id, name, url, platform, severity_filter, active, now, now),
    )
    return get_webhook(webhook_id) or {}


def get_webhook(webhook_id: str) -> dict[str, Any] | None:
    """Get a webhook by ID."""
    return fetch_one("SELECT * FROM webhooks WHERE id = ?", (webhook_id,))


def list_webhooks(active_only: bool = False) -> list[dict[str, Any]]:
    """List all webhooks, optionally filtered to active only."""
    if active_only:
        return fetch_all("SELECT * FROM webhooks WHERE active = 1 ORDER BY created_at DESC")
    return fetch_all("SELECT * FROM webhooks ORDER BY created_at DESC")


def get_active_webhooks(severity: str | None = None) -> list[dict[str, Any]]:
    """Get active webhooks, optionally filtered by alert severity."""
    webhooks = list_webhooks(active_only=True)

    if severity:
        severity_levels = {"low": 1, "medium": 2, "high": 3, "critical": 4}
        alert_level = severity_levels.get(severity, 0)
        webhooks = [
            wh
            for wh in webhooks
            if alert_level >= severity_levels.get(wh.get("severity_filter", "low"), 0)
        ]

    return webhooks


def update_webhook(webhook_id: str, **kwargs: Any) -> dict[str, Any] | None:
    """Update webhook fields."""
    valid_fields = {"name", "url", "platform", "severity_filter", "active"}
    updates = {k: v for k, v in kwargs.items() if k in valid_fields}

    if not updates:
        return get_webhook(webhook_id)

    updates["updated_at"] = utc_now_iso()
    set_clause = ", ".join(f"{k} = ?" for k in updates)
    values = list(updates.values()) + [webhook_id]

    execute(f"UPDATE webhooks SET {set_clause} WHERE id = ?", tuple(values))
    return get_webhook(webhook_id)


def toggle_webhook(webhook_id: str, active: bool) -> dict[str, Any] | None:
    """Enable or disable a webhook."""
    return update_webhook(webhook_id, active=active)


def delete_webhook(webhook_id: str) -> bool:
    """Delete a webhook."""
    result = execute("DELETE FROM webhooks WHERE id = ?", (webhook_id,))
    return result > 0
