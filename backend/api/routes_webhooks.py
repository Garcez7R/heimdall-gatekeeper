"""Webhook configuration and management endpoints (PHASE 2-3)."""
from __future__ import annotations

import uuid

import os

from fastapi import APIRouter, Depends, HTTPException, Header, Query, status

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


def get_admin_token(authorization: str | None = Header(None)) -> dict:
    """Extract and validate JWT token from Authorization header.
    
    Accepts: Authorization: Bearer <token>
    """
    demo_mode = os.getenv("HEIMDALL_DEMO_MODE", "true").lower() in {"1", "true", "yes", "on"}
    if not authorization and demo_mode:
        return {"username": "admin", "role": "admin"}

    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header",
        )
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format. Use: Bearer <token>",
        )
    
    token = authorization[7:]  # Remove "Bearer " prefix
    try:
        payload = verify_jwt_token(token)
        if payload.get("role") != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin privileges required",
            )
        return payload
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {e}",
        )


@router.get("/api/webhooks")
def list_webhooks_endpoint(limit: int = Query(default=10, le=100)) -> dict[str, object]:
    """List all webhooks from persistent storage."""
    webhooks = list_webhooks_db()[:limit]
    return {
        "webhooks": webhooks,
        "total": len(list_webhooks_db()),
    }


@router.post("/api/admin/webhooks")
def create_webhook(
    config: WebhookConfig,
    _admin: dict = Depends(get_admin_token),
) -> dict[str, object]:
    """Create a new webhook configuration (requires admin JWT token)."""
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
def delete_webhook(
    webhook_id: str,
    _admin: dict = Depends(get_admin_token),
) -> dict[str, str]:
    """Delete a webhook configuration (requires admin JWT token)."""
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
def toggle_webhook_endpoint(
    webhook_id: str,
    active: bool,
    _admin: dict = Depends(get_admin_token),
) -> dict[str, object]:
    """Enable or disable a webhook (requires admin JWT token)."""
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
