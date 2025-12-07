---
id: 001
title: Create RAG Chatbot Spec
stage: spec
date: 2025-12-06
surface: agent
model: claude-sonnet-4-5
feature: 001-rag-book-chatbot
branch: 001-rag-book-chatbot
user: Sunaina Ismail
command: /sp.specify
labels: ["rag", "chatbot", "book-integration", "vector-search", "specification"]
links:
  spec: specs/001-rag-book-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-rag-book-chatbot/spec.md
  - specs/001-rag-book-chatbot/checklists/requirements.md
tests:
  - N/A - specification phase
---

## Prompt

```text
# Project Specification: Integrated RAG Chatbot for Book

## Intent
Build and embed an Integrated Retrieval-Augmented Generation (RAG) Chatbot into the published book.
The chatbot must answer questions strictly based on the book's content, explain selected text, and cite the correct chapters.
It will use **FastAPI**, **Qdrant Cloud**, and the **OpenAI-Agents SDK** configured with:

- `GEMINI_API_KEY`
- `GEMINI_CLIENT_BASE_URL`

Before writing any implementation code, the system must use **context7 MCP tools** to fetch the latest documentation on:

- OpenAI-Agents SDK
- Qdrant Cloud
- FastAPI

No LangChain or LlamaIndex will be used.

---

## Success Criteria
- Chatbot answers book-related questions using strict RAG grounding.
- Explanations for selected text reference the correct chapter and section.
- Out-of-scope questions return polite refusals without hallucination.
- Greeting and chit-chat handled gracefully without triggering RAG.
- Qdrant vector search works reliably for ingestion + query.
- Ingestion script supports re-ingestion for updates.
- OpenAI-Agents SDK is correctly configured with Gemini credentials.
- Gemini `text-embedding-004` used for all embeddings.
- All API usage validated via context7 MCP tools before coding.
- Error handling uses a consistent structured format.

---

## Non-Goals
- No LangChain or LlamaIndex.
- No UI beyond the API behavior.
- No authentication or user accounts.
- No recommendation system.
- No content generation outside the book.

---

# Requirements

## Functional Requirements

### 1. Data Ingestion
A reusable ingestion script must:

- Read book chapters from a directory.
- Chunk chapters into semantically coherent segments.
- Generate embeddings using **Gemini `text-embedding-004` via OpenAI-Agents SDK**.
- Upload vectors + metadata (chapter, section, order, text) to Qdrant Cloud.
- Allow re-ingestion for updates or new chapters.
- Log ingestion status and errors.

---

### 2. RAG Pipeline
- Embed user queries using Gemini embeddings.
- Perform semantic search against Qdrant.
- Construct grounded prompts using retrieved text.
- Answers must cite chapter + section.
- Out-of-scope questions must be safely rejected.
- Payload must include chapter/section metadata.

---

### 3. Query Classification
The system must classify queries into:

- Greeting
- Chit-chat
- Book-related question
- Explain-selected-text
- Out-of-scope

Rules:

- Greeting/chit-chat → Friendly response, no RAG.
- Selected text explanation → Use only provided text + metadata.
- Out-of-scope → Polite refusal, no hallucination.

---

### 4. API Endpoint

#### `POST /chat`
A single endpoint that handles:

- Greetings
- Chit-chat
- Book questions
- Selected text explanation (optional)
- Out-of-scope detection

**Request Body:**
```json
{
  "query": "string",
  "selected_text": "string (optional)"
}
```

## Non-Functional Requirements

- Must use **FastAPI**.
- Must use **Qdrant Cloud Free Tier**.
- Must use **OpenAI-Agents SDK** configured with:
  - `GEMINI_API_KEY`
  - `GEMINI_CLIENT_BASE_URL`
- Must fetch all relevant documentation via **context7 MCP tools before implementation**.
- No hallucinations allowed under any circumstance.
- Logging must not leak secrets or credentials.
- All LLM calls must follow documented patterns retrieved via MCP tools.
- Responses must be deterministic and grounded solely in the book's content.

---

## Error Handling Requirements

- Missing Gemini API configuration → return a structured error.
- Qdrant connectivity failure → **retry once** → return a graceful structured error.
- Vector search with zero results → return a **"content not found"** fallback message.
- Input validation must reject:
  - Empty inputs
  - Oversized payloads
  - Malformed JSON


# User Stories & Acceptance Criteria

## User Story 1: Book Questions
**As a reader, I want to ask questions about the book so I can understand the content better.**

### Acceptance Criteria
- RAG retrieval is executed.
- Answer is strictly grounded in the book content.
- Response must include chapter references.
- No hallucinations or external knowledge.

---

## User Story 2: Explain Selected Text
**As a reader, I want explanations for selected text I highlight from the book.**

### Acceptance Criteria
- Explanation uses only the selected text plus stored metadata.
- Includes correct chapter reference.
- No external or fabricated information introduced.

---

## User Story 3: Greeting / Chit-Chat
**As a reader, I want the chatbot to greet naturally when I say hi/hello.**

### Acceptance Criteria
- Greeting intent is detected without triggering RAG retrieval.
- Responds with friendly onboarding guidance.
- Maintains helpful tone.

---

## User Story 4: Out-of-Scope Questions
**As a reader, I want the chatbot to decline irrelevant or unrelated queries.**

### Acceptance Criteria
- Out-of-scope questions are reliably identified.
- Responds with a polite, short refusal.
- Does not hallucinate any information.

---

## User Story 5: Author Ingestion Flow
**As an author, I want to re-ingest chapters easily so the chatbot stays updated.**

### Acceptance Criteria
- Re-ingestion updates or adds vectors for new/edited chapters.
- Logs success and errors clearly.
- Gracefully handles missing chapter files.

---

## User Story 6: Developer Reliability
**As a developer, I want consistent error structures for easy debugging.**

### Acceptance Criteria
- All errors follow the required structured error format.
- Internal logs include stack traces without exposing secrets.
- API responses never expose environment variables or credentials.

---

# Constraints
- Must use **FastAPI**, **Qdrant Cloud**, and **OpenAI-Agents SDK**.
- Must use **Gemini embeddings (`text-embedding-004`)**.
- Must fetch updated documentation using **context7 MCP tools** before building.
- No LangChain, no LlamaIndex frameworks.
- All reasoning must be grounded strictly in the book content.
- **Zero tolerance for hallucinations.**
```

## Response snapshot

Created comprehensive feature specification for the Integrated RAG Chatbot. The spec includes:

**Branch & Files Created**:
- Branch: `001-rag-book-chatbot`
- Spec file: `specs/001-rag-book-chatbot/spec.md`
- Checklist: `specs/001-rag-book-chatbot/checklists/requirements.md`

**Specification Structure**:

1. **User Stories** (6 stories, prioritized P1-P3):
   - P1: Answer Book Questions - Core value proposition
   - P2: Explain Selected Text - Enhanced reading experience
   - P3: Handle Greetings - Conversational UX
   - P2: Reject Out-of-Scope Questions - Trust protection
   - P1: Support Content Re-Ingestion - Maintainability
   - P3: Consistent Error Information - Operational efficiency

2. **Functional Requirements** (30 requirements across 5 categories):
   - Data Ingestion (FR-001 to FR-007)
   - Query Processing (FR-008 to FR-016)
   - Selected Text Explanation (FR-017 to FR-020)
   - API Interface (FR-021 to FR-025)
   - Error Handling (FR-026 to FR-030)

3. **Success Criteria** (10 measurable, technology-agnostic outcomes):
   - 95% accuracy with correct citations
   - Zero hallucinations
   - 3-second response time for 90% of queries
   - 90% query classification accuracy
   - 100% correct chapter references for selected text

4. **Key Entities** (6 data concepts):
   - Book Chapter, Content Segment, Query, Response, Ingestion Log, Error Record

5. **Comprehensive Coverage**:
   - 10 edge cases identified
   - Clear scope boundaries (8 in-scope, 10 out-of-scope items)
   - 13 assumptions (technical, business, data, operational)
   - 8 dependencies (external, internal, data)
   - 7 risks with impact and mitigation strategies

**Quality Validation**:
All validation checklist items passed on first review:
- ✅ No implementation details in requirements
- ✅ Technology-agnostic success criteria
- ✅ All requirements testable and unambiguous
- ✅ Comprehensive edge case coverage
- ✅ Clear prioritization and acceptance scenarios

**Technical Details**:
All implementation specifics (FastAPI, Qdrant, OpenAI-Agents SDK, Gemini) moved to Notes section as guidance rather than requirements, maintaining technology-agnostic specification body.

## Outcome

- ✅ Impact: Comprehensive specification created with 6 prioritized user stories, 30 functional requirements, and 10 measurable success criteria
- 🧪 Tests: N/A - specification phase (acceptance scenarios defined for each user story)
- 📁 Files: 2 files created (spec.md, requirements.md)
- 🔁 Next prompts: Run `/sp.clarify` if any requirements need refinement, or `/sp.plan` to begin architecture design
- 🧠 Reflection: Successfully transformed user input with technical implementation details into a technology-agnostic specification. All FastAPI/Qdrant/OpenAI-Agents SDK specifics moved to Notes section while preserving the "zero hallucination" and "strict grounding" requirements as core functional needs.

## Evaluation notes (flywheel)

- Failure modes observed: None - specification created successfully on first attempt with all validation checks passing
- Graders run and results (PASS/FAIL): PASS - All 14 checklist validation items passed
- Prompt variant (if applicable): N/A - standard /sp.specify workflow
- Next experiment (smallest change to try): Future iterations could explore automated PHR creation via shell script first (as per workflow preference) before falling back to agent-native file creation
