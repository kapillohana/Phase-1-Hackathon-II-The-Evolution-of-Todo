"""Initial migration for the Advanced Todo Application

Revision ID: 001_initial_migration
Revises:
Create Date: 2026-01-11 12:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes

# revision identifiers
revision: str = '001_initial_migration'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Create users table
    op.create_table('user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('hashed_password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # Create tasks table
    op.create_table('task',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column('description', sqlmodel.sql.sqltypes.AutoString(length=1000), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False),
        sa.Column('priority', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=False),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('due_date', sa.DateTime(), nullable=True),
        sa.Column('recurring', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=False),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes
    op.create_index(op.f('ix_task_user_id'), 'task', ['user_id'], unique=False)
    op.create_index(op.f('ix_task_completed'), 'task', ['completed'], unique=False)
    op.create_index(op.f('ix_task_priority'), 'task', ['priority'], unique=False)
    op.create_index(op.f('ix_task_due_date'), 'task', ['due_date'], unique=False)


def downgrade() -> None:
    # Drop indexes
    op.drop_index(op.f('ix_task_due_date'), table_name='task')
    op.drop_index(op.f('ix_task_priority'), table_name='task')
    op.drop_index(op.f('ix_task_completed'), table_name='task')
    op.drop_index(op.f('ix_task_user_id'), table_name='task')

    # Drop tables
    op.drop_table('task')
    op.drop_table('user')
