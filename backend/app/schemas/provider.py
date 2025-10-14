"""
Schemas for AI provider management.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProviderHealth(BaseModel):
    """Health status of an AI provider"""
    provider: str
    status: str  # closed, open, half_open
    failure_count: int
    last_failure_time: Optional[float]
    is_available: bool

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class ProviderStatus(BaseModel):
    """Simple status of a provider"""
    provider: str
    is_available: bool
