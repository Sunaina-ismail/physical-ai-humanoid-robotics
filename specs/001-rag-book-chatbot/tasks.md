# Tasks: Integrated RAG Chatbot for Book

**Input**: Design documents from `/specs/001-rag-book-chatbot/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/openapi.yaml

**Tests**: Tests are NOT included in this implementation (spec does not explicitly request TDD approach)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4, US5, US6)
- Exact file paths included in descriptions

## Path Conventions

This project uses web app structure:
- **Backend**: `backend/app/`, `backend/tests/`, `backend/scripts/`
- **Source**: Book content in `frontend/docs/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create backend directory structure (backend/app/, backend/tests/, backend/scripts/)
- [x] T002 Create requirements.txt with pinned dependencies (fastapi==0.104.1, qdrant-client==1.7.0, openai==1.6.1, openai-agents==0.0.7, pydantic==2.5.0, uvicorn==0.24.0, python-dotenv==1.0.0, psycopg2-binary>=2.9.9, nest-asyncio>=1.6.0)
- [x] T003 [P] Create requirements-dev.txt with development dependencies (pytest==7.4.3, pytest-asyncio==0.21.1, pytest-cov==4.1.0, httpx==0.25.2, black==23.12.0, ruff==0.1.8)
- [x] T004 [P] Create .env.example file with all required environment variables (GEMINI_API_KEY, QDRANT_URL, QDRANT_API_KEY, QDRANT_COLLECTION_NAME, LOG_LEVEL, MAX_QUERY_LENGTH, SIMILARITY_THRESHOLD, TOP_K_RESULTS)
- [x] T005 [P] Create pyproject.toml with Ruff/Black configuration
- [x] T006 [P] Create backend/README.md with setup instructions
- [x] T007 [P] Create .gitignore for Python project (.env, __pycache__, .pytest_cache, .coverage, venv/)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T008 Create backend/app/__init__.py and backend/app/config.py to load environment variables using python-dotenv
- [x] T009 [P] Create backend/app/models.py with all Pydantic data models (BookChapter, ContentSegment, Query, ChapterCitation, Response, IngestionLog, ErrorRecord) per data-model.md
- [x] T010 [P] Create backend/app/utils/__init__.py and backend/app/utils/logger.py with structured logging and secret masking formatter
- [x] T011 [P] Create backend/app/utils/validators.py with input validation functions (validate query length 1-2000 chars, whitespace check)
- [x] T012 Create backend/app/services/__init__.py for services module
- [x] T013 Create backend/app/services/embeddings.py with OpenAI client configured for Gemini embeddings (OpenAI with base_url="https://generativelanguage.googleapis.com/v1beta/openai/", model="text-embedding-004", embedding_dim=768, functions: generate_document_embedding and generate_query_embedding)
- [x] T014 Create backend/app/services/vector_store.py with Qdrant client initialization and basic operations (connect, create_collection with 768-dim COSINE distance, create_payload_index for chapter_number and section_title)
- [x] T015 Create Qdrant collection setup script in backend/scripts/setup_qdrant.py (creates book_content collection with 768-dim vectors, COSINE distance, indexed fields)
- [x] T016 Create backend/app/main.py with FastAPI app initialization, CORS middleware, and basic health endpoint GET /health

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Answer Book Questions (Priority: P1) 🎯 MVP

**Goal**: Enable readers to ask questions about book content and receive accurate, grounded responses with chapter citations

**Independent Test**: Submit various book-related questions via POST /chat and verify responses are accurate, grounded in book content, include correct chapter citations, and return "content not found" for topics not in the book

**Dependencies**: None (foundational phase provides all prerequisites)

### Implementation for User Story 1

- [x] T017 [P] [US1] Implement semantic chunking function in backend/app/services/chunking.py (split by markdown headings, then paragraphs, 200-500 words per chunk per research.md)
- [x] T018 [P] [US1] Create ingestion script in backend/scripts/ingest.py (reads from frontend/docs/, chunks chapters, generates embeddings, uploads to Qdrant with chapter metadata)
- [x] T019 [US1] Implement vector search function in backend/app/services/vector_store.py (search_book_content with top_k=5, score_threshold=0.7, returns results with metadata per research.md)
- [x] T020 [US1] Create backend/app/services/rag_agent.py with OpenAI-Agents SDK configuration (AsyncOpenAI with custom base_url for Gemini, OpenAIChatCompletionsModel with model=gemini-2.0-flash, anti-hallucination instructions per research.md)
- [x] T021 [US1] Implement retrieve_book_content function tool in backend/app/services/rag_agent.py using @function_tool decorator (generates query embedding, searches Qdrant, formats results with citations)
- [x] T022 [US1] Implement query_chatbot function in backend/app/services/rag_agent.py (runs agent with Runner.run, returns final_output)
- [x] T023 [US1] Create POST /chat endpoint in backend/app/main.py for book questions (accepts Query, calls rag_agent.query_chatbot, returns Response with citations)
- [x] T024 [US1] Add error handling for book questions in backend/app/main.py (vector_db_error when Qdrant fails, embedding_error when Gemini fails, not_found when similarity <0.7 per FR-030)
- [x] T025 [US1] Add request validation middleware in backend/app/main.py (validates query 1-2000 chars per FR-024, rejects whitespace-only queries, returns validation_error per ErrorRecord)

**Checkpoint**: At this point, User Story 1 should be fully functional - readers can ask book questions and receive grounded answers with citations

---

## Phase 4: User Story 5 - Support Content Re-Ingestion (Priority: P1)

**Goal**: Enable authors/publishers to update chatbot's knowledge base when editing or adding book chapters

**Independent Test**: Modify a test chapter file, run re-ingestion for that chapter, verify queries about updated content return new information and ingestion logs show replacement operation

**Dependencies**: User Story 1 (uses same chunking and embedding logic)

### Implementation for User Story 5

- [ ] T026 [US5] Implement chapter re-ingestion function in backend/scripts/ingest.py (count existing vectors, delete by chapter_number filter per research.md delete-then-insert pattern, generate new chunks, upsert with wait=True)
- [ ] T027 [US5] Add ingestion logging using IngestionLog model in backend/scripts/ingest.py (log operation type, chapter, segments_processed, vectors_deleted, status, duration per data-model.md)
- [ ] T028 [US5] Add command-line arguments to backend/scripts/ingest.py (--source for directory path, --chapter for specific chapter number, --reingest flag, --dry-run flag)
- [ ] T029 [US5] Add graceful error handling for missing/corrupted files in backend/scripts/ingest.py (log error, continue with other chapters per FR-007, return partial_failure status)
- [ ] T030 [US5] Create ingestion validation function in backend/scripts/ingest.py (verify markdown file exists, has .md extension, non-empty content per BookChapter validators)

**Checkpoint**: At this point, User Stories 1 AND 5 both work - readers get answers, authors can update content

---

## Phase 5: User Story 2 - Explain Selected Text (Priority: P2)

**Goal**: Enable readers to highlight text from the book and get detailed explanations with chapter references

**Independent Test**: Submit requests with selected_text field containing various book passages and verify explanations are accurate, contextual, and include proper chapter/section references

**Dependencies**: User Story 1 (uses same /chat endpoint and RAG infrastructure)

### Implementation for User Story 2

- [ ] T031 [US2] Add selected_text query classification logic in backend/app/services/query_classifier.py (if selected_text field present, classify as QueryType.SELECTED_TEXT per research.md)
- [ ] T032 [US2] Implement explain_selected_text function in backend/app/services/rag_agent.py (embeds selected_text, searches for exact/similar matches in Qdrant, generates explanation using retrieved metadata)
- [ ] T033 [US2] Extend POST /chat endpoint in backend/app/main.py to handle selected_text requests (detects selected_text field, routes to explain_selected_text, returns Response with query_type="selected_text_explanation")
- [ ] T034 [US2] Add validation for selected_text field in backend/app/main.py (max 5000 chars, reject whitespace-only per Query validators, return validation_error if invalid)
- [ ] T035 [US2] Update agent instructions in backend/app/services/rag_agent.py to handle selected text mode (use only provided text + metadata, include chapter/section references per FR-019, no external information per FR-020)

**Checkpoint**: At this point, User Stories 1, 2, AND 5 all work independently - readers can ask questions, explain passages, and authors can update content

---

## Phase 6: User Story 3 - Handle Greetings and Casual Conversation (Priority: P3)

**Goal**: Enable chatbot to respond naturally to greetings and casual messages without triggering content retrieval

**Independent Test**: Send various greetings ("Hi", "Hello", "Thanks") and casual messages and verify friendly responses without RAG retrieval or citations

**Dependencies**: None (independent of RAG functionality)

### Implementation for User Story 3

- [ ] T036 [P] [US3] Create backend/app/services/query_classifier.py with QueryType enum (GREETING, CHIT_CHAT, BOOK_QUESTION, SELECTED_TEXT, OUT_OF_SCOPE) per research.md
- [ ] T037 [P] [US3] Implement classify_query function in backend/app/services/query_classifier.py with regex patterns (greeting patterns: "^(hi|hello|hey)", chit-chat patterns: "how are you|thank|bye" per research.md)
- [ ] T038 [US3] Add greeting response templates in backend/app/services/query_classifier.py (GREETING_RESPONSES list with friendly onboarding messages per research.md)
- [ ] T039 [US3] Add chit-chat response templates in backend/app/services/query_classifier.py (CHIT_CHAT_RESPONSES dict with appropriate replies per research.md)
- [ ] T040 [US3] Integrate query classifier into POST /chat endpoint in backend/app/main.py (classify before RAG, return template responses for greeting/chit-chat with query_type, citations=[], content_found=True)

**Checkpoint**: All core user stories now work - readers can greet, ask questions, explain text; authors can update content

---

## Phase 7: User Story 4 - Reject Out-of-Scope Questions (Priority: P2)

**Goal**: Clearly indicate when questions are outside book scope to prevent incorrect or fabricated information

**Independent Test**: Submit various out-of-scope questions (current events, unrelated topics) and verify polite refusals without any fabricated content

**Dependencies**: User Story 1 (uses same vector search logic to detect out-of-scope via similarity threshold)

### Implementation for User Story 4

- [ ] T041 [US4] Implement out-of-scope detection logic in backend/app/services/rag_agent.py (when all search results have score <0.7, classify as OUT_OF_SCOPE per FR-030)
- [ ] T042 [US4] Add out-of-scope response template in backend/app/services/rag_agent.py (polite refusal message: "I can only answer questions about the book content" per spec acceptance scenario)
- [ ] T043 [US4] Update POST /chat endpoint in backend/app/main.py to handle out-of-scope queries (return Response with query_type="out_of_scope", citations=[], content_found=False per Response validators)
- [ ] T044 [US4] Add logging for out-of-scope queries in backend/app/main.py (track frequency, log query text for future analysis)

**Checkpoint**: All user stories 1-5 fully functional with proper scope enforcement

---

## Phase 8: User Story 6 - Provide Consistent Error Information (Priority: P3)

**Goal**: All errors follow consistent structure for quick debugging and system health monitoring

**Independent Test**: Trigger various error conditions (missing config, network failures, invalid input) and verify all errors follow ErrorRecord schema without exposing secrets

**Dependencies**: Foundational phase (uses ErrorRecord model and logger)

### Implementation for User Story 6

- [ ] T045 [P] [US6] Implement global exception handlers in backend/app/main.py for QdrantException (return database_error with 503 status per research.md error pattern)
- [ ] T046 [P] [US6] Add exception handler for ValidationError in backend/app/main.py (return validation_error with 400 status, details field per ErrorRecord.validation_error factory)
- [ ] T047 [P] [US6] Add exception handler for configuration errors in backend/app/main.py (check GEMINI_API_KEY, QDRANT_URL on startup, return configuration_error with 500 status per ErrorRecord.configuration_error factory)
- [ ] T048 [P] [US6] Add exception handler for Gemini API errors in backend/app/main.py (return embedding_error with 500 status when text-embedding-004 fails)
- [ ] T049 [US6] Implement retry logic for Qdrant connections in backend/app/services/vector_store.py (max 1 retry per FR-029, exponential backoff, log retry attempts)
- [ ] T050 [US6] Add request ID generation middleware in backend/app/main.py (UUID for each request, include in ErrorRecord.request_id and logs)
- [ ] T051 [US6] Verify error responses never expose secrets in backend/app/utils/logger.py (test secret masking with GEMINI_API_KEY, QDRANT_API_KEY per research.md logging strategy)

**Checkpoint**: All user stories complete with production-grade error handling and observability

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T052 [P] Create backend/Dockerfile for production containerization (Python 3.12-slim base, copy requirements.txt, pip install, copy app/, expose 8000, CMD uvicorn per plan.md)
- [ ] T053 [P] Add OpenAPI documentation to POST /chat endpoint in backend/app/main.py (use FastAPI response_model=Response, description from contracts/openapi.yaml)
- [ ] T054 [P] Create backend/tests/conftest.py with pytest fixtures (mock Qdrant client, mock Gemini API, sample book chapters, pre-generated embeddings)
- [ ] T055 Run full ingestion with sample chapters from frontend/docs and verify all chapters searchable
- [ ] T056 Run code formatting with black and ruff on all Python files (backend/app/, backend/tests/, backend/scripts/)
- [ ] T057 Validate quickstart.md steps work end-to-end (environment setup, ingestion, server start, API testing)
- [ ] T058 [P] Add API rate limiting consideration documentation in backend/README.md (Gemini quota: 1500 req/min, Qdrant Cloud free tier limits)
- [ ] T059 Security review of error messages to ensure no credential leakage (audit all ErrorRecord instances, logger calls)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - **BLOCKS all user stories**
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - **US1 (P1)**: Can start immediately after Foundational
  - **US5 (P1)**: Depends on US1 (uses chunking/embedding logic)
  - **US2 (P2)**: Depends on US1 (extends /chat endpoint)
  - **US3 (P3)**: Independent, can run parallel to US1
  - **US4 (P2)**: Depends on US1 (uses vector search)
  - **US6 (P3)**: Can run parallel to other stories (adds error handling)
- **Polish (Phase 9)**: Depends on desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1) - Answer Book Questions**: Can start after Foundational - **No dependencies on other stories**
- **User Story 5 (P1) - Re-Ingestion**: Depends on US1 for chunking/embedding logic
- **User Story 2 (P2) - Explain Selected Text**: Depends on US1 for /chat endpoint and RAG infrastructure
- **User Story 3 (P3) - Greetings**: Independent - Can run parallel to US1
- **User Story 4 (P2) - Reject Out-of-Scope**: Depends on US1 for vector search logic
- **User Story 6 (P3) - Consistent Errors**: Independent - Can run parallel to other stories

### Recommended Implementation Order

**MVP Path (P1 features only)**:
1. Phase 1: Setup (T001-T007)
2. Phase 2: Foundational (T008-T016) ← **CRITICAL BLOCKER**
3. Phase 3: US1 - Answer Book Questions (T017-T025)
4. Phase 4: US5 - Re-Ingestion (T026-T030)
5. **STOP & VALIDATE MVP**: Test that readers can ask questions and authors can update content

**Full Feature Path**:
1-4. (Same as MVP)
5. Phase 5: US2 - Explain Selected Text (T031-T035)
6. Phase 6: US3 - Greetings (T036-T040)
7. Phase 7: US4 - Out-of-Scope (T041-T044)
8. Phase 8: US6 - Error Handling (T045-T051)
9. Phase 9: Polish (T052-T059)

### Parallel Opportunities

**Within Setup (Phase 1)**:
- T003, T004, T005, T006, T007 can all run in parallel (different files)

**Within Foundational (Phase 2)**:
- T009, T010, T011 can run in parallel (models.py, logger.py, validators.py)
- T013, T014 must wait for T012 (services need __init__.py)

**Within US1 (Phase 3)**:
- T017, T018 can run in parallel (chunking.py, ingest.py - different files)
- T019 depends on T014 (extends vector_store.py)

**Within US3 (Phase 6)**:
- T036, T037 can run in parallel with T038, T039 (all in query_classifier.py but different functions)

**Within US6 (Phase 8)**:
- T045, T046, T047, T048 can all run in parallel (different exception handlers in main.py)

**Across User Stories** (after Foundational complete):
- US1 and US3 can run in complete parallel (no shared files)
- US1 and US6 can run in parallel (US6 adds error handling to US1 endpoints)
- US2, US4 must wait for US1 completion (extend same files)

---

## Parallel Example: User Story 1

```bash
# After Foundational phase completes, these US1 tasks can run in parallel:

# Developer A:
Task T017: "Implement semantic chunking function in backend/app/services/chunking.py"

# Developer B (simultaneously):
Task T018: "Create ingestion script in backend/scripts/ingest.py"

# Once T014 (vector_store.py base) is done, Developer C:
Task T019: "Implement vector search function in backend/app/services/vector_store.py"
```

---

## Parallel Example: Multiple User Stories

```bash
# After Foundational phase completes:

# Team A (Priority 1 - MVP):
- Works on US1 (T017-T025) - Answer Book Questions
- Then US5 (T026-T030) - Re-Ingestion

# Team B (simultaneously):
- Works on US3 (T036-T040) - Greetings (independent)
- Then US6 (T045-T051) - Error Handling (can add to US1 endpoints)

# After US1 completes:
# Team C:
- Works on US2 (T031-T035) - Explain Selected Text (extends US1)
- Then US4 (T041-T044) - Out-of-Scope (extends US1)
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 5 Only - Both P1)

1. Complete Phase 1: Setup (7 tasks)
2. Complete Phase 2: Foundational (9 tasks) **← CRITICAL BLOCKER**
3. Complete Phase 3: US1 - Answer Book Questions (9 tasks)
4. Complete Phase 4: US5 - Re-Ingestion (5 tasks)
5. **STOP and VALIDATE MVP**:
   - Test: Submit book questions → Verify accurate answers with citations
   - Test: Modify a chapter → Re-ingest → Verify updated answers
   - Test: Submit out-of-scope question → Verify content not found
6. **Deploy/Demo MVP**: Core value delivered (readers get answers, authors update content)

**MVP Total**: 30 tasks

### Incremental Delivery (All User Stories)

1. Setup + Foundational (16 tasks) → Foundation ready
2. Add US1 (9 tasks) → Test independently → **Readers can ask questions ✓**
3. Add US5 (5 tasks) → Test independently → **Authors can update content ✓ (MVP!)**
4. Add US2 (5 tasks) → Test independently → **Readers can explain selected text ✓**
5. Add US3 (5 tasks) → Test independently → **Friendly greetings work ✓**
6. Add US4 (4 tasks) → Test independently → **Out-of-scope handled ✓**
7. Add US6 (7 tasks) → Test independently → **Production error handling ✓**
8. Polish (8 tasks) → Production ready

**Full Feature Total**: 59 tasks

### Parallel Team Strategy

With multiple developers after Foundational phase completes:

**Team A (P1 features - MVP critical)**:
- Developer 1: US1 tasks T017-T025 (Answer Book Questions)
- Developer 2: US5 tasks T026-T030 (Re-Ingestion) - starts after US1 T017-T018 complete

**Team B (Independent features)**:
- Developer 3: US3 tasks T036-T040 (Greetings)
- Developer 4: US6 tasks T045-T051 (Error Handling)

**Team C (US1-dependent features - waits for US1)**:
- Developer 5: US2 tasks T031-T035 (Explain Selected Text) - starts after US1 T023 complete
- Developer 6: US4 tasks T041-T044 (Out-of-Scope) - starts after US1 T019 complete

This approach parallelizes ~60% of work while respecting dependencies.

---

## Task Count Summary

| Phase | Tasks | Can Parallelize |
|-------|-------|-----------------|
| Phase 1: Setup | 7 | 5 tasks (71%) |
| Phase 2: Foundational | 9 | 3 tasks (33%) |
| Phase 3: US1 - Book Questions (P1) | 9 | 2 tasks (22%) |
| Phase 4: US5 - Re-Ingestion (P1) | 5 | 0 tasks (0%) |
| Phase 5: US2 - Explain Text (P2) | 5 | 0 tasks (0%) |
| Phase 6: US3 - Greetings (P3) | 5 | 2 tasks (40%) |
| Phase 7: US4 - Out-of-Scope (P2) | 4 | 0 tasks (0%) |
| Phase 8: US6 - Errors (P3) | 7 | 4 tasks (57%) |
| Phase 9: Polish | 8 | 5 tasks (63%) |
| **Total** | **59** | **21 (36%)** |

**MVP Scope** (P1 only): 30 tasks (Phases 1, 2, 3, 4)
**Full Feature Scope**: 59 tasks (all phases)

---

## Notes

- **[P] tasks**: Different files, no dependencies - can run in parallel
- **[Story] labels**: Map tasks to user stories for traceability (US1-US6)
- **Each user story** is independently completable and testable
- **Foundational phase** (T008-T016) blocks ALL user story work
- **No tests included**: Spec does not explicitly request TDD approach
- **File paths**: All exact paths provided per backend/ structure from plan.md
- **Commit strategy**: Commit after each task or logical group
- **Checkpoints**: Validate each story independently before moving to next
- **Priority execution**: P1 stories (US1, US5) form MVP, P2 stories (US2, US4) add value, P3 stories (US3, US6) polish UX
