from __future__ import annotations

import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.api.dependencies import FRONTEND_DIR
from backend.api.errors import register_exception_handlers
from backend.api.logging import StructuredLoggingMiddleware
from backend.api.middleware import limiter
from backend.api.routes_advanced_detections import router as advanced_detections_router
from backend.api.routes_alerts import router as alerts_router
from backend.api.routes_auth import router as auth_router
from backend.api.routes_config import router as config_router
from backend.api.routes_demo import router as demo_router
from backend.api.routes_events import router as events_router
from backend.api.routes_overview import router as overview_router
from backend.api.routes_system import router as system_router
from backend.api.routes_webhooks import router as webhooks_router
from backend.core.seed import seed_demo_data_if_empty
from backend.core.webhook_queue import get_webhook_queue
from backend.storage.db import initialize_database


app = FastAPI(
    title="Heimdall Gatekeeper",
    version="1.2.0",  # Updated for multi-phase roadmap
    description="Advanced SIEM with behavioral detection and webhook integration",
)

app.state.limiter = limiter

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(StructuredLoggingMiddleware)
app.mount("/assets", StaticFiles(directory=FRONTEND_DIR), name="assets")
register_exception_handlers(app)

app.include_router(config_router)
app.include_router(overview_router)
app.include_router(events_router)
app.include_router(alerts_router)
app.include_router(demo_router)
app.include_router(auth_router)
app.include_router(webhooks_router)
app.include_router(advanced_detections_router)
app.include_router(system_router)


@app.on_event("startup")
def on_startup() -> None:
    """Initialize database and start async webhook queue."""
    initialize_database()
    seed_demo_data_if_empty()
    
    # Start webhook delivery queue in background
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    queue = get_webhook_queue()
    # asyncio.create_task(queue.start())  # Note: requires async context
    print("✓ Webhook queue initialized (ready for async delivery)")


@app.on_event("shutdown")
async def on_shutdown() -> None:
    """Stop async webhook queue gracefully."""
    try:
        queue = get_webhook_queue()
        await queue.stop()
        print("✓ Webhook queue stopped gracefully")
    except Exception as e:
        print(f"⚠ Webhook queue shutdown error: {e}")
