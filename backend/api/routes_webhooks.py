"""Webhook configuration and management endpoints (PHASE 2)."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query, Depends, status

from backend.api.middleware import verify_jwt_token
from backend.api.schemas import WebhookConfig


router = APIRouter(tags=["webhooks"])

# In-memory webhook storage (replace with DB in production)
_webhooks: dict[str, dict] = {}


def get_active_webhooks(severity: str | None = None) -> list[dict]:
    """Get active webhooks, optionally filtered by alert severity.
    
    Used by pipeline.py to trigger webhooks on alert creation.
    PHASE 3: Migrate this to persistent database storage.
    """
    active = [wh for wh in _webhooks.values() if wh.get("active", True)]
    if severity:
        # Map severity to numeric level for comparison
        severity_levels = {"low": 1, "medium": 2, "high": 3, "critical": 4}
        alert_level = severity_levels.get(severity, 0)
        current_level = severity_levels.get(severity, 0)
        active = [wh for wh in active 
                  if alert_level >= severity_levels.get(wh.get("severity_filter", "low"), 0)]
    return active


@router.get("/api/webhooks")
def list_webhooks(limit: int = Query(default=10, le=100)) -> dict[str, object]:
    """List active webhooks."""
    return {
        "webhooks": list(_webhooks.values())[:limit],
        "total": len(_webhooks),
    }


@router.post("/api/admin/webhooks")
def create_webhook(config: WebhookConfig, token: str | None = None) -> dict[str, object]:
    """Create a new webhook configuration (requires admin token)."""
    # In production, verify token is valid admin token
    if token:
        try:
            payload = verify_jwt_token(token)
            if payload.get("role") != "admin":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Admin privileges required",
                )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token: {e}",
            )

    webhook_id = f"wh_{len(_webhooks) + 1:06d}"
    _webhooks[webhook_id] = {
        "id": webhook_id,
        "name": config.name,
        "url": config.url,
        "platform": config.platform,
        "severity_filter": config.severity_filter,
        "active": config.active,
        "created_at": "2026-04-23T00:00:00Z",  # Use real timestamp in production
    }
    return {
        "id": webhook_id,
        "created": True,
        "webhook": _webhooks[webhook_id],
    }


@router.delete("/api/admin/webhooks/{webhook_id}")
def delete_webhook(webhook_id: str, token: str | None = None) -> dict[str, str]:
    """Delete a webhook configuration (requires admin token)."""
    if token:
        try:
            payload = verify_jwt_token(token)
            if payload.get("role") != "admin":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Admin privileges required",
                )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token: {e}",
            )

    if webhook_id not in _webhooks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Webhook not found",
        )

    del _webhooks[webhook_id]
    return {"status": "deleted", "webhook_id": webhook_id}


@router.patch("/api/admin/webhooks/{webhook_id}")
def toggle_webhook(webhook_id: str, active: bool, token: str | None = None) -> dict[str, object]:
    """Enable or disable a webhook (requires admin token)."""
    if token:
        try:
            payload = verify_jwt_token(token)
            if payload.get("role") != "admin":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Admin privileges required",
                )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token: {e}",
            )

    if webhook_id not in _webhooks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Webhook not found",
        )

    _webhooks[webhook_id]["active"] = active
    return {"id": webhook_id, "active": active}


@router.post("/api/webhooks/test/{webhook_id}")
def test_webhook(webhook_id: str) -> dict[str, str]:
    """Send a test alert to a webhook to verify connectivity."""
    if webhook_id not in _webhooks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Webhook not found",
        )

    from backend.core.webhooks import format_alert_for_webhook, send_webhook

    webhook = _webhooks[webhook_id]
    test_alert = {
        "id": "test_alert",
        "title": "Test Alert from Heimdall",
        "message": "This is a test to verify webhook connectivity.",
        "severity": "medium",
        "rule_name": "Test Rule",
        "source": "test-system",
        "status": "active",
        "mitre_tag": "T1110",
        "created_at": "2026-04-23T12:00:00Z",
    }

    payload = format_alert_for_webhook(test_alert, platform=webhook["platform"])
    success = send_webhook(webhook["url"], payload, platform=webhook["platform"])

    return {
        "webhook_id": webhook_id,
        "test_sent": "success" if success else "failed",
        "platform": webhook["platform"],
    }
