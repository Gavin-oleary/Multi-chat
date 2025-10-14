from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.schemas.conversation import (
    ConversationCreate,
    ConversationUpdate,
    ConversationResponse,
    ConversationWithMessages
)
from app.services import conversation_service

router = APIRouter()


@router.post("/", response_model=ConversationResponse)
async def create_conversation(
    conversation: ConversationCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new conversation"""
    return await conversation_service.create_conversation(conversation.title, db)


@router.get("/", response_model=List[ConversationResponse])
async def list_conversations(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all conversations"""
    return await conversation_service.list_conversations(db, skip, limit)


@router.get("/{conversation_id}", response_model=ConversationWithMessages)
async def get_conversation(
    conversation_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific conversation with all its messages"""
    return await conversation_service.get_conversation(conversation_id, db)


@router.patch("/{conversation_id}", response_model=ConversationResponse)
async def update_conversation(
    conversation_id: int,
    conversation_update: ConversationUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a conversation (e.g., rename it)"""
    return await conversation_service.update_conversation(
        conversation_id,
        conversation_update,
        db
    )


@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a conversation and all its messages"""
    await conversation_service.delete_conversation(conversation_id, db)
    return {"message": "Conversation deleted successfully"}