# 🚀 Quick Start Guide - RAG Techniques Notebooks

Get up and running in 5 minutes!

## Step 1: Install Dependencies (2 minutes)

```bash
# Navigate to project directory
cd RAG_Techniques_Notebooks

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Install packages
pip install -r requirements.txt
```

## Step 2: Configure API Keys (2 minutes)

```bash
# Copy template
cp .env.template .env

# Edit .env file
nano .env  # or use your favorite editor
```

**Minimum required:**
```bash
OPENAI_API_KEY=sk-proj-your-actual-key-here
VECTOR_DB_PROVIDER=faiss  # Use FAISS for local testing (no DB needed)
```

**For cloud vector DB (optional):**
```bash
# Choose ONE of these:

# Pinecone
PINECONE_API_KEY=your-key
PINECONE_ENVIRONMENT=us-east1-gcp
VECTOR_DB_PROVIDER=pinecone

# OR Qdrant
QDRANT_URL=https://your-instance.qdrant.tech
QDRANT_API_KEY=your-key
VECTOR_DB_PROVIDER=qdrant

# OR Weaviate
WEAVIATE_URL=https://your-instance.weaviate.network
WEAVIATE_API_KEY=your-key
VECTOR_DB_PROVIDER=weaviate
```

## Step 3: Start Jupyter (1 minute)

```bash
jupyter lab
```

## Step 4: Run Your First Notebook (30 seconds)

1. Navigate to: `notebooks/simple_rag/`
2. Open: `simple_rag.ipynb`
3. Click "Run All Cells" (or press Shift+Enter through each cell)

That's it! 🎉

## What Happens in Each Notebook?

Every notebook automatically:

1. **Loads your .env configuration** ✅
2. **Checks your API keys** ✅
3. **Sets up paths to shared data** ✅
4. **Imports helper functions** ✅
5. **Displays your current config** ✅

You just focus on the RAG technique!

## Troubleshooting

### "No module named 'dotenv'"
```bash
pip install python-dotenv
```

### "OpenAI API key not found"
1. Open `.env` file
2. Make sure `OPENAI_API_KEY=sk-proj-...` has your actual key
3. Restart Jupyter kernel: Kernel → Restart Kernel

### "Permission denied" on .env
```bash
chmod 600 .env
```

### Import errors
```bash
pip install -r requirements.txt --upgrade
```

## Next Steps

### Beginner Path 🌱
1. `simple_rag` - Understand the basics
2. `choose_chunk_size` - Learn about chunking
3. `reranking` - Improve retrieval quality
4. `fusion_retrieval` - Combine multiple approaches

### Intermediate Path 🚀
1. `contextual_compression` - Optimize context
2. `adaptive_retrieval` - Smart retrieval
3. `CRAG` - Self-correcting RAG
4. `self_rag` - Self-reflecting RAG

### Advanced Path 🔥
1. `Agentic_RAG` - Agent-based orchestration
2. `graph_rag` - Knowledge graph integration
3. `RAPTOR` - Recursive processing
4. `multi_model_rag_with_colpali` - Multimodal RAG

## Pro Tips 💡

1. **Start with FAISS** - No cloud DB setup needed
   ```bash
   VECTOR_DB_PROVIDER=faiss
   ```

2. **Use LangChain tracing** - Debug your chains
   ```bash
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_API_KEY=your-langchain-key
   ```

3. **Test with smaller models first**
   ```bash
   DEFAULT_LLM_MODEL=gpt-3.5-turbo  # Cheaper for testing
   ```

4. **Keep a notebook open** for your `.env` config:
   ```python
   from utils.env_loader import display_config
   display_config()
   ```

## Common Workflows

### Testing Locally
```bash
VECTOR_DB_PROVIDER=faiss
OPENAI_API_KEY=sk-proj-xxx
```
✅ No vector DB signup needed!

### Production Setup
```bash
VECTOR_DB_PROVIDER=pinecone  # or qdrant, weaviate
PINECONE_API_KEY=xxx
OPENAI_API_KEY=sk-proj-xxx
```

### Experimenting with Models
```bash
# In .env, try different models:
DEFAULT_LLM_MODEL=gpt-4-turbo-preview
DEFAULT_EMBEDDING_MODEL=text-embedding-3-large
```

## Need Help?

1. Check the main [README.md](README.md)
2. Look at technique-specific README in each folder
3. Review the `.env.template` for all options
4. Run environment diagnostics:
   ```python
   from utils.env_loader import check_required_keys, display_config
   check_required_keys('OPENAI_API_KEY')
   display_config()
   ```

---

**You're all set!** Pick a technique and start exploring! 🚀

Remember: Start simple (`simple_rag`), then gradually move to advanced techniques.
