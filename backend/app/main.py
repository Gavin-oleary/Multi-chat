from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db
from app.api.v1.router import api_router
from app.utils.logging import setup_logging, get_logger
from contextlib import asynccontextmanager


# Configure structured logging
setup_logging(level="INFO" if not settings.DEBUG else "DEBUG")
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup"""
    await init_db()
    logger.info(f"{settings.PROJECT_NAME} started successfully!")
    logger.info(f"Docs available at: http://{settings.HOST}:{settings.PORT}{settings.API_V1_PREFIX}/docs")
    yield

# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Multi-Model Chat API",
        "version": "1.0.0",
        "docs": f"{settings.API_V1_PREFIX}/docs"
    }


@app.get("/health")
async def health_check():
    """
    Basic health check endpoint for Docker and monitoring.
    For detailed health info, use /api/v1/health
    """
    return {"status": "healthy", "version": "1.0.0"}


# Include API router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )