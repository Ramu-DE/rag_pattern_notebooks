# 📦 Installation & Testing Guide

Complete guide to install dependencies and test your AWS Bedrock + Qdrant setup.

---

## ✅ Current Status

Your project is configured with:
- **AWS Credentials**: ✅ Added to `.env` (temporary session credentials)
- **Qdrant Credentials**: ✅ Pre-configured
- **Region**: us-west-2
- **Dependencies**: ⏳ Need to be installed

**⚠️ Note**: Your AWS credentials are temporary (session-based) and will expire. When they expire, you'll need to get new ones.

---

## 🚀 Quick Install & Test (3 Steps)

### Step 1: Install Dependencies

```bash
cd /workshop/RAG_Techniques_Notebooks

# Option A: Using pip (recommended)
pip install -r requirements.txt

# Option B: Using pip with virtual environment (best practice)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Expected time**: 5-10 minutes depending on your connection

### Step 2: Enable Bedrock Models

Before testing, you must enable models in AWS Console:

1. Go to: https://console.aws.amazon.com/bedrock/
2. Click "Model access" in the left sidebar
3. Click "Manage model access"
4. Enable these models:
   - ☑ **Anthropic Claude 3 Sonnet**
   - ☑ **Amazon Titan Embeddings V2**
5. Click "Save changes"

**Note**: Approval is usually instant, but can take a few minutes.

### Step 3: Test Your Setup

```bash
# Quick test
python3 quick_test.py

# Or use the helper directly
python3 -c "from utils.bedrock_helper import test_full_stack; test_full_stack()"
```

If successful, you should see:
```
✅ All systems operational!
🚀 You're ready to build RAG applications!
```

---

## 📋 Detailed Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Internet connection
- AWS account with Bedrock access

### Install All Dependencies

The `requirements.txt` includes 65+ packages:

**Core Components**:
- `python-dotenv` - Environment management
- `langchain`, `langchain-core`, `langchain-community` - LangChain framework
- `langchain-aws` - AWS Bedrock integration
- `boto3`, `botocore` - AWS SDK
- `qdrant-client` - Qdrant vector database

**Optional Components**:
- Alternative LLM providers (OpenAI, Anthropic, Cohere, Groq)
- Alternative vector DBs (FAISS, Pinecone, Weaviate, Milvus, ChromaDB)
- ML libraries (transformers, sentence-transformers, torch)
- Jupyter (notebook, jupyterlab)

### Installation Options

#### Option 1: Simple Install
```bash
pip install -r requirements.txt
```

#### Option 2: Virtual Environment (Recommended)
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

#### Option 3: Install Core Dependencies Only
If you want to start quickly with minimal packages:

```bash
pip install python-dotenv langchain langchain-aws langchain-community \
    boto3 qdrant-client jupyter
```

---

## 🧪 Testing Your Setup

### Test 1: Environment Loading

```bash
python3 -c "
from utils.env_loader import load_environment, check_required_keys
load_environment()
check_required_keys('AWS_ACCESS_KEY_ID', 'QDRANT_API_KEY')
"
```

**Expected output**:
```
✅ Environment loaded from: /workshop/RAG_Techniques_Notebooks/.env
✅ AWS_ACCESS_KEY_ID: Set
✅ QDRANT_API_KEY: Set
✅ All required API keys are configured!
```

### Test 2: Qdrant Connection

```bash
python3 -c "
from utils.bedrock_helper import test_qdrant_connection
test_qdrant_connection()
"
```

**Expected output**:
```
🧪 Testing Qdrant connection...
✅ Qdrant connected! Found X collection(s)
```

### Test 3: Bedrock Connection

```bash
python3 -c "
from utils.bedrock_helper import test_bedrock_connection
test_bedrock_connection()
"
```

**Expected output**:
```
🧪 Testing AWS Bedrock connection...
✅ Bedrock Embeddings working! Vector dimension: 1024
✅ Bedrock LLM working! Response: Hello
```

### Test 4: Complete Stack

```bash
python3 quick_test.py
```

Or:

```bash
python3 -c "from utils.bedrock_helper import test_full_stack; test_full_stack()"
```

**Expected output**:
```
🔬 Testing Complete RAG Stack (Bedrock + Qdrant)
✅ Bedrock Embeddings working! Vector dimension: 1024
✅ Bedrock LLM working!
✅ Qdrant connected! Found X collection(s)
✅ All systems operational! Ready to build RAG applications.
```

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'dotenv'"

**Solution**: Install dependencies
```bash
pip install python-dotenv
# or install all
pip install -r requirements.txt
```

### Issue: "ModuleNotFoundError: No module named 'langchain_aws'"

**Solution**: Install AWS Bedrock integration
```bash
pip install langchain-aws boto3
```

### Issue: "AccessDeniedException" from Bedrock

**Cause**: Models not enabled in AWS Console

**Solution**:
1. Go to AWS Console → Bedrock → Model Access
2. Enable Claude 3 Sonnet and Titan Embeddings V2
3. Wait 1-2 minutes for activation
4. Try again

### Issue: "ExpiredTokenException" or "InvalidSessionToken"

**Cause**: Your temporary AWS credentials have expired

**Solution**: Get new temporary credentials:
1. Run your AWS authentication command again
2. Export the new credentials
3. Update `.env` with new values
4. Retry

**Note**: Session tokens typically last 1-12 hours depending on how they were created.

### Issue: "Connection timeout" to Qdrant

**Cause**: Network issue or incorrect URL

**Solution**:
1. Check internet connection
2. Verify Qdrant URL in `.env` includes `:6333` port
3. Check Qdrant cluster is active in console

### Issue: "Invalid model ID" or "Model not found"

**Cause**: Model ID incorrect or not available in your region

**Solution**:
1. Check you're using `us-west-2` region (your current region)
2. Verify model IDs in `.env`:
   - `anthropic.claude-3-sonnet-20240229-v1:0`
   - `amazon.titan-embed-text-v2:0`
3. Some models may not be available in all regions

### Issue: Installation taking too long

**Solution**: Install core packages only first:
```bash
pip install python-dotenv langchain-aws boto3 qdrant-client
```

Then test, and install remaining packages later if needed.

---

## ✅ Verification Checklist

- [ ] Python 3.10+ installed: `python3 --version`
- [ ] Dependencies installed: `pip list | grep langchain`
- [ ] Environment loaded: `python3 -c "from utils.env_loader import load_environment; load_environment()"`
- [ ] AWS credentials working: `python3 -c "import boto3; boto3.client('bedrock-runtime', region_name='us-west-2').list_foundation_models()"`
- [ ] Bedrock models enabled in AWS Console
- [ ] Qdrant connection working: `python3 -c "from utils.bedrock_helper import test_qdrant_connection; test_qdrant_connection()"`
- [ ] Complete stack tested: `python3 quick_test.py`

---

## 🎓 Next Steps After Successful Installation

### 1. Start Jupyter Lab

```bash
jupyter lab
```

### 2. Run Test Notebook

Open and run: `TEST_BEDROCK_QDRANT.ipynb`

This notebook will:
- Verify your complete setup
- Test embeddings and LLM
- Create a sample collection
- Run a complete RAG pipeline
- Answer questions using Claude 3

### 3. Try Your First RAG Technique

Navigate to: `notebooks/simple_rag/simple_rag.ipynb`

This is the perfect starting point to learn RAG basics.

### 4. Explore More Techniques

Use `INDEX.ipynb` to navigate all 37 RAG techniques.

---

## 📚 Useful Commands

### Check Installation
```bash
# Check Python version
python3 --version

# Check installed packages
pip list | grep -E "(langchain|boto3|qdrant)"

# Check specific package
pip show langchain-aws
```

### Test Components
```bash
# Test environment
python3 -c "from utils.env_loader import load_environment; load_environment()"

# Test Bedrock
python3 -c "from utils.bedrock_helper import test_bedrock_connection; test_bedrock_connection()"

# Test Qdrant
python3 -c "from utils.bedrock_helper import test_qdrant_connection; test_qdrant_connection()"

# Test everything
python3 quick_test.py
```

### Update Packages
```bash
pip install --upgrade -r requirements.txt
```

---

## 💡 Pro Tips

1. **Use virtual environment**: Keeps dependencies isolated
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install in stages**: Install core packages first, test, then install optional ones

3. **Check AWS quotas**: Make sure you have Bedrock access in us-west-2 region

4. **Monitor costs**: Use AWS CloudWatch to monitor Bedrock usage

5. **Session tokens expire**: Temporary credentials need to be refreshed regularly

---

## 🔄 When Your Credentials Expire

Your current credentials are temporary (session-based). When they expire:

### Symptoms:
- `ExpiredTokenException` errors
- `InvalidSessionToken` errors
- Tests that worked before now fail

### Solution:
1. Get new temporary credentials from your AWS authentication method
2. Update `.env` file with new values:
   ```bash
   AWS_ACCESS_KEY_ID=new_key_here
   AWS_SECRET_ACCESS_KEY=new_secret_here
   AWS_SESSION_TOKEN=new_token_here
   ```
3. Restart Jupyter kernel if running
4. Tests should work again

---

## 🎉 Success Criteria

You'll know everything is working when:

1. ✅ `pip list` shows all required packages
2. ✅ `python3 quick_test.py` passes all tests
3. ✅ `TEST_BEDROCK_QDRANT.ipynb` runs without errors
4. ✅ You can run a simple RAG query and get an answer

---

## 📞 Need Help?

If you're still having issues:

1. **Check AWS Console**: Verify Bedrock models are enabled
2. **Check credentials**: Make sure they haven't expired
3. **Read error messages**: They usually indicate the exact problem
4. **Review documentation**: See `BEDROCK_QDRANT_SETUP.md` for more details

---

**Ready to install?** Run: `pip install -r requirements.txt` then `python3 quick_test.py`

Let's build amazing RAG applications! 🚀
