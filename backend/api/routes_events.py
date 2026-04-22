from __future__ import annotations

from fastapi import APIRouter, Query

from backend.api.schemas import IngestRequest
from backend.core.pipeline import ingest_event, list_events


router = APIRouter(tags=["events"])


@router.get("/api/events")
def events(
    limit: int = Query(default=100, le=500),
    search: str = "",
    severity: str = "",
) -> dict[str, object]:
    return {"rows": list_events(limit=limit, search=search, severity=severity)}


@router.post("/api/events/ingest")
def ingest(payload: IngestRequest) -> dict[str, object]:
    return ingest_event(payload.model_dump())
