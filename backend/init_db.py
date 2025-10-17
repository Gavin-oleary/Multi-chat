"""
Database initialization script.
Run this to create all database tables.
"""

import asyncio
import sqlalchemy
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import create_async_engine
from app.database import init_db, engine, Base, get_db
from app.models import Conversation, Message, SystemPrompt
from app.config import settings
from app.services import system_prompt_service


async def check_tables():
    """Check which tables exist in the database"""
    async with engine.begin() as conn:
        def sync_check(connection):
            inspector = inspect(connection)
            return inspector.get_table_names()
        tables = await conn.run_sync(sync_check)
    return tables


async def main():
    print("🔧 Initializing database...")
    
    # Enable pgvector extension
    print("📦 Enabling pgvector extension...")
    async with engine.begin() as conn:
        await conn.execute(sqlalchemy.text("CREATE EXTENSION IF NOT EXISTS vector"))
    print("✓ pgvector extension enabled")
    
    # Check existing tables
    existing_tables = await check_tables()
    print(f"📋 Existing tables: {existing_tables}")
    
    # Only create tables if they don't exist (safe mode)
    required_tables = ['conversations', 'messages', 'system_prompts', 'documents', 'document_chunks', 'embeddings']
    missing_tables = [t for t in required_tables if t not in existing_tables]
    
    if missing_tables:
        print(f"⚠️  Missing tables: {missing_tables}")
        print("Creating missing tables...")
    elif existing_tables:
        print("✓ All tables already exist - skipping initialization")
        print("💡 Database is ready to use!")
        
        # Just verify system prompts exist
        async for db in get_db():
            try:
                from sqlalchemy import select
                from app.models.system_prompt import SystemPrompt
                result = await db.execute(select(SystemPrompt))
                prompts = result.scalars().all()
                if not prompts:
                    print("⚠️  No system prompts found, initializing defaults...")
                    await system_prompt_service.initialize_default_prompts(db)
                    print("✓ System prompts initialized")
                else:
                    print(f"✓ Found {len(prompts)} system prompts")
            finally:
                break
        
        return 0  # Exit successfully without recreating tables
    
    # Create tables (only if missing)
    try:
        await init_db()
        print("✅ Database tables created successfully!")
        
        # Verify tables were created
        new_tables = await check_tables()
        print(f"📊 Current tables: {new_tables}")
        
        # Show table details
        if "conversations" in new_tables:
            print("   ✓ conversations table created (with BigInteger ID)")
        if "messages" in new_tables:
            print("   ✓ messages table created (with BigInteger conversation_id)")
        if "system_prompts" in new_tables:
            print("   ✓ system_prompts table created")
            
        # Initialize default system prompts
        print("\n🤖 Initializing default system prompts...")
        async for db in get_db():
            await system_prompt_service.initialize_default_prompts(db)
            print("   ✓ Default system prompts created for all models")
            break
            
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return 1
    
    print("\n🎉 Database initialization complete!")
    return 0


if __name__ == "__main__":
    exit(asyncio.run(main()))
