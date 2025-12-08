# Technology Research: RAG Chatbot Implementation

**Feature**: Integrated RAG Chatbot for Book
**Date**: 2025-12-06
**Research Phase**: Phase 0

## Overview

This document captures technology research and implementation decisions for building a RAG (Retrieval-Augmented Generation) chatbot that answers questions strictly based on book content using FastAPI, Qdrant Cloud, Gemini embeddings, and OpenAI-Agents SDK.

---

## Research Question 1: Chunking Strategy

**Decision**: Semantic chunking at paragraph boundaries with 200-500 word target size

**Rationale**:
- Markdown content (Docusaurus docs) naturally chunks at paragraph/heading boundaries
- 200-500 words provides sufficient context without exceeding embedding model limits
- Preserves semantic coherence better than fixed token-count chunking
- Aligns with spec notes (plan.md:300 - "Target chunk size of 200-500 words")

**Implementation Approach**:
```python
def chunk_chapter(chapter_text: str, chapter_meta: dict) -> List[ContentSegment]:
    """
    Split chapter into semantically coherent chunks.

    Strategy:
    1. Split by markdown headings (##, ###) first
    2. If section > 500 words, split by paragraphs (\n\n)
    3. Track order within chapter for sequential retrieval
    """
    sections = split_by_headings(chapter_text)
    chunks = []
    order = 0

    for section_title, section_text in sections:
        paragraphs = section_text.split('\n\n')
        current_chunk = []
        word_count = 0

        for para in paragraphs:
            para_words = len(para.split())
            if word_count + para_words > 500 and current_chunk:
                # Save current chunk
                chunks.append(ContentSegment(
                    text='\n\n'.join(current_chunk),
                    chapter_ref=chapter_meta['chapter_number'],
                    section_ref=section_title,
                    order=order,
                    metadata=chapter_meta
                ))
                order += 1
                current_chunk = [para]
                word_count = para_words
            else:
                current_chunk.append(para)
                word_count += para_words

        # Save remaining chunk
        if current_chunk:
            chunks.append(ContentSegment(
                text='\n\n'.join(current_chunk),
                chapter_ref=chapter_meta['chapter_number'],
                section_ref=section_title,
                order=order,
                metadata=chapter_meta
            ))
            order += 1

    return chunks
```

**Alternatives Considered**:
- Fixed 512-token chunks → Rejected: Breaks semantic boundaries, harder to cite
- Sentence-level chunks → Rejected: Too granular, loses context
- Full chapters → Rejected: Exceeds token limits, reduces precision

**References**:
- Context7 research on semantic chunking best practices
- Plan.md line 300: "Target chunk size of 200-500 words"

---

## Research Question 2: Gemini Embedding Integration

**Decision**: Use `google-generativeai` SDK directly with `task_type` parameter for optimal retrieval

**Rationale**:
- Gemini `text-embedding-004` requires Google's official SDK (not OpenAI SDK)
- `task_type` parameter optimizes embeddings for "retrieval_document" vs "retrieval_query"
- Embedding dimension: 768 (verified from model specs)
- Separate from OpenAI-Agents SDK which handles LLM calls

**Implementation**:
```python
import google.generativeai as genai
import os

# Configure once at startup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_document_embedding(text: str) -> List[float]:
    """Generate embedding for document storage (ingestion)."""
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=text,
        task_type="retrieval_document"  # Optimized for storage
    )
    return result['embedding']

def generate_query_embedding(query: str) -> List[float]:
    """Generate embedding for search query."""
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=query,
        task_type="retrieval_query"  # Optimized for search
    )
    return result['embedding']
```

**Key Parameters**:
- `model`: "models/text-embedding-004" (latest Gemini embedding model)
- `task_type`: "retrieval_document" for ingestion, "retrieval_query" for searches
- Output dimension: 768 floats
- Rate limits: Check Gemini API quotas (typically 1500 requests/minute)

**Alternatives Considered**:
- OpenAI embeddings → Rejected: Spec requires Gemini text-embedding-004
- SentenceTransformers → Rejected: Spec requires Gemini model specifically

**References**:
- Google Generative AI SDK documentation
- Spec requirement: "Gemini `text-embedding-004` used for all embeddings" (spec.md:13)

---

## Research Question 3: Qdrant Collection Schema

**Decision**: Single collection with indexed metadata fields for efficient filtering

**Schema Design**:
```python
from qdrant_client import QdrantClient, models

collection_name = "book_content"
vector_size = 768  # text-embedding-004 dimension

# Create collection with vector config
client.create_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(
        size=vector_size,
        distance=models.Distance.COSINE  # Standard for semantic search
    )
)

# Create payload index for efficient chapter filtering
client.create_payload_index(
    collection_name=collection_name,
    field_name="chapter_number",
    field_schema=models.PayloadSchemaType.INTEGER
)

# Payload structure
payload_schema = {
    "chapter_number": int,        # For filtering by chapter
    "chapter_title": str,          # For citation display
    "section": str | None,         # Section name within chapter
    "order": int,                  # Sequential order in chapter
    "text": str,                   # Original chunk text (for response)
    "created_at": str              # ISO timestamp for re-ingestion tracking
}
```

**Rationale**:
- Single collection simplifies management and search
- COSINE distance metric is standard for normalized embeddings
- Payload index on `chapter_number` enables efficient chapter-specific queries
- `order` field allows reconstructing chapter sequence if needed
- `text` field stored in payload eliminates need to maintain separate text storage

**References**:
- Context7 Qdrant documentation: Collection creation and indexing patterns
- Plan.md lines 351-368: Qdrant Collection Schema decision

---

## Research Question 4: OpenAI-Agents SDK with Gemini Backend

**Decision**: Configure OpenAI SDK client with custom `base_url` pointing to Gemini's OpenAI-compatible endpoint

**Implementation**:
```python
from openai import OpenAI
from agents import Agent, function_tool, Runner
import os

# Create OpenAI client configured for Gemini
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Define tool for RAG retrieval
@function_tool
async def retrieve_book_content(query: str) -> str:
    """
    Retrieve relevant content from the book based on query.

    Args:
        query: The user's question or topic to search for

    Returns:
        Retrieved text segments with chapter citations
    """
    # 1. Generate query embedding
    query_embedding = generate_query_embedding(query)

    # 2. Search Qdrant
    search_results = qdrant_client.search(
        collection_name="book_content",
        query_vector=query_embedding,
        limit=5,  # Retrieve top 5 segments (per clarification)
        score_threshold=0.7  # Minimum similarity (per clarification)
    )

    # 3. Format results with citations
    if not search_results:
        return "No relevant content found in the book."

    formatted_results = []
    for result in search_results:
        chapter = result.payload['chapter_title']
        section = result.payload.get('section', '')
        text = result.payload['text']
        score = result.score

        formatted_results.append(
            f"[Chapter: {chapter}, Section: {section}, Relevance: {score:.2f}]\n{text}"
        )

    return "\n\n---\n\n".join(formatted_results)

# Create RAG agent
agent = Agent(
    client=client,
    model="gemini-1.5-flash",  # Fast, cost-effective model
    name="Book Q&A Assistant",
    instructions="""You are a helpful assistant that answers questions STRICTLY based on retrieved book content.

CRITICAL RULES:
1. ONLY use information from the retrieved content provided by the retrieve_book_content tool
2. NEVER fabricate, infer, or add information not explicitly in the retrieved content
3. ALWAYS cite the chapter and section for each piece of information used
4. If the retrieved content doesn't contain the answer, say "I couldn't find that information in the book"
5. Format citations at the end like: "Sources: Chapter X, Section Y"

Remember: Zero tolerance for hallucinations. Only use retrieved content.""",
    tools=[retrieve_book_content]
)

# Run agent
async def query_chatbot(user_query: str):
    result = await Runner.run(agent, input=user_query)
    return result.final_output
```

**Key Configuration**:
- `base_url`: Gemini's OpenAI-compatible endpoint
- `model`: "gemini-1.5-flash" (fast, cost-effective) or "gemini-1.5-pro" (higher quality)
- Tool pattern: Use `@function_tool` decorator for Qdrant retrieval
- Instructions: Explicit anti-hallucination rules in system prompt

**Rationale**:
- OpenAI-Agents SDK supports custom OpenAI-compatible endpoints via `base_url`
- Gemini provides OpenAI-compatible API at specified endpoint
- Function tools allow clean separation of retrieval logic
- Explicit instructions enforce grounding requirement

**References**:
- Context7 OpenAI-Agents SDK documentation: Custom base URL configuration
- OpenAI-Agents SDK: Function tools and agent creation patterns
- Plan.md lines 385-409: OpenAI-Agents SDK Configuration decision

---

## Research Question 5: Query Classification

**Decision**: Lightweight rule-based classifier using regex patterns

**Implementation**:
```python
import re
from enum import Enum

class QueryType(Enum):
    GREETING = "greeting"
    CHIT_CHAT = "chit_chat"
    BOOK_QUESTION = "book_question"
    SELECTED_TEXT = "selected_text"
    OUT_OF_SCOPE = "out_of_scope"  # Determined after vector search

def classify_query(query: str, has_selected_text: bool = False) -> QueryType:
    """
    Classify query type using rule-based patterns.

    Args:
        query: User's input text
        has_selected_text: Whether selected_text field is provided

    Returns:
        QueryType enum value
    """
    # Priority 1: Selected text explanation
    if has_selected_text:
        return QueryType.SELECTED_TEXT

    # Priority 2: Greeting patterns
    query_lower = query.lower().strip()
    greeting_patterns = [
        r'^(hi|hello|hey|greetings|good\s+(morning|afternoon|evening))',
        r'^(what\'s\s+up|howdy|yo)'
    ]
    for pattern in greeting_patterns:
        if re.match(pattern, query_lower):
            return QueryType.GREETING

    # Priority 3: Chit-chat patterns
    chit_chat_patterns = [
        r'how\s+are\s+you',
        r'thank(s| you)',
        r'(bye|goodbye|see\s+you)',
        r'what\'s\s+your\s+name',
        r'who\s+(are\s+you|made\s+you)'
    ]
    for pattern in chit_chat_patterns:
        if re.search(pattern, query_lower):
            return QueryType.CHIT_CHAT

    # Default: Book question (out-of-scope determined later by similarity score)
    return QueryType.BOOK_QUESTION

# Greeting response templates
GREETING_RESPONSES = [
    "Hello! I'm here to help you with questions about this book. What would you like to know?",
    "Hi there! Ask me anything about the book content, or highlight text for explanations.",
]

# Chit-chat response templates
CHIT_CHAT_RESPONSES = {
    "how_are_you": "I'm just a program, but I'm ready to help you explore this book! What can I answer for you?",
    "thanks": "You're welcome! Feel free to ask more questions about the book.",
    "bye": "Goodbye! Come back anytime you have questions about the book.",
}
```

**Rationale**:
- Simple regex patterns are fast and deterministic
- No need for ML model overhead for clear patterns
- Easy to extend and debug
- Greetings/chit-chat don't require RAG retrieval
- Out-of-scope detection deferred to similarity threshold (0.7)

**Alternatives Considered**:
- ML-based intent classifier → Rejected: Overkill for simple patterns, adds latency
- LLM-based classification → Rejected: Expensive, slower, unnecessary

**References**:
- Plan.md lines 372-383: Query Classification Logic decision
- Spec clarification: Query classification categories (spec.md:136)

---

## Research Question 6: Vector Search Optimization

**Decision**: Use score threshold filtering with top-k retrieval

**Implementation**:
```python
from qdrant_client import QdrantClient, models

def search_book_content(
    query_embedding: List[float],
    top_k: int = 5,  # Per clarification: 3-5 segments
    score_threshold: float = 0.7  # Per clarification: 70% minimum
) -> List[dict]:
    """
    Search for relevant book content with quality filtering.

    Args:
        query_embedding: Query vector from text-embedding-004
        top_k: Number of results to retrieve (3-5)
        score_threshold: Minimum similarity score (0.7)

    Returns:
        List of matching content segments with metadata
    """
    results = qdrant_client.search(
        collection_name="book_content",
        query_vector=query_embedding,
        limit=top_k,
        score_threshold=score_threshold,  # Qdrant filters below this
        with_payload=True,  # Include chapter/section metadata
        with_vectors=False  # Don't return vectors (not needed)
    )

    # If no results meet threshold, return empty (triggers "content not found")
    if not results:
        return []

    return [
        {
            "text": hit.payload["text"],
            "chapter": hit.payload["chapter_title"],
            "section": hit.payload.get("section", ""),
            "score": hit.score
        }
        for hit in results
    ]
```

**Key Parameters**:
- `limit=5`: Retrieve top 5 segments (clarification: 3-5 range)
- `score_threshold=0.7`: Only return results with ≥70% similarity (clarification)
- `with_payload=True`: Include metadata for citations
- `with_vectors=False`: Optimize performance by excluding vectors

**Rationale**:
- Score threshold ensures quality over quantity
- Top-5 provides sufficient context without noise
- Qdrant's native score filtering is efficient
- Metadata payload enables proper citations

**References**:
- Context7 Qdrant documentation: Search with score threshold
- Spec clarifications: 3-5 segments (spec.md:13), 0.7 threshold (spec.md:14)
- Plan.md line 175: FR-030 similarity threshold requirement

---

## Research Question 7: Re-ingestion Safety

**Decision**: Delete-then-insert pattern with logging and atomic operations

**Implementation**:
```python
import logging
from datetime import datetime
from qdrant_client import models

logger = logging.getLogger(__name__)

async def reingest_chapter(chapter_file: str, chapter_meta: dict):
    """
    Re-ingest a chapter by replacing existing vectors.

    Strategy:
    1. Count existing vectors for chapter
    2. Delete all vectors for chapter (by chapter_number filter)
    3. Generate new chunks and embeddings
    4. Insert new vectors
    5. Log operation with before/after counts

    Args:
        chapter_file: Path to markdown file
        chapter_meta: Chapter metadata (number, title, etc.)
    """
    chapter_num = chapter_meta['chapter_number']

    try:
        # 1. Count existing vectors
        existing_count = qdrant_client.count(
            collection_name="book_content",
            count_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="chapter_number",
                        match=models.MatchValue(value=chapter_num)
                    )
                ]
            )
        ).count

        logger.info(f"Re-ingesting Chapter {chapter_num}: Found {existing_count} existing vectors")

        # 2. Delete existing vectors for this chapter
        qdrant_client.delete(
            collection_name="book_content",
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="chapter_number",
                            match=models.MatchValue(value=chapter_num)
                        )
                    ]
                )
            )
        )

        logger.info(f"Deleted {existing_count} existing vectors for Chapter {chapter_num}")

        # 3. Read and chunk chapter
        chapter_text = read_markdown_file(chapter_file)
        chunks = chunk_chapter(chapter_text, chapter_meta)

        # 4. Generate embeddings
        points = []
        for idx, chunk in enumerate(chunks):
            embedding = generate_document_embedding(chunk.text)
            points.append(
                models.PointStruct(
                    id=f"{chapter_num}_{idx}",  # Unique ID pattern
                    vector=embedding,
                    payload={
                        "chapter_number": chapter_num,
                        "chapter_title": chapter_meta['title'],
                        "section": chunk.section_ref,
                        "order": chunk.order,
                        "text": chunk.text,
                        "created_at": datetime.utcnow().isoformat()
                    }
                )
            )

        # 5. Insert new vectors
        qdrant_client.upsert(
            collection_name="book_content",
            points=points,
            wait=True  # Wait for operation to complete
        )

        logger.info(f"Successfully re-ingested Chapter {chapter_num}: {len(points)} new vectors created")

        return {
            "success": True,
            "chapter": chapter_num,
            "old_count": existing_count,
            "new_count": len(points)
        }

    except Exception as e:
        logger.error(f"Re-ingestion failed for Chapter {chapter_num}: {e}", exc_info=True)
        return {
            "success": False,
            "chapter": chapter_num,
            "error": str(e)
        }
```

**Safety Measures**:
- Count before delete for audit trail
- Filter-based deletion ensures only target chapter is affected
- `wait=True` on upsert ensures atomic completion
- Comprehensive logging with before/after counts
- Try-except wrapping for error containment
- Unique ID pattern prevents collisions

**Rationale**:
- Delete-then-insert is simpler than update-in-place for vectors
- Filter-based deletion prevents accidental data loss
- Logging provides audit trail for debugging
- Atomic operations prevent partial updates
- Error handling allows continuation with other chapters

**Alternatives Considered**:
- Update-in-place → Rejected: Qdrant doesn't support true updates, only upsert by ID
- Versioning → Rejected: Adds complexity, spec requires replacement (spec.md:16)
- Blue-green collections → Future enhancement, not needed for v1

**References**:
- Context7 Qdrant documentation: Delete with filters
- Spec clarification: Replace old vectors entirely (spec.md:16)
- Plan.md lines 411-429: Re-ingestion Strategy decision

---

## Implementation Timeline Considerations

1. **Chunking & Embedding** (Priority 1)
   - Critical path: Must be done before any vector operations
   - Estimated effort: 2-3 tasks

2. **Qdrant Setup** (Priority 1)
   - Can be done in parallel with chunking logic
   - Estimated effort: 2 tasks

3. **Query Classification** (Priority 2)
   - Independent of RAG pipeline
   - Can be developed/tested in parallel
   - Estimated effort: 1-2 tasks

4. **OpenAI-Agents Integration** (Priority 1)
   - Depends on Qdrant setup
   - Critical for RAG functionality
   - Estimated effort: 3-4 tasks

5. **Re-ingestion Pipeline** (Priority 2)
   - Builds on initial ingestion
   - Can be delayed until after MVP
   - Estimated effort: 2 tasks

---

## Open Questions & Future Enhancements

### Resolved in Research
- ✅ Chunking strategy: Semantic boundaries, 200-500 words
- ✅ Embedding integration: google-generativeai SDK with task_type
- ✅ Qdrant schema: Single collection with indexed metadata
- ✅ OpenAI-Agents config: Custom base_url to Gemini endpoint
- ✅ Query classification: Rule-based regex patterns
- ✅ Vector search: Score threshold + top-k
- ✅ Re-ingestion: Delete-then-insert with logging

### Future Enhancements (Out of Scope for v1)
- Caching of frequent queries to reduce embedding costs
- A/B testing of chunk sizes for optimal retrieval
- Multi-language support beyond English
- Conversation history for multi-turn Q&A
- User feedback mechanism (thumbs up/down)
- Blue-green collection switching for zero-downtime updates

---

**Research Status**: ✅ Complete
**Next Phase**: Phase 1 Design Artifacts (data-model.md, contracts/, quickstart.md)
