# Implementation Plan: Integrated RAG Chatbot for Book

**Branch**: `001-rag-book-chatbot` | **Date**: 2025-12-06 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-rag-book-chatbot/spec.md`

## Summary

Build an integrated Retrieval-Augmented Generation (RAG) chatbot that answers questions strictly based on book content, explains selected text, and cites correct chapters. The system uses FastAPI for the backend API, Qdrant Cloud for vector storage, Gemini embeddings (text-embedding-004), and OpenAI-Agents SDK configured with Gemini API for response generation. Zero hallucination tolerance - all answers must be grounded in retrieved book content.

## Technical Context

**Language/Version**: Python 3.12+
**Primary Dependencies**:
- FastAPI + Uvicorn (async web framework)
- Qdrant Client (vector database SDK)
- OpenAI-Agents SDK (agent framework with Gemini backend)
- Google Generative AI SDK (Gemini embeddings)
- Pydantic (data validation)
- Python-dotenv (environment config)

**Storage**:
- Vector Database: Qdrant Cloud (free tier) for book content embeddings
- No relational database required (stateless API)

**Testing**:
- Pytest for unit and integration tests
- Pytest-asyncio for async endpoint testing
- Coverage target: >80% for critical paths

**Target Platform**: Linux/Windows server (Docker-ready)
**Project Type**: Web (backend API only, no UI)
**Performance Goals**:
- p90 response time: <3 seconds for RAG queries
- Support 50-100 concurrent users initially
- Embedding generation: <500ms per chunk

**Constraints**:
- Maximum query length: 2000 characters
- Retrieve 3-5 content segments per query
- Minimum similarity threshold: 0.7 (70%)
- Zero hallucinations - strict grounding requirement
- Must use Gemini text-embedding-004 for consistency

**Scale/Scope**:
- Initial deployment: Single book (~20-50 chapters)
- Vector database: ~1000-5000 content segments
- Expected queries: <1000/day initially
- Re-ingestion frequency: Weekly or on-demand

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Applicable Principles

**II. Content Accuracy & Rigor**:
- ✅ **PASS**: Code examples will use exact SDK versions in `requirements.txt`
- ✅ **PASS**: No speculative safety claims - RAG system handles text only
- ✅ **PASS**: All retrieval thresholds (0.7 similarity) based on industry standards

**III. Educational Clarity**:
- ✅ **PASS**: Explicit prerequisites documented for maintainers (Python 3.12+, FastAPI knowledge)
- ✅ **PASS**: Quickstart guide will provide step-by-step setup instructions
- ✅ **PASS**: Error messages designed for clear debugging

**Technical Stack Compliance**:
- ✅ **PASS - Backend**: Python 3.12+ (matches constitution)
- ✅ **PASS - API Framework**: FastAPI (matches constitution)
- ✅ **PASS - Vector Database**: Qdrant (matches constitution)
- ✅ **PASS - Formatting**: Will use Ruff/Black for Python (matches constitution)
- ⚠️ **DEVIATION - Auth**: No Better-Auth needed (feature explicitly excludes authentication per spec Out of Scope)

### Constitution Compliance Summary

**Status**: ✅ **APPROVED with justified deviations**

**Deviations**:
1. **Better-Auth not used**: Authentication is explicitly out of scope per feature spec section "Out of Scope". This is a feature-level design decision, not a violation.

**Validation**:
- All technical stack choices align with constitution
- No safety-critical robot control code (text-only RAG system)
- Educational clarity maintained through comprehensive documentation
- Code quality standards (Ruff/Black) will be enforced

## Project Structure

### Documentation (this feature)

```text
specs/001-rag-book-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification (already exists)
├── research.md          # Phase 0 output (technology decisions)
├── data-model.md        # Phase 1 output (entities and validation)
├── quickstart.md        # Phase 1 output (setup and development guide)
├── contracts/           # Phase 1 output (API schemas)
│   └── openapi.yaml     # OpenAPI 3.1 specification for /chat endpoint
├── checklists/          # Quality validation
│   └── requirements.md  # Specification quality checklist (already exists)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application and /chat endpoint
│   ├── config.py            # Environment variables (GEMINI_API_KEY, QDRANT_URL, etc.)
│   ├── models.py            # Pydantic models (ChatRequest, ChatResponse, etc.)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── embeddings.py    # Gemini text-embedding-004 wrapper
│   │   ├── vector_store.py  # Qdrant client and operations
│   │   ├── query_classifier.py  # Classify query type (greeting, book Q, out-of-scope)
│   │   └── rag_agent.py     # OpenAI-Agents SDK agent with Gemini backend
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py        # Structured logging with secret masking
│   │   └── validators.py    # Input validation (2000 char limit, whitespace check)
│   └── scripts/
│       ├── __init__.py
│       └── ingest.py        # Content ingestion script (reads frontend/docs)
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures (mock Qdrant, mock Gemini)
│   ├── unit/
│   │   ├── test_embeddings.py
│   │   ├── test_vector_store.py
│   │   ├── test_query_classifier.py
│   │   └── test_validators.py
│   ├── integration/
│   │   ├── test_ingest.py   # Test chunking and ingestion pipeline
│   │   ├── test_rag_agent.py
│   │   └── test_chat_endpoint.py
│   └── contract/
│       └── test_openapi_compliance.py
├── .env.example             # Template for environment variables
├── requirements.txt         # Python dependencies with pinned versions
├── pyproject.toml           # Ruff/Black configuration
├── Dockerfile               # Production container image
└── README.md                # Backend setup and development guide
```

**Structure Decision**: Web application structure selected because this is a backend API that serves a frontend (Docusaurus book). The `backend/` directory contains all API code, with clear separation between application logic (`app/`), tests, and deployment configuration. The ingestion script reads from `frontend/docs` to populate the vector database.

## Complexity Tracking

> No constitution violations requiring justification. All technical choices align with established standards.

---

## Phase 0: Research & Technology Decisions

### Research Questions

Based on the user-provided planning input and specification requirements, the following technology decisions need documentation:

1. **Chunking Strategy**: How to split book chapters into semantically coherent segments?
2. **Embedding Integration**: Best practices for using Gemini text-embedding-004 via Google Gen AI SDK?
3. **Qdrant Schema Design**: Optimal collection structure for metadata (chapter, section, order)?
4. **OpenAI-Agents SDK with Gemini**: Configuration pattern for using Gemini as the LLM backend?
5. **Query Classification**: Lightweight approach to detect greeting/chit-chat vs book questions?
6. **Vector Search Optimization**: How to ensure top 3-5 results meet 0.7 similarity threshold?
7. **Re-ingestion Safety**: Pattern to replace existing chapter vectors without data races?

### Output Artifact

These research questions will be addressed in [`research.md`](#research-output) with:
- Decision rationale
- Alternatives considered
- Implementation guidance
- Links to official documentation (Context7 MCP tools to be used)

---

## Phase 1: Design Artifacts

### 1. Data Model (`data-model.md`)

**Entities from Specification**:

1. **Book Chapter** (Source Data)
   - chapter_number: int
   - chapter_title: str
   - full_text: str
   - sections: List[Section]
   - metadata: dict (author, publish_date, version)

2. **Content Segment** (Vector DB Storage)
   - segment_id: UUID
   - text: str (200-500 words)
   - chapter_ref: str
   - section_ref: str
   - order: int
   - embedding: List[float] (dimensionality from text-embedding-004)
   - Stored in Qdrant with metadata payload

3. **Query** (API Input)
   - query: str (1-2000 characters, non-whitespace)
   - selected_text: Optional[str]
   - Validation: FR-024 requirements

4. **Response** (API Output)
   - answer: str
   - source_chapters: List[ChapterCitation]
   - similarity_score: float (0.0-1.0, minimum 0.7 for content responses)
   - mode: Literal["rag", "selected_text", "greeting", "out_of_scope"]

5. **ChapterCitation** (Response Component)
   - chapter: str
   - section: Optional[str]
   - score: float

6. **Ingestion Log** (Logging Only)
   - timestamp: datetime
   - chapters_processed: List[str]
   - success: bool
   - error_messages: List[str]
   - total_segments: int

7. **Error Record** (API Error Response)
   - error_type: str
   - message: str
   - user_message: str (no secrets)
   - timestamp: datetime

**Validation Rules** (from Functional Requirements):
- FR-024: Query must be 1-2000 chars, non-empty after trim
- FR-030: Similarity score must be ≥0.7 for content-based responses
- FR-011: Retrieve exactly 3-5 segments per query
- FR-005: Re-ingestion replaces old vectors entirely

### 2. API Contracts (`contracts/openapi.yaml`)

**Endpoint: POST /chat**

Request Schema:
```yaml
ChatRequest:
  type: object
  required: [query]
  properties:
    query:
      type: string
      minLength: 1
      maxLength: 2000
      description: User question or greeting
    selected_text:
      type: string
      description: Optional highlighted text from book for explanation
```

Response Schema:
```yaml
ChatResponse:
  type: object
  required: [answer, mode, source_chapters]
  properties:
    answer:
      type: string
      description: Generated response or error message
    mode:
      type: string
      enum: [rag, selected_text, greeting, out_of_scope]
    source_chapters:
      type: array
      items:
        type: object
        properties:
          chapter:
            type: string
          section:
            type: string
            nullable: true
          score:
            type: number
            format: float
            minimum: 0.0
            maximum: 1.0
    timestamp:
      type: string
      format: date-time
```

Error Response Schema:
```yaml
ErrorResponse:
  type: object
  required: [error_type, message, user_message]
  properties:
    error_type:
      type: string
      enum: [validation_error, vector_db_error, embedding_error, llm_error, internal_error]
    message:
      type: string
      description: Technical error message (for logs)
    user_message:
      type: string
      description: User-friendly error message (no secrets)
    timestamp:
      type: string
      format: date-time
```

**Additional Endpoint: GET /health**

Response: `{"status": "healthy", "qdrant_connected": bool, "gemini_configured": bool}`

### 3. Quickstart Guide (`quickstart.md`)

**Sections**:
1. Prerequisites (Python 3.12+, Qdrant Cloud account, Gemini API key)
2. Environment Setup (.env configuration)
3. Install Dependencies (`pip install -r requirements.txt`)
4. Run Ingestion Script (populate Qdrant from frontend/docs)
5. Start FastAPI Server (`uvicorn app.main:app --reload`)
6. Test with cURL/Postman examples
7. Run Tests (`pytest`)
8. Troubleshooting (common errors and fixes)

---

## Architecture Decisions

### 1. Embedding Strategy

**Decision**: Use Google Generative AI SDK directly for embeddings, separate from OpenAI-Agents SDK

**Rationale**:
- Text-embedding-004 is a Google model, requires `google-generativeai` SDK
- OpenAI-Agents SDK handles LLM calls (Gemini via OpenAI-compatible endpoint)
- Separation of concerns: embeddings during ingestion vs LLM for responses

**Implementation**:
```python
import google.generativeai as genai
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_embedding(text: str) -> List[float]:
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=text,
        task_type="retrieval_document"  # or "retrieval_query" for queries
    )
    return result['embedding']
```

### 2. Qdrant Collection Schema

**Decision**: Single collection with metadata filtering

**Schema**:
```python
collection_name = "book_content"
vector_size = 768  # text-embedding-004 dimension

payload_schema = {
    "chapter_number": int,
    "chapter_title": str,
    "section": str or None,
    "order": int,  # Sequential order within chapter
    "text": str,  # Original chunk text
    "created_at": str  # ISO timestamp for re-ingestion tracking
}
```

**Indexing**: Create payload index on `chapter_number` for efficient chapter-specific queries

### 3. Query Classification Logic

**Decision**: Rule-based classifier before RAG retrieval

**Classification Rules**:
1. **Greeting**: Matches patterns like "hi", "hello", "hey", "good morning" (case-insensitive)
2. **Chit-chat**: Matches "how are you", "thanks", "thank you", "bye"
3. **Out-of-scope**: If vector search returns all results <0.7 similarity
4. **Selected-text**: If `selected_text` field is provided
5. **Book Question**: Default if above don't match

**Implementation**: Simple regex matching in `query_classifier.py`, no ML model needed

### 4. OpenAI-Agents SDK Configuration

**Decision**: Use OpenAI SDK's base_url override to point to Gemini OpenAI-compatible endpoint

**Configuration**:
```python
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Agent tools for RAG
def retrieve_from_qdrant(query: str) -> List[dict]:
    # Vector search logic
    pass

agent = Agent(
    client=client,
    model="gemini-1.5-flash",  # or gemini-1.5-pro for higher quality
    tools=[retrieve_from_qdrant],
    instructions="You are a book Q&A assistant. ONLY use retrieved content. Never hallucinate."
)
```

### 5. Re-ingestion Strategy

**Decision**: Delete existing chapter vectors by filter, then insert new vectors

**Implementation**:
```python
# Delete old vectors for chapter
qdrant_client.delete(
    collection_name="book_content",
    points_selector=models.FilterSelector(
        filter=models.Filter(
            must=[models.FieldCondition(key="chapter_number", match=models.MatchValue(value=4))]
        )
    )
)

# Insert new vectors
qdrant_client.upsert(collection_name="book_content", points=[...])
```

**Safety**: Use atomic operations where possible; log before/after counts

### 6. Error Handling Pattern

**Decision**: Structured error responses with retry logic for transient failures

**Pattern**:
```python
@app.exception_handler(QdrantException)
async def qdrant_exception_handler(request: Request, exc: QdrantException):
    logger.error(f"Qdrant error: {exc}", exc_info=True)  # Full stack trace
    return JSONResponse(
        status_code=503,
        content={
            "error_type": "vector_db_error",
            "message": str(exc),
            "user_message": "Vector database temporarily unavailable. Please try again.",
            "timestamp": datetime.utcnow().isoformat()
        }
    )
```

**Retry Logic**: Implement retry with exponential backoff for Qdrant connection errors (max 1 retry per FR-029)

### 7. Logging Strategy

**Decision**: Structured JSON logging with secret masking

**Implementation**:
```python
import logging
import json

class SecretMaskingFormatter(logging.Formatter):
    def format(self, record):
        message = super().format(record)
        # Mask API keys, tokens
        message = re.sub(r'(api_key|token)=[^&\s]+', r'\1=***REDACTED***', message)
        return message

logger = logging.getLogger("rag_chatbot")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(SecretMaskingFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)
```

---

## Testing Strategy

### Unit Tests

**Coverage Targets**:
- `embeddings.py`: Test embedding generation (mock Gemini API)
- `vector_store.py`: Test Qdrant CRUD operations (mock client)
- `query_classifier.py`: Test classification rules (100% coverage)
- `validators.py`: Test input validation (edge cases: empty, whitespace, 2000 chars)

### Integration Tests

**Scenarios**:
1. **Ingestion Pipeline**: Mock file reading → chunking → embedding → Qdrant upload
2. **RAG Agent**: Mock Qdrant search → agent response generation
3. **Chat Endpoint**: End-to-end request → classification → retrieval → response

**Mocking Strategy**:
- Use `pytest-mock` for Qdrant client
- Use `responses` library for Gemini API calls
- Fixtures in `conftest.py` for common test data

### Contract Tests

**Validation**:
- OpenAPI schema compliance (request/response match spec)
- Error response format consistency
- HTTP status codes (200, 400, 503, 500)

### Test Data

**Fixtures**:
- Sample book chapters (3-5 markdown files)
- Pre-generated embeddings (numpy arrays)
- Example queries (greetings, book questions, out-of-scope)

---

## Deployment Considerations

### Environment Variables

```bash
# Gemini API
GEMINI_API_KEY=your_api_key_here
GEMINI_CLIENT_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/

# Qdrant Cloud
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key

# Application Config
LOG_LEVEL=INFO
MAX_QUERY_LENGTH=2000
SIMILARITY_THRESHOLD=0.7
TOP_K_SEGMENTS=5
```

### Docker Containerization

**Dockerfile**:
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ ./app/
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Health Checks

**Endpoint**: `GET /health`
- Check Qdrant connectivity (ping collection)
- Check Gemini API key configuration (no actual API call)
- Return 200 if healthy, 503 if degraded

---

## Phase 2 Preview: Task Decomposition

*Note: Detailed tasks will be generated by `/sp.tasks` command. Preview of high-level task categories:*

1. **Setup & Configuration** (5-7 tasks)
   - Initialize backend directory structure
   - Create requirements.txt with pinned versions
   - Configure .env and config.py
   - Set up Ruff/Black formatting
   - Create Qdrant collection

2. **Ingestion Pipeline** (8-10 tasks)
   - Implement markdown file reader
   - Implement semantic chunking logic
   - Integrate Gemini text-embedding-004
   - Implement Qdrant upsert logic
   - Add logging and error handling
   - Test with sample chapters

3. **RAG Components** (10-12 tasks)
   - Implement query classifier
   - Implement vector search service
   - Configure OpenAI-Agents SDK with Gemini
   - Implement retrieval tool for agent
   - Implement response generation with citations
   - Handle similarity threshold logic

4. **API Endpoint** (6-8 tasks)
   - Create Pydantic models
   - Implement /chat POST endpoint
   - Add input validation middleware
   - Implement error handlers
   - Add /health endpoint
   - Document with OpenAPI

5. **Testing** (8-10 tasks)
   - Write unit tests for each service
   - Write integration tests for pipelines
   - Write contract tests for API
   - Set up pytest configuration
   - Achieve 80%+ coverage

6. **Documentation & Deployment** (4-6 tasks)
   - Write quickstart.md
   - Create .env.example
   - Write Dockerfile
   - Test local deployment
   - Document troubleshooting

**Estimated Total**: 41-53 tasks

---

## Success Criteria Mapping

| Success Criterion | Implementation Approach |
|-------------------|------------------------|
| SC-001: 95% accurate responses | Strict grounding with 0.7 similarity threshold, agent instructions |
| SC-002: Zero hallucinations | Agent system prompt + retrieval-only responses |
| SC-003: <3s response time | Async FastAPI, efficient Qdrant queries, Gemini Flash model |
| SC-004: 90% classification accuracy | Rule-based classifier with clear patterns |
| SC-005: 100% correct citations | Extract chapter/section from Qdrant metadata |
| SC-006: 100% out-of-scope rejection | Similarity threshold + explicit refusal response |
| SC-007: 95% ingestion success | Robust error handling, continue-on-error logic |
| SC-008: 100% error handling | Structured error responses, comprehensive logging |
| SC-009: 85% first-attempt success | Clear validation errors, helpful user messages |
| SC-010: Accuracy through updates | Re-ingestion pattern replaces old vectors |

---

## Risk Mitigation

### Technical Risks (from Spec)

1. **Vector search returns irrelevant results**
   - **Mitigation**: 0.7 similarity threshold enforced, test with diverse queries
   - **Monitoring**: Log similarity scores, track "content not found" rate

2. **Embedding service rate limits**
   - **Mitigation**: Batch ingestion with delays, cache embeddings during development
   - **Monitoring**: Track API usage, set up alerts

3. **Content chunking loses context**
   - **Mitigation**: Natural boundary chunking (paragraphs), include surrounding context in metadata
   - **Validation**: Manual review of chunk quality during research phase

### Operational Risks

1. **Re-ingestion disrupts service**
   - **Mitigation**: Schedule during low-usage, add "maintenance mode" flag
   - **Future**: Blue-green collection switching

2. **Query classification errors**
   - **Mitigation**: Log misclassifications, refine patterns iteratively
   - **Monitoring**: Track classification distribution

---

## Next Steps

1. **Complete Phase 0**: Generate `research.md` with technology research findings
2. **Complete Phase 1**: Generate `data-model.md`, `contracts/openapi.yaml`, `quickstart.md`
3. **Update Agent Context**: Run PowerShell script to update Claude-specific context
4. **Run /sp.tasks**: Decompose this plan into executable tasks with test cases

---

**Plan Status**: ✅ Complete (Phases 0-1 outputs to follow)
**Ready for**: `/sp.tasks` command to generate task decomposition
