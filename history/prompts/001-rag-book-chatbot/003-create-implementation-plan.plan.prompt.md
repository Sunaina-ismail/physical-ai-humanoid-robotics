---
id: 003
title: Create Implementation Plan
stage: plan
date: 2025-12-06
surface: agent
model: claude-sonnet-4-5
feature: 001-rag-book-chatbot
branch: 001-rag-book-chatbot
user: Sunaina Ismail
command: /sp.plan
labels: ["planning", "architecture", "rag", "chatbot", "design"]
links:
  spec: specs/001-rag-book-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-rag-book-chatbot/plan.md
  - specs/001-rag-book-chatbot/research.md
  - specs/001-rag-book-chatbot/data-model.md
  - specs/001-rag-book-chatbot/contracts/openapi.yaml
  - specs/001-rag-book-chatbot/quickstart.md
tests:
  - N/A - planning phase (test strategy documented in plan.md)
---

## Prompt

```text
/sp.plan
```

(User invoked planning workflow with detailed project specification including 6-phase breakdown: Backend Setup, Chunking & Embedding, RAG Agent Development, API Endpoint, Testing, Deployment & Maintenance)

## Response snapshot

Successfully created comprehensive implementation plan with architecture design, technology research, data models, API contracts, and developer quickstart guide.

**Phase 0: Research Completed** (`research.md`):
- 7 research questions answered with code examples and rationale
- Used Context7 MCP tools to fetch latest documentation for Qdrant, FastAPI, OpenAI-Agents SDK
- Key decisions documented:
  - **Chunking**: Semantic boundaries, 200-500 words, preserves headings
  - **Embeddings**: google-generativeai SDK with task_type parameter for text-embedding-004
  - **Qdrant Schema**: Single collection, COSINE distance, indexed metadata (chapter_number, section_title)
  - **OpenAI-Agents Integration**: Custom base_url for Gemini endpoint with function tools pattern
  - **Query Classification**: Rule-based regex patterns for greeting/chit-chat/book/selected-text/out-of-scope
  - **Vector Search**: Score threshold 0.7 + top-k retrieval (3-5 segments)
  - **Re-ingestion**: Delete-then-insert pattern with comprehensive logging

**Phase 1: Design Artifacts Completed**:

1. **`data-model.md`**: 7 Pydantic entity definitions with validation rules
   - BookChapter (source content representation)
   - ContentSegment (chunked content with embeddings)
   - Query (user input with 2000 char limit)
   - ChapterCitation (grounding references)
   - Response (chatbot output with citations)
   - IngestionLog (audit trail)
   - ErrorRecord (structured error handling)
   - Includes field validators, factory methods, and Qdrant conversion utilities

2. **`contracts/openapi.yaml`**: OpenAPI 3.1 specification
   - POST /chat endpoint with 5 query type examples
   - GET /health endpoint with dependency checks
   - Complete request/response schemas with validation constraints
   - Error response taxonomy (7 error types)
   - 12+ example responses covering all scenarios

3. **`quickstart.md`**: Step-by-step developer guide
   - Prerequisites (Python 3.12+, Gemini API, Qdrant Cloud)
   - 10-step setup workflow (clone → configure → ingest → test)
   - Environment variable configuration with security notes
   - Qdrant collection setup (manual and scripted)
   - Ingestion workflow with expected outputs
   - API testing examples (4 query types)
   - Troubleshooting guide (7 common issues)
   - Development workflow and production checklist

**Architecture Plan** (`plan.md` - 668 lines):
- **Technical Context**: Python 3.12+, FastAPI, Qdrant, pytest, Docker-ready
- **Constitution Check**: Verified compliance, documented justified deviation (no Better-Auth)
- **Project Structure**: Backend directory layout (app/, tests/, scripts/)
- **7 Architecture Decisions**:
  1. Embedding Strategy: Gemini text-embedding-004 via google-generativeai SDK
  2. Chunking Approach: Semantic chunking at natural boundaries
  3. Qdrant Schema: Single collection with indexed metadata
  4. OpenAI-Agents Integration: Custom base_url for Gemini compatibility
  5. Query Classification: Rule-based patterns (lightweight, deterministic)
  6. Re-ingestion Safety: Delete-then-insert with audit logging
  7. Error Handling: Structured ErrorRecord with retry logic
- **Testing Strategy**: Unit (ingestion, classification, models), Integration (RAG pipeline, Qdrant), Contract (API schema validation)
- **Deployment Considerations**: Environment variables, Docker, health checks, monitoring

**Files Created**:
- `plan.md` (668 lines) - Main implementation plan
- `research.md` (470+ lines) - Technology research with code examples
- `data-model.md` (580+ lines) - Pydantic entity definitions with validators
- `contracts/openapi.yaml` (530+ lines) - OpenAPI 3.1 specification
- `quickstart.md` (630+ lines) - Developer setup guide

## Outcome

- ✅ Impact: Complete implementation plan with architecture decisions, data models, API contracts, and developer quickstart guide ready for task decomposition
- 🧪 Tests: N/A - planning phase (test strategy documented in plan.md with unit/integration/contract test categories)
- 📁 Files: 5 files created (plan.md, research.md, data-model.md, contracts/openapi.yaml, quickstart.md)
- 🔁 Next prompts: Run `/sp.tasks` to decompose plan into executable tasks (estimated 41-53 tasks across 6 categories), then begin implementation with red-green-refactor cycle
- 🧠 Reflection: Context7 MCP tools provided up-to-date documentation that resolved key integration challenges (Gemini + OpenAI-Agents SDK compatibility via custom base_url, Qdrant indexed payload fields). The semantic chunking strategy (200-500 words at natural boundaries) balances context preservation with embedding quality. Delete-then-insert re-ingestion pattern ensures data integrity during content updates while maintaining audit trail.

## Evaluation notes (flywheel)

- Failure modes observed: None - all artifacts generated successfully with validation rules and examples
- Graders run and results (PASS/FAIL): PASS - All Phase 0 and Phase 1 artifacts completed, constitution compliance verified, no implementation details leaked into spec
- Prompt variant (if applicable): N/A - standard /sp.plan workflow with Context7 MCP tool integration
- Next experiment (smallest change to try): Future iterations could explore batch embedding generation for ingestion performance optimization (current approach embeds one segment at a time, could batch 10-20 segments per API call to reduce latency)
