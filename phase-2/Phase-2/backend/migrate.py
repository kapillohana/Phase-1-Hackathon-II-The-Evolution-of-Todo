#!/usr/bin/env python
"""
Migration management script for the Advanced Todo Application
"""

import os
import subprocess
import sys
from pathlib import Path

def run_migrations():
    """Run database migrations using Alembic"""
    # Change to backend directory
    backend_dir = Path(__file__).parent / "backend"
    os.chdir(backend_dir)

    # Set environment variables
    env = os.environ.copy()
    env['PYTHONPATH'] = str(backend_dir)

    try:
        # Run alembic upgrade
        result = subprocess.run([
            "poetry", "run", "alembic", "upgrade", "head"
        ], env=env, capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ Migrations completed successfully!")
            print(result.stdout)
        else:
            print("❌ Migration failed!")
            print(result.stderr)
            return False

    except FileNotFoundError:
        print("❌ Poetry not found. Installing dependencies with pip...")
        # Fallback to pip if poetry is not available
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], check=True)
            result = subprocess.run([
                sys.executable, "-m", "alembic", "upgrade", "head"
            ], env=env, capture_output=True, text=True)

            if result.returncode == 0:
                print("✅ Migrations completed successfully!")
                print(result.stdout)
            else:
                print("❌ Migration failed!")
                print(result.stderr)
                return False
        except Exception as e:
            print(f"❌ Error running migrations: {e}")
            return False

    return True

def create_migration(message):
    """Create a new migration"""
    backend_dir = Path(__file__).parent / "backend"
    os.chdir(backend_dir)

    env = os.environ.copy()
    env['PYTHONPATH'] = str(backend_dir)

    try:
        result = subprocess.run([
            "poetry", "run", "alembic", "revision", "--autogenerate", "-m", message
        ], env=env, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"✅ Migration created: {result.stdout}")
        else:
            print(f"❌ Failed to create migration: {result.stderr}")
    except Exception as e:
        print(f"❌ Error creating migration: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python migrate.py [upgrade|create]")
        print("  upgrade: Run all pending migrations")
        print("  create <message>: Create a new migration with the given message")
        sys.exit(1)

    command = sys.argv[1]

    if command == "upgrade":
        run_migrations()
    elif command == "create":
        if len(sys.argv) < 3:
            print("Please provide a message for the migration")
            sys.exit(1)
        create_migration(sys.argv[2])
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)