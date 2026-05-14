#!/usr/bin/env python3
"""
Quick test script for Bedrock + Qdrant configuration
Run this after installing dependencies with: pip install -r requirements.txt
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("=" * 70)
    print("🧪 Quick Test: AWS Bedrock + Qdrant Configuration")
    print("=" * 70)
    print()

    # Load environment
    try:
        from utils.env_loader import load_environment, check_required_keys
        print("✅ Environment loader imported successfully")

        load_environment()
        print("✅ Environment loaded from .env file")
        print()

        # Check required keys
        check_required_keys(
            'AWS_ACCESS_KEY_ID',
            'AWS_SECRET_ACCESS_KEY',
            'QDRANT_API_KEY'
        )
        print()

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print()
        print("Please install dependencies first:")
        print("  pip install -r requirements.txt")
        print()
        return 1

    # Test Bedrock + Qdrant
    try:
        print("=" * 70)
        print("Testing Complete Stack")
        print("=" * 70)
        print()

        from utils.bedrock_helper import test_full_stack

        results = test_full_stack()

        print()
        print("=" * 70)
        print("🎉 Test Results Summary")
        print("=" * 70)
        print(f"Bedrock Status: {results['bedrock']['status']}")
        print(f"Qdrant Status: {results['qdrant']['status']}")
        print(f"Overall Status: {results['overall_status']}")
        print("=" * 70)

        if results['overall_status'] == 'success':
            print()
            print("✅ All systems operational!")
            print("🚀 You're ready to build RAG applications!")
            print()
            print("Next steps:")
            print("1. Start Jupyter: jupyter lab")
            print("2. Open: TEST_BEDROCK_QDRANT.ipynb")
            print("3. Try: notebooks/simple_rag/simple_rag.ipynb")
            return 0
        else:
            print()
            print("⚠️  Some tests failed. Check the details above.")
            return 1

    except Exception as e:
        print(f"❌ Error during testing: {e}")
        print()
        print("Common issues:")
        print("1. Bedrock models not enabled in AWS Console")
        print("2. AWS credentials expired (session tokens expire quickly)")
        print("3. Network connectivity issues")
        print()
        return 1

if __name__ == "__main__":
    exit(main())
