from backend.core.pipeline import normalize_event, sanitize_event_payload


def test_normalize_event_defaults():
    event = normalize_event(
        {
            "source": "auth-gateway",
            "event_type": "failed_login",
            "title": "Failed login",
            "message": "Multiple failed login attempts",
        }
    )

    assert event.source == "auth-gateway"
    assert event.severity == "low"
    assert event.tags == []


def test_sanitize_invalid_cve_is_removed():
    payload = sanitize_event_payload(
        {
            "source": "scanner",
            "event_type": "inventory",
            "title": "Bad CVE",
            "message": "Noise",
            "cve_id": "not-a-cve",
        }
    )

    assert "cve_id" not in payload
