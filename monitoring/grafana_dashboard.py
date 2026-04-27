"""
Grafana dashboard configuration for Heimdall Gatekeeper monitoring.
"""
import json
from typing import Dict, Any

# Grafana Dashboard JSON for Heimdall monitoring
GRAFANA_DASHBOARD = {
    "dashboard": {
        "id": None,
        "title": "Heimdall Gatekeeper - SIEM Monitoring",
        "tags": ["heimdall", "siem", "security"],
        "timezone": "browser",
        "panels": [
            # System Overview Row
            {
                "id": 1,
                "title": "System Overview",
                "type": "stat",
                "targets": [
                    {
                        "expr": "up",
                        "legendFormat": "System Status"
                    }
                ],
                "fieldConfig": {
                    "defaults": {
                        "mappings": [
                            {
                                "options": {
                                    "0": {"text": "DOWN", "color": "red"},
                                    "1": {"text": "UP", "color": "green"}
                                },
                                "type": "value"
                            }
                        ]
                    }
                },
                "gridPos": {"h": 3, "w": 4, "x": 0, "y": 0}
            },
            {
                "id": 2,
                "title": "Active WebSocket Connections",
                "type": "stat",
                "targets": [
                    {
                        "expr": "heimdall_active_connections",
                        "legendFormat": "Active Connections"
                    }
                ],
                "gridPos": {"h": 3, "w": 4, "x": 4, "y": 0}
            },
            {
                "id": 3,
                "title": "Event Processing Rate",
                "type": "stat",
                "targets": [
                    {
                        "expr": "rate(heimdall_events_processed_total[5m])",
                        "legendFormat": "Events/sec"
                    }
                ],
                "gridPos": {"h": 3, "w": 4, "x": 8, "y": 0}
            },
            {
                "id": 4,
                "title": "Alert Generation Rate",
                "type": "stat",
                "targets": [
                    {
                        "expr": "rate(heimdall_alerts_generated_total[5m])",
                        "legendFormat": "Alerts/sec"
                    }
                ],
                "gridPos": {"h": 3, "w": 4, "x": 12, "y": 0}
            },
            {
                "id": 5,
                "title": "Queue Size",
                "type": "stat",
                "targets": [
                    {
                        "expr": "heimdall_queue_size",
                        "legendFormat": "Queued Events"
                    }
                ],
                "gridPos": {"h": 3, "w": 4, "x": 16, "y": 0}
            },
            {
                "id": 6,
                "title": "API Response Time (P95)",
                "type": "stat",
                "targets": [
                    {
                        "expr": "histogram_quantile(0.95, rate(heimdall_api_request_duration_seconds_bucket[5m]))",
                        "legendFormat": "P95 Response Time"
                    }
                ],
                "fieldConfig": {
                    "defaults": {
                        "unit": "s"
                    }
                },
                "gridPos": {"h": 3, "w": 4, "x": 20, "y": 0}
            },

            # Events and Alerts Row
            {
                "id": 7,
                "title": "Events Processed Over Time",
                "type": "graph",
                "targets": [
                    {
                        "expr": "rate(heimdall_events_processed_total[5m])",
                        "legendFormat": "{{severity}} events"
                    }
                ],
                "gridPos": {"h": 8, "w": 12, "x": 0, "y": 3}
            },
            {
                "id": 8,
                "title": "Alert Distribution by Severity",
                "type": "piechart",
                "targets": [
                    {
                        "expr": "sum(heimdall_alerts_generated_total) by (severity)",
                        "legendFormat": "{{severity}}"
                    }
                ],
                "gridPos": {"h": 8, "w": 6, "x": 12, "y": 3}
            },
            {
                "id": 9,
                "title": "Alert Status Distribution",
                "type": "piechart",
                "targets": [
                    {
                        "expr": "heimdall_alerts_acknowledged_total",
                        "legendFormat": "Acknowledged"
                    },
                    {
                        "expr": "heimdall_alerts_resolved_total",
                        "legendFormat": "Resolved"
                    }
                ],
                "gridPos": {"h": 8, "w": 6, "x": 18, "y": 3}
            },

            # Performance Row
            {
                "id": 10,
                "title": "API Request Rate by Endpoint",
                "type": "graph",
                "targets": [
                    {
                        "expr": "rate(heimdall_api_requests_total[5m])",
                        "legendFormat": "{{endpoint}} ({{method}})"
                    }
                ],
                "gridPos": {"h": 8, "w": 12, "x": 0, "y": 11}
            },
            {
                "id": 11,
                "title": "Database Query Performance",
                "type": "graph",
                "targets": [
                    {
                        "expr": "rate(heimdall_db_query_duration_seconds_sum[5m]) / rate(heimdall_db_query_duration_seconds_count[5m])",
                        "legendFormat": "{{operation}} avg duration"
                    }
                ],
                "fieldConfig": {
                    "defaults": {
                        "unit": "s"
                    }
                },
                "gridPos": {"h": 8, "w": 6, "x": 12, "y": 11}
            },
            {
                "id": 12,
                "title": "Cache Performance",
                "type": "stat",
                "targets": [
                    {
                        "expr": "(sum(rate(heimdall_cache_hits_total[5m])) / (sum(rate(heimdall_cache_hits_total[5m])) + sum(rate(heimdall_cache_misses_total[5m])))) * 100",
                        "legendFormat": "Cache Hit Rate %"
                    }
                ],
                "fieldConfig": {
                    "defaults": {
                        "unit": "percent"
                    }
                },
                "gridPos": {"h": 8, "w": 6, "x": 18, "y": 11}
            },

            # Threat Intelligence Row
            {
                "id": 13,
                "title": "Threat Intelligence Requests",
                "type": "graph",
                "targets": [
                    {
                        "expr": "rate(heimdall_threat_intel_requests_total[5m])",
                        "legendFormat": "{{provider}} {{status}}"
                    }
                ],
                "gridPos": {"h": 8, "w": 12, "x": 0, "y": 19}
            },
            {
                "id": 14,
                "title": "Threat Intelligence Enrichments",
                "type": "barchart",
                "targets": [
                    {
                        "expr": "rate(heimdall_threat_intel_enrichments_total[5m])",
                        "legendFormat": "{{intel_type}}"
                    }
                ],
                "gridPos": {"h": 8, "w": 12, "x": 12, "y": 19}
            },

            # Error Monitoring Row
            {
                "id": 15,
                "title": "API Error Rate",
                "type": "graph",
                "targets": [
                    {
                        "expr": "rate(heimdall_api_requests_total{status=~\"4..|5..\"}[5m]) / rate(heimdall_api_requests_total[5m]) * 100",
                        "legendFormat": "Error Rate %"
                    }
                ],
                "fieldConfig": {
                    "defaults": {
                        "unit": "percent"
                    }
                },
                "gridPos": {"h": 8, "w": 12, "x": 0, "y": 27}
            },
            {
                "id": 16,
                "title": "System Resources",
                "type": "graph",
                "targets": [
                    {
                        "expr": "100 - (avg by (instance) (irate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)",
                        "legendFormat": "CPU Usage %"
                    },
                    {
                        "expr": "(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100",
                        "legendFormat": "Memory Usage %"
                    }
                ],
                "fieldConfig": {
                    "defaults": {
                        "unit": "percent"
                    }
                },
                "gridPos": {"h": 8, "w": 12, "x": 12, "y": 27}
            }
        ],
        "time": {
            "from": "now-1h",
            "to": "now"
        },
        "timepicker": {},
        "templating": {
            "list": []
        },
        "annotations": {
            "list": []
        },
        "refresh": "30s",
        "schemaVersion": 27,
        "version": 0,
        "links": []
    }
}

def get_grafana_dashboard_json() -> str:
    """Get the Grafana dashboard configuration as JSON."""
    return json.dumps(GRAFANA_DASHBOARD, indent=2)

def create_grafana_datasource_config(prometheus_url: str) -> Dict[str, Any]:
    """Create Grafana datasource configuration for Prometheus."""
    return {
        "name": "Heimdall-Prometheus",
        "type": "prometheus",
        "url": prometheus_url,
        "access": "proxy",
        "isDefault": True,
        "jsonData": {
            "timeInterval": "30s",
            "queryTimeout": "60s",
            "httpMethod": "POST"
        }
    }