#!/usr/bin/env python3
"""Test Simple RAG pattern"""

import sys
sys.path.append('.')

import boto3
import json

print("=" * 70)
print("TEST: Simple RAG Pattern")
print("=" * 70)

# Test BedrockEmbeddings
print("\n1. Testing BedrockEmbeddings...")
try:
    from aws_utils.bedrock_client import BedrockEmbeddings
    
    embedder = BedrockEmbeddings('us-west-2', 'amazon.titan-embed-text-v2:0')
    print("   ✓ BedrockEmbeddings initialized")
    
    test_text = "AWS Bedrock provides foundation models"
    embedding = embedder.embed_text(test_text)
    
    print(f"   ✓ Generated embedding: {len(embedding)} dimensions")
    print(f"   ✓ First 5 values: {embedding[:5]}")
    
except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()

# Test BedrockLLM
print("\n2. Testing BedrockLLM...")
try:
    from aws_utils.bedrock_client import BedrockLLM
    
    llm = BedrockLLM('us-west-2', 'anthropic.claude-haiku-4-5-20251001-v1:0', temperature=0.7)
    print("   ✓ BedrockLLM initialized")
    
    prompt = "What is RAG in 10 words?"
    response = llm.generate(prompt)
    
    print(f"   ✓ Generated response: {response[:100]}...")
    
except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()

# Test context-aware generation
print("\n3. Testing context-aware generation...")
try:
    contexts = [
        "RAG stands for Retrieval Augmented Generation.",
        "RAG combines retrieval with language models for better answers."
    ]
    
    query = "What is RAG?"
    answer = llm.generate_with_context(query, contexts)
    
    print(f"   ✓ Generated answer: {answer[:150]}...")
    
except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("SIMPLE RAG TEST COMPLETE")
print("=" * 70)
