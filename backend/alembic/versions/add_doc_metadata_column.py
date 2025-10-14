"""Add doc_metadata column to documents table

Revision ID: add_doc_metadata_column
Revises: add_performance_indexes
Create Date: 2025-10-06

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_doc_metadata_column'
down_revision = 'add_performance_indexes'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add doc_metadata column if it doesn't exist
    op.add_column('documents', sa.Column('doc_metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    
    # Set default value for existing rows
    op.execute("UPDATE documents SET doc_metadata = '{}' WHERE doc_metadata IS NULL")
    
    # Make it non-nullable with a default
    op.alter_column('documents', 'doc_metadata',
                    nullable=False,
                    server_default=sa.text("'{}'::jsonb"))


def downgrade() -> None:
    # Remove the column
    op.drop_column('documents', 'doc_metadata')
