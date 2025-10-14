"""
Service for managing system prompts for different AI models.
"""

from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.system_prompt import SystemPrompt
from app.models.message import ModelProvider
from app.schemas.system_prompt import SystemPromptCreate, SystemPromptUpdate


# Default system prompts for each model
DEFAULT_PROMPTS = {
    ModelProvider.CLAUDE: {
        "name": "Claude Default",
        "description": "Default system prompt for Claude",
        "prompt_template": """You are Claude, an AI assistant created by Anthropic. You are helpful, harmless, and honest. Your goal is to provide clear, accurate, and thoughtful responses while being respectful and considerate.

{rag_context}

When answering questions:
- Be direct and concise when appropriate
- Provide detailed explanations when needed
- Acknowledge when you're uncertain about something
- Use the provided context when available, but clarify when information comes from context vs. general knowledge"""
    },
    ModelProvider.CHATGPT: {
        "name": "ChatGPT Default",
        "description": "Default system prompt for ChatGPT",
        "prompt_template": """You are ChatGPT, a helpful AI assistant. Your responses should be informative, well-structured, and tailored to the user's needs.

{rag_context}

Guidelines:
- Provide accurate and helpful information
- Structure your responses clearly
- Use examples when they help clarify concepts
- Reference the provided context when answering questions"""
    },
    ModelProvider.GEMINI: {
        "name": "Gemini Default",
        "description": "Default system prompt for Gemini",
        "prompt_template": """You are Gemini, Google's AI assistant. You aim to be helpful, creative, and informative while maintaining accuracy and clarity.

{rag_context}

Key principles:
- Provide comprehensive yet accessible answers
- Balance detail with clarity
- Use the provided context to enhance your responses
- Be transparent about the source of your information"""
    },
    ModelProvider.GROK: {
        "name": "Grok Default",
        "description": "Default system prompt for Grok",
        "prompt_template": """You are Grok, an AI assistant with a unique perspective. You combine helpfulness with a touch of humor when appropriate, while maintaining accuracy.

{rag_context}

Your approach:
- Be direct and informative
- Add personality to your responses when suitable
- Use provided context to ground your answers
- Maintain a balance between being engaging and professional"""
    },
    ModelProvider.PERPLEXITY: {
        "name": "Perplexity Default",
        "description": "Default system prompt for Perplexity",
        "prompt_template": """You are Perplexity, an AI assistant focused on providing accurate, well-researched responses. You excel at finding and synthesizing information.

{rag_context}

Your methodology:
- Prioritize accuracy and relevance
- Synthesize information effectively
- Use provided context as your primary source
- Clearly distinguish between context-based and general knowledge"""
    }
}


async def get_system_prompt(
    model_provider: ModelProvider,
    db: AsyncSession,
    include_rag_context: bool = True
) -> Optional[str]:
    """
    Get the active system prompt for a model provider.
    
    Args:
        model_provider: The AI model provider
        db: Database session
        include_rag_context: Whether to include RAG context placeholder
        
    Returns:
        The system prompt template or None if not found
    """
    result = await db.execute(
        select(SystemPrompt).where(
            SystemPrompt.model_provider == model_provider,
            SystemPrompt.is_active == True
        )
    )
    prompt = result.scalar_one_or_none()
    
    if prompt:
        template = prompt.prompt_template
        if not include_rag_context and "{rag_context}" in template:
            # Remove RAG context placeholder if not needed
            template = template.replace("{rag_context}", "").strip()
        return template
    
    return None


async def create_system_prompt(
    prompt_data: SystemPromptCreate,
    db: AsyncSession
) -> SystemPrompt:
    """
    Create a new system prompt.
    
    Args:
        prompt_data: System prompt creation data
        db: Database session
        
    Returns:
        Created system prompt
    """
    # Deactivate existing prompt for this provider
    await db.execute(
        select(SystemPrompt).where(
            SystemPrompt.model_provider == prompt_data.model_provider
        ).update({"is_active": False})
    )
    
    # Create new prompt
    prompt = SystemPrompt(**prompt_data.model_dump())
    db.add(prompt)
    await db.commit()
    await db.refresh(prompt)
    
    return prompt


async def update_system_prompt(
    prompt_id: int,
    update_data: SystemPromptUpdate,
    db: AsyncSession
) -> Optional[SystemPrompt]:
    """
    Update an existing system prompt.
    
    Args:
        prompt_id: ID of the prompt to update
        update_data: Update data
        db: Database session
        
    Returns:
        Updated prompt or None if not found
    """
    result = await db.execute(
        select(SystemPrompt).where(SystemPrompt.id == prompt_id)
    )
    prompt = result.scalar_one_or_none()
    
    if not prompt:
        return None
    
    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(prompt, key, value)
    
    await db.commit()
    await db.refresh(prompt)
    
    return prompt


async def list_system_prompts(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100
) -> List[SystemPrompt]:
    """
    List all system prompts.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of system prompts
    """
    result = await db.execute(
        select(SystemPrompt)
        .order_by(SystemPrompt.model_provider)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def initialize_default_prompts(db: AsyncSession) -> None:
    """
    Initialize default system prompts for all models if they don't exist.
    
    Args:
        db: Database session
    """
    for provider, prompt_config in DEFAULT_PROMPTS.items():
        # Check if prompt already exists
        result = await db.execute(
            select(SystemPrompt).where(
                SystemPrompt.model_provider == provider
            )
        )
        existing = result.scalar_one_or_none()
        
        if not existing:
            prompt = SystemPrompt(
                model_provider=provider,
                **prompt_config
            )
            db.add(prompt)
    
    await db.commit()


async def format_system_prompt(
    template: str,
    rag_context: Optional[str] = None
) -> str:
    """
    Format a system prompt template with optional RAG context.
    
    Args:
        template: System prompt template
        rag_context: Optional RAG context to include
        
    Returns:
        Formatted system prompt
    """
    if rag_context and "{rag_context}" in template:
        rag_section = f"\nRELEVANT CONTEXT FROM KNOWLEDGE BASE:\n{rag_context}\n"
        return template.replace("{rag_context}", rag_section)
    else:
        return template.replace("{rag_context}", "").strip()
