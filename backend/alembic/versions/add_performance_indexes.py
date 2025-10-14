"""Add performance indexes to messages table

Revision ID: add_performance_indexes
Revises: 
Create Date: 2025-10-05

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_performance_indexes'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add index on conversation_id column
    op.create_index(
        'ix_messages_conversation_id', 
        'messages', 
        ['conversation_id'],
        unique=False
    )
    
    # Add index on created_at column
    op.create_index(
        'ix_messages_created_at', 
        'messages', 
        ['created_at'],
        unique=False
    )


def downgrade() -> None:
    # Remove indexes
    op.drop_index('ix_messages_created_at', table_name='messages')
    op.drop_index('ix_messages_conversation_id', table_name='messages')
