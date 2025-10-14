from fastapi import APIRouter
from app.api.v1 import conversations, messages, chat, providers, stream
from app.api.v1 import documents, system_prompts, health


api_router = APIRouter()

# Include sub-routers
api_router.include_router(
    conversations.router,
    prefix="/conversations",
    tags=["conversations"]
)

api_router.include_router(
    messages.router,
    prefix="/messages",
    tags=["messages"]
)

api_router.include_router(
    chat.router,
    prefix="/chat",
    tags=["chat"]
)

api_router.include_router(
    providers.router,
    prefix="/providers",
    tags=["providers"]
)

api_router.include_router(
    stream.router,
    prefix="/stream",
    tags=["stream"]
)

api_router.include_router(
    documents.router,
    prefix="/documents",
    tags=["documents"]
)

api_router.include_router(
    system_prompts.router,
    prefix="/system-prompts",
    tags=["system-prompts"]
)

api_router.include_router(
    health.router,
    tags=["health"]
)