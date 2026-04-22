from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from backend.api.dependencies import FRONTEND_DIR


router = APIRouter(tags=["system"])


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/")
def root() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


@router.get("/{full_path:path}")
def spa_fallback(full_path: str) -> FileResponse:
    candidate = FRONTEND_DIR / full_path
    if candidate.exists() and candidate.is_file():
        return FileResponse(candidate)
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="Endpoint not found")
    return FileResponse(FRONTEND_DIR / "index.html")
