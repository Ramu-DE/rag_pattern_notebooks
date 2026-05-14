# 🧪 Comprehensive Testing Guide

## ✅ Validation Results

**All 37 notebooks have been structurally validated!**

- ✅ **Valid notebooks**: 37/37 (100%)
- ✅ **Environment setup**: 37/37 have proper env loading
- ✅ **JSON structure**: All valid
- ✅ **Integrity**: All required fields present

---

## 📊 Testing Strategy

Since testing all 37 notebooks with live API calls would:
- Take 3-5 hours
- Cost $50-100 in API calls
- Require active AWS credentials

I've created a **multi-level testing approach**:

---

## Level 1: Structure Validation ✅ **COMPLETE**

**Already Done!** All notebooks validated.

```bash
python3 validate_notebooks.py
```

**Results**: 37/37 notebooks pass structural validation

---

## Level 2: Quick Smoke Test (Recommended)

Test first 3 notebooks to verify the setup works:

```bash
# Install dependencies first
pip install -r requirements.txt

# Enable Bedrock models in AWS Console
# Then run quick test:
python3 test_notebooks.py --quick
```

This will test:
1. `Agentic_RAG`
2. `HyDe_Hypothetical_Document_Embedding`
3. `HyPE_Hypothetical_Prompt_Embeddings`

**Expected time**: 10-15 minutes  
**Estimated cost**: $1-2

---

## Level 3: Category Testing

Test notebooks by category:

### Test Basic RAG (4 notebooks)
```bash
python3 test_notebooks.py --notebook simple_rag
python3 test_notebooks.py --notebook simple_csv_rag
```

### Test Advanced Patterns (Best with Claude 3)
```bash
python3 test_notebooks.py --notebook CRAG
python3 test_notebooks.py --notebook self_rag
python3 test_notebooks.py --notebook Agentic_RAG
```

### Test Graph-Based (Works with Qdrant)
```bash
python3 test_notebooks.py --notebook graph_rag
python3 test_notebooks.py --notebook graphrag_with_milvus
```

---

## Level 4: Full Test Suite

Test all 37 notebooks (not recommended unless necessary):

```bash
# This will take 3-5 hours and cost $50-100
python3 test_notebooks.py
```

---

## 🎯 Recommended Testing Plan

### For Learning (You!)

**Phase 1: Validation** ✅ Done
```bash
python3 validate_notebooks.py
```

**Phase 2: Setup Verification**
```bash
pip install -r requirements.txt
python3 quick_test.py
```

**Phase 3: Manual Testing (Best Approach)**

Open Jupyter and manually test key notebooks:

```bash
jupyter lab
```

Then open and run:
1. `TEST_BEDROCK_QDRANT.ipynb` - Verify stack works
2. `notebooks/simple_rag/simple_rag.ipynb` - Test basic RAG
3. `notebooks/reranking/reranking.ipynb` - Test retrieval
4. `notebooks/CRAG/crag.ipynb` - Test advanced pattern

**Why manual?**
- You can see the outputs
- You can understand what's happening
- You can stop if something looks wrong
- You learn how each technique works
- No wasted API calls

---

## 🧪 Testing Tools Created

### 1. `validate_notebooks.py` ✅ Already Run

Validates structure and integrity of all notebooks.

**Usage**:
```bash
python3 validate_notebooks.py
```

**What it checks**:
- JSON structure validity
- Required fields present
- Cell structure correct
- Environment setup present
- Import statements found
- File size and metadata

**Result**: ✅ All 37 notebooks valid

### 2. `test_notebooks.py` (Functional Testing)

Executes notebooks and captures results.

**Usage**:
```bash
# Quick test (first 3 notebooks)
python3 test_notebooks.py --quick

# Test specific notebook
python3 test_notebooks.py --notebook simple_rag

# Test first N notebooks
python3 test_notebooks.py --max 5

# Test all (not recommended)
python3 test_notebooks.py
```

**Requirements**:
- Dependencies installed: `pip install -r requirements.txt`
- AWS credentials valid (not expired)
- Bedrock models enabled
- Internet connection

### 3. `quick_test.py` (Stack Verification)

Tests your Bedrock + Qdrant setup.

**Usage**:
```bash
python3 quick_test.py
```

**What it tests**:
- Environment loading
- AWS Bedrock connection
- Claude 3 Sonnet LLM
- Titan Embeddings V2
- Qdrant Cloud connection

---

## 📋 Validation Report

### Notebook Statistics

| Metric | Value |
|--------|-------|
| Total Notebooks | 37 |
| Valid Structure | 37 (100%) |
| Environment Setup | 37 (100%) |
| Average Size | 78.3 KB |
| Total Size | 2.9 MB |
| Largest | graph_rag (865 KB) |
| Smallest | explainable_retrieval (11 KB) |

### All Notebooks List

1. ✅ Agentic_RAG (538.8 KB)
2. ✅ HyDe_Hypothetical_Document_Embedding (12.4 KB)
3. ✅ HyPE_Hypothetical_Prompt_Embeddings (28.7 KB)
4. ✅ Microsoft_GraphRag (17.1 KB)
5. ✅ adaptive_retrieval (24.9 KB)
6. ✅ choose_chunk_size (12.3 KB)
7. ✅ context_enrichment_window_around_chunk (21.3 KB)
8. ✅ context_enrichment_window_around_chunk_with_llamaindex (14.0 KB)
9. ✅ contextual_chunk_headers (14.1 KB)
10. ✅ contextual_compression (13.4 KB)
11. ✅ crag (21.4 KB)
12. ✅ dartboard (28.3 KB)
13. ✅ document_augmentation (22.0 KB)
14. ✅ explainable_retrieval (10.9 KB)
15. ✅ fusion_retrieval (14.6 KB)
16. ✅ fusion_retrieval_with_llamaindex (14.7 KB)
17. ✅ graph_rag (865.2 KB)
18. ✅ graphrag_with_milvus_vectordb (57.0 KB)
19. ✅ hierarchical_indices (17.6 KB)
20. ✅ json_rag (32.3 KB)
21. ✅ memorag (47.6 KB)
22. ✅ multi_model_rag_with_captioning (13.6 KB)
23. ✅ multi_model_rag_with_colpali (826.3 KB)
24. ✅ proposition_chunking (46.3 KB)
25. ✅ query_transformations (16.4 KB)
26. ✅ raptor (25.0 KB)
27. ✅ relevant_segment_extraction (93.2 KB)
28. ✅ reliable_rag (125.3 KB)
29. ✅ reranking (20.9 KB)
30. ✅ reranking_with_llamaindex (16.3 KB)
31. ✅ retrieval_with_feedback_loop (17.3 KB)
32. ✅ self_rag (17.9 KB)
33. ✅ semantic_chunking (11.6 KB)
34. ✅ simple_csv_rag (17.4 KB)
35. ✅ simple_csv_rag_with_llamaindex (11.7 KB)
36. ✅ simple_rag (22.7 KB)
37. ✅ simple_rag_with_llamaindex (18.0 KB)

---

## 🎯 Recommended Action Plan

### For You (Right Now)

**Step 1: Install Dependencies**
```bash
cd /workshop/RAG_Techniques_Notebooks
pip install -r requirements.txt
```

**Step 2: Enable Bedrock Models**
- AWS Console → Bedrock → Model Access
- Enable: Claude 3 Sonnet + Titan Embeddings V2

**Step 3: Verify Setup**
```bash
python3 quick_test.py
```

**Step 4: Manual Test Key Notebooks**
```bash
jupyter lab
```

Open these notebooks and run them:
1. `TEST_BEDROCK_QDRANT.ipynb` (comprehensive test)
2. `notebooks/simple_rag/simple_rag.ipynb` (learn basics)
3. `notebooks/CRAG/crag.ipynb` (advanced technique)

**Step 5: Explore More** (at your pace)

Navigate with `INDEX.ipynb` and explore techniques that interest you.

---

## 💡 Testing Best Practices

### Do:
✅ Test manually through Jupyter (see what's happening)  
✅ Start with simple techniques first  
✅ Read notebook outputs and understand them  
✅ Test one at a time when learning  
✅ Check AWS costs periodically  

### Don't:
❌ Run all 37 notebooks at once (expensive!)  
❌ Skip reading outputs (you'll miss errors)  
❌ Test without valid AWS credentials  
❌ Ignore cost estimates  

---

## 🔍 What Each Validation Checks

### Structure Validation ✅
- Valid JSON format
- Required notebook fields
- Cell structure integrity
- Metadata present

### Environment Check ✅
- Environment loading cells present
- Helper function imports
- Path configurations

### Import Analysis ✅
- Required packages identified
- Import statements valid
- Dependencies clear

---

## 📊 Test Results Storage

When you run tests, results are saved to:
- `test_results.json` - Detailed execution results
- `notebooks/*/test_output/` - Executed notebook outputs

---

## 🎓 Manual Testing Workflow

The **best way** to test is manually:

1. **Open Jupyter Lab**
   ```bash
   jupyter lab
   ```

2. **Select a notebook** from `notebooks/` folder

3. **Read the introduction** - Understand the technique

4. **Run cells one by one** - See outputs, understand logic

5. **Check results** - Verify it works as expected

6. **Learn!** - Understand how the technique works

This approach:
- Costs less (you stop if issues arise)
- Teaches you more
- Shows actual outputs
- Lets you experiment

---

## ✅ Current Status Summary

| Check | Status | Details |
|-------|--------|---------|
| Structure Validation | ✅ PASS | 37/37 notebooks valid |
| Environment Setup | ✅ PASS | All have env loading |
| JSON Integrity | ✅ PASS | All valid JSON |
| Imports Present | ✅ PASS | All have imports |
| Dependencies Listed | ✅ PASS | requirements.txt ready |
| Test Framework | ✅ READY | Tools created |
| Documentation | ✅ COMPLETE | Guides available |

**Status**: ✅ Ready for manual testing via Jupyter Lab

---

## 🚀 Next Steps

1. ✅ Structure validation - **COMPLETE**
2. ⏳ Install dependencies - `pip install -r requirements.txt`
3. ⏳ Enable Bedrock models - AWS Console
4. ⏳ Run `quick_test.py` - Verify setup
5. ⏳ Manual testing - Jupyter Lab
6. ⏳ Explore techniques - Learn and build!

---

## 📞 Need Help?

- **Validation issues**: Re-run `validate_notebooks.py`
- **Execution errors**: Check AWS credentials and Bedrock access
- **Setup problems**: See `INSTALLATION_GUIDE.md`
- **General help**: See `README.md`

---

**Recommendation**: Skip automated testing of all 37 notebooks. Instead, install dependencies, verify your setup with `quick_test.py`, then manually test key notebooks through Jupyter Lab. This is more educational and cost-effective! 🎓
