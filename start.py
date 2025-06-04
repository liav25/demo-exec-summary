#!/usr/bin/env python3
"""
Quick Start Script for Gen AI Security Report Generator
This script helps you get the application running quickly with all necessary checks.
"""

import os
import sys
import subprocess
import importlib.util


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True


def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        "flask",
        "pandas",
        "plotly",
        "weasyprint",
        "openai",
        "python-dotenv",
        "requests",
        "openpyxl",
    ]

    missing_packages = []

    for package in required_packages:
        if importlib.util.find_spec(package) is None:
            missing_packages.append(package)

    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        return False

    print("✅ All required packages are installed")
    return True


def check_env_file():
    """Check if .env file exists"""
    if not os.path.exists(".env"):
        print("❌ .env file not found")
        return False

    print("✅ .env file found")
    return True


def check_data_files():
    """Check if required data files exist"""
    required_files = [
        "data/security_events.csv",
        "data/phishing_data.csv",
        "data/compliance_data.csv",
    ]

    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)

    if missing_files:
        print(f"❌ Missing data files: {', '.join(missing_files)}")
        return False

    print("✅ All required data files found")
    return True


def install_dependencies():
    """Install dependencies from requirements.txt"""
    try:
        print("📦 Installing dependencies...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        )
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def run_setup():
    """Run the environment setup script"""
    try:
        print("🔧 Running environment setup...")
        subprocess.check_call([sys.executable, "setup_env.py"])
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Setup failed: {e}")
        return False


def start_application():
    """Start the Flask application"""
    try:
        print("🚀 Starting the application...")
        print("   Application will be available at: http://localhost:5000")
        print("   Press Ctrl+C to stop the application")
        subprocess.check_call([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start application: {e}")


def main():
    """Main function to orchestrate the startup process"""
    print("🔧 Gen AI Security Report Generator - Quick Start")
    print("=" * 60)

    # Check Python version
    if not check_python_version():
        sys.exit(1)

    # Check dependencies
    if not check_dependencies():
        print("\n📦 Installing missing dependencies...")
        if not install_dependencies():
            print("\n❌ Failed to install dependencies. Please run:")
            print("   pip install -r requirements.txt")
            sys.exit(1)

    # Check .env file
    if not check_env_file():
        print("\n🔧 Setting up environment configuration...")
        if not run_setup():
            print("\n❌ Environment setup failed. Please run:")
            print("   python setup_env.py")
            sys.exit(1)

    # Check data files
    if not check_data_files():
        print("\n❌ Required data files are missing.")
        print("   Please ensure the following files exist:")
        print("   - data/security_events.csv")
        print("   - data/phishing_data.csv")
        print("   - data/compliance_data.csv")
        sys.exit(1)

    print("\n✅ All checks passed! Starting the application...")
    print("\n📋 Application Features:")
    print("   • AI-powered security report generation")
    print("   • Interactive data visualizations")
    print("   • Professional PDF reports")
    print("   • Email delivery system")
    print("   • Multiple report types and time periods")

    # Start the application
    start_application()


if __name__ == "__main__":
    main()
