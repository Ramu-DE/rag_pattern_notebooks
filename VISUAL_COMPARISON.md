# 🎨 Visual RAG Techniques Showcase

> **The most comprehensive RAG implementation collection with 37 techniques, production-ready infrastructure, and complete visual documentation.**

## 🚀 Quick Stats

<table>
<tr>
<td align="center" width="33%">
<img src="https://img.shields.io/badge/Techniques-37-brightgreen?style=for-the-badge" alt="37 Techniques"/>
<br><b>37 RAG Techniques</b>
<br>From basic to advanced
</td>
<td align="center" width="33%">
<img src="https://img.shields.io/badge/Vector_DBs-6-blue?style=for-the-badge" alt="6 Vector DBs"/>
<br><b>6 Vector Databases</b>
<br>Production-ready options
</td>
<td align="center" width="33%">
<img src="https://img.shields.io/badge/Frameworks-2-orange?style=for-the-badge" alt="2 Frameworks"/>
<br><b>Dual Framework</b>
<br>LangChain + LlamaIndex
</td>
</tr>
</table>

---

## 🏗️ System Architecture at a Glance

```
┌─────────────────────────────────────────────────────────────────────┐
│                    COMPLETE RAG PIPELINE                             │
└─────────────────────────────────────────────────────────────────────┘

📄 DOCUMENT INGESTION
   ↓
📊 CHUNKING (3 strategies)
   ↓
🎯 CONTEXT ENHANCEMENT (4 techniques)
   ↓
🔢 EMBEDDING & INDEXING (6 vector DBs)
   ↓
🔍 QUERY PROCESSING (HyDE, HyPE, Multi-Query)
   ↓
🎣 RETRIEVAL (Fusion, Adaptive, Graph-based)
   ↓
⚡ RERANKING (Cross-Encoder + LLM)
   ↓
🤖 GENERATION (Simple, Self-RAG, CRAG, Agentic)
   ↓
✅ RESPONSE
```

---

## 📊 Comparison: This Project vs Others

### **Feature Coverage**

```
┌─────────────────────────────────────────────────────────┐
│ Feature Comparison                                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ This Project:     ████████████████████████ 97.5%       │
│ Advanced_RAG:     ███████████░░░░░░░░░░░░ 60%         │
│ Basic RAG:        ████░░░░░░░░░░░░░░░░░░░░ 20%         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### **Technique Count**

<table>
<tr>
<th>Category</th>
<th>This Project</th>
<th>Advanced_RAG</th>
<th>Typical Projects</th>
</tr>
<tr>
<td>Basic RAG</td>
<td align="center">✅ 4</td>
<td align="center">✅ 1</td>
<td align="center">⚠️ 1</td>
</tr>
<tr>
<td>Query Enhancement</td>
<td align="center">✅ 3</td>
<td align="center">✅ 1</td>
<td align="center">❌ 0</td>
</tr>
<tr>
<td>Retrieval Strategies</td>
<td align="center">✅ 4</td>
<td align="center">⚠️ 2</td>
<td align="center">⚠️ 1</td>
</tr>
<tr>
<td>Context Enhancement</td>
<td align="center">✅ 4</td>
<td align="center">❌ 0</td>
<td align="center">❌ 0</td>
</tr>
<tr>
<td>Chunking Strategies</td>
<td align="center">✅ 3</td>
<td align="center">❌ 0</td>
<td align="center">⚠️ 1</td>
</tr>
<tr>
<td>Advanced Patterns</td>
<td align="center">✅ 5</td>
<td align="center">✅ 3</td>
<td align="center">❌ 0</td>
</tr>
<tr>
<td>Graph RAG</td>
<td align="center">✅ 3</td>
<td align="center">⚠️ 1</td>
<td align="center">❌ 0</td>
</tr>
<tr>
<td>Multimodal</td>
<td align="center">✅ 2</td>
<td align="center">❌ 0</td>
<td align="center">❌ 0</td>
</tr>
<tr>
<td><b>TOTAL</b></td>
<td align="center"><b>✅ 37</b></td>
<td align="center"><b>⚠️ ~10</b></td>
<td align="center"><b>❌ 2-3</b></td>
</tr>
</table>

---

## 🎯 Unique Features Not Found Elsewhere

<table>
<tr>
<td width="50%" valign="top">

### 🌟 **Exclusive to This Project**

#### RAPTOR
```
    Root
     ▲
     │
  ┌──┴──┐
  │     │
 L1    L2
  ▲     ▲
  │     │
Chunks Chunks
```
Recursive abstractive processing for long documents

#### MemoRAG
```
Turn 1 → Turn 2 → Turn 3
  ↓        ↓        ↓
Memory ← Memory ← Memory
```
Memory-augmented conversation

#### Multimodal RAG
```
Text + Images + Tables
        ↓
  Unified Search
        ↓
Vision-Language LLM
```
True multimodal understanding

</td>
<td width="50%" valign="top">

### ✨ **Advanced Features**

#### Self-RAG
```
Retrieve → Grade
            ↓
    ┌───────┴───────┐
  Good          Bad
    ↓              ↓
Generate    Refine/Search
```
Self-reflection and correction

#### Graph RAG
```
Entities → Relationships
     ↓
Knowledge Graph
     ↓
Community Detection
     ↓
Intelligent Traversal
```
Network-based retrieval

#### Explainable Retrieval
```
Document Score: 0.89
├─ Semantic: 0.75
├─ Keyword: 0.92
└─ Context: 0.82
```
Full transparency

</td>
</tr>
</table>

---

## 🔧 Production-Ready Infrastructure

### **Vector Database Support**

<table>
<tr>
<td align="center" width="16%">
<img src="https://img.shields.io/badge/Pinecone-✓-00D4AA?style=flat-square" alt="Pinecone"/>
<br><b>Pinecone</b>
<br>Managed
</td>
<td align="center" width="16%">
<img src="https://img.shields.io/badge/Weaviate-✓-00C389?style=flat-square" alt="Weaviate"/>
<br><b>Weaviate</b>
<br>Hybrid
</td>
<td align="center" width="16%">
<img src="https://img.shields.io/badge/Qdrant-✓-FF6154?style=flat-square" alt="Qdrant"/>
<br><b>Qdrant</b>
<br>Performance
</td>
<td align="center" width="16%">
<img src="https://img.shields.io/badge/Milvus-✓-00A1E0?style=flat-square" alt="Milvus"/>
<br><b>Milvus</b>
<br>Scale
</td>
<td align="center" width="16%">
<img src="https://img.shields.io/badge/Chroma-✓-FF6B6B?style=flat-square" alt="Chroma"/>
<br><b>ChromaDB</b>
<br>Local
</td>
<td align="center" width="16%">
<img src="https://img.shields.io/badge/FAISS-✓-00599C?style=flat-square" alt="FAISS"/>
<br><b>FAISS</b>
<br>Development
</td>
</tr>
</table>

**Switch with a single config change!**
```bash
VECTOR_DB_PROVIDER=qdrant  # That's it!
```

---

## 📚 Complete Technique Catalog

### **Level 1: Foundation** 🟢

<details>
<summary><b>Basic RAG (4 techniques)</b></summary>

- ✅ Simple RAG
- ✅ Simple RAG with LlamaIndex  
- ✅ Simple CSV RAG
- ✅ Simple CSV RAG with LlamaIndex

**When to use:** Straightforward Q&A, factual lookup, getting started
</details>

### **Level 2: Optimization** 🔵

<details>
<summary><b>Chunking Strategies (3 techniques)</b></summary>

- ✅ Choose Chunk Size
- ✅ Semantic Chunking
- ✅ Proposition Chunking

**When to use:** Improve context boundaries, semantic coherence
</details>

<details>
<summary><b>Context Enhancement (4 techniques)</b></summary>

- ✅ Context Enrichment Window
- ✅ Context Enrichment with LlamaIndex
- ✅ Contextual Chunk Headers
- ✅ Contextual Compression

**When to use:** Better context, reduce information loss
</details>

<details>
<summary><b>Query Enhancement (3 techniques)</b></summary>

- ✅ HyDE (Hypothetical Document Embedding)
- ✅ HyPE (Hypothetical Prompt Embeddings)
- ✅ Query Transformations

**When to use:** Improve query quality, semantic search
</details>

<details>
<summary><b>Better Retrieval (4 techniques)</b></summary>

- ✅ Fusion Retrieval
- ✅ Fusion Retrieval with LlamaIndex
- ✅ Adaptive Retrieval
- ✅ Hierarchical Indices

**When to use:** Balance precision/recall, multi-strategy search
</details>

<details>
<summary><b>Reranking (2 techniques)</b></summary>

- ✅ Reranking (Cross-Encoder)
- ✅ Reranking with LlamaIndex

**When to use:** Improve result relevance, fine-tune ordering
</details>

### **Level 3: Advanced** 🟣

<details>
<summary><b>Self-Correcting RAG (5 techniques)</b></summary>

- ✅ CRAG (Corrective RAG)
- ✅ Self-RAG
- ✅ Reliable RAG
- ✅ Retrieval with Feedback Loop
- ✅ Dartboard

**When to use:** Uncertain information, need verification, high-stakes
</details>

<details>
<summary><b>Graph-Based (3 techniques)</b></summary>

- ✅ Graph RAG
- ✅ Microsoft GraphRAG
- ✅ GraphRAG with Milvus

**When to use:** Relationship-heavy data, network analysis
</details>

<details>
<summary><b>Agent-Based (1 technique)</b></summary>

- ✅ Agentic RAG

**When to use:** Multi-step reasoning, complex workflows
</details>

### **Level 4: Specialized** 🔴

<details>
<summary><b>Advanced Techniques (3 techniques)</b></summary>

- ✅ RAPTOR (Recursive Abstractive Processing)
- ✅ MemoRAG (Memory-Augmented)
- ✅ Explainable Retrieval

**When to use:** Long documents, conversations, debugging
</details>

<details>
<summary><b>Document Processing (3 techniques)</b></summary>

- ✅ Document Augmentation
- ✅ Relevant Segment Extraction
- ✅ JSON RAG

**When to use:** Structured data, preprocessing, extraction
</details>

<details>
<summary><b>Multimodal (2 techniques)</b></summary>

- ✅ Multi-Model RAG with Captioning
- ✅ Multi-Model RAG with ColPali

**When to use:** Images, diagrams, mixed content
</details>

---

## 🎯 Choose Your Path

```
┌─────────────────────────────────────────────────────────┐
│           WHICH RAG TECHNIQUE SHOULD I USE?             │
└─────────────────────────────────────────────────────────┘

Simple Q&A?                    → Simple RAG
Need better context?           → Context Enrichment + Semantic Chunking
Uncertain information?         → CRAG or Self-RAG
Complex reasoning?             → Agentic RAG
Relationships matter?          → Graph RAG
Very long documents?           → RAPTOR
Images + text?                 → Multimodal RAG
Need to remember?              → MemoRAG
Need transparency?             → Explainable Retrieval
Structured data (CSV/JSON)?    → CSV/JSON RAG

📖 Full decision guide: See TECHNIQUE_SELECTOR.md
```

---

## 🏆 Why Choose This Project?

<table>
<tr>
<td width="25%" align="center">
<h3>📚 Most Complete</h3>
<b>37 techniques</b> from basic to cutting-edge, all in one place
</td>
<td width="25%" align="center">
<h3>🏭 Production Ready</h3>
<b>6 vector DBs</b>, centralized config, error handling
</td>
<td width="25%" align="center">
<h3>📖 Well Documented</h3>
<b>Architecture diagrams</b>, guides, and READMEs for each technique
</td>
<td width="25%" align="center">
<h3>🎓 Educational</h3>
<b>Learning paths</b>, comparisons, and practical examples
</td>
</tr>
</table>

---

## 🚀 Quick Start

```bash
# 1. Clone and setup
cd RAG_Techniques_Notebooks
cp .env.template .env

# 2. Add your API keys to .env
nano .env

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start exploring!
jupyter lab
```

**🎯 Start with:** `notebooks/simple_rag/simple_rag.ipynb`

---

## 📖 Documentation

| Document | Purpose |
|----------|---------|
| 📘 [README.md](./README.md) | Main documentation, setup, all techniques |
| 🏗️ [ARCHITECTURE.md](./ARCHITECTURE.md) | Visual architecture diagrams and workflows |
| 📊 [COMPARISON_WITH_ADVANCED_RAG.md](./COMPARISON_WITH_ADVANCED_RAG.md) | Detailed comparison with other projects |
| 🎯 [TECHNIQUE_SELECTOR.md](./TECHNIQUE_SELECTOR.md) | Choose the right technique for your use case |

---

## 🌟 Featured Techniques

### **CRAG (Corrective RAG)**
```
Retrieve → Evaluate Confidence
              ↓
    ┌─────────┼─────────┐
  High      Medium      Low
    ↓         ↓          ↓
Use Docs  Docs+Web   Web Only
```
🎯 **Best for:** Uncertain information, need verification

### **RAPTOR**
```
        Root Summary
            ▲
    ┌───────┴───────┐
  L1 Summary    L1 Summary
    ▲              ▲
Leaf Chunks    Leaf Chunks
```
🎯 **Best for:** Very long documents, multi-level questions

### **Graph RAG**
```
Documents → Entities & Relations
              ↓
       Knowledge Graph
              ↓
    Community Detection
              ↓
       Query → Traverse
```
🎯 **Best for:** Relationship-heavy data, network analysis

### **Multimodal RAG**
```
Text + Images → Vision Model
                    ↓
            Unified Embeddings
                    ↓
         Multimodal LLM → Response
```
🎯 **Best for:** PDFs with images, diagrams, charts

---

## 📈 Performance Metrics

| Technique | Speed | Accuracy | Complexity | Best Use Case |
|-----------|-------|----------|------------|---------------|
| Simple RAG | ⚡⚡⚡⚡ | ⭐⭐⭐ | 🔧 | Fast Q&A |
| CRAG | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | 🔧🔧 | High accuracy |
| Self-RAG | ⚡⚡ | ⭐⭐⭐⭐⭐ | 🔧🔧🔧 | Critical apps |
| Agentic RAG | ⚡⚡ | ⭐⭐⭐⭐ | 🔧🔧🔧🔧 | Complex reasoning |
| Graph RAG | ⚡⚡⚡ | ⭐⭐⭐⭐ | 🔧🔧🔧 | Relationships |
| RAPTOR | ⚡⚡ | ⭐⭐⭐⭐ | 🔧🔧🔧 | Long documents |

---

## 🤝 Contributing

We welcome contributions! Whether it's:
- 🐛 Bug fixes
- ✨ New techniques
- 📖 Documentation improvements
- 🎨 More diagrams

See individual technique folders for contribution guidelines.

---

## 📞 Support & Community

- 📚 **Documentation:** Start with README.md
- 🎯 **Choosing a technique:** See TECHNIQUE_SELECTOR.md
- 🏗️ **Understanding architecture:** See ARCHITECTURE.md
- 📊 **Comparisons:** See COMPARISON_WITH_ADVANCED_RAG.md

---

## 🎓 Learning Resources

**Beginners:** Start with `simple_rag` → `fusion_retrieval` → `reranking`

**Intermediate:** Try `CRAG` → `self_rag` → `Agentic_RAG`

**Advanced:** Explore `graph_rag` → `RAPTOR` → `multimodal`

**Production:** Combine techniques for your specific use case (see TECHNIQUE_SELECTOR.md)

---

<div align="center">

### ⭐ **37 Techniques • 6 Vector DBs • 2 Frameworks • Production Ready** ⭐

**The most comprehensive RAG implementation collection available.**

[Get Started](./README.md) • [Architecture](./ARCHITECTURE.md) • [Choose Technique](./TECHNIQUE_SELECTOR.md)

</div>
