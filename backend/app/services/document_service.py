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
    print(f"🔍 Similarity search for query: '{query[:100]}...'")
    
    # Generate query embedding
    query_embedding = await generate_embedding(query)
    print(f"✓ Generated query embedding: {len(query_embedding)} dimensions")
    
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
            "query_embedding": query_embedding,  # Pass as list, not string!
            "top_k": top_k
        }
    )
    
    results = [dict(row._mapping) for row in result]
    print(f"✓ Found {len(results)} matching documents")
    if results:
        for i, r in enumerate(results[:3]):  # Show top 3
            print(f"  {i+1}. Similarity: {r.get('similarity_score', 0):.4f} - {r.get('chunk_text', '')[:80]}...")
    
    return results


async def get_document(
    document_id: int,
    db: AsyncSession
) -> Optional[Document]:
    """
    Get a document by ID.
    
    Args:
        document_id: The ID of the document
        db: Database session
        
    Returns:
        Document object or None if not found
    """
    result = await db.execute(
        select(Document).where(Document.id == document_id)
    )
    return result.scalar_one_or_none()


async def list_documents(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100
) -> List[Document]:
    """
    List all documents with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of documents
    """
    result = await db.execute(
        select(Document)
        .order_by(Document.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def delete_document(
    document_id: int,
    db: AsyncSession
) -> bool:
    """
    Delete a document and all its chunks and embeddings.
    
    Args:
        document_id: The ID of the document to delete
        db: Database session
        
    Returns:
        True if deleted, False if not found
    """
    document = await get_document(document_id, db)
    if not document:
        return False
    
    await db.delete(document)
    await db.commit()
    return True