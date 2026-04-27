"""
SIEM integration module for Splunk, ELK, and other SIEM platforms.
"""
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import aiohttp
from core.config import settings

logger = logging.getLogger(__name__)

class SIEMExporter:
    """Base class for SIEM exporters."""

    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def export_events(self, events: List[Dict[str, Any]]) -> bool:
        """Export events to SIEM platform."""
        raise NotImplementedError

    async def export_alerts(self, alerts: List[Dict[str, Any]]) -> bool:
        """Export alerts to SIEM platform."""
        raise NotImplementedError

class SplunkHECExporter(SIEMExporter):
    """Splunk HTTP Event Collector integration."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__("splunk", config)
        self.hec_url = config.get("hec_url")
        self.hec_token = config.get("hec_token")
        self.index = config.get("index", "heimdall")
        self.source_type = config.get("source_type", "heimdall:events")

    async def export_events(self, events: List[Dict[str, Any]]) -> bool:
        """Export events to Splunk via HEC."""
        if not self.session or not self.hec_url or not self.hec_token:
            return False

        headers = {
            "Authorization": f"Splunk {self.hec_token}",
            "Content-Type": "application/json"
        }

        success_count = 0
        for event in events:
            # Format for Splunk HEC
            splunk_event = {
                "time": event.get("created_at"),
                "host": "heimdall-gatekeeper",
                "source": "heimdall-events",
                "sourcetype": self.source_type,
                "index": self.index,
                "event": event
            }

            try:
                async with self.session.post(
                    self.hec_url,
                    headers=headers,
                    json=splunk_event,
                    timeout=30
                ) as response:
                    if response.status == 200:
                        success_count += 1
                    else:
                        logger.warning(f"Splunk HEC error: {response.status} - {await response.text()}")

            except Exception as e:
                logger.error(f"Failed to export event to Splunk: {e}")

        return success_count == len(events)

    async def export_alerts(self, alerts: List[Dict[str, Any]]) -> bool:
        """Export alerts to Splunk via HEC."""
        if not self.session or not self.hec_url or not self.hec_token:
            return False

        headers = {
            "Authorization": f"Splunk {self.hec_token}",
            "Content-Type": "application/json"
        }

        success_count = 0
        for alert in alerts:
            # Format for Splunk HEC
            splunk_event = {
                "time": alert.get("created_at"),
                "host": "heimdall-gatekeeper",
                "source": "heimdall-alerts",
                "sourcetype": "heimdall:alerts",
                "index": self.index,
                "event": alert
            }

            try:
                async with self.session.post(
                    self.hec_url,
                    headers=headers,
                    json=splunk_event,
                    timeout=30
                ) as response:
                    if response.status == 200:
                        success_count += 1
                    else:
                        logger.warning(f"Splunk HEC error: {response.status} - {await response.text()}")

            except Exception as e:
                logger.error(f"Failed to export alert to Splunk: {e}")

        return success_count == len(alerts)

class ElasticsearchExporter(SIEMExporter):
    """Elasticsearch integration."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__("elasticsearch", config)
        self.es_url = config.get("es_url")
        self.api_key = config.get("api_key")
        self.username = config.get("username")
        self.password = config.get("password")
        self.index_prefix = config.get("index_prefix", "heimdall")

    def _get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers for Elasticsearch."""
        headers = {"Content-Type": "application/json"}

        if self.api_key:
            headers["Authorization"] = f"ApiKey {self.api_key}"
        elif self.username and self.password:
            import base64
            auth = base64.b64encode(f"{self.username}:{self.password}".encode()).decode()
            headers["Authorization"] = f"Basic {auth}"

        return headers

    async def export_events(self, events: List[Dict[str, Any]]) -> bool:
        """Export events to Elasticsearch via bulk API."""
        if not self.session or not self.es_url:
            return False

        # Create bulk request body
        bulk_body = ""
        index_name = f"{self.index_prefix}-events-{datetime.now().strftime('%Y-%m-%d')}"

        for event in events:
            # Index metadata
            bulk_body += json.dumps({
                "index": {
                    "_index": index_name,
                    "_id": event.get("id")
                }
            }) + "\n"

            # Document
            bulk_body += json.dumps(event) + "\n"

        headers = self._get_auth_headers()

        try:
            async with self.session.post(
                f"{self.es_url}/_bulk",
                headers=headers,
                data=bulk_body,
                timeout=60
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    if result.get("errors", False):
                        logger.warning(f"Elasticsearch bulk errors: {result}")
                        return False
                    return True
                else:
                    logger.error(f"Elasticsearch bulk error: {response.status} - {await response.text()}")
                    return False

        except Exception as e:
            logger.error(f"Failed to export events to Elasticsearch: {e}")
            return False

    async def export_alerts(self, alerts: List[Dict[str, Any]]) -> bool:
        """Export alerts to Elasticsearch via bulk API."""
        if not self.session or not self.es_url:
            return False

        # Create bulk request body
        bulk_body = ""
        index_name = f"{self.index_prefix}-alerts-{datetime.now().strftime('%Y-%m-%d')}"

        for alert in alerts:
            # Index metadata
            bulk_body += json.dumps({
                "index": {
                    "_index": index_name,
                    "_id": alert.get("id")
                }
            }) + "\n"

            # Document
            bulk_body += json.dumps(alert) + "\n"

        headers = self._get_auth_headers()

        try:
            async with self.session.post(
                f"{self.es_url}/_bulk",
                headers=headers,
                data=bulk_body,
                timeout=60
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    if result.get("errors", False):
                        logger.warning(f"Elasticsearch bulk errors: {result}")
                        return False
                    return True
                else:
                    logger.error(f"Elasticsearch bulk error: {response.status} - {await response.text()}")
                    return False

        except Exception as e:
            logger.error(f"Failed to export alerts to Elasticsearch: {e}")
            return False

class SIEMIntegrationManager:
    """Manages integrations with multiple SIEM platforms."""

    def __init__(self):
        self.exporters: Dict[str, SIEMExporter] = {}

    def add_splunk_integration(self, hec_url: str, hec_token: str, index: str = "heimdall") -> None:
        """Add Splunk HEC integration."""
        config = {
            "hec_url": hec_url,
            "hec_token": hec_token,
            "index": index
        }
        self.exporters["splunk"] = SplunkHECExporter(config)
        logger.info("Added Splunk HEC integration")

    def add_elasticsearch_integration(
        self,
        es_url: str,
        api_key: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        index_prefix: str = "heimdall"
    ) -> None:
        """Add Elasticsearch integration."""
        config = {
            "es_url": es_url,
            "api_key": api_key,
            "username": username,
            "password": password,
            "index_prefix": index_prefix
        }
        self.exporters["elasticsearch"] = ElasticsearchExporter(config)
        logger.info("Added Elasticsearch integration")

    async def export_events_to_all(self, events: List[Dict[str, Any]]) -> Dict[str, bool]:
        """Export events to all configured SIEM platforms."""
        results = {}

        for name, exporter in self.exporters.items():
            try:
                async with exporter:
                    success = await exporter.export_events(events)
                    results[name] = success
                    if success:
                        logger.info(f"Successfully exported {len(events)} events to {name}")
                    else:
                        logger.warning(f"Failed to export events to {name}")
            except Exception as e:
                logger.error(f"Error exporting events to {name}: {e}")
                results[name] = False

        return results

    async def export_alerts_to_all(self, alerts: List[Dict[str, Any]]) -> Dict[str, bool]:
        """Export alerts to all configured SIEM platforms."""
        results = {}

        for name, exporter in self.exporters.items():
            try:
                async with exporter:
                    success = await exporter.export_alerts(alerts)
                    results[name] = success
                    if success:
                        logger.info(f"Successfully exported {len(alerts)} alerts to {name}")
                    else:
                        logger.warning(f"Failed to export alerts to {name}")
            except Exception as e:
                logger.error(f"Error exporting alerts to {name}: {e}")
                results[name] = False

        return results

# Global SIEM integration manager
siem_manager = SIEMIntegrationManager()