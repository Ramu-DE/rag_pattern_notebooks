# 🔐 Setting Up Your Vector Database Credentials

This guide will help you add your vector database credentials to get started with the RAG Techniques notebooks.

## 📋 Overview

The `.env` file in the project root stores all your API keys and configuration. You need to add your credentials there before running any notebooks.

## 🚀 Quick Setup (5 Minutes)

### Step 1: Open the .env File

```bash
# Use your favorite text editor
nano .env
# or
vim .env
# or
code .env  # if using VS Code
```

### Step 2: Add Your OpenAI API Key (Required)

```bash
# Find this line in .env:
OPENAI_API_KEY=

# Replace with your actual key:
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Get your OpenAI key:** https://platform.openai.com/api-keys

### Step 3: Choose Your Vector Database

You have several options. Pick ONE that works best for you:

## 📊 Vector Database Options

### Option 1: FAISS (Easiest - No Signup Required!) ✅ RECOMMENDED FOR TESTING

**Best for:** Local testing, learning, no cloud setup needed

```bash
VECTOR_DB_PROVIDER=faiss
```

**That's it!** FAISS runs locally, no API keys needed. Perfect for getting started.

**Pros:**
- ✅ No signup required
- ✅ Completely free
- ✅ Fast local performance
- ✅ Great for learning

**Cons:**
- ❌ Not for production
- ❌ No persistence between sessions (unless you save the index)

---

### Option 2: Pinecone (Easy Cloud Option)

**Best for:** Cloud-hosted, managed service, production-ready

**Signup:** https://www.pinecone.io/

**Free tier:** Yes (1 index, 5GB storage)

```bash
PINECONE_API_KEY=pcsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
PINECONE_ENVIRONMENT=us-east1-gcp
PINECONE_INDEX_NAME=rag-techniques
VECTOR_DB_PROVIDER=pinecone
```

**Setup steps:**
1. Sign up at pinecone.io
2. Create a project
3. Copy your API key
4. Note your environment (e.g., us-east1-gcp)
5. Create an index (or the code will create it)

---

### Option 3: Qdrant (Self-Hosted or Cloud)

**Best for:** Self-hosting, advanced features, performance

**Cloud:** https://cloud.qdrant.io/
**Self-hosted:** https://qdrant.tech/documentation/quick-start/

**Free tier:** Yes (1GB on cloud)

```bash
QDRANT_URL=https://xxxxx.us-east-1.aws.cloud.qdrant.io:6333
QDRANT_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
VECTOR_DB_PROVIDER=qdrant
```

---

### Option 4: Weaviate (Self-Hosted or Cloud)

**Best for:** Semantic search, hybrid search, ML models

**Cloud:** https://console.weaviate.cloud/
**Self-hosted:** https://weaviate.io/developers/weaviate/installation

**Free tier:** Yes (sandbox)

```bash
WEAVIATE_URL=https://xxxxx.weaviate.network
WEAVIATE_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
VECTOR_DB_PROVIDER=weaviate
```

---

### Option 5: Milvus / Zilliz Cloud

**Best for:** Large scale, enterprise, advanced features

**Zilliz Cloud:** https://cloud.zilliz.com/
**Self-hosted Milvus:** https://milvus.io/docs

**Free tier:** Yes (on Zilliz Cloud)

```bash
ZILLIZ_CLOUD_URI=https://xxxxx.api.gcp-us-west1.zillizcloud.com
ZILLIZ_CLOUD_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
VECTOR_DB_PROVIDER=milvus
```

---

### Option 6: ChromaDB (Local or Server)

**Best for:** Local development, simple setup

**Docs:** https://www.trychroma.com/

```bash
CHROMA_HOST=localhost
CHROMA_PORT=8000
VECTOR_DB_PROVIDER=chroma
```

**Note:** For local use, ChromaDB needs to be running. Install with: `pip install chromadb`

---

## 🎯 Recommended Setup Based on Your Needs

### For Learning & Testing 🎓
```bash
OPENAI_API_KEY=sk-proj-xxx
VECTOR_DB_PROVIDER=faiss
```
**Time to setup:** 2 minutes | **Cost:** Free

### For Production Apps 🚀
```bash
OPENAI_API_KEY=sk-proj-xxx
PINECONE_API_KEY=pcsk-xxx
PINECONE_ENVIRONMENT=us-east1-gcp
VECTOR_DB_PROVIDER=pinecone
```
**Time to setup:** 10 minutes | **Cost:** Free tier available

### For Self-Hosting ⚙️
```bash
OPENAI_API_KEY=sk-proj-xxx
QDRANT_URL=http://localhost:6333
VECTOR_DB_PROVIDER=qdrant
```
**Time to setup:** 15-20 minutes | **Cost:** Free (self-hosted)

---

## 🔍 Complete .env Example

Here's a complete example for Pinecone + OpenAI:

```bash
# OpenAI (Required)
OPENAI_API_KEY=sk-proj-aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890

# Vector Database - Pinecone
PINECONE_API_KEY=pcsk-1234567890abcdef
PINECONE_ENVIRONMENT=us-east1-gcp
PINECONE_INDEX_NAME=rag-techniques
VECTOR_DB_PROVIDER=pinecone

# Model Configuration (Optional - has defaults)
DEFAULT_LLM_MODEL=gpt-4
DEFAULT_EMBEDDING_MODEL=text-embedding-ada-002
DEFAULT_TEMPERATURE=0.0

# LangChain Tracing (Optional)
LANGCHAIN_TRACING_V2=false
```

---

## ✅ Verify Your Setup

After adding your credentials:

```bash
# Run verification script
python3 verify_setup.py

# Or test in Python
python3 -c "
from utils.env_loader import load_environment, check_required_keys
load_environment()
check_required_keys('OPENAI_API_KEY')
"
```

---

## 🔒 Security Best Practices

1. **Never commit .env to git**
   - It's already in .gitignore ✅

2. **Use environment-specific .env files**
   ```bash
   .env              # Local development
   .env.production   # Production (never commit!)
   .env.template     # Template (safe to commit)
   ```

3. **Rotate keys regularly**
   - Change API keys periodically
   - Revoke unused keys

4. **Use read-only keys when possible**
   - Some vector DBs offer read-only API keys
   - Use them for production queries

---

## 🆘 Troubleshooting

### "API key not found" error

**Check:**
```bash
# Is the key actually set?
cat .env | grep OPENAI_API_KEY

# Restart Jupyter kernel after editing .env
# In Jupyter: Kernel → Restart Kernel
```

### "Vector database connection failed"

**Check:**
1. Is your vector DB instance running?
2. Is the URL correct?
3. Is the API key valid?
4. Try FAISS first to isolate the issue

```bash
# Test with FAISS (no DB needed)
VECTOR_DB_PROVIDER=faiss
```

### "Invalid API key" error

**Check:**
1. No extra spaces: `API_KEY=sk-xxx` (no space before/after =)
2. No quotes needed: `API_KEY=sk-xxx` not `API_KEY="sk-xxx"`
3. Key is complete: OpenAI keys start with `sk-`

---

## 🎓 Additional API Keys (Optional)

Some advanced notebooks may need additional keys:

### Anthropic (for Claude models)
```bash
ANTHROPIC_API_KEY=sk-ant-xxx
```
**Get key:** https://console.anthropic.com/

### Cohere (for embeddings/reranking)
```bash
COHERE_API_KEY=xxx
```
**Get key:** https://dashboard.cohere.com/

### Groq (for fast LLM inference)
```bash
GROQ_API_KEY=gsk_xxx
```
**Get key:** https://console.groq.com/

### HuggingFace (for models)
```bash
HUGGINGFACE_API_KEY=hf_xxx
```
**Get key:** https://huggingface.co/settings/tokens

---

## 📚 Next Steps

Once your credentials are set up:

1. **Verify setup:**
   ```bash
   python3 verify_setup.py
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start Jupyter:**
   ```bash
   jupyter lab
   ```

4. **Open the master index:**
   - Navigate to `INDEX.ipynb`
   - Choose a technique to try

5. **Start with Simple RAG:**
   - Go to `notebooks/simple_rag/simple_rag.ipynb`
   - Run all cells
   - Everything should work! 🎉

---

## 🎉 You're Ready!

Your credentials are now configured and you're ready to explore all 37 RAG techniques!

**Questions?** Check the main [README.md](README.md) or [QUICKSTART.md](QUICKSTART.md)

Happy learning! 🚀
