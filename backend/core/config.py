from __future__ import annotations

from functools import lru_cache
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
import yaml


BASE_DIR = Path(__file__).resolve().parents[2]
CONFIG_PATH = BASE_DIR / "config" / "config.yaml"
ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)


@lru_cache(maxsize=1)
def load_config() -> dict[str, Any]:
    with CONFIG_PATH.open("r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle) or {}

    storage = config.setdefault("storage", {})
    threat_intel = config.setdefault("threat_intel", {})
    ui = config.setdefault("ui", {})

    config["product_name"] = os.getenv("HEIMDALL_PRODUCT_NAME", config.get("product_name", "Heimdall Gatekeeper"))
    config["tagline"] = os.getenv("HEIMDALL_TAGLINE", config.get("tagline", "Minimal SIEM for Blue Teams"))

    storage["sqlite_path"] = os.getenv("HEIMDALL_SQLITE_PATH", storage.get("sqlite_path", "data/heimdall.db"))
    storage["cloudflare_d1_enabled"] = os.getenv(
        "HEIMDALL_CLOUDFLARE_D1_ENABLED",
        str(storage.get("cloudflare_d1_enabled", "false")),
    ).lower() in {"1", "true", "yes", "on"}

    threat_intel["enabled"] = os.getenv(
        "HEIMDALL_THREAT_INTEL_ENABLED",
        str(threat_intel.get("enabled", "true")),
    ).lower() in {"1", "true", "yes", "on"}
    threat_intel["provider"] = os.getenv("HEIMDALL_THREAT_INTEL_PROVIDER", threat_intel.get("provider", "nvd"))

    ui["default_language"] = os.getenv("HEIMDALL_DEFAULT_LANGUAGE", ui.get("default_language", "pt-BR"))
    ui["default_theme"] = os.getenv("HEIMDALL_DEFAULT_THEME", ui.get("default_theme", "dark"))
    ui["splash_duration_ms"] = int(os.getenv("HEIMDALL_SPLASH_DURATION_MS", str(ui.get("splash_duration_ms", 1200))))
    return config


def reload_config() -> dict[str, Any]:
    load_config.cache_clear()
    return load_config()
