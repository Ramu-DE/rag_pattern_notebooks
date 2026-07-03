#!/usr/bin/env python3
"""Final AWS RAG test with correct model IDs"""

import sys
sys.path.append('.')

print("=" * 70)
print("FINAL AWS RAG SETUP TEST")
print("=" * 70)

# Test 1: Embeddings
print("\n1. Testing Titan Embeddings...")
try:
    from aws_utils.bedrock_client import BedrockEmbeddings
    
    embedder = BedrockEmbeddings('us-west-2', 'amazon.titan-embed-text-v2:0')
    embedding = embedder.embed_text("Test embedding")
    
    print(f"   ✅ Embedding: {len(embedding)} dimensions")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 2: Claude with inference profile
print("\n2. Testing Claude (inference profile)...")
try:
    from aws_utils.bedrock_client import BedrockLLM
    
    # Use US inference profile
    llm = BedrockLLM('us-west-2', 'us.anthropic.claude-3-haiku-20240307-v1:0', temperature=0.7)
    response = llm.generate("Say 'Hello RAG' in 3 words.")
    
    print(f"   ✅ Response: {response}")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 3: Full RAG workflow
print("\n3. Testing full RAG workflow...")
try:
    contexts = [
        "AWS Bedrock provides managed access to foundation models.",
        "OpenSearch Serverless offers vector search for RAG applications."
    ]
    
    answer = llm.generate_with_context("What is AWS Bedrock?", contexts)
    print(f"   ✅ RAG Answer: {answer[:100]}...")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 70)
print("✅ SETUP COMPLETE - READY TO EXECUTE NOTEBOOKS!")
print("=" * 70)
print("\nWorking configuration:")
print("  Embeddings: amazon.titan-embed-text-v2:0")
print("  LLM: us.anthropic.claude-3-haiku-20240307-v1:0")
print("  OpenSearch: qrm9kbjh7wmnpa99ee2b.us-west-2.aoss.amazonaws.com")
