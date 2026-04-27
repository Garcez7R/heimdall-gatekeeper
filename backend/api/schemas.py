from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class IngestRequest(BaseModel):
    """PHASE 1: Enhanced payload validation with strict constraints."""
    source: str = Field(..., min_length=1, max_length=64, description="Event source identifier (e.g., auth-gateway)")
    event_type: str = Field(..., min_length=1, max_length=64, description="Event classification")
    title: str = Field(..., min_length=1, max_length=256, description="Short event description")
    message: str = Field(..., min_length=1, max_length=4096, description="Detailed event message")
    severity: str = Field(default="low", pattern="^(low|medium|high|critical)$")
    ip_address: str | None = Field(None, max_length=45, description="Source or target IP address")
    cve_id: str | None = Field(None, pattern="^CVE-\\d{4}-\\d{4,}$|^$", description="Associated CVE identifier")
    tags: list[str] = Field(default_factory=list, description="Operational tags")
    mitre_tactics: list[str] = Field(default_factory=list, description="MITRE ATT&CK tactics (e.g., T1110)")
    
    @field_validator("severity")
    @classmethod
    def validate_severity(cls, v: str) -> str:
        if v not in ("low", "medium", "high", "critical"):
            raise ValueError("severity must be one of: low, medium, high, critical")
        return v


class AlertAction(BaseModel):
    """Response action on an alert."""
    actor: str = Field(..., min_length=1, max_length=128, description="User or system performing the action")


class WebhookConfig(BaseModel):
    """PHASE 2: Webhook configuration for external alert delivery."""
    name: str = Field(..., min_length=1, max_length=64, description="Webhook identifier")
    url: str = Field(..., min_length=10, max_length=2048, description="Webhook endpoint URL")
    platform: str = Field(..., pattern="^(discord|slack|generic)$", description="Target platform")
    severity_filter: str = Field(default="high", pattern="^(low|medium|high|critical|all)$")
    active: bool = Field(default=True)


class BehavioralDetectionRule(BaseModel):
    """PHASE 3: Multi-stage behavioral detection rule."""
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    stages: list[str] = Field(..., min_length=2, max_length=5, description="Sequence of detection stages")
    time_window_minutes: int = Field(..., ge=1, le=1440)
    group_by: str = Field(default="user", description="Field to correlate on (user, ip, source)")
    conditions: list[dict] = Field(default_factory=list, description="Optional stage conditions")
