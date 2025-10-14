from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
from app.models.message import MessageRole, ModelProvider


class MessageBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=50000)
    role: MessageRole
    
    @validator('content')
    def validate_content(cls, v):
        if not v.strip():
            raise ValueError('Message content cannot be empty')
        return v.strip()


class MessageCreate(MessageBase):
    conversation_id: int = Field(..., ge=1)
    model_provider: Optional[ModelProvider] = None
    
    class Config:
        protected_namespaces = ()


class MessageResponse(MessageBase):
    id: int
    conversation_id: int
    model_provider: Optional[ModelProvider] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
        protected_namespaces = ()