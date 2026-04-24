"""Advanced detection and behavioral correlation endpoint (PHASE 3)."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from backend.api.schemas import BehavioralDetectionRule
from backend.core.advanced_detections import BehavioralCorrelator, normalize_to_ecs


router = APIRouter(tags=["advanced-detections"])


@router.post("/api/debug/test-behavior")
def test_behavioral_detection(rule: BehavioralDetectionRule) -> dict:
    """Test a behavioral detection rule with mock events (DEBUG ENDPOINT)."""
    correlator = BehavioralCorrelator(
        window_minutes=rule.time_window_minutes,
        group_by=rule.group_by,
    )

    # Mock scenario: create events that match the pattern
    # In real usage, this would accept actual events
    mock_events = [
        {
            rule.group_by: "test_user",
            "event_type": "authentication",
            "auth_outcome": "failure",
            "created_at": "2026-04-23T12:00:00Z",
        },
        {
            rule.group_by: "test_user",
            "event_type": "authentication",
            "auth_outcome": "failure",
            "created_at": "2026-04-23T12:01:00Z",
        },
        {
            rule.group_by: "test_user",
            "event_type": "authentication",
            "auth_outcome": "failure",
            "created_at": "2026-04-23T12:02:00Z",
        },
        {
            rule.group_by: "test_user",
            "event_type": "authentication",
            "auth_outcome": "success",
            "created_at": "2026-04-23T12:03:00Z",
        },
    ]

    detections = []
    for event in mock_events:
        detection = correlator.add_event(event)
        if detection:
            detections.append(detection)

    return {
        "rule_name": rule.name,
        "description": rule.description,
        "stages": rule.stages,
        "time_window_minutes": rule.time_window_minutes,
        "group_by": rule.group_by,
        "mock_events_processed": len(mock_events),
        "detections_triggered": len(detections),
        "detections": detections,
        "status": "success",
    }


@router.post("/api/debug/normalize-ecs")
def normalize_event_to_ecs(raw_event: dict) -> dict:
    """Convert raw event to Elastic Common Schema format (DEBUG ENDPOINT)."""
    try:
        ecs_event = normalize_to_ecs(raw_event)
        return {
            "input": raw_event,
            "output": ecs_event,
            "status": "success",
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Normalization failed: {e}")
