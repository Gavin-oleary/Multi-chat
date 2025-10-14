"""
Response caching utilities using Redis.
"""

import hashlib
import json
import redis
from typing import Optional, Dict, List, Any
from datetime import timedelta
import logging

from app.config import settings
from app.models.message import ModelProvider

logger = logging.getLogger(__name__)


class ResponseCache:
    """
    Cache for AI model responses using Redis.
    """
    
    def __init__(self, redis_url: Optional[str] = None):
        """
        Initialize Redis cache.
        
        Args:
            redis_url: Redis connection URL (defaults to settings)
        """
        self.redis_url = redis_url or settings.REDIS_URL
        self._redis = None
        self.cache_ttl = timedelta(hours=24)  # Default TTL
        
    @property
    def redis_client(self) -> Optional[redis.Redis]:
        """Get Redis client (lazy initialization)."""
        if self._redis is None and self.redis_url:
            try:
                self._redis = redis.from_url(
                    self.redis_url,
                    decode_responses=True
                )
                # Test connection
                self._redis.ping()
                logger.info("Redis cache connected successfully")
            except Exception as e:
                logger.warning(f"Failed to connect to Redis: {e}")
                self._redis = None
        return self._redis
    
    def generate_cache_key(
        self,
        prompt: str,
        provider: ModelProvider,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Generate a unique cache key for a prompt + provider + history combination.
        
        Args:
            prompt: The user's prompt
            provider: The AI provider
            conversation_history: Previous conversation messages
            
        Returns:
            Cache key string
        """
        # Create a dictionary of cache inputs
        cache_data = {
            "prompt": prompt.strip().lower(),
            "provider": provider.value,
            "history_length": len(conversation_history) if conversation_history else 0
        }
        
        # Include a summary of conversation history if present
        if conversation_history:
            # Use last few messages to capture context
            recent_history = conversation_history[-6:]  # Last 3 exchanges
            history_summary = []
            for msg in recent_history:
                # Create a normalized version of each message
                normalized = msg.get("content", "").strip().lower()[:100]
                history_summary.append({
                    "role": msg.get("role"),
                    "content_preview": normalized
                })
            cache_data["history_summary"] = history_summary
        
        # Convert to stable JSON string
        cache_string = json.dumps(cache_data, sort_keys=True)
        
        # Generate SHA256 hash
        hash_object = hashlib.sha256(cache_string.encode())
        hash_hex = hash_object.hexdigest()
        
        # Create readable cache key
        return f"chat_response:{provider.value}:{hash_hex[:16]}"
    
    async def get_cached_response(
        self,
        prompt: str,
        provider: ModelProvider,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Optional[str]:
        """
        Get cached response if available.
        
        Args:
            prompt: The user's prompt
            provider: The AI provider
            conversation_history: Previous conversation messages
            
        Returns:
            Cached response content or None
        """
        if not self.redis_client:
            return None
        
        try:
            cache_key = self.generate_cache_key(prompt, provider, conversation_history)
            cached_value = self.redis_client.get(cache_key)
            
            if cached_value:
                logger.info(f"Cache hit for {provider.value}: {cache_key}")
                # Update TTL on cache hit
                self.redis_client.expire(cache_key, self.cache_ttl)
                return cached_value
            
            logger.debug(f"Cache miss for {provider.value}: {cache_key}")
            return None
            
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    async def set_cached_response(
        self,
        prompt: str,
        provider: ModelProvider,
        response: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> bool:
        """
        Cache a response.
        
        Args:
            prompt: The user's prompt
            provider: The AI provider
            response: The response to cache
            conversation_history: Previous conversation messages
            
        Returns:
            True if cached successfully
        """
        if not self.redis_client or not response:
            return False
        
        try:
            cache_key = self.generate_cache_key(prompt, provider, conversation_history)
            
            # Store with TTL
            self.redis_client.setex(
                cache_key,
                self.cache_ttl,
                response
            )
            
            logger.info(f"Cached response for {provider.value}: {cache_key}")
            return True
            
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False
    
    def clear_cache(self, pattern: Optional[str] = None) -> int:
        """
        Clear cache entries.
        
        Args:
            pattern: Optional pattern to match keys (e.g., "chat_response:claude:*")
            
        Returns:
            Number of keys deleted
        """
        if not self.redis_client:
            return 0
        
        try:
            if pattern:
                keys = self.redis_client.keys(pattern)
            else:
                keys = self.redis_client.keys("chat_response:*")
            
            if keys:
                return self.redis_client.delete(*keys)
            return 0
            
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
            return 0
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache stats
        """
        if not self.redis_client:
            return {"enabled": False}
        
        try:
            # Get all cache keys
            keys = self.redis_client.keys("chat_response:*")
            
            # Group by provider
            provider_counts = {}
            for key in keys:
                parts = key.split(":")
                if len(parts) >= 2:
                    provider = parts[1]
                    provider_counts[provider] = provider_counts.get(provider, 0) + 1
            
            return {
                "enabled": True,
                "total_entries": len(keys),
                "providers": provider_counts,
                "ttl_seconds": int(self.cache_ttl.total_seconds())
            }
            
        except Exception as e:
            logger.error(f"Cache stats error: {e}")
            return {"enabled": False, "error": str(e)}


# Global cache instance
response_cache = ResponseCache()
