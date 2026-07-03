# AWS RAG Notebooks Setup Summary

## ✅ Installation Complete

All required Python packages have been installed successfully.

## 📋 Working Configuration

### AWS Resources
- **Account ID**: 562224908971
- **Region**: us-west-2
- **OpenSearch Collection**: movie-search
- **OpenSearch Endpoint**: https://qrm9kbjh7wmnpa99ee2b.us-west-2.aoss.amazonaws.com

### Working Models
- **Embeddings**: `amazon.titan-embed-text-v2:0` ✅
  - 1024 dimensions
  - Fully functional
  
- **LLM (Recommended)**: `us.anthropic.claude-sonnet-4-6` ✅
  - Cross-region inference profile
  - Fast and cost-effective
  
- **Alternative LLMs** (if enabled in your account):
  - `us.anthropic.claude-opus-4-1-20250805-v1:0` (highest quality)
  - `us.anthropic.claude-3-sonnet-20240229-v1:0` (needs enablement)
  - `us.anthropic.claude-3-haiku-20240307-v1:0` (needs enablement)

### Installed Packages
```
boto3==1.43.40
opensearch-py==3.2.0
requests==2.34.2
numpy==2.5.0
jupyter==1.1.1
notebook==7.6.0
ipykernel==7.3.0
matplotlib==3.11.0
pandas==3.0.3
```

## 🔧 Known Issues & Fixes

### 1. Legacy Claude 3 Models
**Issue**: Claude 3 Haiku and Sonnet show "Legacy" access denied errors.
**Solution**: Use cross-region inference profiles with `us.` prefix:
- ✅ `us.anthropic.claude-sonnet-4-6`
- ❌ `anthropic.claude-3-haiku-20240307-v1:0`

### 2. OpenSearch Connection
**Issue**: 404 errors when connecting to OpenSearch.
**Status**: Collection exists but may need:
- Index creation
- Data access policy configuration
- Network policy adjustment

### 3. Model IDs in Notebooks
**Issue**: Notebooks use newer model IDs that require inference profiles.
**Solution**: Update notebook model IDs to use `us.*` inference profiles.

## 📝 Next Steps

### Option 1: Execute Notebooks (Recommended)
Update the notebooks to use working model IDs and run them:

```bash
source venv/bin/activate
jupyter notebook
```

Navigate to `aws_notebooks/` and open any notebook (01-23).

### Option 2: Continue Creating Patterns 24-37
Continue development of remaining 14 patterns without execution.

### Option 3: Fix OpenSearch Indexes
Create proper indexes and data access policies for full functionality.

## 🧪 Test Results

| Component | Status | Details |
|-----------|--------|---------|
| boto3 | ✅ | Connected to account 562224908971 |
| Bedrock API | ✅ | 17 Claude models + 6 Titan models available |
| Titan Embeddings | ✅ | 1024-dim embeddings working |
| Claude Sonnet 4.6 | ✅ | Generation working |
| OpenSearch Connection | ⚠️  | Collection exists, needs config |
| aws_utils module | ✅ | Fixed pandas import |

## 📂 File Structure

```
/workshop/rag_pattern_notebooks/
├── aws_notebooks/           # 23 RAG pattern notebooks
│   ├── 01_Simple_RAG_AWS.ipynb
│   ├── 02_Graph_RAG_AWS.ipynb
│   ├── ...
│   └── 23_Parent_Child_RAG_AWS.ipynb
├── aws_utils/              # Utility modules
│   ├── bedrock_client.py   # ✅ Working
│   ├── opensearch_manager.py
│   ├── rag_evaluator.py    # ✅ Fixed
│   └── diagram_generator.py
├── venv/                   # Virtual environment
├── config.json             # OpenSearch config
├── requirements.txt        # Dependencies
└── test_*.py              # Test scripts
```

## 🚀 Quick Start

```bash
# Activate environment
source venv/bin/activate

# Test setup
python test_final.py

# Start Jupyter
jupyter notebook

# Or run a specific notebook
jupyter nbconvert --to notebook --execute aws_notebooks/01_Simple_RAG_AWS.ipynb
```

## 💰 Cost Estimate

**Per query (typical)**:
- Embeddings (Titan): ~$0.0001
- Generation (Sonnet 4.6): ~$0.003-0.015
- OpenSearch: ~$0.24/hour (collection running)

**Total for testing 23 patterns**: ~$2-5

## 📧 Support

If you encounter issues:
1. Check model access in Bedrock console
2. Verify OpenSearch data access policies
3. Ensure IAM role has bedrock:InvokeModel permission
4. Review AWS_SETUP_SUMMARY.md (this file)

---

**Status**: ✅ Ready for notebook execution with working configuration
**Date**: 2026-07-03
**Notebooks**: 23/37 complete (Phase 1 & 2)
**Remaining**: 14 patterns (Phase 3 & 4)
