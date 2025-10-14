from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime


class DocumentBase(BaseModel):
    content: str = Field(..., min_length=1)
    metadata: Dict = Field(default_factory=dict)


class DocumentCreate(DocumentBase):
    pass


class DocumentResponse(DocumentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class DocumentChunkResponse(BaseModel):
    id: int
    document_id: int
    chunk_text: str
    chunk_index: int
    token_count: Optional[int] = None
    
    class Config:
        from_attributes = True


class EmbeddingResponse(BaseModel):
    id: int
    chunk_id: int
    Embedding_model_used: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class DocumentWithChunks(DocumentResponse):
    chunks: List[DocumentChunkResponse] = []


class SimilaritySearchRequest(BaseModel):
    query: str
    top_k: int = Field(default=5, ge=1, le=50)
    model: str = "text-embedding-ada-002"


class SimilaritySearchResult(BaseModel):
    chunk_id: int
    document_id: int
    chunk_text: str
    similarity_score: float
    document_content: str
    metadata: Dict