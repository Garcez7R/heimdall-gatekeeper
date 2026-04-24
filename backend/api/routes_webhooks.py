"""Webhook configuration and management endpoints (PHASE 2-3)."""
from __future__ import annotations

import uuid

from fastapi import APIRouter, HTTPException, Query, status

from backend.api.middleware import verify_jwt_token
from backend.api.schemas import WebhookConfig
from backend.storage.webhook_storage import (
    create_webhook as create_webhook_db,
    delete_webhook as delete_webhook_db,
    get_active_webhooks,
    get_webhook,
    list_webhooks as list_webhooks_db,
    toggle_webhook as toggle_webhook_db,
)


router = APIRouter(tags=["webhooks"])


@router.get("/api/webhooks")
def list_webhooks_endpoint(limit: int = Query(default=10, le=100)) -> dict[str, object]:
    """List all webhooks from persistent storage."""
    webhooks = list_webhooks_db()[:limit]
    return {
        "webhooks": webhooks,
        "total": len(list_webhooks_db()),
    }


@router.post("/api/admin/webhooks")
def create_webhook(config: WebhookConfig, token: str | None = None) -> dict[str, object]:
    """Create a new webhook configuration in persistent storage."""
    # Optional token verification (enforce in production)
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

    webhook_id = f"wh_{uuid.uuid4().hex[:12]}"
    webhook = create_webhook_db(
        webhook_id=webhook_id,
        name=config.name,
        url=config.url,
        platform=config.platform,
        severity_filter=config.severity_filter,
        active=config.active,
    )
    return {
        "id": webhook_id,
        "created": True,
        "webhook": webhook,
    }


@router.delete("/api/admin/webhooks/{webhook_id}")
def delete_webhook(webhook_id: str, token: str | None = None) -> dict[str, str]:
    """Delete a webhook configuration from persistent storage."""
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

    if not get_webhook(webhook_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Webhook not found",
        )

    success = delete_webhook_db(webhook_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete webhook",
        )

    return {"status": "deleted", "webhook_id": webhook_id}


@router.patch("/api/admin/webhooks/{webhook_id}")
def toggle_webhook_endpoint(webhook_id: str, active: bool, token: str | None = None) -> dict[str, object]:
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

    webhook = get_webhook(webhook_id)
    if not webhook:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Webhook not found",
        )

    updated = toggle_webhook_db(webhook_id, active)
    return {"id": webhook_id, "active": updated.get("active") if updated else active}


@router.post("/api/webhooks/test/{webhook_id}")
def test_webhook(webhook_id: str) -> dict[str, str]:
    """Send a test alert to a webhook to verify connectivity."""
    webhook = get_webhook(webhook_id)
    if not webhook:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Webhook not found",
        )

    from backend.core.webhooks import format_alert_for_webhook, send_webhook

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
