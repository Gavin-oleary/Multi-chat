from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.database import get_db
from app.models.message import Message
from app.schemas.message import MessageResponse

router = APIRouter()


@router.get("/conversation/{conversation_id}", response_model=List[MessageResponse])
async def get_messages_by_conversation(
    conversation_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all messages for a specific conversation.
    
    Args:
        conversation_id: The ID of the conversation
        skip: Number of messages to skip (for pagination)
        limit: Maximum number of messages to return
    """
    result = await db.execute(
        select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(
            Message.created_at
        ).offset(skip).limit(limit)
    )
    messages = result.scalars().all()
    
    return messages


@router.get("/{message_id}", response_model=MessageResponse)
async def get_message(
    message_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific message by ID.
    
    Args:
        message_id: The ID of the message to retrieve
    """
    result = await db.execute(
        select(Message).where(Message.id == message_id)
    )
    message = result.scalar_one_or_none()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return message


@router.delete("/{message_id}")
async def delete_message(
    message_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a specific message.
    
    Args:
        message_id: The ID of the message to delete
    """
    result = await db.execute(
        select(Message).where(Message.id == message_id)
    )
    message = result.scalar_one_or_none()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    db.delete(message)
    await db.commit()
    return {"message": "Message deleted successfully"}