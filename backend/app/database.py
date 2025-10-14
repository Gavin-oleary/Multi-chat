from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config import settings

# Create async database engine with connection pooling
engine = create_async_engine(
    settings.DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://'),
    echo=settings.DEBUG,  # Log SQL queries in debug mode
    pool_size=20,  # Number of connections to maintain in pool
    max_overflow=10,  # Maximum overflow connections beyond pool_size
    pool_pre_ping=True,  # Verify connections before using them
    pool_recycle=3600  # Recycle connections after 1 hour
)

# Create async session factory
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for models
Base = declarative_base()


# Dependency for getting async database sessions
async def get_db():
    """
    Dependency that provides an async database session and ensures it's closed after use.
    Use this in FastAPI endpoints with Depends(get_db)
    """
    async with async_session() as session:
        yield session


async def init_db():
    """
    Initialize database tables.
    Called when the application starts.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)