from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import List, Optional
from app.schemas.message import MessageResponse


class ConversationBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    
    @validator('title')
    def validate_title(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()


class ConversationCreate(ConversationBase):
    pass


class ConversationUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    
    @validator('title')
    def validate_title(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip() if v else v


class ConversationResponse(ConversationBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True  # Replaces orm_mode in Pydantic v2


class ConversationWithMessages(ConversationResponse):
    messages: List[MessageResponse] = []
    
    class Config:
        from_attributes = True