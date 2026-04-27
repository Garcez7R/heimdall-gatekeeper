"""
Redis cache layer for detection rules and performance optimization.
"""
import json
import logging
from typing import Dict, List, Optional, Any
from redis import Redis
from core.config import settings

logger = logging.getLogger(__name__)

class RedisCache:
    """Redis cache for detection rules and performance optimization."""

    def __init__(self):
        self.redis = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
            decode_responses=True,
            socket_timeout=5,
            retry_on_timeout=True
        )
        self.rules_cache_key = "heimdall:rules"
        self.rules_ttl = 3600  # 1 hour

    async def cache_detection_rules(self, rules: Dict[str, Any]) -> bool:
        """Cache detection rules in Redis."""
        try:
            self.redis.setex(
                self.rules_cache_key,
                self.rules_ttl,
                json.dumps(rules)
            )
            logger.info(f"Cached {len(rules)} detection rules")
            return True
        except Exception as e:
            logger.error(f"Failed to cache detection rules: {e}")
            return False

    async def get_detection_rules(self) -> Optional[Dict[str, Any]]:
        """Retrieve cached detection rules."""
        try:
            cached = self.redis.get(self.rules_cache_key)
            if cached:
                return json.loads(cached)
            return None
        except Exception as e:
            logger.error(f"Failed to retrieve cached rules: {e}")
            return None

    async def invalidate_rules_cache(self) -> bool:
        """Invalidate the rules cache."""
        try:
            self.redis.delete(self.rules_cache_key)
            logger.info("Invalidated rules cache")
            return True
        except Exception as e:
            logger.error(f"Failed to invalidate cache: {e}")
            return False

    async def cache_threat_intel(self, intel_type: str, data: Dict[str, Any], ttl: int = 86400) -> bool:
        """Cache threat intelligence data."""
        try:
            key = f"heimdall:intel:{intel_type}"
            self.redis.setex(key, ttl, json.dumps(data))
            return True
        except Exception as e:
            logger.error(f"Failed to cache threat intel {intel_type}: {e}")
            return False

    async def get_threat_intel(self, intel_type: str) -> Optional[Dict[str, Any]]:
        """Retrieve cached threat intelligence."""
        try:
            key = f"heimdall:intel:{intel_type}"
            cached = self.redis.get(key)
            return json.loads(cached) if cached else None
        except Exception as e:
            logger.error(f"Failed to retrieve threat intel {intel_type}: {e}")
            return None

    def is_connected(self) -> bool:
        """Check Redis connection health."""
        try:
            self.redis.ping()
            return True
        except Exception:
            return False

# Global cache instance
redis_cache = RedisCache()