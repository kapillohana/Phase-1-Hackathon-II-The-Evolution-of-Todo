import sys
import os
from pathlib import Path

# Add project root to Python path so 'backend' can be imported
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from sqlmodel import SQLModel

# ⚠️ IMPORTANT: Import your models so SQLModel.metadata knows about them
from backend.src.models.models import User, Task

# Alembic Config object (provides access to alembic.ini)
config = context.config

# Setup Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata for autogenerate support
target_metadata = SQLModel.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode (no DB connection)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode (with real DB connection)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


# Run correct mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()