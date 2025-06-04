#!/usr/bin/env python3
"""
Setup script for Gen AI Security Report Generator
"""

import os
import shutil


def create_env_file():
    """Create .env file from example if it doesn't exist"""
    env_example = """# Gen AI Security Report Generator Configuration
# Copy this file to .env and fill in your actual values

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini

# Email Configuration (for sending reports)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password_here

# Flask Configuration
SECRET_KEY=your_secret_key_here
FLASK_DEBUG=True

# Company Configuration
COMPANY_NAME=SecureCorp Inc.
COMPANY_LOGO=static/images/logo.png

# Optional: Custom configurations
# REPORTS_DIR=generated_reports
# DATA_DIR=data
"""

    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write(env_example)
        print("✅ Created .env file. Please edit it with your actual configuration.")
    else:
        print("ℹ️  .env file already exists.")


def create_placeholder_logo():
    """Create a simple placeholder logo"""
    logo_svg = """<svg width="200" height="60" xmlns="http://www.w3.org/2000/svg">
  <rect width="200" height="60" fill="#1f77b4" rx="5"/>
  <text x="100" y="35" font-family="Arial, sans-serif" font-size="18" font-weight="bold" 
        text-anchor="middle" fill="white">SecureCorp</text>
</svg>"""

    os.makedirs("static/images", exist_ok=True)

    if not os.path.exists("static/images/logo.svg"):
        with open("static/images/logo.svg", "w") as f:
            f.write(logo_svg)
        print("✅ Created placeholder logo at static/images/logo.svg")
    else:
        print("ℹ️  Logo file already exists.")


def main():
    """Main setup function"""
    print("🚀 Setting up Gen AI Security Report Generator...")
    print()

    # Create .env file
    create_env_file()

    # Create placeholder logo
    create_placeholder_logo()

    # Create necessary directories
    directories = ["generated_reports", "static/images", "data", "templates", "utils"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    print()
    print("✅ Setup complete!")
    print()
    print("📋 Next steps:")
    print("1. Edit the .env file with your OpenAI API key and email credentials")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Run the application: python app.py")
    print("4. Open your browser to http://localhost:5000")
    print()
    print("📖 For more information, see the README.md file")


if __name__ == "__main__":
    main()
