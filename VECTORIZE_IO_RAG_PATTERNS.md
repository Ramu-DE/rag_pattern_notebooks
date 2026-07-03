# Vectorize.io RAG Patterns & Hindsight Memory System

## Based on Official Vectorize.io Website & Blog Posts

**Research Date**: 2026-07-03  
**Sources**: vectorize.io, blog posts, documentation

---

## Company Overview

**Vectorize.io** provides:
1. **Hindsight** - Open-source agent memory system (MIT licensed)
2. **RAG Platform** - Complete RAG pipeline with evaluation tools
3. **MCP Integration** - Model Context Protocol for agentic workflows

**Notable Customers**: NVIDIA, Groq, Electronic Arts, Bronson, Brightness

**Compliance**: SOC2 Type 2 Certified

---

## Pattern 1: **Hybrid Retrieval RAG** 🔍
**Source**: Vectorize.io Blog (Sept 2025) - Launch Week Day 4

### Problem Solved
Single retrieval mode fails for diverse query types:
- Pure vector search misses exact keywords (product codes, error codes)
- Pure keyword search misses semantic meaning
- Need both precision AND conceptual understanding

### Three Retrieval Modes

**1. Vector Search** (Semantic):
```
Query: "documents about financial performance"
→ Finds: Q3 reports, earnings analysis, revenue discussions
→ Matches: Conceptual similarity
```

**2. Text Search** (Exact):
```
Query: "error code E-4729"
→ Finds: Exact matches for "E-4729"
→ Matches: Keyword precision
```

**3. Hybrid Search** (Combined):
```
Query: "Q3 revenue guidance"
→ Finds: Documents that are:
  - Semantically about revenue guidance AND
  - Contain exact term "Q3"
→ Matches: Semantic + Exact
```

### Architecture

```
User Query
    ↓
Query Analysis
    ├─ Extract semantic intent
    └─ Extract exact keywords
    ↓
Parallel Search
    ├─ Vector Search (semantic)
    └─ Text Search (keywords)
    ↓
Score Combination
    → Weighted fusion (RRF or custom)
    ↓
Metadata Filtering
    → Boolean logic (AND, OR, NOT)
    → Range queries (dates, numbers)
    ↓
Final Results
```

### Advanced Filtering

**Boolean Logic**:
```python
filter = {
    "AND": [
        {"field": "date", "gte": "2024-Q3"},
        {
            "OR": [
                {"field": "priority", "eq": "high"},
                {"field": "department", "eq": "finance"}
            ]
        },
        {
            "NOT": {"field": "status", "eq": "draft"}
        }
    ]
}

# Q3 2024 docs that are (high-priority OR finance), but not drafts
```

**Range Queries**:
```python
filter = {
    "date": {"gte": "2024-01-01", "lte": "2024-12-31"},
    "priority": {"gte": 5},
    "department": {"in": ["engineering", "product"]}
}
```

### When to Use Each Mode

| Query Type | Best Mode | Example |
|------------|-----------|---------|
| Conceptual | Vector | "How to improve performance?" |
| Exact terms | Text | "SKU-4729 specifications" |
| Mixed | Hybrid | "Q3 2024 AWS pricing" |
| Filtered | Hybrid + Metadata | "Recent high-priority finance docs" |

### Implementation

**Retrieval Endpoint**:
```python
response = vectorize.retrieve(
    query="Q3 revenue guidance",
    mode="hybrid",  # "vector", "text", or "hybrid"
    filters={
        "AND": [
            {"field": "date", "gte": "2024-Q3"},
            {"field": "type", "eq": "guidance"}
        ]
    },
    top_k=10
)

for result in response.results:
    print(f"Score: {result.score}")
    print(f"Text: {result.text}")
    print(f"Metadata: {result.metadata}")
```

### Key Benefits
- ✅ Semantic understanding (vector)
- ✅ Exact keyword matching (text)
- ✅ Structured filtering (metadata)
- ✅ Flexible combination logic

---

## Pattern 2: **Metadata-Enhanced RAG** 📋
**Source**: Vectorize.io Blog (Sept 2025)

### Problem Solved
Raw text retrieval lacks structure:
- Can't filter by document type, date, author
- Can't prioritize based on metadata fields
- Can't combine semantic + structured queries

### Three Metadata Types

**1. System Metadata** (Auto-captured):
```json
{
  "filename": "Q3_Report.pdf",
  "created_at": "2024-07-15T10:30:00Z",
  "modified_at": "2024-07-15T14:22:00Z",
  "source": "google_drive",
  "file_size": 2458123,
  "page_count": 45
}
```

**2. User-Defined Metadata** (Custom):
```json
{
  "department": "finance",
  "document_type": "earnings_report",
  "quarter": "Q3",
  "year": 2024,
  "confidential": true,
  "priority": "high",
  "tags": ["revenue", "guidance", "analyst"]
}
```

**3. Automatic Extraction** (Iris Model):
```python
# Define schema
schema = {
    "fields": [
        {"name": "company_name", "type": "string"},
        {"name": "revenue", "type": "number"},
        {"name": "report_date", "type": "date"},
        {"name": "industry", "type": "string"}
    ]
}

# Iris model automatically extracts from unstructured docs
extracted_metadata = iris_model.extract(document, schema)
```

### Architecture

```
Document Ingestion
    ↓
Automatic Field Extraction
    ├─ System metadata (timestamps, source)
    ├─ User metadata (tags, categories)
    └─ Iris extraction (structured fields)
    ↓
Vector DB with Metadata
    → Each chunk has:
      - Text embedding
      - Full metadata dictionary
    ↓
Retrieval with Filters
    → Semantic search + Metadata filtering
```

### Implementation Patterns

**Schema Definition** (Visual Editor):
```python
# Define what to extract from documents
metadata_schema = {
    "customer_name": {"type": "string", "required": True},
    "contract_value": {"type": "number", "unit": "USD"},
    "start_date": {"type": "date"},
    "end_date": {"type": "date"},
    "renewal_status": {"type": "enum", "values": ["active", "pending", "expired"]},
    "account_manager": {"type": "string"}
}

vectorize.create_pipeline(
    source="contracts_folder",
    metadata_schema=metadata_schema,
    auto_extract=True  # Use Iris model
)
```

**Retrieval with Metadata**:
```python
# Complex query: semantic + structured
response = vectorize.retrieve(
    query="high-value contracts expiring soon",
    mode="hybrid",
    filters={
        "AND": [
            {"contract_value": {"gte": 100000}},
            {"end_date": {"lte": "2024-12-31"}},
            {"renewal_status": {"eq": "pending"}},
            {
                "OR": [
                    {"department": "enterprise"},
                    {"account_manager": "senior_team"}
                ]
            }
        ]
    },
    metadata_boost={
        "priority": 2.0,  # 2x boost for priority field
        "confidential": 0.5  # 0.5x for confidential (lower)
    }
)
```

### Use Cases

**Customer Support**:
```python
# Find recent high-priority issues
retrieve(
    query="authentication problems",
    filters={
        "created_at": {"gte": "7_days_ago"},
        "priority": {"in": ["high", "critical"]},
        "status": {"eq": "open"}
    }
)
```

**Compliance**:
```python
# Find specific regulatory documents
retrieve(
    query="GDPR data retention",
    filters={
        "document_type": "policy",
        "compliance_area": "GDPR",
        "approved": True,
        "version": {"gte": "2.0"}
    }
)
```

**Sales**:
```python
# Find relevant opportunities
retrieve(
    query="cloud migration projects",
    filters={
        "deal_stage": {"in": ["negotiation", "proposal"]},
        "deal_size": {"gte": 50000},
        "industry": {"in": ["finance", "healthcare"]}
    }
)
```

### Key Innovations
- ✅ Automatic extraction (Iris model)
- ✅ Visual schema editor (no code)
- ✅ Multi-level metadata (system + user + extracted)
- ✅ Complex boolean filtering
- ✅ Metadata boosting for relevance

---

## Pattern 3: **Real-Time RAG** ⚡
**Source**: Vectorize.io Blog (Sept 2025)

### Problem Solved
Traditional RAG has stale data:
- Manual pipeline runs (batch processing)
- Scheduled updates (hourly/daily lag)
- Re-deployment needed for new documents
- Users get outdated information

### Architecture: Event-Driven Updates

```
Source System (Google Docs, S3, Database)
    ↓
Change Detection (Webhook or Polling)
    ↓
Automatic Reprocessing
    ├─ Document edited → Re-extract + Re-embed
    ├─ New file added → Extract + Embed + Index
    └─ File deleted → Remove from index
    ↓
Vector DB Update (Live)
    → Usually within minutes
    ↓
Agents Access Fresh Data
```

### Implementation

**Setup Real-Time Pipeline**:
```python
pipeline = vectorize.create_pipeline(
    source="google_drive://shared_folder",
    real_time=True,  # Premium feature
    webhook_url="https://your-app.com/webhook",
    events=["document.created", "document.updated", "document.deleted"]
)

# Configure processing
pipeline.configure(
    chunk_size=512,
    chunk_overlap=50,
    embedding_model="voyage-2",
    auto_metadata=True
)
```

**Webhook Handler** (Optional):
```python
@app.post("/webhook")
def handle_vectorize_event(event: Event):
    if event.type == "document.processed":
        # Document now available in vector DB
        notify_agents(f"New data available: {event.document_id}")
    
    elif event.type == "document.failed":
        # Handle processing errors
        log_error(event.error)
        retry_processing(event.document_id)
```

### Supported Operations

**1. Document Edits**:
```
User edits Google Doc
    ↓ (webhook fires)
Vectorize re-extracts content
    ↓
Re-generates embeddings
    ↓
Updates vector DB entries
    ↓ (< 5 minutes)
Agents see updated content
```

**2. New Documents**:
```
New file added to S3
    ↓ (S3 event notification)
Vectorize processes file
    ↓
Generates chunks + embeddings
    ↓
Adds to vector DB
    ↓ (< 5 minutes)
Searchable immediately
```

**3. Deletions**:
```
File deleted from source
    ↓ (deletion event)
Vectorize removes entries
    ↓
Vector DB cleaned up
    ↓
No longer returned in searches
```

### Configuration Options

```python
real_time_config = {
    "enabled": True,
    "processing_priority": "high",  # "low", "normal", "high"
    "batch_size": 10,  # Process N docs before indexing
    "retry_attempts": 3,
    "retry_delay": "exponential",  # 1s, 2s, 4s, 8s...
    "failure_notification": "email@company.com",
    "sources": [
        {
            "type": "google_drive",
            "folder_id": "abc123",
            "watch_subfolders": True
        },
        {
            "type": "s3",
            "bucket": "docs-bucket",
            "prefix": "knowledge-base/",
            "notifications": True
        }
    ]
}
```

### Performance Characteristics

| Metric | Value |
|--------|-------|
| **Processing Time** | Usually < 5 minutes |
| **Detection Latency** | Seconds (webhook) to minutes (polling) |
| **Throughput** | Handles burst updates |
| **Availability** | Premium add-on |

### Use Cases

**Customer Documentation**:
- Product docs updated → Agents answer with latest features
- Support KB modified → Chatbots give current guidance
- API docs changed → Code assistants use new endpoints

**Internal Knowledge**:
- Team wiki edited → Company chatbot reflects updates
- Policies updated → Compliance agent uses new rules
- Meeting notes added → Context available immediately

**Dynamic Content**:
- News articles published → Research agent accesses current events
- Database records changed → Query agent has fresh data
- CRM updates → Sales agent sees latest opportunities

### Key Benefits
- ✅ No manual pipeline runs
- ✅ No re-deployments needed
- ✅ Fresh data always (< 5 min lag)
- ✅ Event-driven architecture
- ✅ Automatic error handling

---

## Pattern 4: **RAG Evaluation Framework** 🧪
**Source**: Vectorize.io Documentation

### Problem Solved
RAG performance varies wildly based on:
- Embedding model choice
- Chunk size and overlap
- Metadata extraction strategy
- But no way to know what works best for YOUR data

### Evaluation Workflow

```
Your Documents
    ↓
Generate Test Cases
    → Synthetic Q&A pairs from docs
    ↓
Test Multiple Configurations
    ├─ Embedding: OpenAI vs Voyage vs Cohere
    ├─ Chunk size: 256 vs 512 vs 1024
    └─ Overlap: 0 vs 50 vs 100 tokens
    ↓
Measure Performance
    → Retrieval accuracy, latency, cost
    ↓
Select Best Configuration
    → Typically completes < 1 minute
    ↓
Materialize as Pipeline
    → Deploy winner to production
```

### Metrics Evaluated

**1. Retrieval Accuracy**:
- Precision: % relevant in top-K
- Recall: % of all relevant found
- MRR (Mean Reciprocal Rank)
- NDCG (Normalized Discounted Cumulative Gain)

**2. Performance**:
- Query latency (ms)
- Indexing time
- Storage size

**3. Cost**:
- Embedding API costs
- Vector DB storage
- Query costs

### Implementation

```python
# Define evaluation experiment
experiment = vectorize.evaluate_rag(
    documents=["doc1.pdf", "doc2.pdf", "doc3.pdf"],
    
    # Test these embedding models
    embedding_models=[
        "openai/text-embedding-3-small",
        "voyage/voyage-2",
        "cohere/embed-english-v3.0"
    ],
    
    # Test these chunk sizes
    chunk_sizes=[256, 512, 1024],
    
    # Test these overlap strategies
    chunk_overlaps=[0, 50, 100],
    
    # Test queries (auto-generated + custom)
    test_queries="auto",  # or provide custom queries
    
    # Evaluation metrics
    metrics=["accuracy", "latency", "cost"]
)

# Run evaluation (< 1 min)
results = experiment.run()

# View results
print(results.summary())
"""
┌─────────────────────┬──────────┬─────────┬────────┐
│ Configuration       │ Accuracy │ Latency │ Cost   │
├─────────────────────┼──────────┼─────────┼────────┤
│ voyage-2 / 512 / 50 │ 94.2%    │ 45ms    │ $0.02  │
│ openai-3 / 512 / 50 │ 91.8%    │ 38ms    │ $0.01  │
│ cohere-3 / 512 / 50 │ 89.5%    │ 52ms    │ $0.03  │
└─────────────────────┴──────────┴─────────┴────────┘

Winner: voyage-2 / 512 / 50 (best accuracy)
"""

# Deploy winner to production
results.materialize_best(
    pipeline_name="production-rag",
    vector_db="pinecone://prod"
)
```

### Test Query Generation

**Automatic**:
```python
# Vectorize generates test queries from documents
test_queries = vectorize.generate_test_queries(
    documents=docs,
    num_queries=100,
    difficulty_levels=["easy", "medium", "hard"],
    query_types=["factual", "comparative", "analytical"]
)
```

**Custom**:
```python
# Or provide your own
test_queries = [
    {
        "query": "What is the refund policy?",
        "expected_docs": ["refund_policy.pdf"],
        "min_score": 0.8
    },
    {
        "query": "How do I reset my password?",
        "expected_docs": ["account_help.pdf", "security_faq.pdf"],
        "min_score": 0.7
    }
]
```

### Best Practices

**1. Representative Test Set**:
- Include diverse query types
- Cover all document categories
- Mix easy and hard questions
- Include edge cases

**2. Iterative Optimization**:
```python
# Start broad
initial = evaluate_rag(
    embedding_models=["all"],
    chunk_sizes=[256, 512, 1024, 2048]
)

# Narrow down
refined = evaluate_rag(
    embedding_models=initial.top_3_models,
    chunk_sizes=initial.top_2_sizes,
    chunk_overlaps=[0, 25, 50, 75, 100]
)

# Fine-tune winner
final = evaluate_rag(
    embedding_models=[refined.winner.model],
    chunk_sizes=[refined.winner.size],
    chunk_overlaps=[refined.winner.overlap - 10, 
                    refined.winner.overlap, 
                    refined.winner.overlap + 10]
)
```

**3. Re-evaluate Periodically**:
- When documents change significantly
- When new embedding models available
- When query patterns shift
- Monthly or quarterly

### Key Benefits
- ✅ Data-driven configuration
- ✅ Fast iteration (< 1 min)
- ✅ No guesswork
- ✅ Quantified improvements
- ✅ One-click deployment

---

## Pattern 5: **Hindsight Memory System** 🧠
**Source**: Vectorize.io Hindsight Product

### Problem Solved
Traditional RAG is stateless:
- No user-specific context
- No learning from interactions
- No consolidation of knowledge
- Each query is isolated

### Architecture: Beyond Retrieval

```
Traditional RAG:
  Query → Retrieve → Generate → Forget

Hindsight:
  Query → Retrieve + Recall Memory → Generate → Learn → Remember
           ↓                                       ↓
     Vector Search                          Reflection Layer
     (documents)                             (consolidate patterns)
```

### Three Core Capabilities

**1. Per-User Memory**:
```python
# User A's preferences
hindsight.remember(
    user_id="user_a",
    memory={
        "type": "preference",
        "content": "Prefers detailed technical explanations",
        "source": "conversation",
        "timestamp": "2024-07-03T10:30:00Z"
    }
)

# User B's preferences (separate)
hindsight.remember(
    user_id="user_b",
    memory={
        "type": "preference",
        "content": "Prefers executive summaries only",
        "source": "conversation",
        "timestamp": "2024-07-03T10:31:00Z"
    }
)

# Recall returns user-specific memories
user_a_memories = hindsight.recall(
    user_id="user_a",
    query="how should I explain this?"
)
# Returns: "Prefers detailed technical explanations"
```

**2. Cross-Session Persistence**:
```python
# Session 1 (Monday)
hindsight.remember(
    user_id="user_123",
    memory={
        "type": "context",
        "content": "Working on Q3 sales forecast, using Prophet model",
        "session_id": "session_001"
    }
)

# Session 2 (Friday - weeks later)
memories = hindsight.recall(
    user_id="user_123",
    query="where did we leave off?"
)
# Returns: "Working on Q3 sales forecast, using Prophet model"
# Even weeks later, context preserved
```

**3. Fast Parallel Recall** (< 100ms):
```python
# Multiple memory searches in parallel
results = hindsight.recall(
    user_id="user_123",
    queries=[
        "user preferences",
        "recent project context",
        "past tool failures",
        "learned patterns"
    ],
    parallel=True
)
# Returns all in < 100ms
```

### The Learning Layer

**Experience → Knowledge → Judgment**:

```
Level 1: Raw Experiences (Facts)
  • "User corrected: timezone should be PST not EST"
  • "Tool call to Linear API failed with 401"
  • "User prefers bullet points over paragraphs"

       ↓ (Reflection Layer)

Level 2: Synthesized Knowledge (Patterns)
  • "User is in PST timezone"
  • "Linear API requires OAuth refresh"
  • "User prefers concise formats"

       ↓ (Consolidation)

Level 3: Mental Models (Judgment)
  • "Always use PST for this user's timestamps"
  • "Check token expiry before Linear calls"
  • "Default to bullet points for this user"
```

### Implementation

**MCP Integration** (3 Tools):

```python
# 1. Remember (store experience)
remember = {
    "name": "remember",
    "description": "Store a fact, preference, or experience",
    "parameters": {
        "content": "User prefers morning meetings",
        "type": "preference",
        "context": "Scheduling discussion"
    }
}

# 2. Recall (retrieve memories)
recall = {
    "name": "recall",
    "description": "Search memories for relevant context",
    "parameters": {
        "query": "user meeting preferences",
        "limit": 5
    }
}

# 3. Reflect (consolidate patterns)
reflect = {
    "name": "reflect",
    "description": "Synthesize experiences into knowledge",
    "parameters": {
        "experiences": ["exp1", "exp2", "exp3"],
        "consolidate": True
    }
}
```

**Setup** (One Command):
```bash
npx add-skill vectorize-io/hindsight --skill hindsight-docs
```

### Memory Types

**1. Facts**:
```json
{
  "type": "fact",
  "content": "User's company is Acme Corp",
  "source": "user_message",
  "confidence": 1.0
}
```

**2. Preferences**:
```json
{
  "type": "preference",
  "content": "Prefers Python over JavaScript",
  "source": "observed_behavior",
  "strength": 0.8
}
```

**3. Experiences**:
```json
{
  "type": "experience",
  "content": "GitHub API call failed with rate limit",
  "source": "tool_failure",
  "action_taken": "Switched to GraphQL API"
}
```

**4. Patterns** (Synthesized):
```json
{
  "type": "pattern",
  "content": "User asks about deployment every Friday afternoon",
  "source": "reflection",
  "occurrences": 8,
  "confidence": 0.95
}
```

### Compound Memory (Multi-Agent)

**Scenario**: Company with multiple AI agents

```python
# Agent A learns user preference
agent_a.remember(
    user_id="user_123",
    memory={
        "type": "preference",
        "content": "Prefers Slack notifications over email",
        "shared": True  # Make available to other agents
    }
)

# Agent B automatically applies it
agent_b_context = hindsight.recall(
    user_id="user_123",
    query="notification preferences"
)
# Returns: "Prefers Slack notifications"
# Agent B uses Slack without asking
```

### Benchmarks

**LongMemEval Results**:
- **Hindsight**: 94.6%
- Supermemory: 85.2%
- Zep: 71.2%
- GPT-4o (no memory): 60.2%

**Performance**:
- Recall latency: < 100ms
- Storage: Unlimited (cloud)
- Context persistence: Permanent (until deleted)

### Use Cases

**Customer Support**:
- Remember customer's product, industry, preferences
- Recall past issues and resolutions
- Learn common failure patterns

**Personal Assistant**:
- Remember user's schedule preferences
- Track ongoing projects and status
- Learn communication style

**Development Copilot**:
- Remember codebase conventions
- Track attempted solutions (failures and successes)
- Learn user's coding patterns

**Sales Agent**:
- Remember prospect's pain points
- Track deal stage and history
- Learn objection patterns

### Key Innovations
- ✅ Per-user isolation
- ✅ Cross-session persistence
- ✅ Active learning (reflection)
- ✅ Pattern synthesis
- ✅ Sub-100ms recall
- ✅ Model-agnostic
- ✅ Open source (MIT)

---

## Pattern 6: **Agentic Retrieval + MCP Tools** 🤖
**Source**: Vectorize.io Blog (Nov 2025)

### Problem Solved
Traditional RAG is read-only:
- Can retrieve information
- Can't take actions
- Can't update systems
- Can't integrate with operational tools

### Architecture: RAG + Actions

```
Traditional RAG:
  Query → Retrieve → Generate → Response

Agentic RAG:
  Query → Retrieve + Tool Selection → Generate + Execute → Response + Action
           ↓                                     ↓
     Vector Search                        MCP Tool Calls
     (knowledge)                         (create issue, update CRM, query DB)
```

### MCP (Model Context Protocol) Integration

**Available Tools**:
- Linear: Create/update issues
- GitHub: Search issues, create PRs
- Slack: Send messages, search conversations
- CRM: Update records, search contacts
- Databases: Query data, update records
- Custom APIs: Any MCP-compatible server

### Implementation

**Setup MCP Server**:
```python
# In Vectorize agent admin panel
mcp_config = {
    "name": "Linear",
    "url": "https://mcp.linear.app/mcp",
    "auth": {
        "type": "oauth2.1",
        "client_id": "your_client_id",
        "scopes": ["read:issues", "write:issues"]
    },
    "enabled_tools": [
        "linear.search_issues",
        "linear.create_issue",
        "linear.update_issue"
    ]
}

vectorize.add_mcp_server(mcp_config)
```

**Agent Workflow**:
```python
# Agent has access to:
# 1. Vectorize retrieval (knowledge)
# 2. Linear MCP tools (actions)

user_query = "What bugs were reported last week? Create issues for critical ones."

# Agent reasoning:
# Step 1: Retrieve from Intercom conversations
support_convos = vectorize.retrieve(
    query="bugs reported",
    filters={"created_at": {"gte": "7_days_ago"}},
    source="intercom_pipeline"
)

# Step 2: Synthesize findings
bugs = agent.synthesize(support_convos)
# [
#   {"summary": "Login fails on Safari", "severity": "critical"},
#   {"summary": "Typo in email", "severity": "minor"}
# ]

# Step 3: Use MCP tool for critical bugs
for bug in bugs:
    if bug["severity"] == "critical":
        linear.create_issue(
            title=bug["summary"],
            description=f"Reported by: {bug['user']}\nDetails: {bug['details']}",
            priority="urgent",
            team="engineering"
        )

# Response to user:
# "Found 2 bugs. Created Linear issues for 1 critical bug (login issue).
#  Minor typo noted but not urgent."
```

### Real-World Example: Support-to-Engineering Pipeline

**Setup**:
```python
# 1. Create Intercom pipeline
intercom_pipeline = vectorize.create_pipeline(
    source="intercom://conversations",
    schedule="every 1 hour",
    metadata_extract={
        "created_at": "timestamp",
        "user_email": "user.email",
        "conversation_tags": "tags"
    }
)

# 2. Add Linear MCP server
linear_mcp = vectorize.add_mcp_server(
    url="https://mcp.linear.app/mcp",
    auth_method="oauth2.1"
)

# 3. Enable tools
linear_mcp.enable_tools([
    "search_issues",
    "create_issue",
    "add_comment"
])
```

**Agent Behavior**:
```
User: "What features did users request last week? 
       Create a Linear issue to track them."

Agent Internal Process:
1. [Tool: vectorize.retrieve]
   - Query: "feature requests"
   - Filter: created_at >= 7 days ago
   - Source: intercom_pipeline
   
2. [Synthesis]
   - Found 12 conversations
   - Identified 5 distinct features:
     • Dark mode (requested 4x)
     • Export to CSV (requested 3x)
     • Mobile app (requested 2x)
     • SSO integration (requested 2x)
     • Bulk operations (requested 1x)

3. [Tool: linear.create_issue]
   - Title: "Feature Request: Dark Mode"
   - Description: "Requested by 4 users in past week..."
   - Labels: ["feature-request", "ui"]
   - Priority: "high"
   
   (Repeat for top 3 features)

Agent Response:
"Found 5 feature requests from last week. Created Linear issues 
for top 3:
- #ENG-421: Dark mode (4 requests)
- #ENG-422: CSV export (3 requests)  
- #ENG-423: Mobile app (2 requests)

SSO and bulk operations noted but lower priority."
```

### Authentication Options

**1. Bearer Token**:
```json
{
  "auth_type": "bearer",
  "headers": {
    "Authorization": "Bearer YOUR_TOKEN"
  }
}
```

**2. OAuth 2.1** (Recommended):
```json
{
  "auth_type": "oauth2.1",
  "client_id": "your_client_id",
  "authorization_endpoint": "https://api.service.com/oauth/authorize",
  "token_endpoint": "https://api.service.com/oauth/token",
  "scopes": ["read", "write"],
  "auto_refresh": true
}
```

**3. Custom Headers**:
```json
{
  "auth_type": "custom",
  "headers": {
    "X-API-Key": "your_key",
    "X-Client-ID": "your_client_id"
  }
}
```

### Security Features

- ✅ HTTPS encryption (all connections)
- ✅ Per-agent OAuth (isolated credentials)
- ✅ Token auto-refresh (no manual handling)
- ✅ Granular tool permissions (enable specific tools)
- ✅ Audit logs (all tool calls tracked)

### Tool Orchestration

**Multi-Tool Workflow**:
```python
# Agent can chain multiple tools
user: "Find bugs from last sprint and update Jira"

# Agent execution:
1. vectorize.retrieve(
     query="bugs",
     filters={"sprint": "last", "type": "bug"}
   )
   
2. jira.search_issues(
     jql="project=ENG AND status=Open"
   )
   
3. For each bug not in Jira:
     jira.create_issue(...)
     
4. slack.send_message(
     channel="#engineering",
     text="Created 5 Jira issues from support bugs"
   )
```

### Use Cases

**Customer Support → Engineering**:
- Search support conversations (RAG)
- Create engineering issues (Linear/Jira)
- Notify team (Slack)

**Sales → CRM**:
- Search call transcripts (RAG)
- Update lead status (Salesforce)
- Schedule follow-ups (Calendar API)

**Research → Database**:
- Search internal docs (RAG)
- Query analytics database (SQL)
- Generate report (Google Docs API)

**Compliance**:
- Search policy documents (RAG)
- Check employee records (HR system)
- Flag violations (Compliance tool)

### Key Benefits
- ✅ Knowledge + Actions (not just retrieval)
- ✅ Multi-tool orchestration
- ✅ Secure authentication
- ✅ True AI assistants (not just Q&A)
- ✅ Operational integration

---

## Comparison: Vectorize.io Patterns vs Others

| Pattern | Vectorize.io | Standard RAG | NVIDIA | Google |
|---------|-------------|--------------|--------|--------|
| **Hybrid Retrieval** | ✅ Built-in | ❌ Manual | ⚠️ Separate | ⚠️ Limited |
| **Metadata Filtering** | ✅ Advanced | ⚠️ Basic | ⚠️ Basic | ✅ Advanced |
| **Real-Time Updates** | ✅ Event-driven | ❌ Batch | ⚠️ Manual | ✅ Managed |
| **RAG Evaluation** | ✅ < 1 min | ❌ Manual | ❌ None | ❌ None |
| **Memory System** | ✅ Hindsight | ❌ None | ❌ None | ❌ None |
| **Tool Integration** | ✅ MCP | ❌ Custom | ⚠️ Limited | ⚠️ Limited |
| **Per-User Context** | ✅ Built-in | ❌ Manual | ❌ None | ❌ None |
| **Learning Layer** | ✅ Reflection | ❌ None | ❌ None | ❌ None |

---

## Implementation Recommendations

### Start Simple
**Week 1**: Basic RAG
```python
# Upload documents
vectorize.create_pipeline(
    source="s3://docs",
    embedding_model="voyage-2"
)

# Query
results = vectorize.retrieve(query="...")
```

### Add Intelligence
**Week 2**: Hybrid + Metadata
```python
# Add metadata extraction
vectorize.create_pipeline(
    source="s3://docs",
    embedding_model="voyage-2",
    metadata_schema={...},
    auto_extract=True
)

# Query with filters
results = vectorize.retrieve(
    query="...",
    mode="hybrid",
    filters={...}
)
```

### Enable Real-Time
**Week 3**: Live Updates
```python
# Enable real-time processing
pipeline.update(real_time=True)

# Webhook for notifications
pipeline.set_webhook("https://your-app.com/webhook")
```

### Add Memory
**Week 4**: Hindsight
```bash
# Install Hindsight
npx add-skill vectorize-io/hindsight --skill hindsight-docs

# Agents now have remember/recall/reflect
```

### Integrate Tools
**Week 5**: MCP Actions
```python
# Add MCP servers
vectorize.add_mcp_server("linear", {...})
vectorize.add_mcp_server("slack", {...})

# Agents can now take actions
```

### Optimize
**Week 6**: Evaluation
```python
# Run evaluation
results = vectorize.evaluate_rag(
    documents=docs,
    embedding_models="all",
    chunk_sizes=[256, 512, 1024]
)

# Deploy winner
results.materialize_best()
```

---

## Key Takeaways

**From Vectorize.io**:
1. ✅ Hybrid retrieval is essential (vector + text)
2. ✅ Metadata enables powerful filtering
3. ✅ Real-time updates prevent stale data
4. ✅ Evaluation should be automated (< 1 min)
5. ✅ Memory systems beat stateless RAG
6. ✅ Reflection layer consolidates knowledge
7. ✅ Tool integration makes agents actionable
8. ✅ Per-user context is critical

**Unique Innovations**:
- Iris model for automatic metadata extraction
- Sub-100ms memory recall with reflection
- One-minute RAG evaluation framework
- Event-driven real-time processing
- MCP integration for operational tools
- Compound memory for multi-agent systems

**Production-Ready Features**:
- SOC2 Type 2 certified
- OAuth 2.1 with auto-refresh
- Audit logs for compliance
- Visual schema editor (no code)
- Webhook notifications
- Error handling and retries

---

## Resources

- **Website**: https://vectorize.io
- **Hindsight**: https://hindsight.vectorize.io
- **Docs**: https://docs.vectorize.io
- **Blog**: https://vectorize.io/blog
- **GitHub**: https://github.com/vectorize-io
- **Slack**: hindsight-space community

---

**Document Version**: 1.0  
**Last Updated**: 2026-07-03  
**Sources**: Official Vectorize.io website, blog posts, documentation
