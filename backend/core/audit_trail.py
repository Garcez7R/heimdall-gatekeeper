"""
Audit trails and compliance logging for SOX/HIPAA requirements.
"""
import json
import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from enum import Enum
from backend.storage.db import execute
from core.config import settings

logger = logging.getLogger(__name__)

class AuditEvent(Enum):
    """Audit event types for compliance."""
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    ALERT_ACKNOWLEDGE = "alert_acknowledge"
    ALERT_RESOLVE = "alert_resolve"
    WEBHOOK_CREATE = "webhook_create"
    WEBHOOK_UPDATE = "webhook_update"
    WEBHOOK_DELETE = "webhook_delete"
    RULE_CREATE = "rule_create"
    RULE_UPDATE = "rule_update"
    RULE_DELETE = "rule_delete"
    CONFIG_CHANGE = "config_change"
    DATA_EXPORT = "data_export"
    SYSTEM_ACCESS = "system_access"
    API_ACCESS = "api_access"

class AuditSeverity(Enum):
    """Audit event severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AuditTrail:
    """Manages audit trails for compliance and security monitoring."""

    @staticmethod
    def log_event(
        event_type: AuditEvent,
        user_id: str,
        severity: AuditSeverity,
        resource_type: str,
        resource_id: str,
        action: str,
        details: Dict[str, Any],
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> bool:
        """Log an audit event to the database."""
        try:
            timestamp = datetime.now(timezone.utc).isoformat()

            audit_data = {
                "event_type": event_type.value,
                "user_id": user_id,
                "severity": severity.value,
                "resource_type": resource_type,
                "resource_id": resource_id,
                "action": action,
                "details": json.dumps(details),
                "ip_address": ip_address,
                "user_agent": user_agent,
                "session_id": session_id,
                "timestamp": timestamp
            }

            execute("""
                INSERT INTO audit_trail (
                    event_type, user_id, severity, resource_type, resource_id,
                    action, details, ip_address, user_agent, session_id, timestamp
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                audit_data["event_type"], audit_data["user_id"], audit_data["severity"],
                audit_data["resource_type"], audit_data["resource_id"], audit_data["action"],
                audit_data["details"], audit_data["ip_address"], audit_data["user_agent"],
                audit_data["session_id"], audit_data["timestamp"]
            ))

            # Log to structured logger as well
            logger.info(
                f"AUDIT: {event_type.value} | User: {user_id} | Resource: {resource_type}:{resource_id} | Action: {action}",
                extra={
                    "audit_event": audit_data,
                    "compliance": True
                }
            )

            return True

        except Exception as e:
            logger.error(f"Failed to log audit event: {e}")
            return False

    @staticmethod
    def get_audit_trail(
        user_id: Optional[str] = None,
        event_type: Optional[AuditEvent] = None,
        resource_type: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100
    ) -> list:
        """Retrieve audit trail entries with filtering."""
        from backend.storage.db import fetch_all

        try:
            query = """
                SELECT * FROM audit_trail WHERE 1=1
            """
            params = []

            if user_id:
                query += " AND user_id = ?"
                params.append(user_id)

            if event_type:
                query += " AND event_type = ?"
                params.append(event_type.value)

            if resource_type:
                query += " AND resource_type = ?"
                params.append(resource_type)

            if start_date:
                query += " AND timestamp >= ?"
                params.append(start_date)

            if end_date:
                query += " AND timestamp <= ?"
                params.append(end_date)

            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)

            return fetch_all(query, params)

        except Exception as e:
            logger.error(f"Failed to retrieve audit trail: {e}")
            return []

    @staticmethod
    def get_compliance_report(
        start_date: str,
        end_date: str,
        report_type: str = "summary"
    ) -> Dict[str, Any]:
        """Generate compliance reports for SOX/HIPAA."""
        from backend.storage.db import fetch_all, fetch_one

        try:
            # Summary statistics
            total_events = fetch_one("""
                SELECT COUNT(*) as count FROM audit_trail
                WHERE timestamp BETWEEN ? AND ?
            """, (start_date, end_date))["count"]

            events_by_type = fetch_all("""
                SELECT event_type, COUNT(*) as count
                FROM audit_trail
                WHERE timestamp BETWEEN ? AND ?
                GROUP BY event_type
                ORDER BY count DESC
            """, (start_date, end_date))

            events_by_user = fetch_all("""
                SELECT user_id, COUNT(*) as count
                FROM audit_trail
                WHERE timestamp BETWEEN ? AND ?
                GROUP BY user_id
                ORDER BY count DESC
                LIMIT 10
            """, (start_date, end_date))

            # Critical events (failed logins, config changes, etc.)
            critical_events = fetch_all("""
                SELECT * FROM audit_trail
                WHERE severity IN ('high', 'critical')
                AND timestamp BETWEEN ? AND ?
                ORDER BY timestamp DESC
            """, (start_date, end_date))

            return {
                "report_period": {
                    "start_date": start_date,
                    "end_date": end_date
                },
                "summary": {
                    "total_audit_events": total_events,
                    "events_by_type": events_by_type,
                    "events_by_user": events_by_user,
                    "critical_events_count": len(critical_events)
                },
                "critical_events": critical_events if report_type == "detailed" else [],
                "compliance_status": "compliant" if total_events > 0 else "no_data",
                "generated_at": datetime.now(timezone.utc).isoformat()
            }

        except Exception as e:
            logger.error(f"Failed to generate compliance report: {e}")
            return {"error": str(e)}

# Global audit trail instance
audit_trail = AuditTrail()