"""
Health check endpoint for monitoring and load balancers.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database import get_db
import sys

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """
    Health check endpoint that verifies:
    - API is responding
    - Database connection is working
    - Python version
    
    Returns:
        dict: Health status information
    """
    health_status = {
        "status": "healthy",
        "version": "1.0.0",
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "components": {}
    }
    
    # Check database connectivity
    try:
        result = await db.execute(text("SELECT 1"))
        result.scalar()
        health_status["components"]["database"] = "healthy"
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["components"]["database"] = f"unhealthy: {str(e)}"
    
    # Check Redis (optional, don't fail if Redis is not critical)
    try:
        from app.config import settings
        if hasattr(settings, 'REDIS_URL') and settings.REDIS_URL:
            # Only check if Redis is configured
            import redis
            r = redis.from_url(settings.REDIS_URL, socket_connect_timeout=1)
            r.ping()
            health_status["components"]["redis"] = "healthy"
    except ImportError:
        health_status["components"]["redis"] = "not_installed"
    except Exception as e:
        # Redis is optional, so we don't mark the whole service as unhealthy
        health_status["components"]["redis"] = f"unavailable: {str(e)}"
    
    return health_status


@router.get("/ready")
async def readiness_check(db: AsyncSession = Depends(get_db)):
    """
    Kubernetes-style readiness check.
    Returns 200 if service is ready to accept traffic.
    """
    try:
        result = await db.execute(text("SELECT 1"))
        result.scalar()
        return {"ready": True}
    except Exception as e:
        return {"ready": False, "error": str(e)}

