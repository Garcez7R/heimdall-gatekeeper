from __future__ import annotations

from fastapi import APIRouter, Query

from backend.api.schemas import AlertAction
from backend.core.pipeline import list_alerts, update_alert_status


router = APIRouter(tags=["alerts"])


@router.get("/api/alerts")
def alerts(
    limit: int = Query(default=100, le=500),
    status: str = "",
    severity: str = "",
) -> dict[str, object]:
    return {"rows": list_alerts(limit=limit, status=status, severity=severity)}


@router.post("/api/alerts/{alert_id}/acknowledge")
def acknowledge_alert(alert_id: int, payload: AlertAction) -> dict[str, str]:
    rows_updated = update_alert_status(alert_id, "acknowledged", payload.actor)
    if rows_updated == 0:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"status": "acknowledged"}


@router.post("/api/alerts/{alert_id}/resolve")
def resolve_alert(alert_id: int, payload: AlertAction) -> dict[str, str]:
    rows_updated = update_alert_status(alert_id, "resolved", payload.actor)
    if rows_updated == 0:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"status": "resolved"}
