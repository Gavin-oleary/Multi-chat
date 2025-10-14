"""
Initialize pgvector extension for PostgreSQL.
Run this once to enable vector similarity search.
"""

import asyncio
from sqlalchemy import text
from app.database import engine


async def init_pgvector():
    """Enable pgvector extension in PostgreSQL."""
    async with engine.begin() as conn:
        # Enable pgvector extension
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        print("✅ pgvector extension enabled")
        
        # Create index for faster similarity search
        await conn.execute(text("""
            CREATE INDEX IF NOT EXISTS embeddings_vector_idx 
            ON embeddings 
            USING ivfflat (embedding_vector vector_cosine_ops)
            WITH (lists = 100)
        """))
        print("✅ Vector index created")


if __name__ == "__main__":
    asyncio.run(init_pgvector())