from __future__ import annotations

from fastapi import APIRouter

from backend.core.config import load_config


router = APIRouter(tags=["config"])


@router.get("/api/config")
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
