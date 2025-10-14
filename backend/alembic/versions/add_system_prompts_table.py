"""Add system_prompts table

Revision ID: add_system_prompts_table
Revises: add_doc_metadata_column
Create Date: 2025-10-06

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_system_prompts_table'
down_revision = 'add_doc_metadata_column'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create enum type for model providers if it doesn't exist
    op.execute("CREATE TYPE IF NOT EXISTS modelprovider AS ENUM ('claude', 'chatgpt', 'gemini', 'grok', 'perplexity')")
    
    # Create system_prompts table
    op.create_table('system_prompts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('model_provider', postgresql.ENUM('claude', 'chatgpt', 'gemini', 'grok', 'perplexity', name='modelprovider', create_type=False), nullable=False),
        sa.Column('prompt_template', sa.Text(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('include_rag_context', sa.Boolean(), nullable=True, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create index on model_provider
    op.create_index(op.f('ix_system_prompts_id'), 'system_prompts', ['id'], unique=False)
    op.create_index(op.f('ix_system_prompts_model_provider'), 'system_prompts', ['model_provider'], unique=True)


def downgrade() -> None:
    # Drop indexes
    op.drop_index(op.f('ix_system_prompts_model_provider'), table_name='system_prompts')
    op.drop_index(op.f('ix_system_prompts_id'), table_name='system_prompts')
    
    # Drop table
    op.drop_table('system_prompts')
