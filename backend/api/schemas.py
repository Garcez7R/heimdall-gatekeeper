from __future__ import annotations

from pydantic import BaseModel, Field


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
