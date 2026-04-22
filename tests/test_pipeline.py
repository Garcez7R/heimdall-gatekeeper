from backend.core.pipeline import event_to_rule_context, normalize_event, sanitize_event_payload
from backend.core.rules_engine import load_rules


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


def test_rule_matching_supports_slotted_event_payload():
    event = normalize_event(
        {
            "source": "auth-gateway",
            "event_type": "failed_login",
            "title": "Repeated login failure",
            "message": "Multiple failed login attempts for admin user from an external IP.",
            "severity": "medium",
        }
    )

    rule_context = event_to_rule_context(event)
    assert any(rule.matches(rule_context) for rule in load_rules())
