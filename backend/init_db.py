"""
Database initialization script.
Run this to create all database tables.
"""

import asyncio
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
    
    # Check existing tables
    existing_tables = await check_tables()
    print(f"📋 Existing tables: {existing_tables}")
    
    # Drop existing tables if they exist (to update schema)
    if existing_tables:
        print("🗑️  Dropping existing tables to update schema...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        print("✓ Tables dropped")
    
    # Create tables
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
