#!/usr/bin/env python
"""
Application startup script for the Advanced Todo Application
Handles database initialization and startup checks
"""

import os
import sys
from pathlib import Path

# Add the src directory to the path so we can import modules
sys.path.insert(0, str(Path(__file__).parent / "src"))

def initialize_database():
    """Initialize the database and create tables if they don't exist"""
    print("🔍 Checking database connection...")

    try:
        from src.database.database import check_connection, create_db_and_tables

        # Test the database connection
        if check_connection():
            print("✅ Database connection successful!")
        else:
            print("❌ Could not connect to database. Please check your DATABASE_URL in the .env file.")
            return False

        # Create tables if they don't exist
        print("🔧 Creating database tables...")
        create_db_and_tables()
        print("✅ Database tables created successfully!")

        return True
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False

def main():
    """Main startup function"""
    print("🚀 Starting Advanced Todo Application...")

    # Initialize database
    if not initialize_database():
        print("❌ Database initialization failed. Exiting...")
        sys.exit(1)

    print("🎉 Application startup complete!")
    print("💡 To start the server, run: poetry run uvicorn src.main:app --reload")
    print("💡 Or visit http://localhost:8000/docs for the API documentation")

if __name__ == "__main__":
    main()