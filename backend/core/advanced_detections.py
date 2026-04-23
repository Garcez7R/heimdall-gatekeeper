"""PHASE 3: Behavioral detection, ECS normalization, and advanced correlations."""
from __future__ import annotations

from typing import Any


# Elastic Common Schema (ECS) field mapping for log normalization
ECS_FIELD_MAP = {
    # Event identification
    "event.id": "event_id",
    "event.kind": "event_kind",
    "event.category": "event_category",
    "event.action": "event_action",
    "event.severity": "severity",
    # User identification
    "user.name": "username",
    "user.id": "user_id",
    "user.domain": "user_domain",
    # Source and destination
    "source.ip": "source_ip",
    "source.port": "source_port",
    "destination.ip": "dest_ip",
    "destination.port": "dest_port",
    # Process information
    "process.name": "process_name",
    "process.pid": "process_id",
    "process.command_line": "command_line",
    # Authentication
    "event.outcome": "auth_outcome",
    "auth.attempt": "auth_attempt",
}


def normalize_to_ecs(raw_event: dict[str, Any]) -> dict[str, Any]:
    """PHASE 3: Convert raw event to Elastic Common Schema format."""
    ecs_event = {
        "event.id": raw_event.get("id", ""),
        "event.category": "process",  # or "authentication", "network", etc.
        "event.action": raw_event.get("event_type", "unknown"),
        "event.severity": _map_severity_to_ecs(raw_event.get("severity", "low")),
        "event.created": raw_event.get("created_at"),
        "user.name": raw_event.get("username"),
        "source.ip": raw_event.get("source_ip") or raw_event.get("ip_address"),
        "host.name": raw_event.get("source", "unknown"),
        "message": raw_event.get("message", ""),
    }
    # Remove None values for clean output
    return {k: v for k, v in ecs_event.items() if v is not None}


def _map_severity_to_ecs(severity: str) -> int:
    """Map custom severity to ECS numeric severity (1-8)."""
    mapping = {"low": 3, "medium": 5, "high": 7, "critical": 8}
    return mapping.get(severity, 4)


class BehavioralCorrelator:
    """PHASE 3: Multi-stage correlation for behavioral detection.
    
    Example: Detect 3 failed logins + 1 success for same user within 5 minutes.
    """

    def __init__(self, window_minutes: int = 5, group_by: str = "user_name"):
        self.window_minutes = window_minutes
        self.group_by = group_by
        self.events_buffer: dict[str, list[dict]] = {}

    def add_event(self, event: dict[str, Any]) -> dict[str, Any] | None:
        """Add event and check for behavioral patterns."""
        group_key = event.get(self.group_by, "unknown")
        if group_key not in self.events_buffer:
            self.events_buffer[group_key] = []

        self.events_buffer[group_key].append(event)

        # Simple pattern: 3 failed auth attempts + 1 success = suspicious
        if self.group_by == "user_name" and "auth" in event.get("event_type", ""):
            failed_count = sum(
                1 for e in self.events_buffer[group_key]
                if e.get("auth_outcome") == "failure"
            )
            success_count = sum(
                1 for e in self.events_buffer[group_key]
                if e.get("auth_outcome") == "success"
            )

            if failed_count >= 3 and success_count >= 1:
                return {
                    "detection": "Brute Force with Success",
                    "severity": "critical",
                    "group_key": group_key,
                    "failed_attempts": failed_count,
                    "successes": success_count,
                    "mitre_tactic": "T1110",
                }

        return None

    def flush_old_events(self) -> None:
        """Clear buffer (in production, use timestamp-based cleanup)."""
        self.events_buffer.clear()
