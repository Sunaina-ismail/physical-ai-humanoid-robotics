# Data Model

**Feature**: 001-rag-book-chatbot
**Status**: Planning
**Last Updated**: 2025-12-06

## Overview

This document defines the core data entities for the Integrated RAG Chatbot system. All entities use Pydantic for validation and serialization.

---

## Entity Definitions

### 1. BookChapter

Represents a single chapter from the book source content.

```python
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from pathlib import Path

class BookChapter(BaseModel):
    """
    Represents a complete book chapter before chunking.

    Source: Markdown files in frontend/docs directory.
    """
    chapter_number: int = Field(
        ...,
        ge=1,
        description="Sequential chapter number (1-indexed)"
    )
    title: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Chapter title as it appears in the book"
    )
    file_path: Path = Field(
        ...,
        description="Absolute path to the source Markdown file"
    )
    raw_content: str = Field(
        ...,
        min_length=1,
        description="Full chapter content in Markdown format"
    )
    word_count: int = Field(
        ...,
        ge=0,
        description="Total word count for the chapter"
    )
    metadata: dict = Field(
        default_factory=dict,
        description="Additional chapter metadata (author, date, tags, etc.)"
    )

    @field_validator('file_path')
    @classmethod
    def validate_file_exists(cls, v: Path) -> Path:
        if not v.exists():
            raise ValueError(f"Chapter file does not exist: {v}")
        if not v.suffix == '.md':
            raise ValueError(f"Chapter file must be Markdown (.md): {v}")
        return v

    @field_validator('raw_content')
    @classmethod
    def validate_content_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Chapter content cannot be empty or whitespace-only")
        return v
```

**Usage Context**: Created during ingestion when reading from `frontend/docs` directory.

---

### 2. ContentSegment

Represents a chunk of book content after semantic chunking, ready for embedding.

```python
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

class ContentSegment(BaseModel):
    """
    A semantically coherent chunk of book content.

    Target size: 200-500 words
    Stored in Qdrant with vector embedding.
    """
    text: str = Field(
        ...,
        min_length=10,
        description="The actual text content of this segment"
    )
    chapter_number: int = Field(
        ...,
        ge=1,
        description="Chapter this segment belongs to"
    )
    section_title: str = Field(
        ...,
        description="Section heading within the chapter (empty string if none)"
    )
    order: int = Field(
        ...,
        ge=0,
        description="Sequential position within the chapter (0-indexed)"
    )
    word_count: int = Field(
        ...,
        ge=0,
        description="Word count for this segment"
    )
    embedding: Optional[List[float]] = Field(
        default=None,
        description="768-dimensional Gemini embedding vector (None before embedding)"
    )
    metadata: dict = Field(
        default_factory=dict,
        description="Inherited chapter metadata plus segment-specific data"
    )

    @field_validator('text')
    @classmethod
    def validate_text_length(cls, v: str) -> str:
        words = len(v.split())
        if words < 20:
            raise ValueError(f"Segment too short ({words} words, minimum 20)")
        if words > 600:
            raise ValueError(f"Segment too long ({words} words, maximum 600)")
        return v

    @field_validator('embedding')
    @classmethod
    def validate_embedding_dimensions(cls, v: Optional[List[float]]) -> Optional[List[float]]:
        if v is not None:
            if len(v) != 768:
                raise ValueError(f"Embedding must be 768-dimensional, got {len(v)}")
        return v

    def to_qdrant_point(self, point_id: str) -> dict:
        """
        Convert to Qdrant point format.

        Returns:
            dict: Qdrant point with id, vector, and payload
        """
        if self.embedding is None:
            raise ValueError("Cannot convert segment without embedding to Qdrant point")

        return {
            "id": point_id,
            "vector": self.embedding,
            "payload": {
                "text": self.text,
                "chapter_number": self.chapter_number,
                "section_title": self.section_title,
                "order": self.order,
                "word_count": self.word_count,
                **self.metadata
            }
        }
```

**Usage Context**: Created during chunking, embedded before Qdrant upload.

---

### 3. Query

Represents a user's question or input to the chatbot.

```python
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from datetime import datetime

class Query(BaseModel):
    """
    User input to the chatbot.

    Validates length constraints and processes classification.
    """
    query: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="The user's question or input text"
    )
    selected_text: Optional[str] = Field(
        default=None,
        max_length=5000,
        description="Optional text selected from the book for explanation"
    )
    query_type: Optional[Literal[
        "greeting",
        "chit_chat",
        "book_question",
        "selected_text_explanation",
        "out_of_scope"
    ]] = Field(
        default=None,
        description="Classified query type (set by backend)"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the query was received"
    )

    @field_validator('query')
    @classmethod
    def validate_not_whitespace_only(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Query cannot be empty or whitespace-only")
        return v

    @field_validator('selected_text')
    @classmethod
    def validate_selected_text(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Selected text cannot be whitespace-only (omit field instead)")
        return v
```

**Usage Context**: Created from `POST /chat` request body.

---

### 4. ChapterCitation

Represents a citation to a specific book chapter/section.

```python
from pydantic import BaseModel, Field

class ChapterCitation(BaseModel):
    """
    A citation reference to book content.

    Included in chatbot responses to ground answers.
    """
    chapter_number: int = Field(
        ...,
        ge=1,
        description="Chapter number being cited"
    )
    chapter_title: str = Field(
        ...,
        description="Title of the cited chapter"
    )
    section_title: str = Field(
        default="",
        description="Section within the chapter (empty if whole chapter)"
    )
    snippet: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="Brief excerpt from the cited content"
    )
    similarity_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Cosine similarity score (0.7-1.0 range expected)"
    )

    def format_citation(self) -> str:
        """
        Format citation for display in chatbot response.

        Returns:
            str: Human-readable citation string
        """
        if self.section_title:
            return f"Chapter {self.chapter_number}: {self.chapter_title} — {self.section_title}"
        return f"Chapter {self.chapter_number}: {self.chapter_title}"
```

**Usage Context**: Generated during RAG retrieval, included in Response entity.

---

### 5. Response

Represents the chatbot's response to a user query.

```python
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Literal

class Response(BaseModel):
    """
    Chatbot response with grounding and citations.

    Returned by POST /chat endpoint.
    """
    answer: str = Field(
        ...,
        min_length=1,
        description="The chatbot's response text"
    )
    citations: List[ChapterCitation] = Field(
        default_factory=list,
        description="List of chapter citations (empty for greetings/chit-chat)"
    )
    query_type: Literal[
        "greeting",
        "chit_chat",
        "book_question",
        "selected_text_explanation",
        "out_of_scope"
    ] = Field(
        ...,
        description="Classified type of the original query"
    )
    confidence: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Response confidence (None for non-RAG responses)"
    )
    content_found: bool = Field(
        ...,
        description="Whether relevant content was found (always True for non-RAG)"
    )

    @field_validator('citations')
    @classmethod
    def validate_citations_for_query_type(cls, v: List[ChapterCitation], info) -> List[ChapterCitation]:
        """
        Ensure citations align with query type.
        """
        query_type = info.data.get('query_type')

        # Non-RAG query types should have no citations
        if query_type in ['greeting', 'chit_chat', 'out_of_scope']:
            if len(v) > 0:
                raise ValueError(f"Query type '{query_type}' should not have citations")

        # RAG query types should have citations if content was found
        if query_type in ['book_question', 'selected_text_explanation']:
            content_found = info.data.get('content_found', True)
            if content_found and len(v) == 0:
                raise ValueError(f"Query type '{query_type}' with content_found=True must have citations")

        return v

    @field_validator('confidence')
    @classmethod
    def validate_confidence_threshold(cls, v: Optional[float], info) -> Optional[float]:
        """
        Ensure confidence meets minimum threshold for RAG responses.
        """
        if v is not None and v < 0.7:
            raise ValueError(f"Confidence {v} below minimum threshold 0.7")
        return v
```

**Usage Context**: Created by RAG agent, returned in API response.

---

### 6. IngestionLog

Tracks ingestion operations for audit and debugging.

```python
from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime

class IngestionLog(BaseModel):
    """
    Audit log entry for ingestion operations.

    Written to logs during ingestion script execution.
    """
    operation: Literal["initial_ingest", "re_ingest", "delete", "update"] = Field(
        ...,
        description="Type of ingestion operation performed"
    )
    chapter_number: int = Field(
        ...,
        ge=1,
        description="Chapter affected by this operation"
    )
    chapter_title: str = Field(
        ...,
        description="Title of the affected chapter"
    )
    segments_processed: int = Field(
        ...,
        ge=0,
        description="Number of content segments created/updated/deleted"
    )
    vectors_deleted: int = Field(
        default=0,
        ge=0,
        description="Number of old vectors deleted (for re-ingestion)"
    )
    status: Literal["success", "partial_failure", "failure"] = Field(
        ...,
        description="Overall operation status"
    )
    error_message: Optional[str] = Field(
        default=None,
        description="Error details if status is not success"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the operation completed"
    )
    duration_seconds: float = Field(
        ...,
        ge=0.0,
        description="Time taken for the operation"
    )

    def to_log_entry(self) -> str:
        """
        Format as structured log entry.

        Returns:
            str: JSON-formatted log line
        """
        import json
        return json.dumps({
            "level": "ERROR" if self.status == "failure" else "INFO",
            "operation": self.operation,
            "chapter": f"{self.chapter_number}: {self.chapter_title}",
            "segments": self.segments_processed,
            "vectors_deleted": self.vectors_deleted,
            "status": self.status,
            "error": self.error_message,
            "timestamp": self.timestamp.isoformat(),
            "duration_s": self.duration_seconds
        })
```

**Usage Context**: Created after each ingestion operation, written to application logs.

---

### 7. ErrorRecord

Structured error response format.

```python
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

class ErrorRecord(BaseModel):
    """
    Structured error response.

    Returned by API endpoints on failure.
    """
    error_type: Literal[
        "validation_error",
        "configuration_error",
        "database_error",
        "embedding_error",
        "agent_error",
        "not_found",
        "internal_error"
    ] = Field(
        ...,
        description="Category of error"
    )
    message: str = Field(
        ...,
        min_length=1,
        description="Human-readable error description"
    )
    details: Optional[dict] = Field(
        default=None,
        description="Additional error context (no secrets)"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the error occurred"
    )
    request_id: Optional[str] = Field(
        default=None,
        description="Request ID for tracing (if available)"
    )

    def to_api_response(self) -> dict:
        """
        Convert to FastAPI error response format.

        Returns:
            dict: JSON-serializable error response
        """
        return {
            "error": self.error_type,
            "message": self.message,
            "details": self.details,
            "timestamp": self.timestamp.isoformat(),
            "request_id": self.request_id
        }

    @classmethod
    def validation_error(cls, message: str, details: Optional[dict] = None) -> "ErrorRecord":
        """Factory method for validation errors."""
        return cls(error_type="validation_error", message=message, details=details)

    @classmethod
    def configuration_error(cls, message: str) -> "ErrorRecord":
        """Factory method for configuration errors."""
        return cls(error_type="configuration_error", message=message)

    @classmethod
    def database_error(cls, message: str, details: Optional[dict] = None) -> "ErrorRecord":
        """Factory method for database errors."""
        return cls(error_type="database_error", message=message, details=details)

    @classmethod
    def not_found(cls, resource: str) -> "ErrorRecord":
        """Factory method for not found errors."""
        return cls(
            error_type="not_found",
            message=f"No relevant content found for: {resource}"
        )
```

**Usage Context**: Created by exception handlers, returned in API error responses.

---

## Entity Relationships

```
BookChapter (1) --chunks-into--> (N) ContentSegment
                                      |
                                      | embeds-to
                                      v
                                  Qdrant Vector DB
                                      ^
                                      | retrieves-from
                                      |
Query (1) ----classified-as----> query_type
      |                              |
      v                              v
Response (1) --cites--> (N) ChapterCitation
                              |
                              | references
                              v
                        ContentSegment

IngestionLog --tracks--> BookChapter operations
ErrorRecord --captures--> All error scenarios
```

---

## Validation Rules Summary

| Entity | Key Constraints |
|--------|----------------|
| BookChapter | File must exist, be .md format, have non-empty content |
| ContentSegment | 20-600 words, embedding must be 768-dimensional |
| Query | 1-2000 characters, no whitespace-only input |
| ChapterCitation | Similarity score 0.0-1.0, snippet 10-500 chars |
| Response | Citations required for RAG queries with content_found=True, confidence ≥ 0.7 |
| IngestionLog | Segments/vectors counts must be non-negative |
| ErrorRecord | Must have non-empty message, no secrets in details |

---

## Database Mapping

### Qdrant Collection: `book_content`

**Vector Configuration**:
- Dimensions: 768 (Gemini text-embedding-004)
- Distance: COSINE
- Indexed fields: `chapter_number`, `section_title`

**Point Payload Schema** (maps to ContentSegment):
```json
{
  "text": "string (the actual content)",
  "chapter_number": "integer",
  "section_title": "string",
  "order": "integer",
  "word_count": "integer",
  "metadata": {
    "chapter_title": "string",
    // ... additional chapter metadata
  }
}
```

**Search Pattern**:
```python
from qdrant_client import QdrantClient, models

results = client.search(
    collection_name="book_content",
    query_vector=query_embedding,  # 768-dimensional list
    limit=5,
    score_threshold=0.7,
    with_payload=True
)
```

---

## Usage Examples

### Creating a Content Segment

```python
from pathlib import Path
import google.generativeai as genai

# After chunking a chapter
segment = ContentSegment(
    text="Reinforcement learning is a type of machine learning...",
    chapter_number=3,
    section_title="Introduction to RL",
    order=0,
    word_count=342,
    metadata={
        "chapter_title": "Machine Learning Fundamentals",
        "author": "Jane Doe"
    }
)

# Generate embedding
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
result = genai.embed_content(
    model="models/text-embedding-004",
    content=segment.text,
    task_type="retrieval_document"
)
segment.embedding = result['embedding']

# Convert to Qdrant point
point = segment.to_qdrant_point(point_id=f"ch3_seg0")
```

### Creating a Response with Citations

```python
# After RAG retrieval
citations = [
    ChapterCitation(
        chapter_number=3,
        chapter_title="Machine Learning Fundamentals",
        section_title="Introduction to RL",
        snippet="Reinforcement learning is a type of machine learning...",
        similarity_score=0.89
    )
]

response = Response(
    answer="Reinforcement learning is a machine learning paradigm where agents learn through interaction with an environment...",
    citations=citations,
    query_type="book_question",
    confidence=0.89,
    content_found=True
)
```

### Logging an Ingestion Operation

```python
from datetime import datetime
import time

start_time = time.time()

# ... perform ingestion ...

log_entry = IngestionLog(
    operation="re_ingest",
    chapter_number=3,
    chapter_title="Machine Learning Fundamentals",
    segments_processed=15,
    vectors_deleted=12,
    status="success",
    duration_seconds=time.time() - start_time
)

print(log_entry.to_log_entry())  # JSON log line
```

---

## Notes

- All timestamps use UTC timezone
- Pydantic models automatically handle JSON serialization/deserialization
- Field validators enforce data quality at the boundary
- Factory methods on ErrorRecord simplify error creation
- ContentSegment.to_qdrant_point() ensures consistent Qdrant payload structure
- Response validation ensures citations align with query classification
