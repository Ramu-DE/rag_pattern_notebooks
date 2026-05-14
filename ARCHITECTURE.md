# 🏗️ RAG Techniques: Architecture & Workflow Diagrams

## 📐 Complete Architecture Overview

### **End-to-End RAG Pipeline**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           RAG SYSTEM ARCHITECTURE                            │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│                           1. DOCUMENT INGESTION                               │
│                                                                               │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐                │
│  │   PDF    │   │   CSV    │   │   JSON   │   │  Images  │                │
│  └────┬─────┘   └────┬─────┘   └────┬─────┘   └────┬─────┘                │
│       │              │              │              │                         │
│       └──────────────┴──────────────┴──────────────┘                         │
│                            │                                                  │
│                            ▼                                                  │
│               ┌─────────────────────────┐                                    │
│               │  Document Augmentation  │                                    │
│               │  • Metadata extraction  │                                    │
│               │  • Structure analysis   │                                    │
│               │  • Quality enhancement  │                                    │
│               └────────────┬────────────┘                                    │
└────────────────────────────┼─────────────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                         2. CHUNKING STRATEGIES                                │
│                                                                               │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐          │
│  │  Fixed Size      │  │    Semantic      │  │   Proposition    │          │
│  │  Chunking        │  │    Chunking      │  │    Chunking      │          │
│  │                  │  │                  │  │                  │          │
│  │ • 512 tokens     │  │ • By meaning     │  │ • By logical     │          │
│  │ • 20% overlap    │  │ • Coherence      │  │   statements     │          │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘          │
│           │                     │                     │                      │
│           └─────────────────────┴─────────────────────┘                      │
│                                 │                                             │
└─────────────────────────────────┼─────────────────────────────────────────────┘
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                      3. CONTEXT ENHANCEMENT                                   │
│                                                                               │
│  ┌────────────────────────────────────────────────────────────┐             │
│  │  Contextual Chunk Headers                                  │             │
│  │  "This section discusses X in context of Y..."             │             │
│  └──────────────────────┬─────────────────────────────────────┘             │
│                         │                                                     │
│  ┌────────────────────────────────────────────────────────────┐             │
│  │  Window Around Chunk                                       │             │
│  │  [Previous] ─▶ [Current Chunk] ◀─ [Next]                  │             │
│  └──────────────────────┬─────────────────────────────────────┘             │
│                         │                                                     │
│  ┌────────────────────────────────────────────────────────────┐             │
│  │  Contextual Compression                                    │             │
│  │  Remove irrelevant info while keeping context              │             │
│  └──────────────────────┬─────────────────────────────────────┘             │
└──────────────────────────┼──────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                         4. EMBEDDING & INDEXING                               │
│                                                                               │
│  ┌────────────────┐         ┌────────────────┐                              │
│  │  Embeddings    │         │  Hierarchical  │                              │
│  │  Generation    │────────▶│    Indexing    │                              │
│  │                │         │                │                              │
│  │ • OpenAI       │         │  Root Summary  │                              │
│  │ • Cohere       │         │      ▲         │                              │
│  │ • Local models │         │      │         │                              │
│  └────────┬───────┘         │   Level 1      │                              │
│           │                 │      ▲         │                              │
│           │                 │      │         │                              │
│           │                 │  Leaf Chunks   │                              │
│           │                 └────────────────┘                              │
│           ▼                                                                   │
│  ┌─────────────────────────────────────────────────────────┐                │
│  │            Vector Database Storage                       │                │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │                │
│  │  │ Pinecone │ │ Weaviate │ │  Qdrant  │ │  Milvus  │   │                │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘   │                │
│  │  ┌──────────┐ ┌──────────┐                              │                │
│  │  │ ChromaDB │ │  FAISS   │                              │                │
│  │  └──────────┘ └──────────┘                              │                │
│  └─────────────────────────────────────────────────────────┘                │
└──────────────────────────────────────────────────────────────────────────────┘

                                  ═════════════
                                  QUERY TIME
                                  ═════════════

┌──────────────────────────────────────────────────────────────────────────────┐
│                         5. QUERY PROCESSING                                   │
│                                                                               │
│                        ┌────────────────┐                                    │
│                        │  User Query    │                                    │
│                        └───────┬────────┘                                    │
│                                │                                              │
│         ┌──────────────────────┼──────────────────────┐                     │
│         │                      │                      │                      │
│         ▼                      ▼                      ▼                      │
│  ┌────────────┐        ┌─────────────┐        ┌────────────┐               │
│  │   HyDE     │        │ Multi-Query │        │   HyPE     │               │
│  │            │        │ Generation  │        │            │               │
│  │ Generate   │        │             │        │ Hypothetic │               │
│  │ hypothetic │        │ Create 3-5  │        │ prompt     │               │
│  │ document   │        │ variations  │        │ embedding  │               │
│  └─────┬──────┘        └──────┬──────┘        └─────┬──────┘               │
│        │                      │                      │                       │
│        └──────────────────────┴──────────────────────┘                       │
│                               │                                              │
│                               ▼                                              │
│                    ┌───────────────────────┐                                │
│                    │  Query Embedding      │                                │
│                    └──────────┬────────────┘                                │
└────────────────────────────────┼─────────────────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                          6. RETRIEVAL STRATEGIES                              │
│                                                                               │
│  ┌──────────────────────────────────────────────────────────────────┐       │
│  │                      Fusion Retrieval                             │       │
│  │                                                                   │       │
│  │  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │       │
│  │  │   Vector     │    │   Keyword    │    │    Graph     │       │       │
│  │  │   Search     │    │   Search     │    │   Traversal  │       │       │
│  │  │   (Dense)    │    │   (BM25)     │    │   (Triples)  │       │       │
│  │  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘       │       │
│  │         │                   │                   │                │       │
│  │         └───────────────────┴───────────────────┘                │       │
│  │                             │                                     │       │
│  │                             ▼                                     │       │
│  │                    ┌─────────────────┐                           │       │
│  │                    │  Reciprocal     │                           │       │
│  │                    │  Rank Fusion    │                           │       │
│  │                    └────────┬────────┘                           │       │
│  └─────────────────────────────┼──────────────────────────────────────       │
│                                │                                              │
│                                ▼                                              │
│                      ┌──────────────────┐                                    │
│                      │  Initial Results │                                    │
│                      │  (Top 20-50)     │                                    │
│                      └────────┬─────────┘                                    │
└──────────────────────────────┼──────────────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                          7. RERANKING                                         │
│                                                                               │
│  ┌────────────────────────────────────────────────────────┐                 │
│  │            First Stage: Cross-Encoder                  │                 │
│  │                                                         │                 │
│  │  For each (query, document) pair:                      │                 │
│  │  ┌──────┐   ┌──────────┐   ┌─────────────┐            │                 │
│  │  │Query │ + │ Document │ → │Cross-Encoder│ → Score    │                 │
│  │  └──────┘   └──────────┘   └─────────────┘            │                 │
│  │                                                         │                 │
│  │  Advantages: High precision, semantic understanding    │                 │
│  └──────────────────────────┬──────────────────────────────┘                 │
│                             │                                                │
│                             ▼                                                │
│  ┌────────────────────────────────────────────────────────┐                 │
│  │           Second Stage: LLM Reranking                  │                 │
│  │                                                         │                 │
│  │  Prompt:                                                │                 │
│  │  "Given query: {query}                                  │                 │
│  │   Rank these documents by relevance:                    │                 │
│  │   1. {doc1}                                             │                 │
│  │   2. {doc2}                                             │                 │
│  │   ...                                                   │                 │
│  │   Return ranked order and confidence scores."           │                 │
│  │                                                         │                 │
│  │  Advantages: Reasoning capability, task-specific        │                 │
│  └──────────────────────────┬──────────────────────────────┘                 │
│                             │                                                │
│                             ▼                                                │
│                   ┌──────────────────┐                                       │
│                   │  Top K Results   │                                       │
│                   │  (e.g., Top 5)   │                                       │
│                   └────────┬─────────┘                                       │
└──────────────────────────────┼──────────────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                     8. ADVANCED RAG PATTERNS                                  │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────┐            │
│  │  Pattern Selection (Adaptive)                               │            │
│  │                                                              │            │
│  │  ┌─────────────┐                                            │            │
│  │  │ Query Type? │                                            │            │
│  │  └──────┬──────┘                                            │            │
│  │         │                                                    │            │
│  │    ┌────┴────┬────────────┬─────────────┐                  │            │
│  │    │         │            │             │                   │            │
│  │    ▼         ▼            ▼             ▼                   │            │
│  │  Simple   Complex    Uncertain    Multi-hop                │            │
│  │    │         │            │             │                   │            │
│  │    ▼         ▼            ▼             ▼                   │            │
│  │  Basic    Agentic     CRAG      Graph RAG                  │            │
│  │   RAG      RAG      (Corrective)                            │            │
│  └─────────────────────────────────────────────────────────────┘            │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│                    9. SELF-RAG (Self-Reflection)                              │
│                                                                               │
│                        ┌────────────────┐                                    │
│                        │   Retrieved    │                                    │
│                        │   Documents    │                                    │
│                        └───────┬────────┘                                    │
│                                │                                              │
│                                ▼                                              │
│              ┌──────────────────────────────────┐                            │
│              │  Self-Grade: Relevance Check    │                            │
│              │  "Is this document relevant?"   │                            │
│              │  Score: 1-5                     │                            │
│              └──────────────┬───────────────────┘                            │
│                             │                                                │
│                 ┌───────────┴───────────┐                                    │
│                 │                       │                                    │
│           Score ≥ 3               Score < 3                                  │
│                 │                       │                                    │
│                 ▼                       ▼                                    │
│         ┌───────────────┐       ┌─────────────────┐                         │
│         │  Use Document │       │  Retrieve More  │                         │
│         │  for Answer   │       │  or Web Search  │                         │
│         └───────┬───────┘       └────────┬────────┘                         │
│                 │                        │                                   │
│                 └────────────┬───────────┘                                   │
│                              │                                               │
│                              ▼                                               │
│                    ┌──────────────────┐                                      │
│                    │  Generate Answer │                                      │
│                    └────────┬─────────┘                                      │
│                             │                                                │
│                             ▼                                                │
│              ┌──────────────────────────────────┐                            │
│              │  Self-Grade: Answer Quality     │                            │
│              │  "Is this answer good?"         │                            │
│              │  Checks: Completeness,          │                            │
│              │          Factuality,            │                            │
│              │          Relevance              │                            │
│              └──────────────┬───────────────────┘                            │
│                             │                                                │
│                  ┌──────────┴──────────┐                                     │
│                  │                     │                                     │
│            Acceptable            Unacceptable                                │
│                  │                     │                                     │
│                  ▼                     ▼                                     │
│          ┌──────────────┐     ┌────────────────┐                            │
│          │ Return Answer│     │   Regenerate   │                            │
│          └──────────────┘     │  (Max 3 tries) │                            │
│                               └────────────────┘                            │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│                    10. AGENTIC RAG WORKFLOW                                   │
│                                                                               │
│                        ┌────────────────┐                                    │
│                        │  Query Input   │                                    │
│                        └───────┬────────┘                                    │
│                                │                                              │
│                                ▼                                              │
│                    ┌─────────────────────┐                                   │
│                    │  Planning Agent     │                                   │
│                    │  "What do I need    │                                   │
│                    │   to answer this?"  │                                   │
│                    └─────────┬───────────┘                                   │
│                              │                                               │
│                              ▼                                               │
│              ┌───────────────────────────────┐                               │
│              │   Tool Selection              │                               │
│              │                               │                               │
│              │  ┌─────────┐  ┌─────────┐    │                               │
│              │  │Vector DB│  │Web API  │    │                               │
│              │  └────┬────┘  └────┬────┘    │                               │
│              │  ┌─────┴──┐  ┌─────┴────┐    │                               │
│              │  │Graph DB│  │ SQL DB   │    │                               │
│              │  └────┬───┘  └────┬─────┘    │                               │
│              └───────┼───────────┼───────────┘                               │
│                      │           │                                           │
│                      ▼           ▼                                           │
│              ┌────────────────────────┐                                      │
│              │  Execution Agent       │                                      │
│              │  "Execute the plan"    │                                      │
│              └──────────┬─────────────┘                                      │
│                         │                                                    │
│                         ▼                                                    │
│              ┌────────────────────────┐                                      │
│              │  Verification Agent    │                                      │
│              │  "Is this complete?"   │                                      │
│              └──────────┬─────────────┘                                      │
│                         │                                                    │
│                    ┌────┴─────┐                                              │
│                    │          │                                              │
│                   Yes         No                                             │
│                    │          │                                              │
│                    │          └──────┐                                       │
│                    │                 │                                       │
│                    │                 ▼                                       │
│                    │      ┌──────────────────┐                              │
│                    │      │  Refine Plan     │                              │
│                    │      │  Gather More     │                              │
│                    │      └────────┬─────────┘                              │
│                    │               │                                         │
│                    │               │                                         │
│                    └───────────────┘                                         │
│                            │                                                 │
│                            ▼                                                 │
│                   ┌─────────────────┐                                        │
│                   │  Final Response │                                        │
│                   └─────────────────┘                                        │
└──────────────────────────────────────────────────────────────────────────────┘
```

## 🎯 Specialized Techniques Workflows

### **RAPTOR: Recursive Abstractive Processing**

```
┌─────────────────────────────────────────────────────────────────┐
│                      RAPTOR ARCHITECTURE                         │
└─────────────────────────────────────────────────────────────────┘

Input Documents: [Doc1, Doc2, Doc3, ..., DocN]
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│  LEVEL 0: Leaf Nodes (Original Chunks)                  │
│                                                          │
│  [C1] [C2] [C3] [C4] [C5] [C6] [C7] [C8] [C9] [C10]    │
│   │    │    │    │    │    │    │    │    │    │       │
│   └────┴────┘    └────┴────┘    └────┴────┘    └───┐   │
│        │              │              │             │   │
└────────┼──────────────┼──────────────┼─────────────┼───┘
         │              │              │             │
         ▼              ▼              ▼             ▼
┌─────────────────────────────────────────────────────────┐
│  LEVEL 1: First Clustering & Summarization              │
│                                                          │
│  Cluster 1      Cluster 2      Cluster 3    Cluster 4   │
│     ▼               ▼              ▼            ▼       │
│  [Summary-1]   [Summary-2]   [Summary-3]  [Summary-4]  │
│     │               │              │            │       │
│     └───────────────┴──────────────┴────────────┘       │
│                     │                                    │
└─────────────────────┼────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│  LEVEL 2: Second Clustering & Summarization              │
│                                                          │
│         Cluster A            Cluster B                  │
│            ▼                    ▼                        │
│      [Summary-A]          [Summary-B]                   │
│            │                    │                        │
│            └────────────────────┘                        │
│                     │                                    │
└─────────────────────┼────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│  LEVEL 3: Root Summary                                   │
│                                                          │
│              [Global Summary]                            │
│                                                          │
│  "This document collection discusses..."                │
└─────────────────────────────────────────────────────────┘

Query Time:
───────────
    Query: "What is the main theme?"
       │
       ▼
  ┌──────────────────────────────┐
  │  Tree Traversal Strategy:     │
  │                               │
  │  1. Start at root             │
  │  2. If root sufficient → Done │
  │  3. Else → Traverse to        │
  │     relevant child clusters   │
  │  4. Retrieve leaf chunks      │
  │     from best clusters        │
  └──────────────────────────────┘
```

### **Microsoft GraphRAG: Knowledge Graph Approach**

```
┌────────────────────────────────────────────────────────────────┐
│                   GraphRAG PIPELINE                             │
└────────────────────────────────────────────────────────────────┘

Documents
    │
    ▼
┌────────────────────────────────────────────┐
│  1. Entity & Relationship Extraction       │
│                                            │
│  "Apple released iPhone 15 in 2023"        │
│          ↓                                 │
│  Entities:                                 │
│  - Apple (Company)                         │
│  - iPhone 15 (Product)                     │
│  - 2023 (Date)                             │
│                                            │
│  Relationships:                            │
│  - (Apple)-[RELEASED]->(iPhone 15)         │
│  - (iPhone 15)-[RELEASED_IN]->(2023)       │
└──────────────────┬─────────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────────┐
│  2. Graph Construction                     │
│                                            │
│     ┌─────────┐                            │
│     │ Apple   │                            │
│     └────┬────┘                            │
│          │ RELEASED                        │
│          ▼                                 │
│     ┌──────────┐                           │
│     │iPhone 15 │                           │
│     └────┬─────┘                           │
│          │ RELEASED_IN                     │
│          ▼                                 │
│     ┌────────┐                             │
│     │  2023  │                             │
│     └────────┘                             │
└──────────────────┬─────────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────────┐
│  3. Community Detection                    │
│                                            │
│  Communities (Clusters):                   │
│                                            │
│  Community 1: Apple Ecosystem              │
│  ├─ Apple                                  │
│  ├─ iPhone 15                              │
│  ├─ iOS                                    │
│  └─ App Store                              │
│                                            │
│  Community 2: Smartphone Market            │
│  ├─ iPhone 15                              │
│  ├─ Galaxy S23                             │
│  └─ Pixel 8                                │
└──────────────────┬─────────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────────┐
│  4. Community Summarization                │
│                                            │
│  For each community:                       │
│  "Community 1 focuses on Apple's           │
│   product ecosystem, including iOS         │
│   devices and services."                   │
└──────────────────┬─────────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────────┐
│  5. Query Processing                       │
│                                            │
│  Query: "What did Apple release?"          │
│     │                                      │
│     ▼                                      │
│  Map to Community 1                        │
│     │                                      │
│     ▼                                      │
│  Traverse: Apple → RELEASED → iPhone 15    │
│     │                                      │
│     ▼                                      │
│  Answer: "Apple released iPhone 15 in 2023"│
└────────────────────────────────────────────┘
```

### **Multimodal RAG: Vision + Text**

```
┌───────────────────────────────────────────────────────────┐
│              MULTIMODAL RAG ARCHITECTURE                   │
└───────────────────────────────────────────────────────────┘

Input Documents:
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│   Text   │  │  Images  │  │  Tables  │  │   PDFs   │
└────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │             │
     │             ▼             │             │
     │      ┌────────────┐       │             │
     │      │  Vision    │       │             │
     │      │  Model     │       │             │
     │      │  (CLIP/    │       │             │
     │      │  ColPali)  │       │             │
     │      └──────┬─────┘       │             │
     │             │             │             │
     │      ┌──────┴─────┐       │             │
     │      │            │       │             │
     │      ▼            ▼       │             │
     │  ┌────────┐  ┌────────┐   │             │
     │  │Caption │  │Embed.  │   │             │
     │  └───┬────┘  └───┬────┘   │             │
     │      │           │        │             │
     └──────┴───────────┴────────┴─────────────┘
            │
            ▼
     ┌─────────────────────────────┐
     │  Unified Embedding Space    │
     │                             │
     │  Text ←→ Image ←→ Table     │
     │   Embeddings aligned        │
     └─────────────┬───────────────┘
                   │
                   ▼
     ┌─────────────────────────────┐
     │   Vector Store              │
     │   (Multi-modal Index)       │
     └─────────────┬───────────────┘
                   │
                   ▼
     ┌─────────────────────────────┐
     │   Query (Text or Image)     │
     └─────────────┬───────────────┘
                   │
                   ▼
     ┌─────────────────────────────┐
     │   Retrieve Relevant         │
     │   Text + Images + Tables    │
     └─────────────┬───────────────┘
                   │
                   ▼
     ┌─────────────────────────────┐
     │   Multi-modal LLM           │
     │   (GPT-4V, Gemini, Claude)  │
     │   Process all modalities    │
     └─────────────┬───────────────┘
                   │
                   ▼
     ┌─────────────────────────────┐
     │   Rich Multi-modal Response │
     └─────────────────────────────┘
```

## 🎨 Visualization: Technique Selection Decision Tree

```
                          Start Query
                               │
                               ▼
                      ┌────────────────┐
                      │  Analyze Query │
                      └───────┬────────┘
                              │
        ┢━━━━━━━━━━━━━━━━━━━━━┿━━━━━━━━━━━━━━━━━━━━━┪
        ▼                     ▼                     ▼
  ┌──────────┐          ┌──────────┐         ┌──────────┐
  │  Simple  │          │ Complex  │         │ Requires │
  │  Lookup  │          │Question  │         │ Multiple │
  └────┬─────┘          └────┬─────┘         │  Hops    │
       │                     │               └────┬─────┘
       ▼                     ▼                    ▼
┌──────────────┐      ┌──────────────┐    ┌──────────────┐
│  Simple RAG  │      │  Self-RAG    │    │  Graph RAG   │
│  or          │      │  or          │    │  or          │
│  Fusion RAG  │      │  CRAG        │    │  Agentic RAG │
└──────────────┘      └──────────────┘    └──────────────┘

                    Has Structured Data?
                            │
                    ┌───────┴────────┐
                    ▼                ▼
                  Yes               No
                    │                │
                    ▼                ▼
             ┌───────────┐    ┌─────────────┐
             │ JSON RAG  │    │ Standard    │
             │ or        │    │ Techniques  │
             │ CSV RAG   │    └─────────────┘
             └───────────┘

                  Has Images/Multimodal?
                            │
                    ┌───────┴────────┐
                    ▼                ▼
                  Yes               No
                    │                │
                    ▼                ▼
          ┌──────────────────┐  ┌──────────┐
          │ Multimodal RAG   │  │ Text-only│
          │ with ColPali     │  │ RAG      │
          └──────────────────┘  └──────────┘
```

## 📚 Component Deep Dive

### **Chunking Strategy Comparison**

```
┌────────────────────────────────────────────────────────────────┐
│                    CHUNKING STRATEGIES                          │
└────────────────────────────────────────────────────────────────┘

1. FIXED-SIZE CHUNKING
   Input: "AI is transforming healthcare. Machine learning 
           models can diagnose diseases. Deep learning..."
           
   Output:
   ┌─────────────────────────┐
   │ Chunk 1 (512 tokens)    │
   │ "AI is transforming..." │
   └─────────────────────────┘
   ┌─────────────────────────┐
   │ Chunk 2 (512 tokens)    │
   │ "Machine learning..."   │ ← 20% overlap
   └─────────────────────────┘

2. SEMANTIC CHUNKING
   Input: Same text
   
   Output:
   ┌─────────────────────────────────┐
   │ Chunk 1 (Theme: AI in Healthcare)│
   │ "AI is transforming healthcare. │
   │  Machine learning models can     │
   │  diagnose diseases."             │
   └─────────────────────────────────┘
   ┌─────────────────────────────────┐
   │ Chunk 2 (Theme: Deep Learning)   │
   │ "Deep learning..."               │
   └─────────────────────────────────┘
   
3. PROPOSITION CHUNKING
   Input: Same text
   
   Output:
   ┌───────────────────────────────────┐
   │ Proposition 1:                    │
   │ "AI is transforming healthcare"   │
   └───────────────────────────────────┘
   ┌───────────────────────────────────┐
   │ Proposition 2:                    │
   │ "ML models can diagnose diseases" │
   └───────────────────────────────────┘
```

### **Reranking Methods Comparison**

```
┌────────────────────────────────────────────────────────────────┐
│                    RERANKING APPROACHES                         │
└────────────────────────────────────────────────────────────────┘

Initial Retrieval: 20 Documents
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│  METHOD 1: Cross-Encoder Reranking                      │
│                                                          │
│  For each doc:                                           │
│    score = CrossEncoder([query, doc])                    │
│                                                          │
│  Pros: ✅ High accuracy                                  │
│        ✅ Semantic understanding                          │
│  Cons: ❌ Slower (O(n) forward passes)                   │
│        ❌ More expensive                                  │
│                                                          │
│  Result: Top 10 docs                                     │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│  METHOD 2: LLM Reranking                                 │
│                                                          │
│  Single prompt with all docs:                            │
│  "Rank these 10 documents for query: {q}                 │
│   1. {doc1}                                              │
│   2. {doc2}                                              │
│   ...                                                    │
│   Return ranking and confidence."                        │
│                                                          │
│  Pros: ✅ Task-specific reasoning                        │
│        ✅ Explainable                                     │
│  Cons: ❌ Token-intensive                                │
│        ❌ Latency                                         │
│                                                          │
│  Result: Top 5 docs with explanations                    │
└─────────────────────────────────────────────────────────┘
```

---

**This architecture document complements the main README and provides visual understanding of the RAG pipeline flow.**

**Version:** 1.0
**Last Updated:** 2026-05-14
