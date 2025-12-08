# Quickstart Guide

**Feature**: 001-rag-book-chatbot
**Status**: Planning
**Last Updated**: 2025-12-06

## Overview

This guide walks you through setting up and running the Integrated RAG Chatbot for local development. Follow these steps to get the chatbot answering questions based on your book content.

**Estimated Setup Time**: 15-20 minutes

---

## Prerequisites

Before starting, ensure you have:

### Required Software
- **Python 3.12+** ([Download](https://www.python.org/downloads/))
- **Git** ([Download](https://git-scm.com/downloads))
- **Node.js 18+** (if testing frontend integration)

### Required Accounts & API Keys
- **Gemini API Key**:
  - Sign up at [Google AI Studio](https://makersuite.google.com/app/apikey)
  - Generate an API key
  - Free tier includes 60 requests/minute for embeddings and generation

- **Qdrant Cloud Account**:
  - Sign up at [Qdrant Cloud](https://cloud.qdrant.io/)
  - Create a free cluster (1GB storage, 100K vectors)
  - Note your cluster URL and API key

### Knowledge Requirements
- Basic Python programming
- Familiarity with REST APIs
- Understanding of virtual environments
- Basic command-line usage

---

## Step 1: Clone and Navigate to Backend

```bash
# Navigate to project root
cd D:\physical-ai-humanoid-robotics

# The backend directory will be created during implementation
# For now, this is the expected structure:
# backend/
#   ├── app/
#   │   ├── __init__.py
#   │   ├── main.py              # FastAPI application
#   │   ├── config.py            # Configuration management
#   │   ├── models.py            # Pydantic data models
#   │   ├── ingestion/           # Ingestion pipeline
#   │   ├── rag/                 # RAG logic and agents
#   │   └── api/                 # API endpoints
#   ├── tests/                   # Test suite
#   ├── scripts/                 # Utility scripts
#   ├── requirements.txt         # Python dependencies
#   └── .env.example             # Environment template
```

---

## Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# Verify Python version
python --version  # Should show Python 3.12.x or higher
```

---

## Step 3: Install Dependencies

```bash
# Navigate to backend directory (once created)
cd backend

# Install production dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Verify installation
pip list | grep -E "fastapi|qdrant|google-generativeai|openai"
```

**Expected Core Dependencies** (from research.md):
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
qdrant-client==1.7.0
google-generativeai==0.3.2
openai==1.6.1
python-dotenv==1.0.0
```

**Development Dependencies**:
```
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
httpx==0.25.2
black==23.12.0
ruff==0.1.8
```

---

## Step 4: Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use your preferred editor
```

**Required `.env` Configuration**:
```bash
# Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_CLIENT_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/

# Qdrant Configuration
QDRANT_URL=https://your-cluster.qdrant.io:6333
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_COLLECTION_NAME=book_content

# Application Settings
LOG_LEVEL=INFO
ENVIRONMENT=development
MAX_QUERY_LENGTH=2000
SIMILARITY_THRESHOLD=0.7
TOP_K_RESULTS=5

# Optional: Request tracking
ENABLE_REQUEST_IDS=true
```

**Security Note**: Never commit `.env` to version control. Ensure `.env` is in `.gitignore`.

---

## Step 5: Set Up Qdrant Collection

```bash
# Run the Qdrant setup script
python scripts/setup_qdrant.py

# Expected output:
# ✓ Connected to Qdrant at https://your-cluster.qdrant.io:6333
# ✓ Collection 'book_content' created successfully
# ✓ Indexed fields: chapter_number, section_title
# ✓ Configuration: 768 dimensions, COSINE distance
```

**Manual Setup Alternative** (if script not yet implemented):
```python
from qdrant_client import QdrantClient, models

client = QdrantClient(
    url="https://your-cluster.qdrant.io:6333",
    api_key="your_qdrant_api_key"
)

client.create_collection(
    collection_name="book_content",
    vectors_config=models.VectorParams(
        size=768,  # Gemini text-embedding-004 dimension
        distance=models.Distance.COSINE
    )
)

# Create payload indexes for faster filtering
client.create_payload_index(
    collection_name="book_content",
    field_name="chapter_number",
    field_schema=models.PayloadSchemaType.INTEGER
)

client.create_payload_index(
    collection_name="book_content",
    field_name="section_title",
    field_schema=models.PayloadSchemaType.KEYWORD
)
```

---

## Step 6: Ingest Book Content

```bash
# Run the ingestion script
python scripts/ingest_chapters.py --source ../frontend/docs

# Expected output:
# Reading chapters from: D:\physical-ai-humanoid-robotics\frontend\docs
#
# Processing Chapter 1: Introduction to Physical AI...
#   ✓ Chunked into 12 segments (avg 342 words)
#   ✓ Generated embeddings (768-dim)
#   ✓ Uploaded to Qdrant
#   Duration: 8.3s
#
# Processing Chapter 2: Humanoid Robotics Basics...
#   ✓ Chunked into 15 segments (avg 298 words)
#   ✓ Generated embeddings (768-dim)
#   ✓ Uploaded to Qdrant
#   Duration: 10.1s
#
# ========================================
# Ingestion Summary:
#   Total chapters: 10
#   Total segments: 127
#   Total vectors: 127
#   Success rate: 100%
#   Total duration: 1m 42s
# ========================================
```

**Ingestion Options**:
```bash
# Ingest specific chapter
python scripts/ingest_chapters.py --source ../frontend/docs --chapter 3

# Re-ingest (replaces existing vectors for updated chapters)
python scripts/ingest_chapters.py --source ../frontend/docs --reingest

# Dry run (no uploads)
python scripts/ingest_chapters.py --source ../frontend/docs --dry-run
```

**Verify Ingestion**:
```python
from qdrant_client import QdrantClient

client = QdrantClient(url="...", api_key="...")
info = client.get_collection("book_content")

print(f"Total vectors: {info.points_count}")  # Should match segment count
print(f"Vector size: {info.config.params.vectors.size}")  # Should be 768
```

---

## Step 7: Start the Development Server

```bash
# Start FastAPI server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Expected output:
# INFO:     Will watch for changes in these directories: ['D:\\physical-ai-humanoid-robotics\\backend']
# INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
# INFO:     Started reloader process [12345] using WatchFiles
# INFO:     Started server process [12346]
# INFO:     Waiting for application startup.
# INFO:     Application startup complete.
```

**Production Mode** (no auto-reload):
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## Step 8: Verify the API

### Health Check

```bash
curl http://localhost:8000/health

# Expected response:
{
  "status": "healthy",
  "checks": {
    "api": "ok",
    "qdrant": "ok",
    "gemini_config": "ok"
  },
  "timestamp": "2025-12-06T10:35:00Z"
}
```

### Interactive API Docs

Open in your browser:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Step 9: Test the Chatbot

### Example 1: Book Question

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is reinforcement learning?"
  }'

# Expected response:
{
  "answer": "Reinforcement learning is a machine learning paradigm where agents learn through interaction with an environment to maximize cumulative reward...",
  "citations": [
    {
      "chapter_number": 3,
      "chapter_title": "Machine Learning Fundamentals",
      "section_title": "Introduction to RL",
      "snippet": "Reinforcement learning is a type of machine learning where agents learn through interaction...",
      "similarity_score": 0.89
    }
  ],
  "query_type": "book_question",
  "confidence": 0.89,
  "content_found": true
}
```

### Example 2: Selected Text Explanation

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Explain this concept",
    "selected_text": "Reinforcement learning is a type of machine learning where agents learn through interaction with an environment."
  }'

# Expected response:
{
  "answer": "This passage describes the core mechanism of reinforcement learning...",
  "citations": [
    {
      "chapter_number": 3,
      "chapter_title": "Machine Learning Fundamentals",
      "section_title": "Introduction to RL",
      "snippet": "Reinforcement learning is a type of machine learning where agents learn through interaction...",
      "similarity_score": 1.0
    }
  ],
  "query_type": "selected_text_explanation",
  "confidence": 1.0,
  "content_found": true
}
```

### Example 3: Greeting

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Hello!"
  }'

# Expected response:
{
  "answer": "Hello! I'm your book assistant. I can answer questions about the book's content, explain concepts, and help you understand specific passages. What would you like to know?",
  "citations": [],
  "query_type": "greeting",
  "confidence": null,
  "content_found": true
}
```

### Example 4: Out-of-Scope Query

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the weather today?"
  }'

# Expected response:
{
  "answer": "I can only answer questions about this book's content. Please ask me about topics covered in the chapters.",
  "citations": [],
  "query_type": "out_of_scope",
  "confidence": null,
  "content_found": true
}
```

---

## Step 10: Run Tests

```bash
# Run full test suite
pytest

# Run with coverage report
pytest --cov=app --cov-report=html

# Run specific test categories
pytest tests/unit/           # Unit tests only
pytest tests/integration/    # Integration tests only
pytest tests/contracts/      # Contract tests only

# Run tests matching a pattern
pytest -k "test_query_classification"

# Verbose output
pytest -v
```

**Expected Test Output**:
```
============================= test session starts ==============================
platform win32 -- Python 3.12.0, pytest-7.4.3
collected 47 items

tests/unit/test_chunking.py ..................                          [ 38%]
tests/unit/test_classification.py .........                             [ 57%]
tests/unit/test_models.py ..........                                    [ 78%]
tests/integration/test_rag_pipeline.py .....                            [ 89%]
tests/contracts/test_api.py .....                                       [100%]

============================= 47 passed in 12.34s ===============================
```

---

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'app'`

**Solution**: Ensure you're in the `backend/` directory and the virtual environment is activated.

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

---

### Issue: `qdrant_client.exceptions.UnexpectedResponse: <Response [401]>`

**Solution**: Check your Qdrant API key and URL in `.env`.

```bash
# Verify Qdrant credentials
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('URL:', os.getenv('QDRANT_URL')); print('Key present:', bool(os.getenv('QDRANT_API_KEY')))"
```

---

### Issue: `google.generativeai.types.generation_types.StopCandidateException`

**Solution**: Gemini API key is invalid or quota exceeded.

```bash
# Test Gemini API directly
python -c "import google.generativeai as genai; import os; from dotenv import load_dotenv; load_dotenv(); genai.configure(api_key=os.getenv('GEMINI_API_KEY')); print(genai.embed_content(model='models/text-embedding-004', content='test'))"
```

---

### Issue: `ValueError: Query exceeds maximum length of 2000 characters`

**Solution**: This is expected validation. Shorten your query or adjust `MAX_QUERY_LENGTH` in `.env`.

---

### Issue: Empty `citations` array for book questions

**Solution**: Content may not be ingested, or similarity threshold is too high.

```bash
# Check Qdrant collection
python -c "from qdrant_client import QdrantClient; import os; from dotenv import load_dotenv; load_dotenv(); client = QdrantClient(url=os.getenv('QDRANT_URL'), api_key=os.getenv('QDRANT_API_KEY')); print(client.get_collection('book_content').points_count)"

# If count is 0, re-run ingestion:
python scripts/ingest_chapters.py --source ../frontend/docs

# If count > 0 but still no results, lower threshold temporarily:
# In .env: SIMILARITY_THRESHOLD=0.5
```

---

### Issue: Slow response times (> 5 seconds)

**Possible Causes**:
1. Large chunk sizes (> 500 words)
2. High `TOP_K_RESULTS` value (> 10)
3. Network latency to Qdrant/Gemini

**Solutions**:
```bash
# Adjust configuration in .env
TOP_K_RESULTS=3              # Reduce retrieval count
SIMILARITY_THRESHOLD=0.75    # Reduce search space

# Check network latency
ping your-cluster.qdrant.io
```

---

### Issue: `RuntimeError: No embeddings generated for segment`

**Solution**: Gemini API rate limit exceeded or network issue.

```bash
# Add retry logic in ingestion script (already implemented in research.md)
# Or manually reduce batch size:
python scripts/ingest_chapters.py --source ../frontend/docs --batch-size 5
```

---

## Development Workflow

### Typical Development Cycle

1. **Make Code Changes**: Edit files in `app/`
2. **Auto-Reload**: FastAPI server automatically reloads (if using `--reload`)
3. **Test Manually**: Use `curl` or Swagger UI at http://localhost:8000/docs
4. **Run Tests**: `pytest tests/unit/test_<module>.py`
5. **Check Coverage**: `pytest --cov=app`
6. **Format Code**: `black app/ tests/`
7. **Lint Code**: `ruff check app/ tests/`
8. **Commit Changes**: Follow conventional commit format

### Code Quality Commands

```bash
# Format all code
black app/ tests/ scripts/

# Check code quality
ruff check app/ tests/ scripts/

# Auto-fix linting issues
ruff check --fix app/ tests/ scripts/

# Type checking (if using mypy)
mypy app/
```

---

## Next Steps

After successfully completing this quickstart:

1. **Read the Implementation Plan**: Review `specs/001-rag-book-chatbot/plan.md` for architectural decisions
2. **Explore Data Models**: See `specs/001-rag-book-chatbot/data-model.md` for entity definitions
3. **Review API Contracts**: Check `specs/001-rag-book-chatbot/contracts/openapi.yaml` for full API specification
4. **Understand RAG Research**: Read `specs/001-rag-book-chatbot/research.md` for technology decisions
5. **Run Task Decomposition**: Execute `/sp.tasks` to see implementation breakdown
6. **Integrate with Frontend**: Connect the chatbot to the Docusaurus book interface

---

## Production Deployment Checklist

Before deploying to production:

- [ ] Set `ENVIRONMENT=production` in `.env`
- [ ] Use production Qdrant cluster (not free tier for high traffic)
- [ ] Configure proper logging (structured JSON logs)
- [ ] Set up monitoring (health checks, metrics, alerts)
- [ ] Enable CORS with specific allowed origins
- [ ] Use HTTPS for all API endpoints
- [ ] Set up rate limiting (e.g., 100 requests/minute per IP)
- [ ] Configure secrets management (not `.env` files)
- [ ] Set `LOG_LEVEL=WARNING` or `ERROR` (not `INFO`)
- [ ] Enable request ID tracking for debugging
- [ ] Set up error tracking (e.g., Sentry)
- [ ] Configure database backups (Qdrant snapshots)
- [ ] Test failover scenarios (Qdrant/Gemini downtime)
- [ ] Document runbooks for common issues
- [ ] Set up CI/CD pipeline (GitHub Actions)

---

## Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Qdrant Documentation**: https://qdrant.tech/documentation/
- **Gemini API Documentation**: https://ai.google.dev/docs
- **OpenAI-Agents SDK**: https://github.com/openai/openai-agents-python
- **Pydantic Documentation**: https://docs.pydantic.dev/

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the implementation plan (`specs/001-rag-book-chatbot/plan.md`)
3. Search existing GitHub issues
4. Create a new issue with detailed reproduction steps

---

**Last Updated**: 2025-12-06
**Maintainer**: Development Team
