#!/usr/bin/env python
"""
Quick Start Script for Legal Chatbot API
Checks environment and provides setup instructions
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("❌ Python 3.11+ required")
        return False
    
    print("✅ Python version OK")
    return True

def check_virtual_env():
    """Check if virtual environment exists"""
    venv_path = Path("legal_chatbot")
    
    if venv_path.exists():
        print("✅ Virtual environment found")
        return True
    else:
        print("⚠️  Virtual environment not found")
        print("   Run: python -m venv legal_chatbot")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    required = ["fastapi", "uvicorn", "langchain", "chromadb", "openai"]
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} not installed")
            missing.append(package)
    
    if missing:
        print("\n⚠️  Missing dependencies detected")
        print("   Run: pip install -r requirements.txt")
        return False
    
    return True

def check_env_file():
    """Check if .env file exists"""
    env_path = Path(".env")
    
    if env_path.exists():
        print("✅ .env file found")
        
        # Check if it has required keys
        with open(env_path) as f:
            content = f.read()
            if "OPENAI_API_KEY" in content:
                print("✅ OPENAI_API_KEY configured")
            else:
                print("⚠️  OPENAI_API_KEY not found in .env")
        
        return True
    else:
        print("❌ .env file not found")
        print("   Create .env with:")
        print("   OPENAI_API_KEY=your_key")
        print("   OPENAI_BASE_URL=https://openrouter.ai/api/v1")
        return False

def check_vector_db():
    """Check if vector DB exists"""
    db_path = Path("scripts/chroma_day1")
    
    if db_path.exists():
        print("✅ Vector database found")
        return True
    else:
        print("❌ Vector database not found")
        print("   Expected: scripts/chroma_day1/")
        return False

def print_next_steps(all_ok):
    """Print next steps based on checks"""
    print("\n" + "=" * 60)
    
    if all_ok:
        print("✅ ALL CHECKS PASSED - Ready to run!")
        print("=" * 60)
        print("\nStart the API server:")
        print("\n  Option 1 (Development):")
        print("    uvicorn main:app --reload --port 8000")
        print("\n  Option 2 (Production):")
        print("    python main.py")
        print("\nThen visit:")
        print("  - API Docs: http://localhost:8000/docs")
        print("  - Health Check: http://localhost:8000/health")
        
    else:
        print("⚠️  SETUP INCOMPLETE")
        print("=" * 60)
        print("\nComplete these steps:")
        print("\n1. Create virtual environment:")
        print("   python -m venv legal_chatbot")
        print("\n2. Activate virtual environment:")
        print("   legal_chatbot\\Scripts\\activate  # Windows")
        print("   source legal_chatbot/bin/activate  # macOS/Linux")
        print("\n3. Install dependencies:")
        print("   pip install -r requirements.txt")
        print("\n4. Create .env file with your API key")
        print("\n5. Run this script again: python quick_start.py")

def main():
    print("=" * 60)
    print("Legal Chatbot API - Quick Start Check")
    print("=" * 60)
    print()
    
    checks = [
        check_python_version(),
        check_virtual_env(),
        check_env_file(),
        check_vector_db(),
        check_dependencies(),
    ]
    
    all_ok = all(checks)
    print_next_steps(all_ok)
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
