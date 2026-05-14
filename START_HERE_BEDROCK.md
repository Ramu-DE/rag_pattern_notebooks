# 🚀 START HERE - Bedrock + Qdrant Configuration

## ✅ Your Configuration

Your RAG Techniques project is configured with:

- **LLM**: AWS Bedrock (Claude 3 Sonnet)
- **Embeddings**: AWS Bedrock (Titan Embeddings V2)
- **Vector Database**: Qdrant Cloud ✅ **Already Configured!**

---

## 🎯 Quick Start (3 Steps)

### Step 1: Add AWS Credentials (Required)

Edit the `.env` file and add your AWS credentials:

```bash
cd /workshop/RAG_Techniques_Notebooks
nano .env  # or use your editor
```

Add these lines:
```bash
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=us-east-1
```

**Don't have AWS credentials?** See [BEDROCK_QDRANT_SETUP.md](BEDROCK_QDRANT_SETUP.md) for detailed instructions.

### Step 2: Enable Bedrock Models

1. Go to AWS Console → Bedrock → Model Access
2. Enable these models:
   - ✅ Anthropic Claude 3 Sonnet
   - ✅ Amazon Titan Embeddings V2
3. Save (usually instant approval)

### Step 3: Install & Test

```bash
# Install dependencies
pip install -r requirements.txt

# Test your setup
python3 -c "from utils.bedrock_helper import test_full_stack; test_full_stack()"

# If successful, start Jupyter
jupyter lab
```

---

## 🧪 Test Notebook

Open `TEST_BEDROCK_QDRANT.ipynb` to verify everything works!

This notebook tests:
- ✅ AWS Bedrock connection
- ✅ Claude 3 Sonnet LLM
- ✅ Titan Embeddings V2
- ✅ Qdrant Cloud connection
- ✅ Complete RAG pipeline

---

## 📊 What's Configured

### ✅ Qdrant Cloud (Ready!)
- **Status**: ✅ Configured and ready to use
- **Endpoint**: https://3f10b053-66f8-4f2b-9427-6a765e5a2fc8.eu-west-2-0.aws.cloud.qdrant.io:6333
- **Region**: EU West 2 (London)
- **Credentials**: Already in `.env` file

### ⏳ AWS Bedrock (Needs Your Credentials)
- **LLM Model**: Claude 3 Sonnet
- **Embedding Model**: Titan Embeddings V2 (1024 dims)
- **Region**: us-east-1 (configurable)
- **Credentials**: Need to be added to `.env`

---

## 🎓 Your First RAG Application

Once configured, try this simple example:

```python
from utils.bedrock_helper import quick_setup
from langchain.schema import Document

# Initialize everything
llm, embeddings, vectorstore = quick_setup("my_collection")

# Add a document
docs = [Document(page_content="RAG is awesome!")]
vectorstore.add_documents(docs)

# Query
retriever = vectorstore.as_retriever()
results = retriever.get_relevant_documents("What is RAG?")

# Generate answer
from langchain.chains import RetrievalQA
qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
answer = qa({"query": "What is RAG?"})
print(answer["result"])
```

---

## 📚 Documentation

- **Quick Setup**: [BEDROCK_QDRANT_SETUP.md](BEDROCK_QDRANT_SETUP.md) ← Read this for detailed AWS setup
- **Complete Guide**: [README.md](README.md)
- **Quick Start**: [QUICKSTART.md](QUICKSTART.md)
- **Test Notebook**: [TEST_BEDROCK_QDRANT.ipynb](TEST_BEDROCK_QDRANT.ipynb)

---

## 🏗️ Project Structure

```
RAG_Techniques_Notebooks/
├── .env                           ← ADD YOUR AWS CREDENTIALS HERE
├── TEST_BEDROCK_QDRANT.ipynb     ← START WITH THIS TEST
├── BEDROCK_QDRANT_SETUP.md       ← DETAILED SETUP GUIDE
├── notebooks/                     ← 37 RAG techniques
│   ├── simple_rag/               ← Try this first
│   ├── graph_rag/                ← Great with Claude 3
│   └── Agentic_RAG/              ← Claude as orchestrator
└── utils/
    ├── bedrock_helper.py         ← Bedrock + Qdrant utilities
    └── env_loader.py             ← Environment management
```

---

## 💰 Cost Estimate

For 1000 RAG queries (typical learning session):

- **Embeddings**: ~$0.10 (Titan V2)
- **LLM**: ~$18 (Claude 3 Sonnet, 2K tokens/query)
- **Vector DB**: Free tier on Qdrant
- **Total**: ~$18.10

**Want cheaper?** Use Claude 3 Haiku (87% cheaper!):
```bash
DEFAULT_LLM_MODEL=anthropic.claude-3-haiku-20240307-v1:0
```

---

## 🐛 Troubleshooting

### "AccessDeniedException" from Bedrock
1. Check IAM permissions include `AmazonBedrockFullAccess`
2. Enable models in Bedrock console → Model access

### "Qdrant connection failed"
- Qdrant is already configured! ✅
- Check internet connection if issues persist

### "Invalid credentials"
- Verify AWS keys in `.env` have no extra spaces
- Format: `AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE`
- No quotes needed

---

## ✅ Configuration Checklist

- [x] Qdrant credentials configured ✅
- [ ] AWS Access Key added to `.env`
- [ ] AWS Secret Key added to `.env`
- [ ] Bedrock models enabled in AWS Console
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Tested with: `TEST_BEDROCK_QDRANT.ipynb`

---

## 🎯 Next Steps

1. **Add AWS credentials** to `.env`
2. **Enable Bedrock models** in AWS Console
3. **Test setup**: Run `TEST_BEDROCK_QDRANT.ipynb`
4. **Start learning**: Try `notebooks/simple_rag/`

---

## 🌟 Why This Stack?

### AWS Bedrock
- ✅ Managed service (no infrastructure)
- ✅ Claude 3 Sonnet (excellent reasoning)
- ✅ Titan Embeddings V2 (optimized for retrieval)
- ✅ Pay per use (no idle costs)
- ✅ Enterprise-grade security

### Qdrant Cloud
- ✅ Fully managed vector database
- ✅ High-performance search
- ✅ Production-ready
- ✅ Already configured for you!

### Combined
- ✅ Production-grade stack
- ✅ Scalable architecture
- ✅ Cost-effective
- ✅ Easy to use

---

## 📞 Need Help?

1. **Detailed Setup**: [BEDROCK_QDRANT_SETUP.md](BEDROCK_QDRANT_SETUP.md)
2. **AWS Docs**: https://docs.aws.amazon.com/bedrock/
3. **Qdrant Docs**: https://qdrant.tech/documentation/
4. **Test Notebook**: `TEST_BEDROCK_QDRANT.ipynb`

---

## 🚀 Ready?

Once you add AWS credentials to `.env`:

```bash
# Test
python3 -c "from utils.bedrock_helper import test_full_stack; test_full_stack()"

# Start Jupyter
jupyter lab

# Open
TEST_BEDROCK_QDRANT.ipynb
```

**Let's build amazing RAG applications with Claude 3 + Qdrant!** 🎉
