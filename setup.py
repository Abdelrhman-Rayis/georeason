#!/usr/bin/env python3
"""
Zoal AI Setup Script
This script helps you set up the Zoal AI chatbot application.
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_env_file():
    """Create .env file with template"""
    env_content = """# Zoal AI Environment Variables
# Add your API keys here

# OpenAI API Key (Get from https://platform.openai.com/)
OPENAI_API_KEY=your_openai_api_key_here

# Google API Key (Get from https://makersuite.google.com/app/apikey)
GOOGLE_API_KEY=your_google_api_key_here

# Django Secret Key (Generate a new one for production)
SECRET_KEY=your_django_secret_key_here

# Debug mode (Set to False in production)
DEBUG=True
"""
    
    env_file = Path('.env')
    if not env_file.exists():
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ Created .env file with template")
        print("📝 Please edit .env file and add your API keys")
    else:
        print("ℹ️  .env file already exists")

def main():
    print("🚀 Welcome to Zoal AI Setup!")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path('manage.py').exists():
        print("❌ Error: Please run this script from the zoal_ai project directory")
        sys.exit(1)
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("❌ Failed to install dependencies. Please check your Python environment.")
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    # Run migrations
    if not run_command("python manage.py makemigrations", "Creating database migrations"):
        print("❌ Failed to create migrations")
        sys.exit(1)
    
    if not run_command("python manage.py migrate", "Applying database migrations"):
        print("❌ Failed to apply migrations")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit the .env file and add your API keys")
    print("2. Run: python manage.py runserver")
    print("3. Open http://127.0.0.1:8000 in your browser")
    print("\n🌍 Enjoy chatting with Zoal AI!")

if __name__ == "__main__":
    main() 