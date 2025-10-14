from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class MessageRole(str, enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ModelProvider(str, enum.Enum):
    CLAUDE = "claude"
    CHATGPT = "chatgpt"
    GEMINI = "gemini"
    GROK = "grok"
    PERPLEXITY = "perplexity"


class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(BigInteger, ForeignKey("conversations.id"), nullable=False, index=True)
    role = Column(SQLEnum(MessageRole), nullable=False)
    content = Column(Text, nullable=False)
    model_provider = Column(SQLEnum(ModelProvider), nullable=True)  # Null for user messages
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relationship to conversation
    conversation = relationship("Conversation", back_populates="messages")
    
    def __repr__(self):
        return f"<Message(id={self.id}, role='{self.role}', provider='{self.model_provider}')>"