from __future__ import annotations

from backend.core.pipeline import ingest_event
from backend.storage.db import fetch_one


DEMO_EVENTS = [
    {
        "source": "auth-gateway",
        "event_type": "failed_login",
        "title": "Repeated login failure",
        "message": "Multiple failed login attempts for admin user from an external IP.",
        "severity": "medium",
        "ip_address": "198.51.100.24",
        "tags": ["auth", "bruteforce", "demo"],
    },
    {
        "source": "identity-core",
        "event_type": "privilege_escalation",
        "title": "Unexpected admin elevation",
        "message": "A standard operator account received administrative privileges unexpectedly.",
        "severity": "critical",
        "ip_address": "203.0.113.18",
        "tags": ["iam", "privilege", "demo"],
    },
    {
        "source": "vuln-scanner",
        "event_type": "vulnerability_reference",
        "title": "Critical edge package exposure",
        "message": "Observed vulnerable package reference CVE-2024-3094 during inventory correlation.",
        "severity": "high",
        "cve_id": "CVE-2024-3094",
        "ip_address": "10.10.0.17",
        "tags": ["cve", "supply-chain", "demo"],
    },
    {
        "source": "vpn-edge",
        "event_type": "authentication_failure",
        "title": "VPN authentication drift",
        "message": "Authentication failures reached a threshold that may indicate credential stuffing.",
        "severity": "high",
        "ip_address": "192.0.2.44",
        "tags": ["vpn", "access", "demo"],
    },
]


def seed_demo_data_if_empty() -> None:
    row = fetch_one("SELECT COUNT(*) AS total FROM events")
    if row and int(row["total"]) > 0:
        return

    for event in DEMO_EVENTS:
        ingest_event(event)
