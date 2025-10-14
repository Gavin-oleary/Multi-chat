from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.services import chat_service
from app.services.conversation_service import get_or_create_conversation
from app.services.document_service import similarity_search

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def send_chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Send a prompt to all (or selected) AI models and get responses.
    Creates a new conversation if conversation_id is not provided.
    Optionally augments prompt with RAG context.
    """
    
    # Get or create conversation
    title = chat_service.generate_conversation_title(request.prompt)
    conversation = await get_or_create_conversation(
        request.conversation_id,
        title,
        db
    )
    
    # RAG: Retrieve context if enabled
    rag_context = None
    context_chunks = None
    if request.use_rag:
        print(f"RAG enabled: Searching for context with query: '{request.prompt[:50]}...' (top_k={request.top_k})")
        try:
            context_results = await similarity_search(
                query=request.prompt,
                db=db,
                top_k=request.top_k
            )
            print(f"RAG search completed: Found {len(context_results) if context_results else 0} results")
            
            if context_results:
                # Format context for injection
                context_chunks = [
                    {
                        "chunk_id": r["chunk_id"],
                        "text": r["chunk_text"],
                        "similarity": float(r["similarity_score"]),
                        "metadata": r.get("doc_metadata", {})
                    }
                    for r in context_results
                ]
                
                # Build context string
                context_text = "\n\n".join([
                    f"[Context {i+1} - Similarity: {r['similarity_score']:.2f}]\n{r['chunk_text']}"
                    for i, r in enumerate(context_results)
                ])
                
                rag_context = context_text
                print(f"RAG context prepared: {len(rag_context)} characters")
        except Exception as e:
            # Log error but don't fail the request
            print(f"RAG context retrieval failed: {e}")
            rag_context = None
    
    # Save user message
    user_message = await chat_service.save_user_message(
        conversation.id,
        request.prompt,
        db
    )
    
    # Generate responses from all models (with optional RAG context)
    responses = await chat_service.generate_multi_model_responses(
        prompt=request.prompt,
        conversation_id=conversation.id,
        db=db,
        selected_models=request.models,
        rag_context=rag_context
    )
    
    # Save assistant responses
    await chat_service.save_assistant_responses(
        conversation.id,
        responses,
        db
    )
    
    return ChatResponse(
        conversation_id=conversation.id,
        user_message_id=user_message.id,
        responses=responses,
        rag_context_used=request.use_rag and rag_context is not None,
        context_chunks=context_chunks if request.use_rag else None
    )