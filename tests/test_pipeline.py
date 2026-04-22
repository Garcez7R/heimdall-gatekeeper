from backend.core.pipeline import normalize_event


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
