"""Add default value for is_active column

Revision ID: 002_add_is_active_default
Revises: 001_initial_migration
Create Date: 2026-01-23 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes

# revision identifiers
revision: str = '002_add_is_active_default'
down_revision: Union[str, None] = '001_initial_migration'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Update existing records to have is_active=True
    op.execute("UPDATE user SET is_active = TRUE WHERE is_active IS NULL;")

    # Alter the column to have a default value
    with op.batch_alter_table('user') as batch_op:
        batch_op.alter_column('is_active',
                           existing_type=sa.Boolean(),
                           nullable=False,
                           server_default=sa.text('1'))


def downgrade() -> None:
    with op.batch_alter_table('user') as batch_op:
        batch_op.alter_column('is_active',
                           existing_type=sa.Boolean(),
                           nullable=True,
                           server_default=None)