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

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

# Create the database engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_size=10,           # Number of connections to maintain in the pool
    max_overflow=20,        # Additional connections beyond pool_size
    pool_pre_ping=True,     # Verify connections before use
    echo=False,             # Set to True for SQL debugging
    connect_args={
        "connect_timeout": 10,  # Connection timeout
    }
)


def create_db_and_tables():
    """
    Create all database tables based on SQLModel definitions
    Should be called during application startup
    """
    from ..models.models import User, Task  # Import models to register them
    from sqlmodel import SQLModel

    SQLModel.metadata.create_all(engine)


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
        with Session(engine) as session:
            # Simple test to check if we can connect
            result = session.exec("SELECT 1").first()
            return result is not None
    except Exception as e:
        print(f"Database connection error: {e}")
        return False


# Initialize the database tables on import (optional)
# Uncomment the line below if you want to auto-create tables on startup
# create_db_and_tables()