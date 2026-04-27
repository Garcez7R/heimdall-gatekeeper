"""
Threat Intelligence feeds integration (MISP, OTX, etc.)
"""
import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import aiohttp
from core.config import settings
from core.redis_cache import redis_cache
from core.prometheus_metrics import metrics

logger = logging.getLogger(__name__)

class ThreatIntelProvider:
    """Base class for threat intelligence providers."""

    def __init__(self, name: str, base_url: str, api_key: Optional[str] = None):
        self.name = name
        self.base_url = base_url
        self.api_key = api_key
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Make HTTP request to threat intel API."""
        if not self.session:
            return None

        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            async with self.session.get(url, headers=headers, params=params, timeout=30) as response:
                metrics.record_threat_intel_request(self.name, str(response.status))

                if response.status == 200:
                    return await response.json()
                else:
                    logger.warning(f"Threat intel request failed: {self.name} - {response.status}")
                    return None

        except Exception as e:
            logger.error(f"Threat intel request error: {self.name} - {e}")
            metrics.record_threat_intel_request(self.name, "error")
            return None

class OTXProvider(ThreatIntelProvider):
    """AlienVault OTX integration."""

    def __init__(self):
        super().__init__("otx", "https://otx.alienvault.com/api/v1", settings.OTX_API_KEY)

    async def get_ip_reputation(self, ip: str) -> Optional[Dict[str, Any]]:
        """Get IP reputation from OTX."""
        cache_key = f"otx_ip_{ip}"
        cached = await redis_cache.get_threat_intel(cache_key)

        if cached:
            metrics.record_cache_hit("threat_intel")
            return cached

        metrics.record_cache_miss("threat_intel")
        data = await self._make_request(f"indicators/IPv4/{ip}/general")

        if data:
            await redis_cache.cache_threat_intel(cache_key, data, ttl=3600)  # 1 hour
            metrics.record_threat_intel_enrichment("ip_reputation")

        return data

    async def get_domain_reputation(self, domain: str) -> Optional[Dict[str, Any]]:
        """Get domain reputation from OTX."""
        cache_key = f"otx_domain_{domain}"
        cached = await redis_cache.get_threat_intel(cache_key)

        if cached:
            metrics.record_cache_hit("threat_intel")
            return cached

        metrics.record_cache_miss("threat_intel")
        data = await self._make_request(f"indicators/domain/{domain}/general")

        if data:
            await redis_cache.cache_threat_intel(cache_key, data, ttl=3600)
            metrics.record_threat_intel_enrichment("domain_reputation")

        return data

class MISPProvider(ThreatIntelProvider):
    """MISP threat intelligence platform integration."""

    def __init__(self):
        super().__init__("misp", settings.MISP_URL, settings.MISP_API_KEY)

    async def get_recent_events(self, limit: int = 50) -> Optional[List[Dict]]:
        """Get recent MISP events."""
        cache_key = "misp_recent_events"
        cached = await redis_cache.get_threat_intel(cache_key)

        if cached:
            metrics.record_cache_hit("threat_intel")
            return cached

        metrics.record_cache_miss("threat_intel")
        params = {
            "limit": str(limit),
            "published": "1",  # Only published events
            "timestamp": str(int((datetime.now() - timedelta(days=7)).timestamp()))  # Last 7 days
        }

        data = await self._make_request("events/restSearch", params)

        if data and "response" in data:
            events = data["response"]
            await redis_cache.cache_threat_intel(cache_key, events, ttl=1800)  # 30 minutes
            metrics.record_threat_intel_enrichment("misp_events")
            return events

        return []

class ThreatIntelAggregator:
    """Aggregates threat intelligence from multiple sources."""

    def __init__(self):
        self.providers = {
            "otx": OTXProvider(),
            "misp": MISPProvider()
        }

    async def enrich_ip(self, ip: str) -> Dict[str, Any]:
        """Enrich IP address with threat intelligence."""
        enrichment = {
            "ip": ip,
            "sources": {},
            "malicious_score": 0,
            "tags": [],
            "last_seen": None
        }

        async with self.providers["otx"] as otx:
            otx_data = await otx.get_ip_reputation(ip)
            if otx_data:
                enrichment["sources"]["otx"] = otx_data
                # Calculate malicious score based on pulse count
                pulse_count = otx_data.get("pulse_info", {}).get("count", 0)
                enrichment["malicious_score"] = min(pulse_count * 10, 100)

                # Extract tags
                pulses = otx_data.get("pulse_info", {}).get("pulses", [])
                for pulse in pulses[:5]:  # Limit to top 5
                    enrichment["tags"].extend(pulse.get("tags", []))

        return enrichment

    async def enrich_domain(self, domain: str) -> Dict[str, Any]:
        """Enrich domain with threat intelligence."""
        enrichment = {
            "domain": domain,
            "sources": {},
            "malicious_score": 0,
            "tags": [],
            "last_seen": None
        }

        async with self.providers["otx"] as otx:
            otx_data = await otx.get_domain_reputation(domain)
            if otx_data:
                enrichment["sources"]["otx"] = otx_data
                pulse_count = otx_data.get("pulse_info", {}).get("count", 0)
                enrichment["malicious_score"] = min(pulse_count * 10, 100)

                pulses = otx_data.get("pulse_info", {}).get("pulses", [])
                for pulse in pulses[:5]:
                    enrichment["tags"].extend(pulse.get("tags", []))

        return enrichment

    async def get_misp_indicators(self) -> List[Dict]:
        """Get indicators from MISP."""
        async with self.providers["misp"] as misp:
            return await misp.get_recent_events() or []

    async def check_indicator_match(self, indicator_value: str, indicator_type: str) -> Dict[str, Any]:
        """Check if an indicator matches known threats."""
        if indicator_type == "ip":
            return await self.enrich_ip(indicator_value)
        elif indicator_type == "domain":
            return await self.enrich_domain(indicator_value)
        else:
            return {"indicator": indicator_value, "type": indicator_type, "matched": False}

# Global threat intelligence aggregator
threat_intel = ThreatIntelAggregator()