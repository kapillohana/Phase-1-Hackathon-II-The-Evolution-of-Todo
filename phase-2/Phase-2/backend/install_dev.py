#!/usr/bin/env python
"""
Development installation script for the Advanced Todo Application
Installs dependencies in a way that avoids compilation issues on Windows
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and show progress"""
    print(f"\n🔧 {description}")
    print(f"Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=isinstance(cmd, str))
        if result.returncode == 0:
            print(f"✅ Success: {description}")
            return True
        else:
            print(f"❌ Failed: {description}")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return False

def install_dependencies():
    """Install dependencies in the correct order to avoid compilation issues"""

    print("🚀 Starting development setup for Advanced Todo Application...")

    # Step 1: Upgrade pip first
    if not run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"],
                      "Upgrading pip, setuptools, and wheel"):
        return False

    # Step 2: Install core dependencies without database drivers
    core_deps = [
        "python-dotenv==1.0.0",
        "pydantic==2.5.0",
        "pydantic-settings==2.1.0",
        "pyjwt==2.8.0",
        "typing-extensions>=4.0.0"
    ]

    if not run_command([sys.executable, "-m", "pip", "install"] + core_deps,
                      "Installing core dependencies"):
        return False

    # Step 3: Install FastAPI ecosystem
    fastapi_deps = [
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0",
        "starlette==0.27.0"
    ]

    if not run_command([sys.executable, "-m", "pip", "install"] + fastapi_deps,
                      "Installing FastAPI ecosystem"):
        return False

    # Step 4: Install SQLModel without PostgreSQL dependencies initially
    if not run_command([sys.executable, "-m", "pip", "install", "sqlmodel==0.0.16", "SQLAlchemy==2.0.23"],
                      "Installing SQLModel and SQLAlchemy"):
        return False

    # Step 5: Install authentication dependencies
    auth_deps = [
        "bcrypt==4.0.1",
        "passlib[bcrypt]==1.7.4",
        "email-validator==2.1.0.post1"
    ]

    if not run_command([sys.executable, "-m", "pip", "install"] + auth_deps,
                      "Installing authentication dependencies"):
        return False

    # Step 6: Install security and utility dependencies
    security_deps = [
        "cryptography>=42.0.0",
        "jose==1.0.0"
    ]

    if not run_command([sys.executable, "-m", "pip", "install"] + security_deps,
                      "Installing security dependencies"):
        return False

    # Step 7: Install Alembic for migrations
    if not run_command([sys.executable, "-m", "pip", "install", "alembic==1.13.1"],
                      "Installing Alembic"):
        return False

    print("\n🎉 Core dependencies installed successfully!")
    print("\n💡 Next steps:")
    print("   1. The app will use SQLite by default (no database server needed)")
    print("   2. Run 'python startup.py' to initialize the database")
    print("   3. Run 'uvicorn src.main:app --reload' to start the server")
    print("   4. For PostgreSQL support later, install psycopg2-binary or asyncpg")

    return True

if __name__ == "__main__":
    success = install_dependencies()

    if success:
        print("\n✅ Development environment setup complete!")
        print("You can now run the application with SQLite database.")
    else:
        print("\n❌ Installation failed. Please check the error messages above.")
        print("You may need to install Microsoft C++ Build Tools for PostgreSQL support.")
        sys.exit(1)