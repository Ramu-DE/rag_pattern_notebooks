#!/usr/bin/env python3
"""
Simple test to verify basic RAG workflow works
"""

import sys
from pathlib import Path

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent))

def test_basic_rag():
    """Test basic RAG workflow"""
    print("=" * 70)
    print("Testing Basic RAG Workflow")
    print("=" * 70)
    print()

    # Test 1: Environment Loading
    print("1. Testing environment loading...")
    try:
        from utils.env_loader import load_environment, check_required_keys
        load_environment()
        check_required_keys('AWS_ACCESS_KEY_ID', 'QDRANT_API_KEY')
        print("   ✅ Environment loaded successfully")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False

    # Test 2: Bedrock Helper
    print("\n2. Testing Bedrock helper imports...")
    try:
        from utils.bedrock_helper import (
            get_bedrock_llm,
            get_bedrock_embeddings,
            get_qdrant_vectorstore,
            get_qdrant_client
        )
        print("   ✅ All helper functions imported")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False

    # Test 3: Get LLM
    print("\n3. Testing LLM initialization...")
    try:
        llm = get_bedrock_llm()
        print("   ✅ LLM initialized")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False

    # Test 4: Get Embeddings
    print("\n4. Testing embeddings initialization...")
    try:
        embeddings = get_bedrock_embeddings()
        print("   ✅ Embeddings initialized")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False

    # Test 5: Test embedding
    print("\n5. Testing embedding generation...")
    try:
        test_vec = embeddings.embed_query("This is a test")
        print(f"   ✅ Generated embedding (dimension: {len(test_vec)})")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False

    # Test 6: LLM invocation
    print("\n6. Testing LLM invocation...")
    try:
        response = llm.invoke("Say 'Hello World' and nothing else.")
        response_text = response.content if hasattr(response, 'content') else str(response)
        print(f"   ✅ LLM responded: {response_text[:100]}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False

    # Test 7: Qdrant client
    print("\n7. Testing Qdrant connection...")
    try:
        client = get_qdrant_client()
        collections = client.get_collections()
        print(f"   ✅ Connected to Qdrant ({len(collections.collections)} collections)")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False

    # Test 8: Create test vectorstore
    print("\n8. Testing vectorstore creation...")
    try:
        vectorstore = get_qdrant_vectorstore("test-rag-workflow", embeddings)
        print("   ✅ Vectorstore created")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False

    # Test 9: Add documents
    print("\n9. Testing document addition...")
    try:
        test_docs = [
            "Retrieval-Augmented Generation (RAG) combines retrieval and generation.",
            "Vector databases store embeddings for semantic search.",
            "AWS Bedrock provides managed AI services including Claude and Titan models."
        ]
        vectorstore.add_texts(test_docs)
        print(f"   ✅ Added {len(test_docs)} documents")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False

    # Test 10: Similarity search
    print("\n10. Testing similarity search...")
    try:
        query = "What is RAG?"
        results = vectorstore.similarity_search(query, k=2)
        print(f"   ✅ Found {len(results)} relevant documents")
        if results:
            print(f"   📄 Top result: {results[0].page_content[:80]}...")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False

    # Test 11: RAG chain
    print("\n11. Testing complete RAG chain...")
    try:
        from langchain.chains import RetrievalQA

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 2})
        )

        question = "What is RAG?"
        answer = qa_chain.invoke({"query": question})
        print(f"   ✅ RAG chain executed")
        print(f"   ❓ Question: {question}")
        print(f"   💡 Answer: {answer['result'][:150]}...")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False

    # Test 12: Cleanup
    print("\n12. Cleaning up test collection...")
    try:
        client.delete_collection("test-rag-workflow")
        print("   ✅ Test collection deleted")
    except Exception as e:
        print(f"   ⚠️  Cleanup failed (non-critical): {e}")

    print()
    print("=" * 70)
    print("✅ ALL TESTS PASSED!")
    print("=" * 70)
    print()
    print("🎉 Basic RAG workflow is fully functional!")
    print()
    print("You can now:")
    print("  1. Start Jupyter Lab: jupyter lab")
    print("  2. Open: notebooks/simple_rag/simple_rag.ipynb")
    print("  3. Run cells to explore RAG techniques")
    print()

    return True

if __name__ == "__main__":
    success = test_basic_rag()
    sys.exit(0 if success else 1)
