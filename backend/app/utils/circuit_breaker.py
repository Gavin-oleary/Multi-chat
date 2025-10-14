"""
Circuit breaker pattern implementation for AI providers.
Prevents cascading failures when AI providers are down.
"""

import asyncio
import time
from typing import Optional, Callable, Any, Dict
from enum import Enum
from functools import wraps


class CircuitState(Enum):
    """States of the circuit breaker"""
    CLOSED = "closed"  # Normal operation
    OPEN = "open"      # Provider is failing, reject requests
    HALF_OPEN = "half_open"  # Testing if provider is back


class CircuitBreaker:
    """
    Circuit breaker implementation for AI providers.
    
    When a provider fails multiple times, the circuit opens and subsequent
    requests are rejected immediately without calling the provider.
    After a timeout period, the circuit enters half-open state to test
    if the provider is back online.
    """
    
    def __init__(
        self,
        failure_threshold: int = 3,
        timeout: int = 60,
        recovery_timeout: int = 30
    ):
        """
        Initialize circuit breaker.
        
        Args:
            failure_threshold: Number of failures before opening circuit
            timeout: Seconds to wait before entering half-open state
            recovery_timeout: Timeout for individual requests in seconds
        """
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = 0
        self.state = CircuitState.CLOSED
        self._lock = asyncio.Lock()
        
    @property
    def is_open(self) -> bool:
        """Check if circuit is open"""
        return self.state == CircuitState.OPEN
    
    @property
    def is_closed(self) -> bool:
        """Check if circuit is closed"""
        return self.state == CircuitState.CLOSED
    
    async def _check_state(self) -> None:
        """Check and update circuit state"""
        async with self._lock:
            if self.state == CircuitState.OPEN:
                # Check if timeout has passed
                if time.time() - self.last_failure_time >= self.timeout:
                    self.state = CircuitState.HALF_OPEN
                    self.failure_count = 0
    
    async def _on_success(self) -> None:
        """Handle successful call"""
        async with self._lock:
            self.failure_count = 0
            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.CLOSED
    
    async def _on_failure(self) -> None:
        """Handle failed call"""
        async with self._lock:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
    
    async def call(
        self,
        func: Callable,
        provider_name: str,
        *args,
        **kwargs
    ) -> Any:
        """
        Execute function with circuit breaker protection.
        
        Args:
            func: Async function to call
            provider_name: Name of the provider for error messages
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func
            
        Returns:
            Result of func
            
        Raises:
            Exception: If circuit is open or function fails
        """
        await self._check_state()
        
        if self.state == CircuitState.OPEN:
            raise Exception(f"{provider_name} circuit breaker is OPEN")
        
        try:
            # Add timeout to prevent hanging
            result = await asyncio.wait_for(
                func(*args, **kwargs),
                timeout=self.recovery_timeout
            )
            await self._on_success()
            return result
        except Exception as e:
            await self._on_failure()
            raise e


class ProviderCircuitManager:
    """
    Manages circuit breakers for all AI providers.
    """
    
    def __init__(
        self,
        failure_threshold: int = 3,
        timeout: int = 60,
        recovery_timeout: int = 30
    ):
        """
        Initialize circuit manager.
        
        Args:
            failure_threshold: Number of failures before opening circuit
            timeout: Seconds to wait before entering half-open state
            recovery_timeout: Timeout for individual requests in seconds
        """
        self.breakers: Dict[str, CircuitBreaker] = {}
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.recovery_timeout = recovery_timeout
    
    def get_breaker(self, provider_name: str) -> CircuitBreaker:
        """
        Get or create circuit breaker for provider.
        
        Args:
            provider_name: Name of the provider
            
        Returns:
            Circuit breaker instance
        """
        if provider_name not in self.breakers:
            self.breakers[provider_name] = CircuitBreaker(
                failure_threshold=self.failure_threshold,
                timeout=self.timeout,
                recovery_timeout=self.recovery_timeout
            )
        return self.breakers[provider_name]
    
    def get_provider_states(self) -> Dict[str, str]:
        """
        Get current state of all providers.
        
        Returns:
            Dict mapping provider names to their circuit states
        """
        return {
            provider: breaker.state.value
            for provider, breaker in self.breakers.items()
        }
    
    def get_healthy_providers(self, providers: list) -> list:
        """
        Filter providers to only include those with closed circuits.
        
        Args:
            providers: List of provider names to check
            
        Returns:
            List of providers with closed circuits
        """
        healthy = []
        for provider in providers:
            breaker = self.get_breaker(provider)
            if breaker.is_closed or breaker.state == CircuitState.HALF_OPEN:
                healthy.append(provider)
        return healthy


# Global circuit manager instance
circuit_manager = ProviderCircuitManager()
