from fastapi import APIRouter, Depends, HTTPException
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
    try:
        # CRITICAL DEBUG: Log the incoming request
        print("=" * 80)
        print("CHAT REQUEST RECEIVED:")
        print(f"  Prompt: {request.prompt[:100]}...")
        print(f"  use_rag: {request.use_rag}")
        print(f"  top_k: {request.top_k}")
        print(f"  conversation_id: {request.conversation_id}")
        print(f"  models: {request.models}")
        print("=" * 80)
        
        # Generate title for new conversations
        title = chat_service.generate_conversation_title(request.prompt)
        
        # Get or create conversation
        conversation = await get_or_create_conversation(
            request.conversation_id,
            title,
            db
        )
        
        print(f"Chat request - Conversation ID: {conversation.id}, Prompt: {request.prompt[:50]}...")
        
        # Save user message
        user_message = await chat_service.save_user_message(
            conversation.id,
            request.prompt,
            db
        )
        
        # Retrieve RAG context if enabled
        rag_context = None
        context_chunks = None
        
        # CRITICAL: Check if RAG is enabled
        if request.use_rag:
            print(f"✓ RAG IS ENABLED - searching for top {request.top_k} contexts")
            try:
                similar_docs = await similarity_search(
                    query=request.prompt,
                    db=db,
                    top_k=request.top_k
                )
                
                print(f"✓ RAG search returned {len(similar_docs) if similar_docs else 0} results")
                
                if similar_docs:
                    # Combine document contents for context
                    rag_context = "\n\n".join([
                        f"[Document {i+1}]:\n{doc['chunk_text']}"
                        for i, doc in enumerate(similar_docs)
                    ])
                    
                    # Store metadata about context chunks
                    context_chunks = [
                        {
                            "content": doc['chunk_text'][:200] + "..." if len(doc['chunk_text']) > 200 else doc['chunk_text'],
                            "similarity": doc['similarity_score'],
                            "metadata": doc.get('doc_metadata', {})
                        }
                        for doc in similar_docs
                    ]
                    print(f"✓ RAG context created: {len(rag_context)} characters")
                    print(f"✓ First 200 chars of context: {rag_context[:200]}...")
                else:
                    print("✗ No relevant documents found for RAG context")
            except Exception as e:
                print(f"✗ RAG ERROR: {str(e)}")
                import traceback
                traceback.print_exc()
        else:
            print("✗ RAG IS DISABLED - use_rag=False")
        
        # Get responses from models
        print(f"Sending to models with RAG context: {bool(rag_context)}")
        responses = await chat_service.generate_multi_model_responses(
            prompt=request.prompt,
            conversation_id=conversation.id,
            db=db,
            selected_models=request.models,
            rag_context=rag_context
        )
        
        # Save successful responses
        await chat_service.save_assistant_responses(
            conversation.id,
            responses,
            db
        )
        
        # CRITICAL: Return conversation_id in response so frontend can track it
        print(f"✓ Returning response - conversation_id: {conversation.id}, rag_used: {bool(rag_context)}")
        return ChatResponse(
            conversation_id=conversation.id,
            user_message_id=user_message.id,
            responses=responses,
            rag_context_used=bool(rag_context),
            context_chunks=context_chunks
        )
        
    except Exception as e:
        print(f"✗ ERROR in chat endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat request: {str(e)}"
        )