#!/usr/bin/env python3
"""Test AWS setup for RAG notebooks"""

import json
import sys

print("=" * 70)
print("AWS RAG SETUP TEST")
print("=" * 70)

# Test 1: boto3
print("\n1. Testing boto3...")
try:
    import boto3
    print("   ✓ boto3 imported")
    
    sts = boto3.client('sts', region_name='us-west-2')
    identity = sts.get_caller_identity()
    print(f"   ✓ AWS Account: {identity['Account']}")
    print(f"   ✓ User: {identity['Arn'].split('/')[-1]}")
except Exception as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

# Test 2: Bedrock
print("\n2. Testing Bedrock...")
try:
    bedrock = boto3.client('bedrock', region_name='us-west-2')
    models = bedrock.list_foundation_models()
    
    claude_models = [m for m in models['modelSummaries'] if 'claude' in m['modelId'].lower()]
    titan_models = [m for m in models['modelSummaries'] if 'titan-embed' in m['modelId'].lower()]
    
    print(f"   ✓ Found {len(claude_models)} Claude models")
    print(f"   ✓ Found {len(titan_models)} Titan embedding models")
    
    if claude_models:
        print(f"   ✓ Example: {claude_models[0]['modelId']}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 3: OpenSearch
print("\n3. Testing OpenSearch...")
try:
    import opensearchpy
    print("   ✓ opensearch-py imported")
    
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    print(f"   ✓ Config loaded: {config['collection_name']}")
    print(f"   ✓ Endpoint: {config['endpoint']}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 4: OpenSearch connection
print("\n4. Testing OpenSearch connection...")
try:
    from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
    
    credentials = boto3.Session().get_credentials()
    auth = AWSV4SignerAuth(credentials, 'us-west-2', 'aoss')
    
    host = config['endpoint'].replace('https://', '').replace('http://', '')
    
    client = OpenSearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        timeout=30
    )
    
    info = client.info()
    print(f"   ✓ Connected to OpenSearch")
    print(f"   ✓ Version: {info.get('version', {}).get('number', 'N/A')}")
    
    # List indices
    indices = client.cat.indices(format='json')
    print(f"   ✓ Found {len(indices)} indices")
    
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "=" * 70)
print("SETUP TEST COMPLETE")
print("=" * 70)
