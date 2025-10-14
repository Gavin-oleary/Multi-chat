"""
Conversation service for handling conversation-related operations.
Contains business logic for CRUD operations on conversations.
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.conversation import ConversationCreate, ConversationUpdate


async def create_conversation(
    title: str,
    db: AsyncSession
) -> Conversation:
    """
    Create a new conversation.
    
    Args:
        title: The conversation title
        db: Database session
        
    Returns:
        The created Conversation object
    """
    conversation = Conversation(title=title)
    db.add(conversation)
    await db.commit()
    await db.refresh(conversation)
    return conversation


async def get_conversation(
    conversation_id: int,
    db: AsyncSession
) -> Conversation:
    """
    Get a conversation by ID.
    
    Args:
        conversation_id: The ID of the conversation
        db: Database session
        
    Returns:
        The Conversation object
        
    Raises:
        HTTPException: If conversation not found
    """
    result = await db.execute(
        select(Conversation)
        .options(selectinload(Conversation.messages))
        .where(Conversation.id == conversation_id)
    )
    conversation = result.scalar_one_or_none()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return conversation


async def list_conversations(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100
) -> List[Conversation]:
    """
    List all conversations with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of Conversation objects
    """
    result = await db.execute(
        select(Conversation)
        .order_by(Conversation.updated_at.desc())
        .offset(skip)
        .limit(limit)
    )
    conversations = result.scalars().all()
    
    return conversations


async def update_conversation(
    conversation_id: int,
    conversation_update: ConversationUpdate,
    db: AsyncSession
) -> Conversation:
    """
    Update a conversation.
    
    Args:
        conversation_id: The ID of the conversation
        conversation_update: The update data
        db: Database session
        
    Returns:
        The updated Conversation object
        
    Raises:
        HTTPException: If conversation not found
    """
    conversation = await get_conversation(conversation_id, db)
    
    # Update fields if provided
    if conversation_update.title is not None:
        conversation.title = conversation_update.title
    
    await db.commit()
    await db.refresh(conversation)
    return conversation


async def delete_conversation(
    conversation_id: int,
    db: AsyncSession
) -> None:
    """
    Delete a conversation and all its messages.
    
    Args:
        conversation_id: The ID of the conversation
        db: Database session
        
    Raises:
        HTTPException: If conversation not found
    """
    conversation = await get_conversation(conversation_id, db)
    await db.delete(conversation)
    await db.commit()


async def get_or_create_conversation(
    conversation_id: Optional[int],
    default_title: str,
    db: AsyncSession
) -> Conversation:
    """
    Get an existing conversation or create a new one.
    
    Args:
        conversation_id: Optional ID of existing conversation
        default_title: Title to use if creating new conversation
        db: Database session
        
    Returns:
        The Conversation object (existing or newly created)
    """
    if conversation_id is not None:
        return await get_conversation(conversation_id, db)
    else:
        return await create_conversation(default_title, db)


async def count_messages(
    conversation_id: int,
    db: AsyncSession
) -> int:
    """
    Count the number of messages in a conversation.
    
    Args:
        conversation_id: The ID of the conversation
        db: Database session
        
    Returns:
        Number of messages in the conversation
    """
    result = await db.execute(
        select(func.count()).select_from(Message).where(
            Message.conversation_id == conversation_id
        )
    )
    return result.scalar()


async def get_conversation_summary(
    conversation_id: int,
    db: AsyncSession
) -> dict:
    """
    Get a summary of a conversation including message counts.
    
    Args:
        conversation_id: The ID of the conversation
        db: Database session
        
    Returns:
        Dictionary with conversation summary data
    """
    conversation = await get_conversation(conversation_id, db)
    message_count = await count_messages(conversation_id, db)
    
    return {
        "id": conversation.id,
        "title": conversation.title,
        "created_at": conversation.created_at,
        "updated_at": conversation.updated_at,
        "message_count": message_count
    }