# BM25 Wins at Scale — Retrieval Pipeline Benchmark

## Overview

Empirical experiment proving that BM25 (lexical inverted-index retrieval) dominates agentic and long-context retrieval pipelines across increasing corpus sizes.

**Source Document**: OECD "The Agentic AI Landscape and Its Conceptual Foundations" (Feb 2026, 34 pages)

## Experiment Design

### Corpus Architecture

| Tier | Documents | Tokens | Composition |
|------|-----------|--------|-------------|
| T0 | 18 | 3,938 | 10 gold + 8 traps |
| T1 | 93 | 48,949 | + 75 noise |
| T2 | 243 | 135,669 | + 150 noise |
| T3 | 543 | 307,900 | + 300 noise |
| T4 | 1,143 | 668,208 | + 600 noise |
| T5 | 2,343 | 1,380,110 | + 1,200 noise |
| T6 | 4,743 | 2,834,662 | + 2,400 noise |
| T7 | 9,543 | 5,723,498 | + 4,800 noise |

Gold documents and adversarial traps sit in the bedrock (T0). Each tier adds ONLY noise — same questions, same gold answers.

### Pipelines Tested

| Pipeline | Retrieval Method | LLM for Retrieval? |
|----------|------------------|--------------------|
| **BM25** | Inverted index, top-k | No |
| **Dense** | Titan Embed v2, cosine similarity | Embed only |
| **Agent** | LIST/GREP/READ tool loop | Yes (each call) |
| **Agent+BM25** | Agent with BM25 search tool | Yes (fewer calls) |
| **Long-Context** | Stuff all docs into context window | Yes (all at once) |

### Ground Truth

29 Q&A pairs covering definitions, statistics (38%, 920%, 49K), enumerations, and comparisons — all sourced from the OECD paper.

## Results

### Accuracy by Tier

| Pipeline | T0 (18) | T1 (93) | T2 (243) | T3 (543) | T4 (1143) | T5 (2343) |
|----------|:-------:|:-------:|:--------:|:--------:|:---------:|:---------:|
| **BM25** | 66% | 69% | 69% | 69% | 69% | 69% |
| Long-Context | 69% | 69% | 69% | FAIL | FAIL | FAIL |
| Agent (40 calls) | 17% | - | - | - | - | - |
| Agent+BM25 | 7% | - | - | - | - | - |

### Token Cost per Question

| Pipeline | T0 | T2 | T5 |
|----------|---:|---:|---:|
| **BM25** | 1,667 | 1,866 | 1,869 |
| Long-Context | 5,062 | 152,320 | FAIL |
| Agent | 15,174 | - | - |

## Key Findings

1. **BM25 dominates from T0** — 66% vs Agent's 17% at the smallest tier
2. **BM25 cost is flat** — only 12% increase across 133x corpus growth
3. **Agent burns 9.1x more tokens** for 4x worse accuracy
4. **Long-context hits a wall** — FAILS at T3+ (200K token limit), 91x cost at T2
5. **Mechanism** — corpus-wide ranking (BM25) beats sequential exploration (agent)

## Setup

```bash
pip install boto3 tiktoken rank-bm25 pymupdf python-dotenv

# Copy and edit credentials
cp .env.example .env
```

## Files

| File | Description |
|------|-------------|
| `BM25_Wins_at_Scale_AWS.ipynb` | Main experiment notebook (executed with outputs) |
| `corpus_generator.py` | Corpus builder: gold docs, traps, noise tiers |
| `results/final_summary.json` | Compiled experiment results |
| `.env.example` | AWS credential template |

## AWS Stack

- **Amazon Bedrock** — Claude Haiku 4.5 (`us.anthropic.claude-haiku-4-5-20251001-v1:0`)
- **Amazon Bedrock** — Titan Embed v2 (for dense pipeline)
- **boto3** — Bedrock Converse API
