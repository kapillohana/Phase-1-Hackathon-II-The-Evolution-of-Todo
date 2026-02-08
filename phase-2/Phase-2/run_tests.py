#!/usr/bin/env python3
"""
Test Runner for Advanced Todo Application
This script helps run tests to identify the dashboard task creation issue
"""

import sys
import os
import subprocess
from pathlib import Path

def run_tests():
    """Run the tests to identify the dashboard task creation issue"""
    
    # Change to the backend directory
    backend_dir = Path(__file__).parent / "backend"
    os.chdir(backend_dir)
    
    print("Testing Advanced Todo Application")
    print("=" * 50)
    
    # Check if virtual environment exists
    venv_dir = backend_dir / "venv"
    if not venv_dir.exists():
        print("ERROR: Virtual environment not found at:", venv_dir)
        print("Please create a virtual environment first:")
        print("  python -m venv venv")
        return False
    
    print(f"Virtual environment found at: {venv_dir}")
    
    # Determine the Python executable path based on OS
    if sys.platform.startswith('win'):
        # Windows
        python_executable = venv_dir / "Scripts" / "python.exe"
        pip_executable = venv_dir / "Scripts" / "pip.exe"
    else:
        # Unix-like (Linux/Mac)
        python_executable = venv_dir / "bin" / "python"
        pip_executable = venv_dir / "bin" / "pip"
    
    if not python_executable.exists():
        print(f"ERROR: Python executable not found at: {python_executable}")
        return False
    
    print(f"Python executable found at: {python_executable}")
    
    # Check if required packages are installed
    required_packages = [
        "fastapi",
        "sqlmodel", 
        "pytest",
        "python-jose",
        "passlib",
        "bcrypt"
    ]
    
    print("\nChecking for required packages...")
    missing_packages = []
    
    for package in required_packages:
        try:
            result = subprocess.run([
                str(python_executable), "-c", f"import {package.split('[')[0]}"
            ], capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                missing_packages.append(package)
        except subprocess.TimeoutExpired:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing packages: {missing_packages}")
        print("\nInstalling missing packages...")
        try:
            # Install requirements from the requirements.txt file
            subprocess.run([
                str(pip_executable), "install", "-r", "requirements.txt"
            ], check=True, capture_output=False)
            print("Packages installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Failed to install packages: {e}")
            return False
    else:
        print("All required packages are already installed.")
    
    # Run the specific tests for the dashboard issue
    print("\nRunning dashboard issue tests...")
    try:
        result = subprocess.run([
            str(python_executable), "-m", "pytest", 
            "tests/test_dashboard_issue.py", "-v", "-s"
        ], capture_output=False, check=True)
        
        print("\nDashboard issue tests completed successfully!")
        
        # Also run the auth flow tests
        print("\nRunning authentication flow tests...")
        result = subprocess.run([
            str(python_executable), "-m", "pytest", 
            "tests/test_auth_task_flow.py", "-v", "-s"
        ], capture_output=False, check=True)
        
        print("\nAuthentication flow tests completed successfully!")
        
        # Run the end-to-end workflow tests
        print("\nRunning end-to-end workflow tests...")
        result = subprocess.run([
            str(python_executable), "-m", "pytest", 
            "tests/test_end_to_end_workflow.py", "-v", "-s"
        ], capture_output=False, check=True)
        
        print("\nAll tests completed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\nERROR: Tests failed with return code {e.returncode}")
        return False

def diagnose_common_issues():
    """Diagnose common issues that might cause the dashboard task creation problem"""
    print("\nDiagnosing Common Issues")
    print("-" * 30)
    
    backend_dir = Path(__file__).parent / "backend"
    os.chdir(backend_dir)
    
    # Check if database exists
    db_path = backend_dir / "todo_app.db"
    if db_path.exists():
        print(f"✓ Database exists: {db_path}")
        print(f"  Size: {db_path.stat().st_size} bytes")
    else:
        print(f"✗ Database not found: {db_path}")
        print("  The application might try to create it automatically")
    
    # Check if the database connection works
    try:
        import sys
        venv_dir = backend_dir / "venv"
        if sys.platform.startswith('win'):
            site_packages = venv_dir / "Lib" / "site-packages"
        else:
            site_packages = venv_dir / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"
        
        sys.path.insert(0, str(site_packages))
        sys.path.insert(0, str(backend_dir / "src"))
        
        from sqlmodel import create_engine
        engine = create_engine("sqlite:///./todo_app.db")
        connection = engine.connect()
        connection.close()
        print("✓ Database connection works")
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
    
    # Check if the API endpoints are properly defined
    try:
        sys.path.insert(0, str(backend_dir / "src"))
        from src.main import app
        print("✓ Main application loads successfully")
        
        # Check for the required routes
        routes = [route.path for route in app.routes]
        required_routes = ["/auth/login", "/auth/me", "/{user_id}/tasks", "/{user_id}/tasks/{task_id}"]
        
        for route in required_routes:
            if any(route.replace("{user_id}", "123").replace("{task_id}", "456") in r for r in routes):
                print(f"✓ Route found: {route}")
            else:
                print(f"? Route might be missing or differently formatted: {route}")
                
    except Exception as e:
        print(f"✗ Application loading failed: {e}")

if __name__ == "__main__":
    print("Advanced Todo Application - Test Runner")
    print("This script will help identify the dashboard task creation issue\n")
    
    # First diagnose common issues
    diagnose_common_issues()
    
    # Then run the tests
    success = run_tests()
    
    if success:
        print("\n" + "=" * 50)
        print("TESTING COMPLETE")
        print("All tests have been run successfully.")
        print("If the dashboard task creation issue persists,")
        print("please share the test output for further analysis.")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("TESTING FAILED")
        print("Some tests failed or prerequisites weren't met.")
        print("Please check the output above for details.")
        print("=" * 50)