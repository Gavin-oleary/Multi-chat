from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, ARRAY, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base
from pgvector.sqlalchemy import Vector


class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    doc_metadata = Column(JSONB, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Document(id={self.id}, content='{self.content[:50]}...')>"


class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    chunk_text = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    token_count = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    document = relationship("Document", back_populates="chunks")
    embeddings = relationship("Embedding", back_populates="chunk", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<DocumentChunk(id={self.id}, chunk_index={self.chunk_index})>"


class Embedding(Base):
    __tablename__ = "embeddings"
    
    id = Column(Integer, primary_key=True, index=True)
    chunk_id = Column(Integer, ForeignKey("document_chunks.id", ondelete="CASCADE"), nullable=False, index=True)
    embedding_vector = Column(Vector(1536))  # pgvector type
    model_used = Column(String(100), nullable=False, default="text-embedding-ada-002")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    chunk = relationship("DocumentChunk", back_populates="embeddings")
    
    def __repr__(self):
        return f"<Embedding(id={self.id}, model={self.model_used})>"