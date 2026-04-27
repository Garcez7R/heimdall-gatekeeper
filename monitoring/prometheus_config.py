"""
Prometheus configuration for Heimdall Gatekeeper monitoring.
"""
import yaml
from typing import Dict, Any

# Prometheus configuration
PROMETHEUS_CONFIG = {
    "global": {
        "scrape_interval": "15s",
        "evaluation_interval": "15s"
    },
    "rule_files": [
        "alert_rules.yml"
    ],
    "alerting": {
        "alertmanagers": [
            {
                "static_configs": [
                    {
                        "targets": ["alertmanager:9093"]
                    }
                ]
            }
        ]
    },
    "scrape_configs": [
        {
            "job_name": "heimdall-gatekeeper",
            "static_configs": [
                {
                    "targets": ["heimdall:8000"]
                }
            ],
            "metrics_path": "/metrics",
            "scrape_interval": "15s"
        },
        {
            "job_name": "node-exporter",
            "static_configs": [
                {
                    "targets": ["node-exporter:9100"]
                }
            ]
        }
    ]
}

# Alert rules for Heimdall
ALERT_RULES = {
    "groups": [
        {
            "name": "heimdall_alerts",
            "rules": [
                {
                    "alert": "HeimdallDown",
                    "expr": "up{job=\"heimdall-gatekeeper\"} == 0",
                    "for": "5m",
                    "labels": {
                        "severity": "critical"
                    },
                    "annotations": {
                        "summary": "Heimdall Gatekeeper is down",
                        "description": "Heimdall Gatekeeper has been down for more than 5 minutes."
                    }
                },
                {
                    "alert": "HighEventProcessingLatency",
                    "expr": "histogram_quantile(0.95, rate(heimdall_events_processing_duration_seconds_bucket[5m])) > 2",
                    "for": "5m",
                    "labels": {
                        "severity": "warning"
                    },
                    "annotations": {
                        "summary": "High event processing latency",
                        "description": "Event processing latency is above 2 seconds (95th percentile)."
                    }
                },
                {
                    "alert": "HighAPIErrorRate",
                    "expr": "rate(heimdall_api_requests_total{status=~\"4..|5..\"}[5m]) / rate(heimdall_api_requests_total[5m]) * 100 > 5",
                    "for": "5m",
                    "labels": {
                        "severity": "warning"
                    },
                    "annotations": {
                        "summary": "High API error rate",
                        "description": "API error rate is above 5%."
                    }
                },
                {
                    "alert": "QueueSizeHigh",
                    "expr": "heimdall_queue_size > 1000",
                    "for": "2m",
                    "labels": {
                        "severity": "warning"
                    },
                    "annotations": {
                        "summary": "Event queue size is high",
                        "description": "Event processing queue has more than 1000 items."
                    }
                },
                {
                    "alert": "LowCacheHitRate",
                    "expr": "(sum(rate(heimdall_cache_hits_total[5m])) / (sum(rate(heimdall_cache_hits_total[5m])) + sum(rate(heimdall_cache_misses_total[5m])))) * 100 < 80",
                    "for": "10m",
                    "labels": {
                        "severity": "info"
                    },
                    "annotations": {
                        "summary": "Low cache hit rate",
                        "description": "Cache hit rate is below 80%."
                    }
                },
                {
                    "alert": "ThreatIntelFailures",
                    "expr": "rate(heimdall_threat_intel_requests_total{status=\"error\"}[5m]) > 5",
                    "for": "5m",
                    "labels": {
                        "severity": "warning"
                    },
                    "annotations": {
                        "summary": "Threat intelligence API failures",
                        "description": "Threat intelligence API has more than 5 failures per minute."
                    }
                }
            ]
        }
    ]
}

def get_prometheus_config_yaml() -> str:
    """Get Prometheus configuration as YAML."""
    return yaml.dump(PROMETHEUS_CONFIG, default_flow_style=False)

def get_alert_rules_yaml() -> str:
    """Get alert rules as YAML."""
    return yaml.dump(ALERT_RULES, default_flow_style=False)

def create_docker_compose_monitoring() -> str:
    """Create docker-compose.yml for monitoring stack."""
    compose_config = {
        "version": "3.8",
        "services": {
            "prometheus": {
                "image": "prom/prometheus:latest",
                "container_name": "heimdall-prometheus",
                "ports": ["9090:9090"],
                "volumes": [
                    "./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml",
                    "./monitoring/alert_rules.yml:/etc/prometheus/alert_rules.yml",
                    "prometheus_data:/prometheus"
                ],
                "command": [
                    "--config.file=/etc/prometheus/prometheus.yml",
                    "--storage.tsdb.path=/prometheus",
                    "--web.console.libraries=/etc/prometheus/console_libraries",
                    "--web.console.templates=/etc/prometheus/consoles",
                    "--storage.tsdb.retention.time=200h",
                    "--web.enable-lifecycle"
                ],
                "restart": "unless-stopped"
            },
            "grafana": {
                "image": "grafana/grafana:latest",
                "container_name": "heimdall-grafana",
                "ports": ["3000:3000"],
                "environment": {
                    "GF_SECURITY_ADMIN_PASSWORD": "admin",
                    "GF_USERS_ALLOW_SIGN_UP": "false"
                },
                "volumes": [
                    "grafana_data:/var/lib/grafana",
                    "./monitoring/grafana/provisioning:/etc/grafana/provisioning"
                ],
                "restart": "unless-stopped"
            },
            "alertmanager": {
                "image": "prom/alertmanager:latest",
                "container_name": "heimdall-alertmanager",
                "ports": ["9093:9093"],
                "volumes": [
                    "./monitoring/alertmanager.yml:/etc/alertmanager/config.yml"
                ],
                "restart": "unless-stopped"
            },
            "node-exporter": {
                "image": "prom/node-exporter:latest",
                "container_name": "heimdall-node-exporter",
                "ports": ["9100:9100"],
                "volumes": [
                    "/proc:/host/proc:ro",
                    "/sys:/host/sys:ro",
                    "/:/rootfs:ro"
                ],
                "command": [
                    "--path.procfs=/host/proc",
                    "--path.rootfs=/rootfs",
                    "--path.sysfs=/host/sys",
                    "--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)"
                ],
                "restart": "unless-stopped"
            }
        },
        "volumes": {
            "prometheus_data": {},
            "grafana_data": {}
        }
    }

    return yaml.dump(compose_config, default_flow_style=False)