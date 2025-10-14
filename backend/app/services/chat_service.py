"""
Chat service for handling multi-model chat operations with RAG support.
Contains business logic for orchestrating multiple AI model responses.
"""

import asyncio
import time
from typing import List, Dict, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.conversation import Conversation
from app.models.message import Message, MessageRole, ModelProvider
from app.schemas.chat import ModelResponse
from app.clients.base import BaseAIClient
from app.api.deps import get_ai_clients
from app.utils.circuit_breaker import circuit_manager
from app.utils.validation import sanitize_string, validate_prompt_length
from app.utils.cache import response_cache
from app.services import system_prompt_service


def create_system_prompt_with_context(context: str) -> str:
    """
    Create a system prompt that includes RAG context.
    
    Args:
        context: Retrieved context from documents
        
    Returns:
        System prompt with context
    """
    system_prompt = f"""You are a helpful assistant with access to a knowledge base. You have been provided with context from relevant documents to help answer user questions.

IMPORTANT INSTRUCTIONS:
1. Base your answers primarily on the provided context when relevant
2. If the context contains the exact information needed, cite it directly
3. If the context is partially relevant, use it as a foundation and clearly indicate when you're adding general knowledge
4. If the context is not relevant to the question, you may provide answers from your general knowledge
5. Be concise but comprehensive in your responses

RETRIEVED CONTEXT FROM KNOWLEDGE BASE:
{context}"""
    
    return system_prompt


async def get_model_response(
    client: BaseAIClient,
    provider: ModelProvider,
    prompt: str,
    history: List[Dict[str, str]],
    rag_context: Optional[str] = None,
    system_prompt: Optional[str] = None
) -> ModelResponse:
    """
    Get response from a single AI model with circuit breaker protection and caching.
    
    Args:
        client: AI client instance
        provider: Model provider enum
        prompt: User prompt (potentially augmented with RAG context)
        history: Conversation history
        rag_context: Optional RAG context (for cache key differentiation)
        
    Returns:
        ModelResponse object
    """
    # Create cache key
    cache_key = f"{provider.value}:{hash(prompt)}:{hash(str(history))}"
    if rag_context:
        cache_key += f":{hash(rag_context)}"
    
    # Check cache
    cached = response_cache.get(cache_key)
    if cached:
        return ModelResponse(
            provider=provider,
            content=cached['content'],
            latency_ms=0  # Cached response
        )
    
    try:
        start_time = time.time()
        
        # Get response from model
        response = await client.generate_response(prompt, history, system_prompt)
        
        latency_ms = (time.time() - start_time) * 1000
        
        # Cache successful response
        response_cache.set(cache_key, {'content': response}, ttl=3600)
        
        # Record success in circuit breaker
        circuit_manager.record_success(provider.value)
        
        return ModelResponse(
            provider=provider,
            content=response,
            latency_ms=latency_ms
        )
        
    except Exception as e:
        # Record failure in circuit breaker
        circuit_manager.record_failure(provider.value)
        
        return ModelResponse(
            provider=provider,
            content="",
            error=str(e)
        )


async def format_conversation_history(
    conversation_id: int,
    db: AsyncSession
) -> List[Dict[str, str]]:
    """
    Format conversation history for AI models.
    Creates a balanced view where each set of model responses is represented
    by a single assistant message (using the best/most comprehensive response).
    
    Args:
        conversation_id: ID of the conversation
        db: Database session
        
    Returns:
        List of message dicts with role and content
    """
    result = await db.execute(
        select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at)
    )
    messages = result.scalars().all()
    
    history: List[Dict[str, str]] = []
    current_assistant_responses: List[Message] = []
    
    for msg in messages:
        if msg.role == MessageRole.USER:
            if current_assistant_responses:
                best_response = max(current_assistant_responses, key=lambda r: len(r.content))
                history.append({"role": "assistant", "content": best_response.content})
                current_assistant_responses = []
            
            history.append({"role": "user", "content": msg.content})
            
        elif msg.role == MessageRole.ASSISTANT:
            current_assistant_responses.append(msg)
    
    if current_assistant_responses:
        best_response = max(current_assistant_responses, key=lambda r: len(r.content))
        history.append({"role": "assistant", "content": best_response.content})
    
    return history


async def generate_multi_model_responses(
    prompt: str,
    conversation_id: int,
    db: AsyncSession,
    selected_models: Optional[List[ModelProvider]] = None,
    rag_context: Optional[str] = None
) -> List[ModelResponse]:
    """
    Generate responses from multiple AI models in parallel.
    
    Args:
        prompt: The user's prompt
        conversation_id: ID of the conversation for context
        db: Database session
        selected_models: Optional list of specific models to use
        rag_context: Optional RAG context to augment the prompt
        
    Returns:
        List of ModelResponse objects
    """
    # Get conversation history
    history = await format_conversation_history(conversation_id, db)
    
    # Get AI clients
    all_clients = get_ai_clients()
    
    # Determine which models to use
    if selected_models:
        models_to_use = selected_models
    else:
        all_providers = list(ModelProvider)
        healthy_providers = circuit_manager.get_healthy_providers(
            [p.value for p in all_providers]
        )
        models_to_use = [
            p for p in all_providers 
            if p.value in healthy_providers
        ]
        
        if not models_to_use:
            models_to_use = all_providers
    
    # Create tasks for parallel execution with model-specific prompts
    tasks = []
    for provider in models_to_use:
        # Get model-specific system prompt
        model_system_prompt = await system_prompt_service.get_system_prompt(provider, db)
        
        # Format with RAG context if available
        if model_system_prompt and rag_context:
            model_system_prompt = await system_prompt_service.format_system_prompt(
                model_system_prompt, rag_context
            )
        elif not model_system_prompt and rag_context:
            # Fallback to generic prompt if no model-specific prompt exists
            model_system_prompt = create_system_prompt_with_context(rag_context)
        
        tasks.append(
            get_model_response(
                all_clients[provider],
                provider,
                prompt,
                history,
                rag_context,
                model_system_prompt
            )
        )
    
    # Execute all tasks in parallel
    responses = await asyncio.gather(*tasks)
    
    return responses


async def save_user_message(
    conversation_id: int,
    prompt: str,
    db: AsyncSession
) -> Message:
    """
    Save user message to database.
    
    Args:
        conversation_id: ID of the conversation
        prompt: The user's message content
        db: Database session
        
    Returns:
        The created Message object
    """
    user_message = Message(
        conversation_id=conversation_id,
        role=MessageRole.USER,
        content=prompt
    )
    db.add(user_message)
    await db.commit()
    await db.refresh(user_message)
    return user_message


async def save_assistant_responses(
    conversation_id: int,
    responses: List[ModelResponse],
    db: AsyncSession
) -> None:
    """
    Save successful assistant responses to database.
    
    Args:
        conversation_id: ID of the conversation
        responses: List of model responses
        db: Database session
    """
    for response in responses:
        if not response.error:
            assistant_message = Message(
                conversation_id=conversation_id,
                role=MessageRole.ASSISTANT,
                content=response.content,
                model_provider=response.provider
            )
            db.add(assistant_message)
    
    await db.commit()


def generate_conversation_title(prompt: str, max_length: int = 50) -> str:
    """
    Generate a conversation title from the first prompt.
    
    Args:
        prompt: The user's first message
        max_length: Maximum length of the title
        
    Returns:
        A truncated and sanitized version of the prompt as the title
    """
    title = sanitize_string(prompt, max_length)
    
    if len(prompt) > max_length:
        title = title[:max_length-3] + "..."
    
    return title