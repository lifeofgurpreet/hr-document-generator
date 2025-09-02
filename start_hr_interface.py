#!/usr/bin/env python3
"""
HR Document Generator Interface Startup Script
"""

import os
import sys
import subprocess

def check_openai_key():
    """Check if OpenAI API key is set"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("⚠️  Warning: OPENAI_API_KEY environment variable is not set!")
        print("🔄 Starting in DEMO MODE - documents will be generated without AI enhancement")
        print("\nTo enable full AI features, set your OpenAI API key:")
        print("\nFor macOS/Linux:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        print("\nFor Windows:")
        print("set OPENAI_API_KEY=your-api-key-here")
        print("\nOr create a .env file in the project root with:")
        print("OPENAI_API_KEY=your-api-key-here")
        return False
    print("✅ OpenAI API key found - full AI features enabled!")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Packages installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install packages. Please run: pip install -r requirements.txt")
        return False

def start_app():
    """Start the Flask application"""
    print("🚀 Starting HR Document Generator Interface...")
    print("📱 The interface will be available at: http://localhost:5001")
    print("🔄 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def main():
    print("🎯 HR Document Generator Interface")
    print("=" * 40)
    
    # Check OpenAI API key (but don't fail if not set)
    check_openai_key()
    
    # Install requirements
    if not install_requirements():
        return
    
    # Start the application
    start_app()

if __name__ == '__main__':
    main()
