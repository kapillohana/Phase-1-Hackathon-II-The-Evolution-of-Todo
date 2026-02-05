#!/usr/bin/env python
"""
Core installation script - minimal dependencies for the Todo app
"""
import subprocess
import sys

def install_core_deps():
    """Install only the essential dependencies"""
    print("📦 Installing core dependencies...")

    # Install packages one by one to isolate issues
    packages = [
        "python-dotenv==1.0.0",
        "pydantic==2.5.0",
        "pydantic-settings==2.1.0",
        "pyjwt==2.8.0",
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0",
        "bcrypt==4.0.1",
        "passlib[bcrypt]==1.7.4",
        "email-validator==2.1.0.post1",
        "cryptography>=42.0.0"
    ]

    for package in packages:
        print(f"Installing {package}...")
        result = subprocess.run([sys.executable, "-m", "pip", "install", package])
        if result.returncode != 0:
            print(f"❌ Failed to install {package}")
            return False
        else:
            print(f"✅ {package} installed")

    # Install SQLModel separately to handle database
    print("Installing SQLModel...")
    result = subprocess.run([sys.executable, "-m", "pip", "install", "SQLAlchemy==2.0.23"])
    if result.returncode == 0:
        result = subprocess.run([sys.executable, "-m", "pip", "install", "sqlmodel==0.0.16"])

    if result.returncode != 0:
        print("⚠️ SQLModel installation failed, but continuing...")
    else:
        print("✅ SQLModel installed")

    print("✅ Core dependencies installed!")
    print("\n💡 Run: python startup.py")
    return True

if __name__ == "__main__":
    install_core_deps()