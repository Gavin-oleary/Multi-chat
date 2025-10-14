from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict
from app.models.message import ModelProvider


class ChatRequest(BaseModel):
    """Request to send a prompt to all models"""
    prompt: str = Field(..., min_length=1, max_length=10000)
    conversation_id: Optional[int] = Field(None, ge=1)  # If None, create new conversation
    models: Optional[List[ModelProvider]] = None  # If None, use all models
    
    # RAG options
    use_rag: Optional[bool] = False
    top_k: Optional[int] = Field(default=3, ge=1, le=10)
    
    @validator('prompt')
    def validate_prompt(cls, v):
        if not v.strip():
            raise ValueError('Prompt cannot be empty')
        # Basic token estimation (rough approximation: ~4 chars per token)
        estimated_tokens = len(v) / 4
        if estimated_tokens > 2000:  # Adjust based on your needs
            raise ValueError(f'Prompt too long: approximately {int(estimated_tokens)} tokens (max 2000)')
        return v.strip()
    
    @validator('models')
    def validate_models(cls, v):
        if v is not None and len(v) == 0:
            raise ValueError('If models are specified, at least one must be selected')
        return v


class ModelResponse(BaseModel):
    """Response from a single model"""
    provider: ModelProvider
    content: str
    error: Optional[str] = None  # If the model failed to respond
    latency_ms: Optional[float] = None  # Time taken to get response


class ChatResponse(BaseModel):
    """Response containing all model responses"""
    conversation_id: int
    user_message_id: int
    responses: List[ModelResponse]
    rag_context_used: bool = False
    context_chunks: Optional[List[Dict]] = None
    
class StreamChunk(BaseModel):
    """For streaming responses (future enhancement)"""
    provider: ModelProvider
    content: str
    is_final: bool = False