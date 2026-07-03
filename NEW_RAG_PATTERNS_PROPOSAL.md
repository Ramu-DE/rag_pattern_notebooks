# New RAG Patterns - Industry Implementation & Failure Cases

## Based on NVIDIA RAG Factory + Deep Research

**Date**: 2026-07-03  
**Current Patterns**: 23 (Patterns 1-23 completed)  
**Proposed New Patterns**: 14 (Patterns 24-37)

---

## Pattern Selection Criteria

✅ Real-world production use cases  
✅ Address specific failure modes  
✅ Industry-validated implementations  
✅ Not covered in existing 23 patterns  
✅ Practical AWS/Bedrock implementation  

---

## Phase 3: Production & Failure Recovery Patterns (24-30)

### Pattern 24: **Query Decomposition RAG** ⭐ NVIDIA Pattern
**Source**: NVIDIA GenerativeAIExamples  
**Problem Solved**: Single-hop RAG fails for complex multi-step queries

**Real Failure Case**:
- Query: "Compare Q1 revenue between 2023 and 2024 and calculate growth rate"
- Simple RAG: Retrieves one document, misses comparison
- **Solution**: Decompose into: (1) Get 2023 Q1, (2) Get 2024 Q1, (3) Calculate growth

**Architecture**:
- Recursive agent breaks query into sub-questions
- Two tools: `search` (RAG) and `math` (computation)
- Continues until all sub-answers collected

**Implementation**:
```python
tools = [
    create_rag_tool(),      # Vector search
    create_math_tool()      # Calculations
]
agent = create_decomposition_agent(llm, tools)
```

**AWS Components**:
- Bedrock (Claude Sonnet 4.6 for decomposition)
- OpenSearch for sub-query retrieval
- Lambda for orchestration

---

### Pattern 25: **Structured Data RAG (Tabular)** ⭐ NVIDIA Pattern
**Source**: NVIDIA GenerativeAIExamples + PandasAI  
**Problem Solved**: Vector embeddings fail for structured/tabular data

**Real Failure Case**:
- CSV with sales data: [Date, Product, Revenue, Region]
- Query: "Show top 3 products in Q2 2024 by revenue"
- Vector RAG: Embeds rows → wrong semantic match
- **Solution**: Generate SQL/Pandas code, execute on data

**Architecture**:
- Load CSV into DataFrame
- LLM generates Python/SQL code
- Execute code safely on data
- Return structured results

**Implementation**:
```python
# LLM generates code
code = llm.generate(f"Generate pandas code for: {query}")
# Safe execution
result = safe_exec(code, dataframe)
```

**AWS Components**:
- Bedrock (code generation)
- Athena (for SQL queries)
- S3 (data storage)
- No vector database needed!

---

### Pattern 26: **Reranking RAG** ⭐ Production Critical
**Source**: NVIDIA NeMo Retriever, Cohere Rerank  
**Problem Solved**: Top-K retrieval returns irrelevant chunks in top results

**Real Failure Case**:
- Retrieve top-10 chunks by cosine similarity
- Chunks 1-3 are tangentially related
- Chunks 7-9 are highly relevant
- LLM sees irrelevant chunks first → hallucination

**Architecture**:
1. **First-stage**: Fast vector search (top-50)
2. **Rerank**: Cross-encoder reranks to top-5
3. **Generation**: Use reranked chunks

**Key Insight**:
- Bi-encoder (embeddings): Fast but less accurate
- Cross-encoder (reranker): Slow but precise
- Two-stage = best of both

**Implementation**:
```python
# Stage 1: Fast retrieval
chunks = vector_db.search(query, top_k=50)

# Stage 2: Precision reranking
reranked = reranker.rerank(query, chunks, top_k=5)

# Stage 3: Generation with best chunks
answer = llm.generate_with_context(query, reranked)
```

**AWS Components**:
- OpenSearch (first-stage retrieval)
- Bedrock (reranking with Claude)
- Or SageMaker (cross-encoder model)

---

### Pattern 27: **Fallback RAG** 🔥 Failure Recovery
**Source**: Industry practice (Notion, Perplexity)  
**Problem Solved**: Single retrieval strategy fails

**Real Failure Cases**:
1. Vector search returns nothing → User gets "no results"
2. Query has typos → Semantic search fails
3. Recent documents not yet indexed → User frustrated

**Architecture - Cascading Fallbacks**:
```
Query → Vector Search
          ↓ (0 results)
        Keyword Search (BM25)
          ↓ (0 results)
        Fuzzy Search
          ↓ (0 results)
        Web Search (external)
          ↓ (0 results)
        Default Response
```

**Implementation**:
```python
def fallback_rag(query):
    # Try 1: Vector search
    results = vector_search(query)
    if results: return generate(query, results)
    
    # Try 2: Keyword search
    results = keyword_search(query)
    if results: return generate(query, results)
    
    # Try 3: Fuzzy search (typo tolerance)
    results = fuzzy_search(query)
    if results: return generate(query, results)
    
    # Try 4: Web search
    results = web_search(query)
    if results: return generate(query, results)
    
    # Try 5: Default response
    return "I don't have information on that. Would you like me to search elsewhere?"
```

**AWS Components**:
- OpenSearch (vector + keyword + fuzzy)
- Bedrock (generation)
- Lambda (orchestration)
- Tavily API (web search)

---

### Pattern 28: **Citation RAG** 📚 Production Essential
**Source**: ChatGPT, Perplexity, enterprise systems  
**Problem Solved**: Users can't verify LLM responses

**Real Failure Case**:
- User: "What is our refund policy?"
- LLM: "Refunds within 30 days" (wrong, actually 14 days)
- No citation → User trusts wrong answer → Legal issue

**Architecture**:
```
Query → Retrieve chunks (with metadata)
      → Generate answer with inline citations
      → Return answer + source documents
```

**Implementation**:
```python
# Retrieve with metadata
chunks = retrieve_with_metadata(query, top_k=5)

# Prompt with citation instructions
prompt = f"""
Answer based on these sources. Cite sources as [1], [2], etc.

Sources:
[1] {chunks[0].text} (from: {chunks[0].source})
[2] {chunks[1].text} (from: {chunks[1].source})

Question: {query}

Answer with inline citations:
"""

answer = llm.generate(prompt)

# Return with sources
return {
    'answer': answer,
    'sources': [c.metadata for c in chunks]
}
```

**Output Example**:
```
"Refunds are available within 14 days[1]. For damaged items, 
we offer 30-day returns[2]."

Sources:
[1] Refund Policy v2.3, page 12
[2] Damaged Goods Policy, section 4.1
```

**AWS Components**:
- OpenSearch (with metadata tracking)
- Bedrock (citation-aware generation)
- S3 (source document storage)

---

### Pattern 29: **Hybrid Search RAG** 🔬 Production Standard
**Source**: Weaviate, Pinecone, Elasticsearch  
**Problem Solved**: Pure vector search misses exact keyword matches

**Real Failure Cases**:
1. Query: "AWS EC2 t3.micro pricing"
   - Vector: Returns general AWS pricing docs
   - **Need**: Exact t3.micro mention

2. Query: "HIPAA compliance checklist"
   - Vector: Returns HIPAA-related content
   - **Need**: Exact checklist document

**Architecture**:
```
Query → Parallel:
         ├─ Vector Search (semantic)
         └─ Keyword Search (exact match - BM25)
      → Combine scores (RRF or weighted)
      → Unified results
```

**Scoring Strategies**:
1. **RRF (Reciprocal Rank Fusion)**:
   ```python
   score = 1/(k + rank_vector) + 1/(k + rank_keyword)
   ```

2. **Weighted Combination**:
   ```python
   score = alpha * score_vector + (1-alpha) * score_keyword
   ```

**Implementation**:
```python
# Parallel search
vector_results = vector_search(query, top_k=20)
keyword_results = keyword_search(query, top_k=20)

# Combine with RRF
combined = rrf_combine(vector_results, keyword_results, k=60)

# Generate with hybrid results
answer = llm.generate_with_context(query, combined[:5])
```

**AWS Components**:
- OpenSearch (supports both vector + BM25)
- Bedrock (generation)

**When to Use**:
- Product search (model numbers, SKUs)
- Technical documentation (API names, error codes)
- Legal documents (specific clauses, case numbers)
- Medical records (diagnosis codes, drug names)

---

### Pattern 30: **Streaming RAG** ⚡ UX Critical
**Source**: ChatGPT, Claude, production UX  
**Problem Solved**: Users wait 5-10s for full answer

**Real Failure Case**:
- Long answer (500 words)
- User sees nothing for 8 seconds
- User thinks system is broken
- **Solution**: Stream tokens as generated

**Architecture**:
```
Query → Retrieve (1-2s)
      → Stream generation:
         Token 1 → Send
         Token 2 → Send
         Token 3 → Send
         ...
```

**Implementation**:
```python
def streaming_rag(query):
    # Quick retrieval
    chunks = retrieve(query, top_k=5)
    
    # Stream generation
    for token in llm.stream(query, chunks):
        yield token  # Send immediately to client
```

**Client-side**:
```javascript
fetch('/rag/stream', {method: 'POST', body: query})
  .then(response => {
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    
    function read() {
      reader.read().then(({done, value}) => {
        if (done) return;
        const text = decoder.decode(value);
        displayText(text);  // Update UI immediately
        read();
      });
    }
    read();
  });
```

**AWS Components**:
- Bedrock (streaming API)
- Lambda with streaming response
- API Gateway (HTTP streaming)

**Performance**:
- Time to first token: <1s
- Perceived latency: 80% improvement
- User satisfaction: Significantly higher

---

## Phase 4: Advanced Production Patterns (31-37)

### Pattern 31: **Multi-Tenancy RAG** 🏢 Enterprise Critical
**Source**: Enterprise SaaS (Salesforce, HubSpot)  
**Problem Solved**: Data isolation between customers

**Real Failure Case**:
- Customer A's query retrieves Customer B's documents
- Data breach, compliance violation
- **Solution**: Strict tenant isolation

**Architecture**:
```
Query + TenantID → Filter by tenant
                 → Retrieve (tenant-scoped)
                 → Generate (tenant context only)
```

**Implementation Strategies**:

1. **Namespace Isolation** (Recommended):
```python
# Each tenant gets own index
index_name = f"rag_tenant_{tenant_id}"
results = vector_db.search(index_name, query)
```

2. **Metadata Filtering**:
```python
results = vector_db.search(
    query,
    filter={"tenant_id": tenant_id}
)
```

3. **Separate Databases** (Ultra-secure):
```python
db = get_tenant_database(tenant_id)
results = db.search(query)
```

**AWS Components**:
- OpenSearch (index per tenant or filtering)
- Cognito (tenant authentication)
- Lambda (tenant context injection)
- KMS (tenant-specific encryption)

**Security Checklist**:
- ✅ Tenant ID in every query
- ✅ Index-level or row-level isolation
- ✅ Encrypted at rest per tenant
- ✅ Audit logs per tenant
- ✅ Rate limiting per tenant

---

### Pattern 32: **Temporal RAG** 📅 Time-Aware
**Source**: Bloomberg Terminal, Financial services  
**Problem Solved**: Outdated information in responses

**Real Failure Cases**:
1. Query: "What is the current interest rate?"
   - RAG returns 2022 data
   - User makes decision on old data

2. Query: "Latest COVID guidelines"
   - Returns 2020 guidance
   - Dangerous for medical advice

**Architecture**:
```
Query → Extract temporal intent
      → Retrieve with time filtering
      → Prioritize recent documents
      → Generate with temporal context
```

**Implementation**:
```python
def temporal_rag(query):
    # Detect temporal intent
    time_intent = extract_time(query)  # "current", "2023", "latest"
    
    # Time-based retrieval
    if time_intent == "current" or time_intent == "latest":
        # Prioritize recent
        results = vector_db.search(
            query,
            filter={"date": {"$gte": "2024-01-01"}},
            boost_recent=True
        )
    elif time_intent == "historical":
        # All time range
        results = vector_db.search(query)
    else:
        # Specific time
        results = vector_db.search(
            query,
            filter={"date": time_intent}
        )
    
    # Add temporal context to prompt
    prompt = f"Using information from {time_intent}, answer: {query}"
    return llm.generate(prompt, results)
```

**Metadata Schema**:
```json
{
  "text": "...",
  "published_date": "2024-07-03",
  "last_updated": "2024-07-03",
  "valid_from": "2024-01-01",
  "valid_until": "2024-12-31",
  "version": "2.3"
}
```

**AWS Components**:
- OpenSearch (date range filtering)
- Bedrock (temporal reasoning)
- EventBridge (document expiration)

**Use Cases**:
- Financial data (prices, rates, reports)
- Medical guidelines (protocols, treatments)
- Legal documents (regulations, laws)
- News and current events
- Product specifications

---

### Pattern 33: **Federated RAG** 🌐 Multi-Source
**Source**: Google Search, Perplexity  
**Problem Solved**: Information scattered across multiple systems

**Real Scenario**:
- Company has:
  - Internal docs in SharePoint
  - Code in GitHub
  - Slack conversations
  - Confluence wiki
  - External partner APIs

**Architecture**:
```
Query → Parallel search across:
         ├─ Internal vector DB
         ├─ External APIs
         ├─ Real-time data sources
         └─ Web search
      → Merge and deduplicate
      → Rerank combined results
      → Generate unified answer
```

**Implementation**:
```python
async def federated_rag(query):
    # Parallel searches
    results = await asyncio.gather(
        search_internal_docs(query),
        search_github(query),
        search_slack(query),
        search_confluence(query),
        search_web(query)
    )
    
    # Merge and deduplicate
    merged = merge_and_dedup(results)
    
    # Rerank across sources
    reranked = rerank(query, merged, top_k=10)
    
    # Generate with source attribution
    answer = llm.generate_with_sources(query, reranked)
    
    return answer
```

**Challenges**:
1. **Authentication**: Each source needs credentials
2. **Latency**: Slowest source blocks response
3. **Cost**: Multiple API calls
4. **Consistency**: Different data formats

**Solutions**:
- Cache frequently accessed sources
- Timeout fast failures
- Prioritize high-value sources
- Standardize metadata format

**AWS Components**:
- Lambda (parallel orchestration)
- API Gateway (source connectors)
- DynamoDB (caching layer)
- Bedrock (generation)

---

### Pattern 34: **Guardrailed RAG** 🛡️ Safety Critical
**Source**: NVIDIA NeMo Guardrails, LlamaGuard  
**Problem Solved**: Unsafe or policy-violating responses

**Real Failure Cases**:
1. Medical RAG gives harmful advice
2. HR bot leaks salary information
3. Customer support shares internal pricing

**Architecture**:
```
Query → Input Guardrails (check query safety)
      → Retrieve documents
      → Output Guardrails (check response safety)
      → Safe response or rejection
```

**Guardrail Types**:

1. **Input Guardrails**:
   - Jailbreak detection
   - PII in query
   - Off-topic detection
   - Hate speech filter

2. **Output Guardrails**:
   - Hallucination detection
   - Factuality check
   - PII leakage prevention
   - Topic compliance

3. **Retrieval Guardrails**:
   - Sensitive document filtering
   - Access control enforcement

**Implementation**:
```python
def guardrailed_rag(query, user_role):
    # Input guardrails
    if is_jailbreak(query):
        return "I can't assist with that request."
    
    if contains_pii(query):
        query = remove_pii(query)
    
    # Retrieval with access control
    chunks = retrieve_with_access_control(query, user_role)
    
    # Generate
    answer = llm.generate(query, chunks)
    
    # Output guardrails
    if contains_hallucination(answer, chunks):
        return "I need to verify that information."
    
    if contains_sensitive_info(answer, user_role):
        answer = redact_sensitive(answer, user_role)
    
    return answer
```

**AWS Components**:
- Bedrock (guardrail capabilities)
- Comprehend (PII detection)
- Lambda (custom guardrails)

**Compliance Use Cases**:
- Healthcare (HIPAA)
- Finance (SOX, GDPR)
- Legal (attorney-client privilege)
- HR (employee data protection)

---

### Pattern 35: **Active Retrieval RAG** 🎯 Precision Optimization
**Source**: Research papers, advanced systems  
**Problem Solved**: Retrieval happens before seeing LLM needs

**Traditional RAG Problem**:
```
Query → Retrieve (fixed top-k)
      → LLM: "I need more info on X, but got Y"
      → No way to get X
```

**Active Retrieval Solution**:
```
Query → Initial Retrieve (small top-k)
      → LLM attempts answer
      → LLM: "Need more info on X"
      → Additional Retrieve (targeted)
      → LLM completes answer
```

**Implementation**:
```python
def active_retrieval_rag(query):
    # Initial retrieval
    chunks = retrieve(query, top_k=3)
    
    # First generation attempt with reflection
    prompt = f"""
    Context: {chunks}
    Question: {query}
    
    If you have enough information, answer the question.
    If you need more information, specify what you need in format:
    NEED_INFO: <what you need>
    """
    
    response = llm.generate(prompt)
    
    # Check if more retrieval needed
    while "NEED_INFO:" in response:
        needed = extract_need(response)
        additional = retrieve(needed, top_k=2)
        chunks.extend(additional)
        
        # Retry with more context
        response = llm.generate(query, chunks)
    
    return response
```

**Benefits**:
- Adaptive retrieval depth
- Targeted information gathering
- Reduced hallucination
- Better context utilization

**AWS Components**:
- Bedrock (with tool calling)
- OpenSearch (multiple retrieval rounds)
- Lambda (orchestration)

---

### Pattern 36: **Explainable RAG** 🔍 Transparency
**Source**: Enterprise AI requirements, regulated industries  
**Problem Solved**: Black box decisions unacceptable

**Requirements**:
- Show which documents influenced answer
- Explain why documents were selected
- Trace reasoning path
- Provide confidence scores

**Architecture**:
```
Query → Retrieve with scores
      → Generate with reasoning
      → Return:
         - Answer
         - Source chunks with relevance scores
         - Reasoning trace
         - Confidence assessment
```

**Implementation**:
```python
def explainable_rag(query):
    # Retrieve with detailed scores
    chunks = retrieve_with_scores(query, top_k=5)
    
    # Explain retrieval
    retrieval_explanation = {
        'query_embedding': query_vector,
        'chunks': [
            {
                'text': chunk.text,
                'similarity_score': chunk.score,
                'source': chunk.metadata,
                'why_retrieved': explain_similarity(query, chunk)
            }
            for chunk in chunks
        ]
    }
    
    # Generate with reasoning
    prompt = f"""
    Answer the question and explain your reasoning.
    
    Context: {chunks}
    Question: {query}
    
    Format:
    ANSWER: [your answer]
    REASONING: [which parts of context you used and why]
    CONFIDENCE: [high/medium/low] because [explanation]
    """
    
    response = llm.generate(prompt)
    
    return {
        'answer': extract_answer(response),
        'reasoning': extract_reasoning(response),
        'confidence': extract_confidence(response),
        'retrieval_explanation': retrieval_explanation,
        'chunks_used': identify_chunks_used(response, chunks)
    }
```

**Output Example**:
```json
{
  "answer": "AWS EC2 t3.micro costs $0.0104/hour in us-east-1",
  "reasoning": "Found pricing in AWS pricing document from chunk 2, cross-referenced with chunk 4 for region confirmation",
  "confidence": {
    "level": "high",
    "reason": "Multiple consistent sources, recent data (2024-07-01)"
  },
  "sources": [
    {
      "chunk_id": 2,
      "text": "t3.micro: $0.0104 per hour",
      "relevance": 0.94,
      "used_in_answer": true
    }
  ]
}
```

**AWS Components**:
- Bedrock (reasoning traces)
- OpenSearch (score tracking)
- CloudWatch (audit trails)

**Use Cases**:
- Financial advice (SEC compliance)
- Medical decisions (liability)
- Legal research (case justification)
- Insurance claims (decision explanation)

---

### Pattern 37: **Synthetic Data RAG** 🔄 Data Flywheel
**Source**: NVIDIA Data Flywheel, OpenAI fine-tuning  
**Problem Solved**: Limited training data for domain-specific RAG

**The Problem**:
- RAG performance depends on:
  - Quality of embeddings
  - Quality of retrieval
  - Quality of generation
- But domain-specific evaluation data is scarce

**Solution - Generate Synthetic Q&A**:
```
Documents → Extract passages
         → Generate questions (LLM)
         → Validate questions (LLM + human)
         → Create Q&A pairs
         → Fine-tune embedding model
         → Evaluate and iterate
```

**Implementation**:
```python
def generate_synthetic_qa(documents):
    qa_pairs = []
    
    for doc in documents:
        # Extract key passages
        passages = chunk_document(doc)
        
        for passage in passages:
            # Generate questions
            prompt = f"""
            Generate 3 questions that can be answered using this passage.
            Make them varied: factual, analytical, and comparison.
            
            Passage: {passage}
            
            Questions:
            """
            questions = llm.generate(prompt)
            
            # Create Q&A pairs
            for question in parse_questions(questions):
                qa_pairs.append({
                    'question': question,
                    'answer': passage,
                    'document_id': doc.id
                })
    
    return qa_pairs

# Use for evaluation
def evaluate_rag(qa_pairs):
    scores = []
    for qa in qa_pairs:
        # Retrieve for synthetic question
        chunks = retrieve(qa['question'])
        
        # Check if correct passage retrieved
        if qa['answer'] in chunks:
            scores.append(1)
        else:
            scores.append(0)
    
    recall = sum(scores) / len(scores)
    return recall
```

**Data Flywheel Loop**:
```
1. Deploy RAG
   ↓
2. Collect real queries
   ↓
3. Generate synthetic variations
   ↓
4. Evaluate retrieval quality
   ↓
5. Fine-tune embedding model
   ↓
6. Re-deploy improved RAG
   ↓
7. Collect more data → Loop to step 2
```

**AWS Components**:
- Bedrock (question generation)
- SageMaker (embedding fine-tuning)
- S3 (synthetic data storage)
- Step Functions (flywheel orchestration)

**Benefits**:
- Continuous improvement
- Domain adaptation
- Quality measurement
- Reduced manual annotation

---

## Implementation Priority

### High Priority (Implement First)
1. ✅ **Pattern 26: Reranking RAG** - Immediate accuracy boost
2. ✅ **Pattern 27: Fallback RAG** - Reliability improvement
3. ✅ **Pattern 28: Citation RAG** - Trust and verification
4. ✅ **Pattern 29: Hybrid Search** - Better retrieval

### Medium Priority
5. **Pattern 24: Query Decomposition** - Complex queries
6. **Pattern 30: Streaming RAG** - UX improvement
7. **Pattern 32: Temporal RAG** - Time-sensitive domains
8. **Pattern 34: Guardrailed RAG** - Safety requirements

### Advanced (Later)
9. **Pattern 25: Structured Data RAG** - Tabular data
10. **Pattern 31: Multi-Tenancy RAG** - Enterprise
11. **Pattern 33: Federated RAG** - Multi-source
12. **Pattern 35: Active Retrieval** - Optimization
13. **Pattern 36: Explainable RAG** - Compliance
14. **Pattern 37: Synthetic Data RAG** - Continuous improvement

---

## Next Steps

1. **Review proposal with user**
2. **Select patterns to implement** (recommend starting with 24-30)
3. **Create AWS notebooks** for each pattern
4. **Test with real use cases**
5. **Document failure cases and solutions**
6. **Measure performance improvements**

---

## Cost-Benefit Analysis

| Pattern | Complexity | Impact | Priority |
|---------|-----------|--------|----------|
| Reranking | Low | High | P0 |
| Fallback | Low | High | P0 |
| Citation | Low | High | P0 |
| Hybrid Search | Low | High | P0 |
| Query Decomposition | Medium | High | P1 |
| Streaming | Low | Medium | P1 |
| Temporal | Medium | Medium | P1 |
| Guardrailed | Medium | High | P1 |
| Structured Data | Medium | Medium | P2 |
| Multi-Tenancy | High | High | P2 |
| Federated | High | Medium | P2 |
| Active Retrieval | High | Medium | P3 |
| Explainable | Medium | Medium | P3 |
| Synthetic Data | High | High | P3 |

---

**Total New Patterns**: 14 (24-37)  
**Focus**: Production reliability, failure recovery, enterprise needs  
**All based on**: Real-world implementations and documented failure cases
