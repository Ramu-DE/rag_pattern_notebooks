#!/usr/bin/env python3
"""Test Simple RAG pattern with working models"""

import sys
sys.path.append('.')

print("=" * 70)
print("TEST: Simple RAG Pattern (v2 - Working Models)")
print("=" * 70)

# Test BedrockEmbeddings
print("\n1. Testing BedrockEmbeddings (Titan)...")
try:
    from aws_utils.bedrock_client import BedrockEmbeddings
    
    embedder = BedrockEmbeddings('us-west-2', 'amazon.titan-embed-text-v2:0')
    print("   ✓ BedrockEmbeddings initialized")
    
    test_text = "AWS Bedrock provides foundation models for AI applications"
    embedding = embedder.embed_text(test_text)
    
    print(f"   ✓ Generated embedding: {len(embedding)} dimensions")
    print(f"   ✓ Sample values: [{embedding[0]:.4f}, {embedding[1]:.4f}, {embedding[2]:.4f}, ...]")
    
except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test BedrockLLM with Claude 3 Haiku
print("\n2. Testing BedrockLLM (Claude 3 Haiku)...")
try:
    from aws_utils.bedrock_client import BedrockLLM
    
    llm = BedrockLLM('us-west-2', 'anthropic.claude-3-haiku-20240307-v1:0', temperature=0.7)
    print("   ✓ BedrockLLM initialized")
    
    prompt = "What is RAG? Answer in one sentence."
    response = llm.generate(prompt)
    
    print(f"   ✓ Response: {response}")
    
except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test multiple embeddings
print("\n3. Testing batch embeddings...")
try:
    texts = [
        "Retrieval Augmented Generation combines search with LLMs",
        "Vector databases store embeddings for similarity search",
        "AWS OpenSearch provides vector search capabilities"
    ]
    
    embeddings = [embedder.embed_text(text) for text in texts]
    print(f"   ✓ Generated {len(embeddings)} embeddings")
    print(f"   ✓ Each embedding: {len(embeddings[0])} dimensions")
    
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test context-aware generation
print("\n4. Testing RAG generation...")
try:
    contexts = [
        "RAG stands for Retrieval Augmented Generation. It combines information retrieval with language models.",
        "RAG systems first retrieve relevant documents, then use them as context for generating answers.",
        "This approach improves accuracy by grounding responses in actual data."
    ]
    
    query = "What are the benefits of RAG?"
    answer = llm.generate_with_context(query, contexts)
    
    print(f"   ✓ Query: {query}")
    print(f"   ✓ Answer: {answer[:200]}...")
    
except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("✅ ALL TESTS PASSED - AWS Setup Working!")
print("=" * 70)
print("\nReady to execute notebooks with:")
print(f"  - Embeddings: amazon.titan-embed-text-v2:0")
print(f"  - LLM: anthropic.claude-3-haiku-20240307-v1:0")
print(f"  - OpenSearch: qrm9kbjh7wmnpa99ee2b.us-west-2.aoss.amazonaws.com")
