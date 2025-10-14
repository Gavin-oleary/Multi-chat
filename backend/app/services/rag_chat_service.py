"""
RAG-enhanced chat service that retrieves relevant context from documents.
"""

from typing import List, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.document_service import similarity_search
from app.models.message import ModelProvider


async def get_rag_context(
    query: str,
    db: AsyncSession,
    top_k: int = 3
) -> str:
    """
    Retrieve relevant document chunks for RAG.
    
    Args:
        query: User's query
        db: Database session
        top_k: Number of relevant chunks to retrieve
        
    Returns:
        Formatted context string
    """
    results = await similarity_search(query, db, top_k)
    
    if not results:
        return ""
    
    context_parts = []
    for idx, result in enumerate(results, 1):
        context_parts.append(
            f"[Document {idx}] (Relevance: {result['similarity_score']:.2f})\n"
            f"{result['chunk_text']}\n"
        )
    
    return "\n".join(context_parts)


async def format_rag_prompt(
    user_prompt: str,
    context: str,
    history: List[Dict[str, str]]
) -> str:
    """
    Format the prompt with RAG context.
    
    Args:
        user_prompt: Original user prompt
        context: Retrieved context from documents
        history: Conversation history
        
    Returns:
        Enhanced prompt with context
    """
    if not context:
        return user_prompt
    
    rag_prompt = f"""You are a helpful assistant with access to a knowledge base. Use the following context to answer the user's question. If the context doesn't contain relevant information, answer based on your general knowledge.

Context from Knowledge Base:
{context}

User Question: {user_prompt}

Please provide a comprehensive answer, citing the context when relevant."""
    
    return rag_prompt


async def generate_rag_response(
    prompt: str,
    conversation_id: int,
    db: AsyncSession,
    use_rag: bool = True,
    top_k: int = 3,
    selected_models: Optional[List[ModelProvider]] = None
):
    """
    Generate responses with optional RAG enhancement.
    
    Args:
        prompt: User's prompt
        conversation_id: Conversation ID
        db: Database session
        use_rag: Whether to use RAG
        top_k: Number of document chunks to retrieve
        selected_models: Models to use
        
    Returns:
        Enhanced prompt and context info
    """
    context = ""
    enhanced_prompt = prompt
    
    if use_rag:
        # Retrieve relevant context
        context = await get_rag_context(prompt, db, top_k)
        
        # Get conversation history
        from app.services.chat_service import format_conversation_history
        history = await format_conversation_history(conversation_id, db)
        
        # Format prompt with context
        enhanced_prompt = await format_rag_prompt(prompt, context, history)
    
    return {
        "enhanced_prompt": enhanced_prompt,
        "context": context,
        "context_used": bool(context)
    }