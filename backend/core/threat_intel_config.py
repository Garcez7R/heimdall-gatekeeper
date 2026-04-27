"""
Threat Intelligence feeds configuration and management.
"""
import os
from core.config import settings

# Threat Intelligence Feed Configurations
THREAT_INTEL_CONFIGS = {
    "otx": {
        "name": "AlienVault OTX",
        "url": "https://otx.alienvault.com/api/v1",
        "api_key": os.getenv("OTX_API_KEY", ""),
        "enabled": bool(os.getenv("OTX_API_KEY", "")),
        "rate_limit": 1000,  # requests per day
        "cache_ttl": 3600,   # 1 hour
        "endpoints": {
            "ip": "/indicators/IPv4/{ip}/general",
            "domain": "/indicators/domain/{domain}/general",
            "hash": "/indicators/file/{hash}/general"
        }
    },
    "misp": {
        "name": "MISP Threat Sharing",
        "url": os.getenv("MISP_URL", ""),
        "api_key": os.getenv("MISP_API_KEY", ""),
        "enabled": bool(os.getenv("MISP_URL", "") and os.getenv("MISP_API_KEY", "")),
        "rate_limit": 500,   # requests per day
        "cache_ttl": 1800,   # 30 minutes
        "endpoints": {
            "events": "/events/restSearch",
            "attributes": "/attributes/restSearch"
        }
    },
    "abuseipdb": {
        "name": "AbuseIPDB",
        "url": "https://api.abuseipdb.com/api/v2",
        "api_key": os.getenv("ABUSEIPDB_API_KEY", ""),
        "enabled": bool(os.getenv("ABUSEIPDB_API_KEY", "")),
        "rate_limit": 1000,  # requests per day
        "cache_ttl": 3600,   # 1 hour
        "endpoints": {
            "check": "/check",
            "reports": "/reports"
        }
    },
    "virustotal": {
        "name": "VirusTotal",
        "url": "https://www.virustotal.com/api/v3",
        "api_key": os.getenv("VIRUSTOTAL_API_KEY", ""),
        "enabled": bool(os.getenv("VIRUSTOTAL_API_KEY", "")),
        "rate_limit": 500,   # requests per day (free tier)
        "cache_ttl": 3600,   # 1 hour
        "endpoints": {
            "ip": "/ip_addresses/{ip}",
            "domain": "/domains/{domain}",
            "hash": "/files/{hash}"
        }
    },
    "shodan": {
        "name": "Shodan",
        "url": "https://api.shodan.io",
        "api_key": os.getenv("SHODAN_API_KEY", ""),
        "enabled": bool(os.getenv("SHODAN_API_KEY", "")),
        "rate_limit": 100,    # requests per day (free tier)
        "cache_ttl": 7200,    # 2 hours
        "endpoints": {
            "ip": "/shodan/host/{ip}",
            "search": "/shodan/host/search"
        }
    }
}

def get_enabled_feeds() -> dict:
    """Get all enabled threat intelligence feeds."""
    return {name: config for name, config in THREAT_INTEL_CONFIGS.items() if config["enabled"]}

def get_feed_config(feed_name: str) -> dict:
    """Get configuration for a specific feed."""
    return THREAT_INTEL_CONFIGS.get(feed_name, {})

def validate_feed_configs() -> list:
    """Validate all feed configurations and return issues."""
    issues = []

    for name, config in THREAT_INTEL_CONFIGS.items():
        if config["enabled"]:
            # Check required fields
            if not config.get("url"):
                issues.append(f"{name}: Missing URL configuration")

            if not config.get("api_key"):
                issues.append(f"{name}: Missing API key")

            # Check rate limits are reasonable
            if config.get("rate_limit", 0) <= 0:
                issues.append(f"{name}: Invalid rate limit")

            # Check cache TTL is reasonable
            if config.get("cache_ttl", 0) < 300:  # 5 minutes minimum
                issues.append(f"{name}: Cache TTL too short (minimum 300 seconds)")

    return issues

# Example environment variables for .env file
ENV_TEMPLATE = """
# Threat Intelligence API Keys
# Get your keys from the respective services:

# AlienVault OTX (https://otx.alienvault.com/)
OTX_API_KEY=your_otx_api_key_here

# MISP (https://www.misp-project.org/)
MISP_URL=https://your-misp-instance.com
MISP_API_KEY=your_misp_api_key_here

# AbuseIPDB (https://www.abuseipdb.com/)
ABUSEIPDB_API_KEY=your_abuseipdb_api_key_here

# VirusTotal (https://www.virustotal.com/)
VIRUSTOTAL_API_KEY=your_virustotal_api_key_here

# Shodan (https://www.shodan.io/)
SHODAN_API_KEY=your_shodan_api_key_here
"""

def generate_env_template() -> str:
    """Generate environment template for threat intel configuration."""
    return ENV_TEMPLATE.strip()

# Feed priority order (higher = more trusted)
FEED_PRIORITIES = {
    "misp": 10,      # Highest priority - curated threat intel
    "otx": 8,        # High priority - community driven
    "virustotal": 7, # Good reputation
    "abuseipdb": 6,  # Good for IP reputation
    "shodan": 5      # Good for exposure data
}

def get_feed_priority(feed_name: str) -> int:
    """Get priority score for a feed."""
    return FEED_PRIORITIES.get(feed_name, 0)

def get_feeds_by_priority() -> list:
    """Get enabled feeds sorted by priority."""
    enabled_feeds = get_enabled_feeds()
    return sorted(
        enabled_feeds.items(),
        key=lambda x: get_feed_priority(x[0]),
        reverse=True
    )