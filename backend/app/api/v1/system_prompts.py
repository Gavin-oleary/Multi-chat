from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.schemas.system_prompt import (
    SystemPromptCreate,
    SystemPromptUpdate,
    SystemPromptResponse,
    SystemPromptList
)
from app.services import system_prompt_service
from app.models.message import ModelProvider

router = APIRouter()


@router.get("/", response_model=SystemPromptList)
async def list_system_prompts(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all system prompts."""
    prompts = await system_prompt_service.list_system_prompts(db, skip, limit)
    return SystemPromptList(
        prompts=prompts,
        total=len(prompts)
    )


@router.get("/{model_provider}", response_model=SystemPromptResponse)
async def get_system_prompt(
    model_provider: ModelProvider,
    db: AsyncSession = Depends(get_db)
):
    """Get the active system prompt for a specific model."""
    prompt_text = await system_prompt_service.get_system_prompt(model_provider, db)
    if not prompt_text:
        raise HTTPException(status_code=404, detail="System prompt not found")
    
    # Get the full prompt object
    from sqlalchemy import select
    from app.models.system_prompt import SystemPrompt
    
    result = await db.execute(
        select(SystemPrompt).where(
            SystemPrompt.model_provider == model_provider,
            SystemPrompt.is_active == True
        )
    )
    prompt = result.scalar_one_or_none()
    
    if not prompt:
        raise HTTPException(status_code=404, detail="System prompt not found")
    
    return prompt


@router.post("/", response_model=SystemPromptResponse)
async def create_system_prompt(
    prompt_data: SystemPromptCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new system prompt."""
    prompt = await system_prompt_service.create_system_prompt(prompt_data, db)
    return prompt


@router.put("/{prompt_id}", response_model=SystemPromptResponse)
async def update_system_prompt(
    prompt_id: int,
    update_data: SystemPromptUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an existing system prompt."""
    prompt = await system_prompt_service.update_system_prompt(prompt_id, update_data, db)
    if not prompt:
        raise HTTPException(status_code=404, detail="System prompt not found")
    return prompt


@router.post("/initialize-defaults")
async def initialize_defaults(db: AsyncSession = Depends(get_db)):
    """Initialize default system prompts for all models."""
    await system_prompt_service.initialize_default_prompts(db)
    return {"message": "Default system prompts initialized"}


@router.delete("/{prompt_id}")
async def delete_system_prompt(
    prompt_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a system prompt."""
    from sqlalchemy import select, delete
    from app.models.system_prompt import SystemPrompt
    
    # Check if prompt exists
    result = await db.execute(
        select(SystemPrompt).where(SystemPrompt.id == prompt_id)
    )
    prompt = result.scalar_one_or_none()
    
    if not prompt:
        raise HTTPException(status_code=404, detail="System prompt not found")
    
    # Delete the prompt
    await db.execute(
        delete(SystemPrompt).where(SystemPrompt.id == prompt_id)
    )
    await db.commit()
    
    return {"message": "System prompt deleted successfully"}
