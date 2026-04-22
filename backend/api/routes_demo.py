from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter

from backend.core.metrics import save_metric
from backend.core.seed import seed_demo_data_if_empty


router = APIRouter(tags=["demo"])


@router.post("/api/demo/bootstrap")
def bootstrap_demo() -> dict[str, str]:
    seed_demo_data_if_empty()
    save_metric("demo_bootstrap_at", datetime.now(timezone.utc).isoformat())
    return {"status": "ok"}
