from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(slots=True)
class EventPayload:
    source: str
    event_type: str
    title: str
    message: str
    severity: str = "low"
    ip_address: str | None = None
    cve_id: str | None = None
    tags: list[str] = field(default_factory=list)
    raw_payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now_iso)


@dataclass(slots=True)
class AlertPayload:
    rule_name: str
    severity: str
    title: str
    message: str
    source: str
    event_id: int | None = None
    ip_address: str | None = None
    cve_id: str | None = None
    cve_score: float | None = None
    mitre_tag: str | None = None
    created_at: str = field(default_factory=utc_now_iso)
