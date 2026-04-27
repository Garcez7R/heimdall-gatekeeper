"""
Prometheus metrics and monitoring for Heimdall Gatekeeper.
"""
import time
from typing import Dict, Any
from prometheus_client import Counter, Gauge, Histogram, CollectorRegistry, generate_latest
from core.config import settings

# Create registry
registry = CollectorRegistry()

# Event processing metrics
events_processed = Counter(
    'heimdall_events_processed_total',
    'Total number of events processed',
    ['severity', 'source'],
    registry=registry
)

events_processing_time = Histogram(
    'heimdall_events_processing_duration_seconds',
    'Time spent processing events',
    ['rule_type'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0],
    registry=registry
)

# Alert metrics
alerts_generated = Counter(
    'heimdall_alerts_generated_total',
    'Total number of alerts generated',
    ['severity', 'rule_name'],
    registry=registry
)

alerts_acknowledged = Counter(
    'heimdall_alerts_acknowledged_total',
    'Total number of alerts acknowledged',
    ['severity'],
    registry=registry
)

alerts_resolved = Counter(
    'heimdall_alerts_resolved_total',
    'Total number of alerts resolved',
    ['severity'],
    registry=registry
)

# System metrics
active_connections = Gauge(
    'heimdall_active_connections',
    'Number of active WebSocket connections',
    registry=registry
)

queue_size = Gauge(
    'heimdall_queue_size',
    'Current size of the event processing queue',
    registry=registry
)

# API metrics
api_requests = Counter(
    'heimdall_api_requests_total',
    'Total number of API requests',
    ['method', 'endpoint', 'status'],
    registry=registry
)

api_request_duration = Histogram(
    'heimdall_api_request_duration_seconds',
    'API request duration',
    ['method', 'endpoint'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0],
    registry=registry
)

# Database metrics
db_connections = Gauge(
    'heimdall_db_connections_active',
    'Number of active database connections',
    registry=registry
)

db_query_duration = Histogram(
    'heimdall_db_query_duration_seconds',
    'Database query duration',
    ['operation'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0],
    registry=registry
)

# Cache metrics
cache_hits = Counter(
    'heimdall_cache_hits_total',
    'Total number of cache hits',
    ['cache_type'],
    registry=registry
)

cache_misses = Counter(
    'heimdall_cache_misses_total',
    'Total number of cache misses',
    ['cache_type'],
    registry=registry
)

# Threat intelligence metrics
threat_intel_requests = Counter(
    'heimdall_threat_intel_requests_total',
    'Total threat intelligence API requests',
    ['provider', 'status'],
    registry=registry
)

threat_intel_enrichments = Counter(
    'heimdall_threat_intel_enrichments_total',
    'Total events enriched with threat intelligence',
    ['intel_type'],
    registry=registry
)

class MetricsCollector:
    """Collects and exposes Prometheus metrics."""

    @staticmethod
    def record_event_processed(severity: str, source: str):
        """Record an event being processed."""
        events_processed.labels(severity=severity, source=source).inc()

    @staticmethod
    def record_event_processing_time(rule_type: str, duration: float):
        """Record event processing duration."""
        events_processing_time.labels(rule_type=rule_type).observe(duration)

    @staticmethod
    def record_alert_generated(severity: str, rule_name: str):
        """Record an alert being generated."""
        alerts_generated.labels(severity=severity, rule_name=rule_name).inc()

    @staticmethod
    def record_alert_acknowledged(severity: str):
        """Record an alert being acknowledged."""
        alerts_acknowledged.labels(severity=severity).inc()

    @staticmethod
    def record_alert_resolved(severity: str):
        """Record an alert being resolved."""
        alerts_resolved.labels(severity=severity).inc()

    @staticmethod
    def update_active_connections(count: int):
        """Update active WebSocket connections count."""
        active_connections.set(count)

    @staticmethod
    def update_queue_size(size: int):
        """Update event queue size."""
        queue_size.set(size)

    @staticmethod
    def record_api_request(method: str, endpoint: str, status: int, duration: float):
        """Record API request metrics."""
        api_requests.labels(method=method, endpoint=endpoint, status=status).inc()
        api_request_duration.labels(method=method, endpoint=endpoint).observe(duration)

    @staticmethod
    def update_db_connections(count: int):
        """Update active database connections."""
        db_connections.set(count)

    @staticmethod
    def record_db_query(operation: str, duration: float):
        """Record database query duration."""
        db_query_duration.labels(operation=operation).observe(duration)

    @staticmethod
    def record_cache_hit(cache_type: str):
        """Record cache hit."""
        cache_hits.labels(cache_type=cache_type).inc()

    @staticmethod
    def record_cache_miss(cache_type: str):
        """Record cache miss."""
        cache_misses.labels(cache_type=cache_type).inc()

    @staticmethod
    def record_threat_intel_request(provider: str, status: str):
        """Record threat intelligence API request."""
        threat_intel_requests.labels(provider=provider, status=status).inc()

    @staticmethod
    def record_threat_intel_enrichment(intel_type: str):
        """Record threat intelligence enrichment."""
        threat_intel_enrichments.labels(intel_type=intel_type).inc()

    @staticmethod
    def get_metrics() -> str:
        """Get all metrics in Prometheus format."""
        return generate_latest(registry).decode('utf-8')

# Global metrics collector
metrics = MetricsCollector()