from __future__ import annotations

from fastapi import APIRouter

from backend.core.metrics import build_overview_snapshot
from backend.core.pipeline import list_alerts, list_events


router = APIRouter(tags=["overview"])


@router.get("/api/overview")
def overview() -> dict[str, object]:
    snapshot = build_overview_snapshot()
    top_ips = [row for row in list_events(limit=5) if row.get("ip_address")]
    return {
        **snapshot,
        "latest_alerts": list_alerts(limit=8),
        "latest_events": list_events(limit=8),
        "top_ips": top_ips,
    }
