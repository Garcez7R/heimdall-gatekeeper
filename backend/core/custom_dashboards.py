"""
Customizable dashboards for users with drag-and-drop widgets.
"""
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from backend.storage.db import execute, fetch_all, fetch_one
from core.config import settings

logger = logging.getLogger(__name__)

class DashboardWidget:
    """Represents a dashboard widget."""

    def __init__(
        self,
        widget_id: str,
        widget_type: str,
        title: str,
        config: Dict[str, Any],
        position: Dict[str, int],
        size: Dict[str, int]
    ):
        self.widget_id = widget_id
        self.widget_type = widget_type
        self.title = title
        self.config = config
        self.position = position  # {"x": int, "y": int}
        self.size = size  # {"width": int, "height": int}

    def to_dict(self) -> Dict[str, Any]:
        """Convert widget to dictionary."""
        return {
            "widget_id": self.widget_id,
            "widget_type": self.widget_type,
            "title": self.title,
            "config": self.config,
            "position": self.position,
            "size": self.size
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DashboardWidget':
        """Create widget from dictionary."""
        return cls(
            widget_id=data["widget_id"],
            widget_type=data["widget_type"],
            title=data["title"],
            config=data["config"],
            position=data["position"],
            size=data["size"]
        )

class CustomDashboard:
    """Manages customizable user dashboards."""

    @staticmethod
    def create_dashboard(
        user_id: str,
        dashboard_name: str,
        is_default: bool = False
    ) -> Optional[str]:
        """Create a new dashboard for a user."""
        try:
            dashboard_id = f"dash_{user_id}_{int(datetime.now().timestamp())}"

            execute("""
                INSERT INTO user_dashboards (
                    dashboard_id, user_id, dashboard_name, is_default,
                    widgets, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                dashboard_id, user_id, dashboard_name, is_default,
                json.dumps([]),  # Empty widgets array
                datetime.now(timezone.utc).isoformat(),
                datetime.now(timezone.utc).isoformat()
            ))

            logger.info(f"Created dashboard {dashboard_id} for user {user_id}")
            return dashboard_id

        except Exception as e:
            logger.error(f"Failed to create dashboard: {e}")
            return None

    @staticmethod
    def get_user_dashboards(user_id: str) -> List[Dict[str, Any]]:
        """Get all dashboards for a user."""
        try:
            dashboards = fetch_all("""
                SELECT dashboard_id, dashboard_name, is_default, widgets,
                       created_at, updated_at
                FROM user_dashboards
                WHERE user_id = ?
                ORDER BY is_default DESC, updated_at DESC
            """, (user_id,))

            return [{
                "dashboard_id": d["dashboard_id"],
                "dashboard_name": d["dashboard_name"],
                "is_default": bool(d["is_default"]),
                "widgets": json.loads(d["widgets"]) if d["widgets"] else [],
                "created_at": d["created_at"],
                "updated_at": d["updated_at"]
            } for d in dashboards]

        except Exception as e:
            logger.error(f"Failed to get user dashboards: {e}")
            return []

    @staticmethod
    def get_dashboard(dashboard_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific dashboard."""
        try:
            dashboard = fetch_one("""
                SELECT dashboard_id, dashboard_name, is_default, widgets,
                       created_at, updated_at
                FROM user_dashboards
                WHERE dashboard_id = ? AND user_id = ?
            """, (dashboard_id, user_id))

            if dashboard:
                return {
                    "dashboard_id": dashboard["dashboard_id"],
                    "dashboard_name": dashboard["dashboard_name"],
                    "is_default": bool(dashboard["is_default"]),
                    "widgets": json.loads(dashboard["widgets"]) if dashboard["widgets"] else [],
                    "created_at": dashboard["created_at"],
                    "updated_at": dashboard["updated_at"]
                }
            return None

        except Exception as e:
            logger.error(f"Failed to get dashboard {dashboard_id}: {e}")
            return None

    @staticmethod
    def update_dashboard_widgets(
        dashboard_id: str,
        user_id: str,
        widgets: List[Dict[str, Any]]
    ) -> bool:
        """Update dashboard widgets."""
        try:
            execute("""
                UPDATE user_dashboards
                SET widgets = ?, updated_at = ?
                WHERE dashboard_id = ? AND user_id = ?
            """, (
                json.dumps(widgets),
                datetime.now(timezone.utc).isoformat(),
                dashboard_id, user_id
            ))

            logger.info(f"Updated widgets for dashboard {dashboard_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to update dashboard widgets: {e}")
            return False

    @staticmethod
    def delete_dashboard(dashboard_id: str, user_id: str) -> bool:
        """Delete a dashboard."""
        try:
            execute("""
                DELETE FROM user_dashboards
                WHERE dashboard_id = ? AND user_id = ?
            """, (dashboard_id, user_id))

            logger.info(f"Deleted dashboard {dashboard_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to delete dashboard: {e}")
            return False

    @staticmethod
    def set_default_dashboard(dashboard_id: str, user_id: str) -> bool:
        """Set a dashboard as the default for a user."""
        try:
            # First, unset all defaults for this user
            execute("""
                UPDATE user_dashboards
                SET is_default = 0
                WHERE user_id = ?
            """, (user_id,))

            # Then set the new default
            execute("""
                UPDATE user_dashboards
                SET is_default = 1, updated_at = ?
                WHERE dashboard_id = ? AND user_id = ?
            """, (
                datetime.now(timezone.utc).isoformat(),
                dashboard_id, user_id
            ))

            logger.info(f"Set dashboard {dashboard_id} as default for user {user_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to set default dashboard: {e}")
            return False

class WidgetTemplates:
    """Predefined widget templates."""

    @staticmethod
    def get_available_widgets() -> List[Dict[str, Any]]:
        """Get list of available widget types."""
        return [
            {
                "type": "alert_summary",
                "name": "Alert Summary",
                "description": "Summary of active alerts by severity",
                "default_config": {
                    "show_chart": True,
                    "time_range": "24h"
                },
                "default_size": {"width": 4, "height": 3}
            },
            {
                "type": "event_timeline",
                "name": "Event Timeline",
                "description": "Timeline of recent events",
                "default_config": {
                    "max_events": 50,
                    "time_range": "1h"
                },
                "default_size": {"width": 8, "height": 4}
            },
            {
                "type": "threat_map",
                "name": "Threat Map",
                "description": "Geographic view of threats",
                "default_config": {
                    "map_type": "world",
                    "time_range": "7d"
                },
                "default_size": {"width": 6, "height": 4}
            },
            {
                "type": "rule_performance",
                "name": "Rule Performance",
                "description": "Detection rule hit statistics",
                "default_config": {
                    "top_n": 10,
                    "time_range": "7d"
                },
                "default_size": {"width": 4, "height": 3}
            },
            {
                "type": "system_metrics",
                "name": "System Metrics",
                "description": "System performance metrics",
                "default_config": {
                    "metrics": ["cpu", "memory", "disk"],
                    "time_range": "1h"
                },
                "default_size": {"width": 4, "height": 3}
            },
            {
                "type": "recent_alerts",
                "name": "Recent Alerts",
                "description": "List of most recent alerts",
                "default_config": {
                    "max_alerts": 10,
                    "show_acknowledged": False
                },
                "default_size": {"width": 4, "height": 4}
            }
        ]

# Global dashboard manager
dashboard_manager = CustomDashboard()
widget_templates = WidgetTemplates()