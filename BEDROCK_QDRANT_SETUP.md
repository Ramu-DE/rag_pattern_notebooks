# 🚀 AWS Bedrock + Qdrant Setup Guide

Your project is configured to use:
- **AWS Bedrock** for LLM and Embeddings (Claude 3 Sonnet + Titan Embeddings v2)
- **Qdrant Cloud** for Vector Database (Already configured! ✅)

---

## ✅ What's Already Configured

### Qdrant Cloud (Ready to Use!)
- **Endpoint**: https://3f10b053-66f8-4f2b-9427-6a765e5a2fc8.eu-west-2-0.aws.cloud.qdrant.io:6333
- **Cluster ID**: 3f10b053-66f8-4f2b-9427-6a765e5a2fc8
- **API Key**: Configured in `.env` ✅
- **Region**: EU West 2 (London)

---

## 🔧 What You Need to Add

### AWS Bedrock Credentials

You need to add your AWS credentials to access Bedrock models.

#### Step 1: Get AWS Credentials

**Option A: Use Existing AWS Account**
1. Go to AWS Console: https://console.aws.amazon.com/
2. Navigate to IAM → Users → Your User → Security Credentials
3. Create an Access Key
4. Copy both Access Key ID and Secret Access Key

**Option B: Create New IAM User for Bedrock**
```bash
# Required permissions for the IAM user:
- AmazonBedrockFullAccess
# Or create custom policy with:
- bedrock:InvokeModel
- bedrock:InvokeModelWithResponseStream
```

#### Step 2: Enable Bedrock Models

1. Go to AWS Console → Bedrock
2. Navigate to "Model access" in the left sidebar
3. Click "Manage model access"
4. Enable these models:
   - ✅ **Anthropic Claude 3 Sonnet** (for LLM)
   - ✅ **Amazon Titan Embeddings V2** (for embeddings)
   - ✅ **Anthropic Claude 3 Haiku** (optional, faster/cheaper)
5. Click "Save changes" and wait for approval (usually instant)

#### Step 3: Add Credentials to .env

Open `/workshop/RAG_Techniques_Notebooks/.env` and update:

```bash
# AWS Bedrock Configuration
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_REGION=us-east-1
```

**Important Security Notes:**
- Never commit `.env` to version control (already in .gitignore ✅)
- Use IAM user with minimal required permissions
- Rotate credentials regularly

---

## 🧪 Test Your Setup

### Quick Test

```bash
cd /workshop/RAG_Techniques_Notebooks
python3 -c "from utils.bedrock_helper import test_full_stack; test_full_stack()"
```

This will test:
- ✅ AWS Bedrock connection
- ✅ Embeddings model (Titan v2)
- ✅ LLM model (Claude 3 Sonnet)
- ✅ Qdrant connection
- ✅ Qdrant collections

### Test in Python

```python
from utils.bedrock_helper import test_full_stack

# Run comprehensive test
results = test_full_stack()

# Or test components individually
from utils.bedrock_helper import test_bedrock_connection, test_qdrant_connection

test_bedrock_connection()
test_qdrant_connection()
```

### Test in Jupyter Notebook

Create a test notebook:

```python
# Load environment
from utils.env_loader import load_environment, check_required_keys
load_environment()
check_required_keys('AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'QDRANT_API_KEY')

# Test Bedrock + Qdrant
from utils.bedrock_helper import test_full_stack
test_full_stack()

# If all tests pass, do a quick setup
from utils.bedrock_helper import quick_setup
llm, embeddings, vectorstore = quick_setup("test_collection")

# Test a simple embedding
test_doc = "This is a test document."
test_vector = embeddings.embed_query(test_doc)
print(f"✅ Generated embedding with {len(test_vector)} dimensions")

# Test LLM
response = llm.invoke("What is RAG in AI?")
print(f"✅ LLM Response: {response.content[:100]}...")
```

---

## 📊 Your Current Configuration

### LLM Settings
```bash
Provider: AWS Bedrock
Model: anthropic.claude-3-sonnet-20240229-v1:0
Temperature: 0.0
Region: us-east-1
```

**Claude 3 Sonnet Features:**
- Context window: 200K tokens
- Output: Up to 4K tokens
- Best balance of intelligence, speed, and cost
- Excellent for RAG applications

**Alternative Models** (change in .env):
```bash
# Faster and cheaper
DEFAULT_LLM_MODEL=anthropic.claude-3-haiku-20240307-v1:0

# Most capable (higher cost)
DEFAULT_LLM_MODEL=anthropic.claude-3-5-sonnet-20240620-v1:0

# Amazon's model
DEFAULT_LLM_MODEL=amazon.titan-text-premier-v1:0
```

### Embedding Settings
```bash
Provider: AWS Bedrock
Model: amazon.titan-embed-text-v2:0
Dimensions: 1024
Region: us-east-1
```

**Titan Embeddings V2 Features:**
- Vector dimension: 1024
- Input: Up to 8K tokens
- Optimized for semantic search
- Better than V1 for retrieval tasks

**Alternative Models** (change in .env):
```bash
# Legacy Titan (1536 dimensions)
DEFAULT_EMBEDDING_MODEL=amazon.titan-embed-text-v1

# Cohere (English only, 1024 dimensions)
DEFAULT_EMBEDDING_MODEL=cohere.embed-english-v3

# Cohere (Multilingual, 1024 dimensions)
DEFAULT_EMBEDDING_MODEL=cohere.embed-multilingual-v3
```

### Vector Database Settings
```bash
Provider: Qdrant Cloud
URL: https://3f10b053-66f8-4f2b-9427-6a765e5a2fc8.eu-west-2-0.aws.cloud.qdrant.io:6333
Region: EU West 2 (London)
Status: ✅ Configured and ready
```

---

## 🎯 Quick Start with Bedrock + Qdrant

### Example 1: Simple RAG Pipeline

```python
from utils.bedrock_helper import quick_setup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader

# Initialize components
llm, embeddings, vectorstore = quick_setup("my_documents")

# Load and split documents
loader = TextLoader("../../data/sample.txt")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = text_splitter.split_documents(documents)

# Add to Qdrant
vectorstore.add_documents(chunks)

# Query
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
relevant_docs = retriever.get_relevant_documents("Your question here")

# Generate answer with Claude
from langchain.chains import RetrievalQA

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

result = qa_chain({"query": "Your question here"})
print(result["result"])
```

### Example 2: Direct Usage

```python
from utils.bedrock_helper import (
    get_bedrock_llm,
    get_bedrock_embeddings,
    get_qdrant_vectorstore
)

# Get components
llm = get_bedrock_llm(temperature=0.7)
embeddings = get_bedrock_embeddings()
vectorstore = get_qdrant_vectorstore("my_collection")

# Use them
embedding_vector = embeddings.embed_query("test")
response = llm.invoke("Hello!")
```

---

## 💰 Cost Considerations

### AWS Bedrock Pricing (as of 2024)

**Claude 3 Sonnet:**
- Input: $0.003 per 1K tokens
- Output: $0.015 per 1K tokens
- ~$0.018 per request (avg 1K in + 1K out)

**Claude 3 Haiku (Cheaper):**
- Input: $0.00025 per 1K tokens
- Output: $0.00125 per 1K tokens
- ~$0.00138 per request (87% cheaper!)

**Titan Embeddings V2:**
- $0.0001 per 1K tokens
- Very cost-effective

**Example costs for 1000 RAG queries:**
- Embeddings (1K per query): $0.10
- Claude Sonnet (2K tokens per query): $18
- **Total: ~$18.10**

### Qdrant Cloud Pricing

**Your current tier:** Check your Qdrant console
- Free tier: 1GB storage, 1 node
- Paid: Scales with storage and throughput

---

## 🔒 Security Best Practices

### For AWS Credentials

1. **Never hardcode credentials** ✅ (Using .env)
2. **Use IAM roles** when possible (EC2/Lambda)
3. **Rotate keys regularly** (every 90 days)
4. **Minimal permissions** (only Bedrock access)
5. **Monitor usage** in AWS CloudWatch

### For Qdrant

1. **API key is secured** ✅ (In .env, gitignored)
2. **Use HTTPS** ✅ (Already configured)
3. **Rotate API keys** periodically
4. **Monitor access** in Qdrant console

---

## 🐛 Troubleshooting

### "AccessDeniedException" from Bedrock

**Cause:** IAM user lacks permissions or models not enabled

**Fix:**
1. Check IAM permissions include `AmazonBedrockFullAccess`
2. Go to Bedrock console → Model access
3. Enable Claude 3 Sonnet and Titan Embeddings
4. Wait a few minutes for activation

### "Invalid region" error

**Fix:** Check your AWS region supports Bedrock:
```bash
# Supported regions:
us-east-1 (N. Virginia) ✅
us-west-2 (Oregon) ✅
eu-west-1 (Ireland) ✅
ap-southeast-1 (Singapore) ✅
```

### Qdrant connection timeout

**Fix:**
1. Check internet connection
2. Verify URL includes port `:6333`
3. Check API key is correct (no spaces)
4. Verify cluster is active in Qdrant console

### "Collection not found" error

**Fix:** The collection will be created automatically on first use.
Or create manually:
```python
from utils.bedrock_helper import create_qdrant_collection
create_qdrant_collection("my_collection", vector_size=1024)
```

### Embedding dimension mismatch

**Cause:** Collection created with wrong vector size

**Fix:**
- Titan V2: 1024 dimensions
- Titan V1: 1536 dimensions
- Cohere: 1024 dimensions

Delete and recreate collection with correct size:
```python
from utils.bedrock_helper import get_qdrant_client

client = get_qdrant_client()
client.delete_collection("collection_name")

# Recreate with correct size
from utils.bedrock_helper import create_qdrant_collection
create_qdrant_collection("collection_name", vector_size=1024)
```

---

## 📚 Using with RAG Notebooks

All 37 notebooks will automatically use Bedrock + Qdrant once configured!

### Notebooks that work great with Bedrock:

1. **simple_rag** - Perfect introduction
2. **semantic_chunking** - Titan embeddings excel here
3. **reranking** - Claude 3 is excellent at reranking
4. **CRAG** - Claude's reasoning shines
5. **graph_rag** - Works seamlessly with Qdrant
6. **Agentic_RAG** - Claude 3 as orchestrator

### Notebooks requiring adjustments:

Some notebooks have hardcoded OpenAI calls. To use Bedrock:

```python
# Instead of:
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Use:
from utils.bedrock_helper import get_bedrock_llm, get_bedrock_embeddings

llm = get_bedrock_llm()
embeddings = get_bedrock_embeddings()
```

---

## 🎓 Next Steps

1. **Add AWS credentials** to `.env`
2. **Run test**: `python3 -c "from utils.bedrock_helper import test_full_stack; test_full_stack()"`
3. **Try simple_rag**: Open `notebooks/simple_rag/simple_rag.ipynb`
4. **Explore advanced**: Graph RAG, Agentic RAG work great with Claude 3

---

## 📞 Support Resources

- **AWS Bedrock Docs**: https://docs.aws.amazon.com/bedrock/
- **Qdrant Docs**: https://qdrant.tech/documentation/
- **Claude 3 Guide**: https://docs.anthropic.com/claude/docs
- **Your Qdrant Console**: https://cloud.qdrant.io/

---

## ✅ Configuration Checklist

- [x] Qdrant credentials configured ✅
- [ ] AWS Access Key ID added to .env
- [ ] AWS Secret Access Key added to .env
- [ ] Bedrock models enabled in AWS Console
- [ ] Tested connection with `test_full_stack()`
- [ ] Ran first notebook successfully

---

**Once AWS credentials are added, you're ready to build production-grade RAG applications with Bedrock + Qdrant!** 🚀
