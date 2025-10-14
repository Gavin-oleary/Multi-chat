from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.message import ModelProvider


class SystemPromptBase(BaseModel):
    """Base schema for system prompts"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    model_provider: ModelProvider
    prompt_template: str = Field(..., min_length=1)
    is_active: bool = True
    include_rag_context: bool = True


class SystemPromptCreate(SystemPromptBase):
    """Schema for creating a system prompt"""
    pass


class SystemPromptUpdate(BaseModel):
    """Schema for updating a system prompt"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    prompt_template: Optional[str] = Field(None, min_length=1)
    is_active: Optional[bool] = None
    include_rag_context: Optional[bool] = None


class SystemPromptResponse(SystemPromptBase):
    """Schema for system prompt responses"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SystemPromptList(BaseModel):
    """Schema for listing system prompts"""
    prompts: list[SystemPromptResponse]
    total: int
