"""
AWS Bedrock Helper Functions for RAG Techniques
Provides utilities for using Bedrock LLMs and embeddings with Qdrant
"""

import os
import boto3
from typing import Optional, List
from langchain_aws import BedrockEmbeddings, ChatBedrock
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams


def get_bedrock_client(
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    aws_session_token: Optional[str] = None,
    region_name: Optional[str] = None
):
    """
    Create and return a Bedrock client.

    Args:
        aws_access_key_id: AWS access key (uses env var if not provided)
        aws_secret_access_key: AWS secret key (uses env var if not provided)
        aws_session_token: AWS session token for temporary credentials (uses env var if not provided)
        region_name: AWS region (uses env var if not provided)

    Returns:
        boto3.client: Bedrock runtime client
    """
    access_key = aws_access_key_id or os.getenv('AWS_ACCESS_KEY_ID')
    secret_key = aws_secret_access_key or os.getenv('AWS_SECRET_ACCESS_KEY')
    session_token = aws_session_token or os.getenv('AWS_SESSION_TOKEN')
    region = region_name or os.getenv('AWS_REGION') or os.getenv('AWS_DEFAULT_REGION', 'us-east-1')

    if not access_key or not secret_key:
        raise ValueError(
            "AWS credentials not found. Please set AWS_ACCESS_KEY_ID and "
            "AWS_SECRET_ACCESS_KEY in your .env file."
        )

    # Build client kwargs
    client_kwargs = {
        'service_name': 'bedrock-runtime',
        'aws_access_key_id': access_key,
        'aws_secret_access_key': secret_key,
        'region_name': region
    }

    # Add session token if present (for temporary credentials)
    if session_token:
        client_kwargs['aws_session_token'] = session_token

    return boto3.client(**client_kwargs)


def get_bedrock_embeddings(
    model_id: Optional[str] = None,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    aws_session_token: Optional[str] = None,
    region_name: Optional[str] = None
):
    """
    Get Bedrock embeddings model.

    Args:
        model_id: Bedrock embedding model ID (uses env var if not provided)
        aws_access_key_id: AWS access key
        aws_secret_access_key: AWS secret key
        aws_session_token: AWS session token (for temporary credentials)
        region_name: AWS region

    Returns:
        BedrockEmbeddings: Bedrock embeddings instance
    """
    model = model_id or os.getenv('DEFAULT_EMBEDDING_MODEL', 'amazon.titan-embed-text-v2:0')
    access_key = aws_access_key_id or os.getenv('AWS_ACCESS_KEY_ID')
    secret_key = aws_secret_access_key or os.getenv('AWS_SECRET_ACCESS_KEY')
    session_token = aws_session_token or os.getenv('AWS_SESSION_TOKEN')
    region = region_name or os.getenv('AWS_REGION') or os.getenv('AWS_DEFAULT_REGION', 'us-east-1')

    if not access_key or not secret_key:
        raise ValueError(
            "AWS credentials not found. Please set AWS_ACCESS_KEY_ID and "
            "AWS_SECRET_ACCESS_KEY in your .env file."
        )

    return BedrockEmbeddings(
        model_id=model,
        credentials_profile_name=None,
        region_name=region,
        client=get_bedrock_client(access_key, secret_key, session_token, region)
    )


def get_bedrock_llm(
    model_id: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: int = 4096,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    aws_session_token: Optional[str] = None,
    region_name: Optional[str] = None
):
    """
    Get Bedrock LLM for chat/completion.

    Args:
        model_id: Bedrock LLM model ID (uses env var if not provided)
        temperature: Temperature for generation
        max_tokens: Maximum tokens to generate
        aws_access_key_id: AWS access key
        aws_secret_access_key: AWS secret key
        aws_session_token: AWS session token (for temporary credentials)
        region_name: AWS region

    Returns:
        ChatBedrock: Bedrock LLM instance
    """
    model = model_id or os.getenv('DEFAULT_LLM_MODEL', 'anthropic.claude-3-sonnet-20240229-v1:0')
    temp = temperature if temperature is not None else float(os.getenv('DEFAULT_TEMPERATURE', '0.0'))
    access_key = aws_access_key_id or os.getenv('AWS_ACCESS_KEY_ID')
    secret_key = aws_secret_access_key or os.getenv('AWS_SECRET_ACCESS_KEY')
    session_token = aws_session_token or os.getenv('AWS_SESSION_TOKEN')
    region = region_name or os.getenv('AWS_REGION') or os.getenv('AWS_DEFAULT_REGION', 'us-east-1')

    if not access_key or not secret_key:
        raise ValueError(
            "AWS credentials not found. Please set AWS_ACCESS_KEY_ID and "
            "AWS_SECRET_ACCESS_KEY in your .env file."
        )

    return ChatBedrock(
        model_id=model,
        model_kwargs={
            "temperature": temp,
            "max_tokens": max_tokens
        },
        client=get_bedrock_client(access_key, secret_key, session_token, region)
    )


def get_qdrant_client(
    url: Optional[str] = None,
    api_key: Optional[str] = None
):
    """
    Create and return a Qdrant client.

    Args:
        url: Qdrant URL (uses env var if not provided)
        api_key: Qdrant API key (uses env var if not provided)

    Returns:
        QdrantClient: Qdrant client instance
    """
    qdrant_url = url or os.getenv('QDRANT_URL')
    qdrant_api_key = api_key or os.getenv('QDRANT_API_KEY')

    if not qdrant_url or not qdrant_api_key:
        raise ValueError(
            "Qdrant credentials not found. Please set QDRANT_URL and "
            "QDRANT_API_KEY in your .env file."
        )

    return QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key,
        timeout=60
    )


def create_qdrant_collection(
    collection_name: str,
    vector_size: int = 1024,
    distance: Distance = Distance.COSINE,
    client: Optional[QdrantClient] = None
):
    """
    Create a Qdrant collection if it doesn't exist.

    Args:
        collection_name: Name of the collection
        vector_size: Dimension of vectors (1024 for Titan v2, 1536 for Titan v1)
        distance: Distance metric to use
        client: Qdrant client (creates new if not provided)

    Returns:
        bool: True if collection was created, False if it already existed
    """
    if client is None:
        client = get_qdrant_client()

    # Check if collection exists
    collections = client.get_collections().collections
    collection_names = [col.name for col in collections]

    if collection_name in collection_names:
        print(f"✅ Collection '{collection_name}' already exists")
        return False

    # Create collection
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=vector_size,
            distance=distance
        )
    )
    print(f"✅ Created collection '{collection_name}' with vector size {vector_size}")
    return True


def get_qdrant_vectorstore(
    collection_name: str,
    embeddings=None,
    client: Optional[QdrantClient] = None,
    create_if_missing: bool = True
):
    """
    Get a Qdrant vector store for LangChain.

    Args:
        collection_name: Name of the collection
        embeddings: Embeddings model (uses Bedrock if not provided)
        client: Qdrant client (creates new if not provided)
        create_if_missing: Whether to create collection if it doesn't exist

    Returns:
        Qdrant: LangChain Qdrant vector store
    """
    if client is None:
        client = get_qdrant_client()

    if embeddings is None:
        embeddings = get_bedrock_embeddings()

    # Create collection if needed
    if create_if_missing:
        # Determine vector size based on embedding model
        model_id = os.getenv('DEFAULT_EMBEDDING_MODEL', 'amazon.titan-embed-text-v2:0')
        vector_size = 1024 if 'v2' in model_id else 1536

        try:
            create_qdrant_collection(
                collection_name=collection_name,
                vector_size=vector_size,
                client=client
            )
        except Exception as e:
            print(f"ℹ️  Collection creation note: {e}")

    return Qdrant(
        client=client,
        collection_name=collection_name,
        embeddings=embeddings
    )


def test_bedrock_connection():
    """
    Test connection to AWS Bedrock.

    Returns:
        dict: Status of connection test
    """
    try:
        print("🧪 Testing AWS Bedrock connection...")

        # Test embeddings
        embeddings = get_bedrock_embeddings()
        test_text = "This is a test."
        test_embedding = embeddings.embed_query(test_text)

        print(f"✅ Bedrock Embeddings working! Vector dimension: {len(test_embedding)}")

        # Test LLM
        llm = get_bedrock_llm()
        test_response = llm.invoke("Say 'Hello' in one word.")

        print(f"✅ Bedrock LLM working! Response: {test_response.content[:50]}")

        return {
            "embeddings": True,
            "llm": True,
            "embedding_dim": len(test_embedding),
            "status": "success"
        }

    except Exception as e:
        print(f"❌ Bedrock connection failed: {str(e)}")
        return {
            "embeddings": False,
            "llm": False,
            "status": "failed",
            "error": str(e)
        }


def test_qdrant_connection():
    """
    Test connection to Qdrant.

    Returns:
        dict: Status of connection test
    """
    try:
        print("🧪 Testing Qdrant connection...")

        client = get_qdrant_client()
        collections = client.get_collections()

        print(f"✅ Qdrant connected! Found {len(collections.collections)} collection(s)")

        for col in collections.collections:
            print(f"   - {col.name} ({col.vectors_count} vectors)")

        return {
            "connected": True,
            "collections": len(collections.collections),
            "status": "success"
        }

    except Exception as e:
        print(f"❌ Qdrant connection failed: {str(e)}")
        return {
            "connected": False,
            "status": "failed",
            "error": str(e)
        }


def test_full_stack():
    """
    Test the complete RAG stack (Bedrock + Qdrant).

    Returns:
        dict: Combined status of all tests
    """
    print("=" * 60)
    print("🔬 Testing Complete RAG Stack (Bedrock + Qdrant)")
    print("=" * 60)
    print()

    bedrock_status = test_bedrock_connection()
    print()
    qdrant_status = test_qdrant_connection()

    print()
    print("=" * 60)

    if bedrock_status["status"] == "success" and qdrant_status["status"] == "success":
        print("✅ All systems operational! Ready to build RAG applications.")
    else:
        print("⚠️  Some systems failed. Please check your credentials.")

    print("=" * 60)

    return {
        "bedrock": bedrock_status,
        "qdrant": qdrant_status,
        "overall_status": "success" if (
            bedrock_status["status"] == "success" and
            qdrant_status["status"] == "success"
        ) else "failed"
    }


# Convenience function for quick setup
def quick_setup(collection_name: str = "rag_collection"):
    """
    Quick setup that returns LLM, embeddings, and vector store.

    Args:
        collection_name: Name for the Qdrant collection

    Returns:
        tuple: (llm, embeddings, vectorstore)
    """
    print(f"🚀 Quick Setup: Initializing Bedrock + Qdrant...")

    llm = get_bedrock_llm()
    embeddings = get_bedrock_embeddings()
    vectorstore = get_qdrant_vectorstore(collection_name, embeddings)

    print("✅ Setup complete!")
    print(f"   - LLM: {os.getenv('DEFAULT_LLM_MODEL', 'claude-3-sonnet')}")
    print(f"   - Embeddings: {os.getenv('DEFAULT_EMBEDDING_MODEL', 'titan-embed-v2')}")
    print(f"   - Vector Store: Qdrant collection '{collection_name}'")

    return llm, embeddings, vectorstore


if __name__ == "__main__":
    # Run tests if executed directly
    test_full_stack()
