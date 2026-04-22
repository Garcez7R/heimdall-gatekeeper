from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from backend.core.config import load_config
from backend.core.metrics import build_overview_snapshot, build_status_snapshot, save_metric
from backend.core.pipeline import ingest_event, list_alerts, list_events, update_alert_status
from backend.core.seed import seed_demo_data_if_empty
from backend.storage.db import initialize_database


BASE_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(title="Heimdall Gatekeeper", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/assets", StaticFiles(directory=FRONTEND_DIR), name="assets")


class IngestRequest(BaseModel):
    source: str = Field(..., min_length=1)
    event_type: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)
    severity: str = "low"
    ip_address: str | None = None
    cve_id: str | None = None
    tags: list[str] = Field(default_factory=list)


class AlertAction(BaseModel):
    actor: str = Field(..., min_length=1)


@app.on_event("startup")
def on_startup() -> None:
    initialize_database()
    seed_demo_data_if_empty()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/config")
def config() -> dict[str, object]:
    cfg = load_config()
    ui = cfg.get("ui", {})
    return {
        "product_name": cfg.get("product_name", "Heimdall Gatekeeper"),
        "tagline": cfg.get("tagline", "Minimal SIEM for Blue Teams"),
        "languages": ui.get("languages", ["pt-BR", "en", "es"]),
        "default_language": ui.get("default_language", "en"),
        "default_theme": ui.get("default_theme", "dark"),
        "splash_duration_ms": ui.get("splash_duration_ms", 1200),
    }


@app.get("/api/overview")
def overview() -> dict[str, object]:
    snapshot = build_overview_snapshot()
    top_ips = [
        row
        for row in list_events(limit=5)
        if row.get("ip_address")
    ]
    return {
        **snapshot,
        "latest_alerts": list_alerts(limit=8),
        "latest_events": list_events(limit=8),
        "top_ips": top_ips,
    }


@app.get("/api/events")
def events(
    limit: int = Query(default=100, le=500),
    search: str = "",
    severity: str = "",
) -> dict[str, object]:
    return {"rows": list_events(limit=limit, search=search, severity=severity)}


@app.get("/api/alerts")
def alerts(limit: int = Query(default=100, le=500), status: str = "") -> dict[str, object]:
    return {"rows": list_alerts(limit=limit, status=status)}


@app.post("/api/events/ingest")
def ingest(payload: IngestRequest) -> dict[str, object]:
    return ingest_event(payload.model_dump())


@app.post("/api/demo/bootstrap")
def bootstrap_demo() -> dict[str, str]:
    seed_demo_data_if_empty()
    save_metric("demo_bootstrap_at", datetime.now(timezone.utc).isoformat())
    return {"status": "ok"}


@app.post("/api/alerts/{alert_id}/acknowledge")
def acknowledge_alert(alert_id: int, payload: AlertAction) -> dict[str, str]:
    update_alert_status(alert_id, "acknowledged", payload.actor)
    return {"status": "acknowledged"}


@app.post("/api/alerts/{alert_id}/resolve")
def resolve_alert(alert_id: int, payload: AlertAction) -> dict[str, str]:
    update_alert_status(alert_id, "resolved", payload.actor)
    return {"status": "resolved"}


@app.get("/")
def root() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/{full_path:path}")
def spa_fallback(full_path: str) -> FileResponse:
    candidate = FRONTEND_DIR / full_path
    if candidate.exists() and candidate.is_file():
        return FileResponse(candidate)
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="Endpoint not found")
    return FileResponse(FRONTEND_DIR / "index.html")
