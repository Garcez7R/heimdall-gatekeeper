"""
Pre-configured dashboards for different team roles and use cases.
"""
from core.custom_dashboards import DashboardWidget, CustomDashboard
from typing import List, Dict, Any

# Pre-configured dashboards for different roles
TEAM_DASHBOARDS = {
    "soc_analyst": {
        "name": "SOC Analyst Dashboard",
        "description": "Real-time monitoring for security operations center analysts",
        "widgets": [
            {
                "widget_id": "active_alerts",
                "widget_type": "alert_summary",
                "title": "Active Alerts",
                "config": {
                    "show_chart": True,
                    "time_range": "1h",
                    "severities": ["critical", "high", "medium"]
                },
                "position": {"x": 0, "y": 0},
                "size": {"width": 6, "height": 4}
            },
            {
                "widget_id": "recent_events",
                "widget_type": "recent_alerts",
                "title": "Recent Security Events",
                "config": {
                    "max_alerts": 20,
                    "show_acknowledged": True,
                    "time_range": "2h"
                },
                "position": {"x": 6, "y": 0},
                "size": {"width": 6, "height": 4}
            },
            {
                "widget_id": "threat_timeline",
                "widget_type": "event_timeline",
                "title": "Threat Timeline",
                "config": {
                    "max_events": 100,
                    "time_range": "4h",
                    "severities": ["critical", "high"]
                },
                "position": {"x": 0, "y": 4},
                "size": {"width": 8, "height": 5}
            },
            {
                "widget_id": "top_ips",
                "widget_type": "threat_map",
                "title": "Top Threat Sources",
                "config": {
                    "map_type": "table",
                    "time_range": "24h",
                    "limit": 10
                },
                "position": {"x": 8, "y": 4},
                "size": {"width": 4, "height": 5}
            }
        ]
    },
    "threat_hunter": {
        "name": "Threat Hunter Dashboard",
        "description": "Advanced analytics for threat hunting operations",
        "widgets": [
            {
                "widget_id": "anomaly_detection",
                "widget_type": "rule_performance",
                "title": "Detection Rule Performance",
                "config": {
                    "top_n": 15,
                    "time_range": "7d",
                    "show_trends": True
                },
                "position": {"x": 0, "y": 0},
                "size": {"width": 8, "height": 4}
            },
            {
                "widget_id": "threat_intel",
                "widget_type": "threat_intel_summary",
                "title": "Threat Intelligence Feed Status",
                "config": {
                    "feeds": ["otx", "misp", "virustotal"],
                    "time_range": "24h"
                },
                "position": {"x": 8, "y": 0},
                "size": {"width": 4, "height": 4}
            },
            {
                "widget_id": "behavioral_patterns",
                "widget_type": "behavioral_correlation",
                "title": "Behavioral Analysis",
                "config": {
                    "correlation_window": "1h",
                    "min_events": 3,
                    "patterns": ["brute_force", "lateral_movement", "data_exfil"]
                },
                "position": {"x": 0, "y": 4},
                "size": {"width": 6, "height": 5}
            },
            {
                "widget_id": "mitre_matrix",
                "widget_type": "mitre_tactics",
                "title": "MITRE ATT&CK Coverage",
                "config": {
                    "show_heatmap": True,
                    "time_range": "30d"
                },
                "position": {"x": 6, "y": 4},
                "size": {"width": 6, "height": 5}
            }
        ]
    },
    "incident_responder": {
        "name": "Incident Response Dashboard",
        "description": "Focused dashboard for incident response teams",
        "widgets": [
            {
                "widget_id": "incident_timeline",
                "widget_type": "incident_timeline",
                "title": "Incident Timeline",
                "config": {
                    "incident_id": None,  # Dynamic
                    "show_evidence": True,
                    "time_range": "24h"
                },
                "position": {"x": 0, "y": 0},
                "size": {"width": 12, "height": 6}
            },
            {
                "widget_id": "response_actions",
                "widget_type": "response_actions",
                "title": "Response Actions",
                "config": {
                    "incident_id": None,  # Dynamic
                    "show_templates": True
                },
                "position": {"x": 0, "y": 6},
                "size": {"width": 6, "height": 4}
            },
            {
                "widget_id": "affected_assets",
                "widget_type": "affected_assets",
                "title": "Affected Assets",
                "config": {
                    "incident_id": None,  # Dynamic
                    "group_by": "asset_type"
                },
                "position": {"x": 6, "y": 6},
                "size": {"width": 6, "height": 4}
            }
        ]
    },
    "ciso_executive": {
        "name": "CISO Executive Dashboard",
        "description": "High-level security metrics for executive reporting",
        "widgets": [
            {
                "widget_id": "security_posture",
                "widget_type": "kpi_summary",
                "title": "Security Posture KPIs",
                "config": {
                    "kpis": [
                        "mean_time_to_detect",
                        "mean_time_to_respond",
                        "alert_accuracy",
                        "threat_coverage"
                    ],
                    "time_range": "30d"
                },
                "position": {"x": 0, "y": 0},
                "size": {"width": 6, "height": 4}
            },
            {
                "widget_id": "risk_trends",
                "widget_type": "risk_trends",
                "title": "Risk Trends",
                "config": {
                    "metrics": ["alert_volume", "severity_trends", "compliance_score"],
                    "time_range": "90d",
                    "show_forecast": True
                },
                "position": {"x": 6, "y": 0},
                "size": {"width": 6, "height": 4}
            },
            {
                "widget_id": "compliance_status",
                "widget_type": "compliance_dashboard",
                "title": "Compliance Status",
                "config": {
                    "standards": ["SOX", "HIPAA", "PCI-DSS", "NIST"],
                    "show_details": False
                },
                "position": {"x": 0, "y": 4},
                "size": {"width": 8, "height": 4}
            },
            {
                "widget_id": "executive_reports",
                "widget_type": "report_generator",
                "title": "Executive Reports",
                "config": {
                    "report_types": ["weekly_summary", "monthly_metrics", "quarterly_review"],
                    "auto_generate": True
                },
                "position": {"x": 8, "y": 4},
                "size": {"width": 4, "height": 4}
            }
        ]
    },
    "devsecops": {
        "name": "DevSecOps Dashboard",
        "description": "Security metrics integrated with development pipeline",
        "widgets": [
            {
                "widget_id": "pipeline_security",
                "widget_type": "pipeline_security",
                "title": "Pipeline Security Gates",
                "config": {
                    "pipelines": ["main", "develop", "feature-branches"],
                    "show_failures": True,
                    "time_range": "7d"
                },
                "position": {"x": 0, "y": 0},
                "size": {"width": 8, "height": 4}
            },
            {
                "widget_id": "vulnerability_trends",
                "widget_type": "vulnerability_trends",
                "title": "Vulnerability Trends",
                "config": {
                    "severity_levels": ["critical", "high", "medium"],
                    "time_range": "30d",
                    "show_fix_rate": True
                },
                "position": {"x": 8, "y": 0},
                "size": {"width": 4, "height": 4}
            },
            {
                "widget_id": "code_quality",
                "widget_type": "code_security_metrics",
                "title": "Code Security Quality",
                "config": {
                    "metrics": ["sast_findings", "dependency_vulns", "code_coverage"],
                    "repositories": ["heimdall-gatekeeper", "heimdall-mobile"]
                },
                "position": {"x": 0, "y": 4},
                "size": {"width": 6, "height": 4}
            },
            {
                "widget_id": "deployment_security",
                "widget_type": "deployment_security",
                "title": "Deployment Security",
                "config": {
                    "environments": ["dev", "staging", "prod"],
                    "show_approvals": True
                },
                "position": {"x": 6, "y": 4},
                "size": {"width": 6, "height": 4}
            }
        ]
    }
}

def create_team_dashboards_for_user(user_id: str, roles: List[str]) -> List[str]:
    """
    Create pre-configured dashboards for a user based on their roles.

    Args:
        user_id: User ID
        roles: List of user roles (e.g., ["soc_analyst", "threat_hunter"])

    Returns:
        List of created dashboard IDs
    """
    created_dashboards = []

    for role in roles:
        if role in TEAM_DASHBOARDS:
            dashboard_config = TEAM_DASHBOARDS[role]

            # Create the dashboard
            dashboard_id = CustomDashboard.create_dashboard(
                user_id=user_id,
                dashboard_name=dashboard_config["name"],
                is_default=(role == roles[0])  # First role is default
            )

            if dashboard_id:
                # Add widgets to the dashboard
                CustomDashboard.update_dashboard_widgets(
                    dashboard_id=dashboard_id,
                    user_id=user_id,
                    widgets=dashboard_config["widgets"]
                )

                created_dashboards.append(dashboard_id)

    return created_dashboards

def get_available_team_dashboards() -> Dict[str, Dict[str, Any]]:
    """Get all available team dashboard templates."""
    return TEAM_DASHBOARDS

def create_default_dashboards_for_new_user(user_id: str) -> List[str]:
    """Create default dashboards for a new user (SOC Analyst profile)."""
    return create_team_dashboards_for_user(user_id, ["soc_analyst"])

# Quick setup functions for common scenarios
def setup_soc_team_dashboards(team_members: List[str]) -> Dict[str, List[str]]:
    """Setup SOC team dashboards for multiple users."""
    results = {}
    for user_id in team_members:
        dashboards = create_team_dashboards_for_user(user_id, ["soc_analyst", "incident_responder"])
        results[user_id] = dashboards
    return results

def setup_security_team_dashboards(team_members: List[str]) -> Dict[str, List[str]]:
    """Setup comprehensive security team dashboards."""
    results = {}
    for user_id in team_members:
        dashboards = create_team_dashboards_for_user(
            user_id,
            ["soc_analyst", "threat_hunter", "incident_responder"]
        )
        results[user_id] = dashboards
    return results