from typing import List, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from app.models.document import Document, DocumentChunk, Embedding
from app.config import settings


async def create_document_with_embeddings(
    content: str,
    metadata: Dict,
    db: AsyncSession,
    chunk_size: int = 500
) -> Document:
    """
    Create a document, chunk it, and generate embeddings.
    """
    # Create document
    document = Document(content=content, doc_metadata=metadata)
    db.add(document)
    await db.flush()  # Get the ID without committing
    
    # Chunk the content
    chunks = chunk_text(content, chunk_size)
    
    # Create chunks and embeddings
    for idx, chunk_content in enumerate(chunks):
        # Create chunk
        chunk = DocumentChunk(
            document_id=document.id,
            chunk_text=chunk_content,
            chunk_index=idx,
            token_count=len(chunk_content.split())  # Simple token count
        )
        db.add(chunk)
        await db.flush()
        
        # Generate embedding
        embedding_vector = await generate_embedding(chunk_content)
        
        embedding = Embedding(
            chunk_id=chunk.id,
            embedding_vector=embedding_vector,
            model_used="text-embedding-ada-002"
        )
        db.add(embedding)
    
    await db.commit()
    await db.refresh(document)
    return document


def chunk_text(text: str, chunk_size: int = 500) -> List[str]:
    """
    Simple text chunking by character count with overlap.
    """
    chunks = []
    words = text.split()
    current_chunk = []
    current_length = 0
    
    for word in words:
        current_chunk.append(word)
        current_length += len(word) + 1  # +1 for space
        
        if current_length >= chunk_size:
            chunks.append(' '.join(current_chunk))
            # Keep last 50 words for overlap
            current_chunk = current_chunk[-50:]
            current_length = sum(len(w) + 1 for w in current_chunk)
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks


async def generate_embedding(text: str) -> List[float]:
    """
    Generate embedding using OpenAI's API.
    """
    from openai import OpenAI
    
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    
    return response.data[0].embedding


async def similarity_search(
    query: str,
    db: AsyncSession,
    top_k: int = 5
) -> List[Dict]:
    """
    Perform semantic similarity search using cosine similarity.
    """
    # Generate query embedding
    query_embedding = await generate_embedding(query)
    
    # Perform similarity search using pgvector
    query_sql = text("""
        SELECT 
            dc.id as chunk_id,
            dc.document_id,
            dc.chunk_text,
            d.content as document_content,
            d.doc_metadata,
            1 - (e.embedding_vector <=> :query_embedding) as similarity_score
        FROM embeddings e
        JOIN document_chunks dc ON e.chunk_id = dc.id
        JOIN documents d ON dc.document_id = d.id
        ORDER BY e.embedding_vector <=> :query_embedding
        LIMIT :top_k
    """)
    
    result = await db.execute(
        query_sql,
        {
            "query_embedding": str(query_embedding),
            "top_k": top_k
        }
    )
    
    return [dict(row._mapping) for row in result]