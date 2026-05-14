# 👋 START HERE - RAG Techniques Notebooks

Welcome! This is your complete guide to 37 advanced RAG (Retrieval-Augmented Generation) techniques.

---

## ⚡ Super Quick Start (5 Minutes)

### 1️⃣ Add Your API Key

Open the `.env` file and add your OpenAI key:

```bash
OPENAI_API_KEY=sk-proj-your-actual-key-here
VECTOR_DB_PROVIDER=faiss
```

**Don't have an OpenAI key?** Get one at: https://platform.openai.com/api-keys

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Start Jupyter

```bash
jupyter lab
```

### 4️⃣ Try Your First Notebook

Open: `notebooks/simple_rag/simple_rag.ipynb`

Click "Run All Cells" and watch it work! 🎉

---

## 📚 What's Inside?

This project contains **37 fully functional RAG technique notebooks**, including:

- ✅ **Simple RAG** - Start here to learn basics
- ✅ **Graph RAG** - Knowledge graph integration
- ✅ **Agentic RAG** - LLM agent orchestration
- ✅ **CRAG** - Self-correcting retrieval
- ✅ **Multimodal RAG** - Images + text
- ✅ **35+ more techniques!**

Each technique is in its own folder with:
- Fully functional Jupyter notebook
- Individual README
- Shared data and utilities

---

## 📖 Documentation Guide

We have several docs - here's when to use each:

| Document | When to Read |
|----------|-------------|
| **START_HERE.md** (this file) | Right now! Your entry point |
| **[QUICKSTART.md](QUICKSTART.md)** | Quick 5-minute setup guide |
| **[SETUP_CREDENTIALS.md](SETUP_CREDENTIALS.md)** | Detailed guide for vector DB setup |
| **[README.md](README.md)** | Complete project documentation |
| **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** | What was created & statistics |
| **[INDEX.ipynb](INDEX.ipynb)** | Interactive notebook navigator |

---

## 🎯 Choose Your Path

### 🌱 I'm New to RAG
Start here:
1. **Read**: [QUICKSTART.md](QUICKSTART.md)
2. **Configure**: Add OpenAI key to `.env`
3. **Run**: `notebooks/simple_rag/simple_rag.ipynb`
4. **Next**: Try `choose_chunk_size` and `reranking`

### 🚀 I'm Ready to Build Production Systems
Jump to:
1. **[SETUP_CREDENTIALS.md](SETUP_CREDENTIALS.md)** - Configure production vector DB
2. **`notebooks/reliable_rag/`** - Production patterns
3. **`notebooks/adaptive_retrieval/`** - Smart retrieval
4. **`notebooks/CRAG/`** - Self-correcting RAG

### 🔬 I Want Advanced Techniques
Explore:
1. **`notebooks/graph_rag/`** - Knowledge graphs
2. **`notebooks/Agentic_RAG/`** - Agent orchestration
3. **`notebooks/RAPTOR/`** - Recursive processing
4. **`notebooks/multi_model_rag_with_colpali/`** - Multimodal

### 📊 I Work With Structured Data
Check out:
1. **`notebooks/simple_csv_rag/`** - CSV/tabular data
2. **`notebooks/json_rag/`** - JSON structures
3. **`notebooks/graph_rag/`** - Graph databases

---

## 🔧 Setup Requirements

### Minimum Setup (For Learning)
```bash
# In .env file:
OPENAI_API_KEY=sk-proj-xxx
VECTOR_DB_PROVIDER=faiss
```
**Time:** 2 minutes | **Cost:** Free (uses local FAISS)

### Production Setup (For Real Apps)
```bash
# In .env file:
OPENAI_API_KEY=sk-proj-xxx
PINECONE_API_KEY=pcsk-xxx
PINECONE_ENVIRONMENT=us-east1-gcp
VECTOR_DB_PROVIDER=pinecone
```
**Time:** 10 minutes | **Cost:** Free tier available

See **[SETUP_CREDENTIALS.md](SETUP_CREDENTIALS.md)** for detailed instructions.

---

## ✅ Verify Your Setup

Run the verification script:

```bash
python3 verify_setup.py
```

You should see:
- ✅ 37/37 notebooks found
- ✅ All utilities in place
- ⚠️ .env needs your keys (expected until you add them)

---

## 🎓 Learning Path Recommendations

### Week 1: Foundations (5-7 hours)
- Day 1-2: `simple_rag` + `simple_rag_with_llamaindex`
- Day 3: `choose_chunk_size` + `semantic_chunking`
- Day 4: `reranking` + `fusion_retrieval`
- Day 5: `contextual_compression`

### Week 2: Advanced Patterns (6-8 hours)
- Day 1: `query_transformations` + `HyDE`
- Day 2: `adaptive_retrieval` + `hierarchical_indices`
- Day 3: `CRAG` + `self_rag`
- Day 4: `reliable_rag`
- Day 5: Practice & experimentation

### Week 3: Specialized Techniques (8-10 hours)
- Day 1-2: `graph_rag` + `Microsoft_GraphRag`
- Day 3: `Agentic_RAG`
- Day 4: `RAPTOR` + `memorag`
- Day 5: `multi_model_rag_with_colpali`

---

## 🗺️ Project Structure

```
RAG_Techniques_Notebooks/
├── START_HERE.md           ← You are here!
├── .env                    ← Add your API keys here
├── INDEX.ipynb             ← Interactive navigator
├── notebooks/              ← 37 technique folders
│   ├── simple_rag/
│   ├── graph_rag/
│   ├── Agentic_RAG/
│   └── ...34 more
├── utils/                  ← Shared utilities
├── data/                   ← Sample data files
└── images/                 ← Diagrams & visualizations
```

---

## 🚨 Common Issues & Quick Fixes

### ❌ "OpenAI API key not found"
**Fix:** Edit `.env` and add: `OPENAI_API_KEY=sk-proj-your-key`
Then restart Jupyter kernel.

### ❌ "No module named 'dotenv'"
**Fix:** Run `pip install python-dotenv`

### ❌ Import errors
**Fix:** Run `pip install -r requirements.txt`

### ❌ "Vector database connection failed"
**Fix:** Start with FAISS (no connection needed):
```bash
VECTOR_DB_PROVIDER=faiss
```

### ❌ Notebook cells fail
**Fix:** 
1. Check `.env` has your OpenAI key
2. Restart Jupyter kernel
3. Run cells from top to bottom

---

## 🎯 What Makes This Project Special?

### ✅ Centralized Configuration
- Single `.env` file for all notebooks
- No hardcoded API keys
- Easy to switch vector databases

### ✅ Fully Functional
- All 37 notebooks work out of the box
- Automatic environment loading
- Shared resources (data, images, utilities)

### ✅ Well Organized
- Each technique in its own folder
- Individual README files
- Consistent structure

### ✅ Production Ready
- Support for 6 vector databases
- Proper error handling
- Security best practices

---

## 🔐 Security Note

⚠️ **IMPORTANT:** Never commit your `.env` file to git!

It's already in `.gitignore` to protect your API keys.

---

## 📞 Getting Help

### For Setup Issues:
1. Read [QUICKSTART.md](QUICKSTART.md)
2. Check [SETUP_CREDENTIALS.md](SETUP_CREDENTIALS.md)
3. Run `python3 verify_setup.py`

### For Technique Questions:
1. Open the technique's folder
2. Read its README.md
3. Check the notebook itself (has explanations)

### For Errors:
1. Restart Jupyter kernel
2. Check `.env` configuration
3. Verify all dependencies installed

---

## 🚀 Next Steps - Do This Now!

1. **[ ] Edit `.env`** - Add your OpenAI API key
2. **[ ] Install packages** - Run `pip install -r requirements.txt`
3. **[ ] Start Jupyter** - Run `jupyter lab`
4. **[ ] Open INDEX.ipynb** - Navigate all techniques
5. **[ ] Try simple_rag** - Run your first notebook

---

## 💡 Pro Tips

1. **Start with FAISS** - No vector DB signup needed for learning
2. **Use INDEX.ipynb** - Interactive way to explore all techniques
3. **Read technique READMEs** - Each folder has usage tips
4. **Restart kernel after .env changes** - Jupyter needs a restart
5. **One technique at a time** - Master basics before advanced

---

## 🎉 You're Ready!

Everything is set up. Just add your OpenAI key to `.env` and start exploring!

**Recommended first notebook:** `notebooks/simple_rag/simple_rag.ipynb`

**Have questions?** Check the documentation files listed above.

**Ready to start?** Open [INDEX.ipynb](INDEX.ipynb) in Jupyter Lab!

---

## 📊 Quick Stats

- ✅ 37 RAG techniques
- ✅ 37 Jupyter notebooks
- ✅ 61 Python dependencies
- ✅ 6 vector databases supported
- ✅ 100% ready to use

---

**Let's build something amazing with RAG!** 🚀

