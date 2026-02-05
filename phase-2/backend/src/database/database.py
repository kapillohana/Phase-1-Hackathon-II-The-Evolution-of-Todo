"""
Database connection and session management for the Advanced Todo Application
Uses SQLModel with Neon Serverless PostgreSQL
"""
from sqlmodel import create_engine, Session
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment with SQLite as fallback
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Handle SQLite URL specially (doesn't support pool_size, max_overflow, etc.)
if DATABASE_URL.startswith("sqlite"):
    # SQLite specific engine configuration
    engine = create_engine(
        DATABASE_URL,
        echo=False,  # Set to True for SQL debugging
        connect_args={"check_same_thread": False}  # Required for SQLite
    )
else:
    # PostgreSQL engine configuration
    engine = create_engine(
        DATABASE_URL,
        pool_size=5,            # Reduced for development
        max_overflow=10,        # Reduced for development
        pool_pre_ping=True,     # Verify connections before use
        echo=False,             # Set to True for SQL debugging
        pool_recycle=300,       # Recycle connections
        connect_args={
            "connect_timeout": 10,  # Connection timeout (only for PostgreSQL)
        }
    )


def create_db_and_tables():
    """
    Create all database tables based on SQLModel definitions
    Should be called during application startup
    """
    try:
        from ..models.models import User, Task  # Import models to register them
        from sqlmodel import SQLModel

        # Create all tables
        SQLModel.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        raise


def get_session() -> Generator[Session, None, None]:
    """
    Generator function to provide database sessions
    Used with FastAPI dependency injection
    """
    with Session(engine) as session:
        yield session


# Additional utility functions for database management

def get_async_session() -> Generator[Session, None, None]:
    """
    Async generator for async database sessions (if needed in future)
    """
    with Session(engine) as session:
        yield session


def check_connection():
    """
    Function to test database connectivity
    """
    try:
        from sqlmodel import text
        with Session(engine) as session:
            # Test connection differently for SQLite vs PostgreSQL
            if DATABASE_URL.startswith("sqlite"):
                # SQLite test
                result = session.exec(text("SELECT 1")).first()
            else:
                # PostgreSQL test
                result = session.exec(text("SELECT 1")).first()
            return result is not None
    except Exception as e:
        print(f"Database connection error: {e}")
        return False


# Initialize the database tables on import (optional)
# Uncomment the line below if you want to auto-create tables on startup
# create_db_and_tables()
