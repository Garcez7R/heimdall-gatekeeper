from __future__ import annotations

from fastapi import APIRouter, Query

from backend.api.schemas import AlertAction
from backend.core.pipeline import list_alerts, update_alert_status


router = APIRouter(tags=["alerts"])


@router.get("/api/alerts")
def alerts(limit: int = Query(default=100, le=500), status: str = "") -> dict[str, object]:
    return {"rows": list_alerts(limit=limit, status=status)}


@router.post("/api/alerts/{alert_id}/acknowledge")
def acknowledge_alert(alert_id: int, payload: AlertAction) -> dict[str, str]:
    update_alert_status(alert_id, "acknowledged", payload.actor)
    return {"status": "acknowledged"}


@router.post("/api/alerts/{alert_id}/resolve")
def resolve_alert(alert_id: int, payload: AlertAction) -> dict[str, str]:
    update_alert_status(alert_id, "resolved", payload.actor)
    return {"status": "resolved"}
