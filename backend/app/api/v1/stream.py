"""
WebSocket endpoint for streaming chat responses.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import json
import asyncio
from typing import Dict, List, Optional
import time

from app.database import get_db
from app.schemas.chat import ChatRequest
from app.models.message import ModelProvider, MessageRole, Message
from app.services import chat_service
from app.services.conversation_service import get_or_create_conversation
from app.api.deps import get_ai_clients
from app.utils.circuit_breaker import circuit_manager

router = APIRouter()


async def stream_model_response(
    websocket: WebSocket,
    provider: ModelProvider,
    client,
    prompt: str,
    history: List[Dict[str, str]]
) -> Optional[str]:
    """
    Stream a single model's response over WebSocket.
    
    Returns the complete response content or None if failed.
    """
    start_time = time.time()
    breaker = circuit_manager.get_breaker(provider.value)
    
    try:
        # Send initial status
        await websocket.send_json({
            "type": "model_start",
            "provider": provider.value,
            "timestamp": time.time()
        })
        
        # Check if the client supports streaming
        if hasattr(client, 'generate_stream'):
            # Stream the response
            full_content = ""
            async for chunk in client.generate_stream(prompt, history):
                full_content += chunk
                await websocket.send_json({
                    "type": "model_chunk",
                    "provider": provider.value,
                    "content": chunk,
                    "timestamp": time.time()
                })
        else:
            # Fallback to non-streaming with progress updates
            async def generate_with_updates():
                await websocket.send_json({
                    "type": "model_thinking",
                    "provider": provider.value,
                    "timestamp": time.time()
                })
                return await breaker.call(
                    client.generate_response,
                    provider.value,
                    prompt,
                    history
                )
            
            full_content = await generate_with_updates()
            
            # Send the complete response
            await websocket.send_json({
                "type": "model_chunk",
                "provider": provider.value,
                "content": full_content,
                "timestamp": time.time()
            })
        
        # Send completion status
        latency_ms = (time.time() - start_time) * 1000
        await websocket.send_json({
            "type": "model_complete",
            "provider": provider.value,
            "latency_ms": latency_ms,
            "timestamp": time.time()
        })
        
        return full_content
        
    except Exception as e:
        latency_ms = (time.time() - start_time) * 1000
        error_msg = str(e)
        
        # Log the error for debugging
        print(f"Error in {provider.value}: {error_msg}")
        import traceback
        traceback.print_exc()
        
        if "circuit breaker is OPEN" in error_msg:
            error_msg = f"{provider.value} is temporarily unavailable"
        
        await websocket.send_json({
            "type": "model_error",
            "provider": provider.value,
            "error": error_msg,
            "latency_ms": latency_ms,
            "timestamp": time.time()
        })
        
        return None


@router.websocket("/chat")
async def websocket_chat(
    websocket: WebSocket,
    db: AsyncSession = Depends(get_db)
):
    """
    WebSocket endpoint for streaming chat responses.
    
    Client sends:
    {
        "prompt": "user question",
        "conversation_id": 123,  // optional
        "models": ["claude", "chatgpt", ...]  // optional
    }
    
    Server sends:
    {
        "type": "model_start" | "model_chunk" | "model_complete" | "model_error" | "model_thinking",
        "provider": "claude",
        "content": "response chunk",  // for model_chunk
        "error": "error message",     // for model_error
        "latency_ms": 123.45,        // for model_complete/model_error
        "timestamp": 1234567890.123
    }
    """
    await websocket.accept()
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            
            # Validate request
            try:
                request = ChatRequest(**data)
            except Exception as e:
                await websocket.send_json({
                    "type": "error",
                    "error": f"Invalid request: {str(e)}"
                })
                continue
            
            # Get or create conversation
            title = chat_service.generate_conversation_title(request.prompt)
            conversation = await get_or_create_conversation(
                request.conversation_id,
                title,
                db
            )
            
            # Send conversation info
            await websocket.send_json({
                "type": "conversation_info",
                "conversation_id": conversation.id,
                "timestamp": time.time()
            })
            
            # Save user message
            user_message = await chat_service.save_user_message(
                conversation.id,
                request.prompt,
                db
            )
            
            # Get conversation history
            history = await chat_service.format_conversation_history(conversation.id, db)
            
            # Get AI clients
            all_clients = get_ai_clients()
            
            # Determine which models to use
            if request.models:
                models_to_use = request.models
            else:
                all_providers = list(ModelProvider)
                healthy_providers = circuit_manager.get_healthy_providers(
                    [p.value for p in all_providers]
                )
                models_to_use = [
                    p for p in all_providers 
                    if p.value in healthy_providers
                ]
            
            # Stream responses from all models concurrently
            tasks = []
            for provider in models_to_use:
                print(f"Creating task for provider: {provider.value}")
                task = stream_model_response(
                    websocket,
                    provider,
                    all_clients[provider],
                    request.prompt,
                    history
                )
                tasks.append((provider, task))
            
            print(f"Running {len(tasks)} tasks concurrently")
            # Run all streaming tasks concurrently
            results = await asyncio.gather(
                *[task for _, task in tasks],
                return_exceptions=True
            )
            print(f"All tasks completed. Results: {[type(r).__name__ for r in results]}")
            
            # Save successful responses to database
            assistant_messages = []
            for (provider, _), result in zip(tasks, results):
                if isinstance(result, str) and result:  # Successful response
                    assistant_messages.append(Message(
                        conversation_id=conversation.id,
                        role=MessageRole.ASSISTANT,
                        content=result,
                        model_provider=provider
                    ))
            
            if assistant_messages:
                for msg in assistant_messages:
                    db.add(msg)
                await db.commit()
            
            # Send final completion message
            await websocket.send_json({
                "type": "all_complete",
                "timestamp": time.time()
            })
            
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "error": str(e)
        })
        await websocket.close()
