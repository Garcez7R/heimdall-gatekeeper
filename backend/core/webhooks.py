"""PHASE 2: Webhook integrations and MITRE ATT&CK mapping."""
from __future__ import annotations

import json
from typing import Any

import requests


MITRE_TACTICS = {
    "T1110": {"tactic": "Brute Force", "technique": "Credential Stuffing"},
    "T1068": {"tactic": "Privilege Escalation", "technique": "Exploitation for Privilege Escalation"},
    "T1021": {"tactic": "Lateral Movement", "technique": "Remote Services"},
    "T1087": {"tactic": "Discovery", "technique": "Account Discovery"},
    "T1078": {"tactic": "Defense Evasion", "technique": "Valid Accounts"},
}


def get_mitre_tactic(tag: str) -> dict[str, Any]:
    """Resolve MITRE ATT&CK tactic from tag."""
    return MITRE_TACTICS.get(tag, {"tactic": "Unknown", "technique": tag})


def format_alert_for_webhook(alert: dict, platform: str = "generic") -> dict | str:
    """PHASE 2: Format alert for webhook delivery (Discord, Slack, generic)."""
    if platform == "discord":
        embed = {
            "title": alert.get("title", "Alert"),
            "description": alert.get("message", ""),
            "color": _severity_to_color(alert.get("severity", "low")),
            "fields": [
                {"name": "Severity", "value": alert.get("severity", "low").upper(), "inline": True},
                {"name": "Rule", "value": alert.get("rule_name", "N/A"), "inline": True},
                {"name": "Source", "value": alert.get("source", "N/A"), "inline": False},
                {"name": "Status", "value": alert.get("status", "active").upper(), "inline": True},
            ],
        }
        if alert.get("mitre_tag"):
            mitre = get_mitre_tactic(alert["mitre_tag"])
            embed["fields"].append(
                {"name": "MITRE ATT&CK", "value": f"{alert['mitre_tag']}: {mitre['tactic']}", "inline": True}
            )
        return {"embeds": [embed]}

    elif platform == "slack":
        color = _severity_to_hex_color(alert.get("severity", "low"))
        attachment = {
            "color": color,
            "title": alert.get("title", "Alert"),
            "text": alert.get("message", ""),
            "fields": [
                {"title": "Severity", "value": alert.get("severity", "low").upper(), "short": True},
                {"title": "Rule", "value": alert.get("rule_name", "N/A"), "short": True},
                {"title": "Source", "value": alert.get("source", "N/A"), "short": False},
            ],
            "footer": "Heimdall Gatekeeper",
        }
        if alert.get("mitre_tag"):
            mitre = get_mitre_tactic(alert["mitre_tag"])
            attachment["fields"].append(
                {"title": "MITRE ATT&CK", "value": f"{alert['mitre_tag']}: {mitre['tactic']}", "short": True}
            )
        return {"attachments": [attachment]}

    else:
        # Generic JSON format
        return {
            "alert_id": alert.get("id"),
            "title": alert.get("title"),
            "severity": alert.get("severity"),
            "rule": alert.get("rule_name"),
            "source": alert.get("source"),
            "message": alert.get("message"),
            "status": alert.get("status"),
            "mitre_tactic": alert.get("mitre_tag"),
            "timestamp": alert.get("created_at"),
        }


def send_webhook(url: str, payload: dict | str, platform: str = "generic") -> bool:
    """Send alert to webhook endpoint."""
    try:
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        return response.status_code < 300
    except Exception as e:
        print(f"Webhook delivery failed to {url}: {e}")
        return False


def _severity_to_color(severity: str) -> int:
    """Map severity to Discord embed color."""
    colors = {"critical": 0xFF5555, "high": 0xFFAA00, "medium": 0xFFFF00, "low": 0x00FF00}
    return colors.get(severity, 0x808080)


def _severity_to_hex_color(severity: str) -> str:
    """Map severity to Slack hex color."""
    colors = {"critical": "#FF5555", "high": "#FFAA00", "medium": "#FFFF00", "low": "#00FF00"}
    return colors.get(severity, "#808080")
