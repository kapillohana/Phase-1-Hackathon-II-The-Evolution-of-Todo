#!/usr/bin/env python3
"""
Script to fix the is_active default value in the database schema
"""

import subprocess
import os
import sys

def run_command(cmd, cwd=None):
    """Run a command and return the result"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(f"Success: {result.stdout}")
    return True

def main():
    backend_dir = "/mnt/c/Users/PMLS/Desktop/hackathon2-phase2/Phase-1-Hackathon-II-The-Evolution-of-Todo/backend"

    # First, let's try to run the alembic migration
    print("Creating a new migration for is_active default fix...")

    # Create a new migration to add the default value
    cmd = f"cd {backend_dir} && python -m alembic revision --autogenerate -m 'Fix user.is_active default'"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(f"Alembic revision result: {result.stdout}")
    if result.stderr:
        print(f"Alembic revision error: {result.stderr}")

    # Now try to upgrade the database
    cmd = f"cd {backend_dir} && python -m alembic upgrade head"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(f"Alembic upgrade result: {result.stdout}")
    if result.stderr:
        print(f"Alembic upgrade error: {result.stderr}")

if __name__ == "__main__":
    main()