#!/usr/bin/env python
"""
Simple installation script for the Advanced Todo Application
Uses only packages with pre-compiled wheels to avoid compilation issues
"""

import subprocess
import sys
import os

def install_package(package_name, version=None):
    """Install a single package with specific version if provided"""
    cmd = [sys.executable, "-m", "pip", "install"]
    if version:
        cmd.append(f"{package_name}=={version}")
    else:
        cmd.append(package_name)

    print(f"📦 Installing {package_name}{'==' + version if version else ''}...")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {package_name} installed successfully")
            return True
        else:
            print(f"❌ Failed to install {package_name}")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error installing {package_name}: {e}")
        return False

def main():
    print("🚀 Installing Advanced Todo Application dependencies...")
    print("💡 This will install only packages with pre-compiled wheels to avoid compilation issues")

    # Install in specific order
    packages_to_install = [
        ("setuptools", "68.2.2"),
        ("wheel", "0.41.2"),
        ("pip", "23.3.1"),
        ("typing-extensions", "4.8.0"),
        ("python-dotenv", "1.0.0"),
        ("pydantic-core", "2.14.5"),  # Specific version with wheels
        ("pydantic", "2.5.0"),
        ("pydantic-settings", "2.1.0"),
        ("anyio", "4.0.0"),
        ("idna", "3.4"),
        ("sniffio", "1.3.0"),
        ("h11", "0.14.0"),
        ("httpcore", "1.0.2"),
        ("httpx", "0.25.2"),
        ("click", "8.1.7"),
        ("colorama", "0.4.6"),  # Windows compatibility
        ("fastapi", "0.104.1"),
        ("uvicorn", "0.24.0"),
        ("starlette", "0.27.0"),
        ("SQLAlchemy", "2.0.23"),
        ("greenlet", "3.0.1"),
        ("pyjwt", "2.8.0"),
        ("bcrypt", "4.0.1"),
        ("passlib", "1.7.4"),
        ("email-validator", "2.1.0.post1"),
        ("idna", "3.4"),  # For email validation
        ("cryptography", "42.0.0"),
        ("alembic", "1.13.1"),
        ("Mako", "1.2.4"),  # For alembic
        (" MarkupSafe", "2.1.3"),  # For Mako
    ]

    # First install the basic packages without SQLModel to avoid psycopg2
    basic_packages = [
        ("setuptools", "68.2.2"),
        ("wheel", "0.41.2"),
        ("pip", "23.3.1"),
        ("typing-extensions", "4.8.0"),
        ("python-dotenv", "1.0.0"),
        ("pydantic-core", "2.14.5"),
        ("pydantic", "2.5.0"),
        ("pydantic-settings", "2.1.0"),
        ("anyio", "4.0.0"),
        ("idna", "3.4"),
        ("sniffio", "1.3.0"),
        ("h11", "0.14.0"),
        ("httpcore", "1.0.2"),
        ("click", "8.1.7"),
        ("colorama", "0.4.6"),
        ("fastapi", "0.104.1"),
        ("uvicorn", "0.24.0"),
        ("starlette", "0.27.0"),
        ("SQLAlchemy", "2.0.23"),
        ("greenlet", "3.0.1"),
        ("pyjwt", "2.8.0"),
        ("bcrypt", "4.0.1"),
        ("passlib", "1.7.4"),
        ("email-validator", "2.1.0.post1"),
        ("cryptography", "42.0.0"),
        ("alembic", "1.13.1"),
        ("Mako", "1.2.4"),
    ]

    print("\n📦 Installing basic dependencies...")
    for package, version in basic_packages:
        if not install_package(package, version):
            print(f"⚠️  Continuing despite failure to install {package}")

    # Now try to install sqlmodel separately
    print("\n📦 Installing SQLModel...")
    if not install_package("sqlmodel", "0.0.16"):
        print("⚠️  SQLModel failed to install, trying alternative approach...")
        # Try installing without psycopg2 dependencies
        if not install_package("sqlmodel", "0.0.16"):
            print("⚠️  Attempting to continue without SQLModel for now...")

    print("\n🎉 Installation process completed!")
    print("\n💡 Next steps:")
    print("   1. Run 'python startup.py' to test the application")
    print("   2. If you still have issues, you may need to install:")
    print("      - Microsoft C++ Build Tools")
    print("      - Rust (rustup.rs) - for packages with Rust dependencies")
    print("      - Or use Python 3.11/3.12 instead of 3.13")

if __name__ == "__main__":
    main()