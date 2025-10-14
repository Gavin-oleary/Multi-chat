"""
API endpoints for AI provider management and health status.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, List, Optional
from app.models.message import ModelProvider
from app.utils.circuit_breaker import circuit_manager, CircuitState
from app.schemas.provider import ProviderHealth, ProviderStatus
from app.utils.cache import response_cache

router = APIRouter()


@router.get("/health", response_model=Dict[str, ProviderHealth])
async def get_provider_health():
    """
    Get health status of all AI providers.
    
    Returns:
        Dict mapping provider names to their health status
    """
    states = circuit_manager.get_provider_states()
    health_status = {}
    
    for provider in ModelProvider:
        provider_name = provider.value
        breaker = circuit_manager.get_breaker(provider_name)
        
        health_status[provider_name] = ProviderHealth(
            provider=provider_name,
            status=states.get(provider_name, "closed"),
            failure_count=breaker.failure_count,
            last_failure_time=breaker.last_failure_time if breaker.last_failure_time > 0 else None,
            is_available=breaker.is_closed or breaker.state.value == "half_open"
        )
    
    return health_status


@router.get("/available", response_model=List[str])
async def get_available_providers():
    """
    Get list of currently available AI providers.
    
    Returns:
        List of provider names that are available for use
    """
    all_providers = [p.value for p in ModelProvider]
    healthy_providers = circuit_manager.get_healthy_providers(all_providers)
    return healthy_providers


@router.post("/reset/{provider_name}")
async def reset_provider_circuit(provider_name: str):
    """
    Reset circuit breaker for a specific provider.
    
    Args:
        provider_name: Name of the provider to reset
        
    Returns:
        Success message
    """
    # Validate provider name
    valid_providers = [p.value for p in ModelProvider]
    if provider_name not in valid_providers:
        raise ValueError(f"Invalid provider: {provider_name}")
    
    # Reset the circuit breaker
    breaker = circuit_manager.get_breaker(provider_name)
    breaker.state = CircuitState.CLOSED
    breaker.failure_count = 0
    breaker.last_failure_time = 0
    
    return {"message": f"Circuit breaker for {provider_name} has been reset"}


@router.get("/cache/stats")
async def get_cache_stats():
    """
    Get cache statistics.
    
    Returns:
        Cache statistics including total entries and provider breakdown
    """
    return response_cache.get_cache_stats()


@router.delete("/cache")
async def clear_cache(provider: Optional[str] = None):
    """
    Clear response cache.
    
    Args:
        provider: Optional provider name to clear cache for specific provider
        
    Returns:
        Number of cache entries cleared
    """
    if provider:
        # Validate provider
        valid_providers = [p.value for p in ModelProvider]
        if provider not in valid_providers:
            raise HTTPException(status_code=400, detail=f"Invalid provider: {provider}")
        
        pattern = f"chat_response:{provider}:*"
    else:
        pattern = None
    
    cleared = response_cache.clear_cache(pattern)
    return {
        "message": f"Cleared {cleared} cache entries",
        "provider": provider,
        "count": cleared
    }
