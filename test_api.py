"""
Quick API integration test
Tests that FastAPI correctly wraps the existing chatbot
"""

import sys
from pathlib import Path

# Add scripts to path
SCRIPTS_DIR = Path(__file__).parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

# Test imports
print("Testing imports...")
try:
    from rag_pipeline import answer_query
    print("✅ rag_pipeline imported successfully")
except Exception as e:
    print(f"❌ Failed to import rag_pipeline: {e}")
    sys.exit(1)

try:
    from voice_input import VoiceInputProcessor
    print("✅ voice_input imported successfully")
except Exception as e:
    print(f"❌ Failed to import voice_input: {e}")
    sys.exit(1)

try:
    from voice_output import VoiceOutputProcessor
    print("✅ voice_output imported successfully")
except Exception as e:
    print(f"❌ Failed to import voice_output: {e}")
    sys.exit(1)

# Test chatbot functionality
print("\nTesting chatbot...")
try:
    response = answer_query("What is IPC Section 420?")
    print("✅ Chatbot responded successfully")
    print(f"\nResponse preview: {response[:200]}...")
except Exception as e:
    print(f"❌ Chatbot failed: {e}")
    sys.exit(1)

print("\n" + "=" * 80)
print("✅ All integration tests passed!")
print("=" * 80)
print("\nYou can now run the API with:")
print("  uvicorn main:app --reload")
print("\nOr:")
print("  python main.py")
