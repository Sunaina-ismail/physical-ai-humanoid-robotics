# Integrated RAG Chatbot Backend

Backend API for the book's Integrated Retrieval-Augmented Generation (RAG) chatbot.

## Features

- **RAG-powered Q&A**: Answer questions strictly based on book content
- **Selected Text Explanation**: Explain highlighted passages from the book
- **Query Classification**: Handle greetings, chit-chat, and out-of-scope questions
- **Chapter Citations**: All answers include proper chapter/section references
- **Zero Hallucination**: Strict grounding requirement - no fabricated information

## Tech Stack

- **Framework**: FastAPI (async Python web framework)
- **Vector Database**: Qdrant Cloud (semantic search)
- **Embeddings**: Gemini text-embedding-004 (768-dimensional)
- **Agent**: OpenAI-Agents SDK with Gemini backend
- **Validation**: Pydantic (data models)

## Prerequisites

- Python 3.12+
- Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- Qdrant Cloud account ([Sign up](https://cloud.qdrant.io/))

## Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 2. Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your credentials
# - GEMINI_API_KEY: Your Gemini API key
# - QDRANT_URL: Your Qdrant cluster URL
# - QDRANT_API_KEY: Your Qdrant API key
```

### 3. Setup Qdrant Collection

```bash
# Run collection setup script
python scripts/setup_qdrant.py
```

### 4. Ingest Book Content

```bash
# Ingest chapters from frontend/docs directory
python scripts/ingest.py --source ../frontend/docs
```

### 5. Start Development Server

```bash
# Start FastAPI server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Development

### Code Formatting

```bash
# Format code with Black
black app/ tests/ scripts/

# Lint code with Ruff
ruff check app/ tests/ scripts/

# Auto-fix linting issues
ruff check --fix app/ tests/ scripts/
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_embeddings.py

# Run tests matching pattern
pytest -k "test_query"
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Environment configuration
│   ├── models.py            # Pydantic data models
│   ├── services/            # Business logic
│   │   ├── embeddings.py    # Gemini embeddings
│   │   ├── vector_store.py  # Qdrant operations
│   │   ├── query_classifier.py  # Query type detection
│   │   ├── rag_agent.py     # OpenAI-Agents SDK agent
│   │   └── chunking.py      # Content chunking
│   └── utils/               # Utilities
│       ├── logger.py        # Structured logging
│       └── validators.py    # Input validation
├── tests/
│   ├── unit/                # Unit tests
│   ├── integration/         # Integration tests
│   └── conftest.py          # Pytest fixtures
├── scripts/
│   ├── setup_qdrant.py      # Qdrant collection setup
│   └── ingest.py            # Content ingestion
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── pyproject.toml           # Tool configuration
└── .env.example             # Environment template
```

## API Endpoints

### POST /chat

Main chatbot endpoint for all query types.

**Request**:
```json
{
  "query": "What is reinforcement learning?",
  "selected_text": "optional highlighted text"
}
```

**Response**:
```json
{
  "answer": "Reinforcement learning is...",
  "citations": [
    {
      "chapter_number": 3,
      "chapter_title": "Machine Learning Fundamentals",
      "section_title": "Introduction to RL",
      "snippet": "Reinforcement learning is...",
      "similarity_score": 0.89
    }
  ],
  "query_type": "book_question",
  "confidence": 0.89,
  "content_found": true
}
```

### GET /health

Health check endpoint.

**Response**:
```json
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

## Troubleshooting

### Issue: ModuleNotFoundError

**Solution**: Ensure virtual environment is activated and dependencies are installed:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Issue: Qdrant Connection Error (401)

**Solution**: Check QDRANT_URL and QDRANT_API_KEY in .env file.

### Issue: Empty citations array

**Solution**:
1. Check Qdrant collection has vectors: `python scripts/setup_qdrant.py --check`
2. If empty, re-run ingestion: `python scripts/ingest.py --source ../frontend/docs`
3. If still empty, lower SIMILARITY_THRESHOLD in .env (try 0.5)

### Issue: GEMINI_API_KEY not set

**Solution**: Add your Gemini API key to .env file.

## Documentation

- [Feature Specification](../specs/001-rag-book-chatbot/spec.md)
- [Implementation Plan](../specs/001-rag-book-chatbot/plan.md)
- [Data Models](../specs/001-rag-book-chatbot/data-model.md)
- [API Contracts](../specs/001-rag-book-chatbot/contracts/openapi.yaml)
- [Quickstart Guide](../specs/001-rag-book-chatbot/quickstart.md)

## Deployment on Railway

### Step 1: Prepare Your Account
1. Sign up for a [Railway](https://railway.app) account
2. Install the Railway CLI: `npm install -g @railway/cli`
3. Login: `railway login`

### Step 2: Create a New Project
1. In your Railway dashboard, click "New Project"
2. Choose "GitHub Repo" and connect to your repository
3. Or use CLI: `railway init`

### Step 3: Set Environment Variables
In your Railway dashboard:
1. Go to your project
2. Click on "Variables" tab
3. Add the following environment variables:

**Required:**
- `GEMINI_API_KEY`: Your Gemini API key
- `GEMINI_BASE_URL`: `https://generativelanguage.googleapis.com/v1beta/openai/`
- `QDRANT_URL`: Your Qdrant instance URL
- `QDRANT_API_KEY`: Your Qdrant API key

**Optional:**
- `QDRANT_COLLECTION_NAME`: Default is `chatkit-bot`
- `LOG_LEVEL`: Default is `INFO`
- `MAX_QUERY_LENGTH`: Default is `2000`
- `SIMILARITY_THRESHOLD`: Default is `0.7`
- `TOP_K_RESULTS`: Default is `5`
- `ENVIRONMENT`: Default is `development`

### Step 4: Configure Build Settings

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Step 5: Deploy
1. Make sure your repository has a `requirements.txt` file
2. Push your changes to GitHub (if using GitHub integration)
3. Railway will automatically build and deploy your application
4. Monitor the build logs in the Railway dashboard

### Step 6: Setup Qdrant Collection (Post-Deployment)

After deployment, you need to set up your Qdrant collection:

1. **SSH into your Railway instance:**
   ```bash
   railway ssh
   ```

2. **Run the setup script:**
   ```bash
   python scripts/setup_qdrant.py
   ```

### Step 7: Ingest Content (Post-Deployment)

To add content to your Qdrant collection:

1. **Prepare your content:** Ensure your textbook content is in the `../frontend/docs` directory structure

2. **Run the ingestion script:**
   ```bash
   python scripts/ingest.py --source ../frontend/docs
   ```

## Alternative: Deploy Using Railway CLI

1. **Initialize Railway project:**
   ```bash
   cd backend
   railway init
   ```

2. **Link to your project:**
   ```bash
   railway link
   ```

3. **Set environment variables:**
   ```bash
   railway var set GEMINI_API_KEY=your_key_here
   railway var set GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
   railway var set QDRANT_URL=your_qdrant_url_here
   railway var set QDRANT_API_KEY=your_qdrant_api_key_here
   ```

4. **Deploy:**
   ```bash
   railway up
   ```

## Railway-Specific Configuration

### Environment Variables for Railway
```
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_COLLECTION_NAME=chatkit-bot
LOG_LEVEL=INFO
MAX_QUERY_LENGTH=2000
SIMILARITY_THRESHOLD=0.7
TOP_K_RESULTS=5
ENVIRONMENT=production
```

### Railway Configuration File
You can also create a `railway.toml` file in your project root:
```toml
[build]
builder = "nixpacks"
buildCommand = "pip install -r requirements.txt"

[deploy]
startCommand = "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
```

## Scaling Considerations on Railway

- **Qdrant**: Consider upgrading your Qdrant plan for production use
- **Gemini API**: Monitor usage and quotas for production traffic
- **Railway Resources**: Adjust instance size based on traffic needs
- **Database**: Monitor Qdrant performance and scale as needed

## Security on Railway

- Use Railway's secure environment variable storage
- Never commit API keys to version control
- Consider using Railway's private networking for production
- Implement proper authentication for production use if needed

## License

MIT
