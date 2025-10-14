from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum
from sqlalchemy.sql import func
from app.database import Base
from app.models.message import ModelProvider


class SystemPrompt(Base):
    __tablename__ = "system_prompts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    model_provider = Column(Enum(ModelProvider), nullable=False, unique=True)
    prompt_template = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    include_rag_context = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<SystemPrompt(id={self.id}, name='{self.name}', model={self.model_provider})>"
