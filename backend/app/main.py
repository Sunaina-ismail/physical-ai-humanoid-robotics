"""
FastAPI Application

Main entry point for the RAG chatbot backend API.
"""

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app import __version__
from app.config import settings
from app.models import ErrorRecord, Query, Response
from app.services.rag_agent import rag_agent
from app.utils.logger import setup_logger
from app.utils.validators import validate_query_length

logger = setup_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="RAG Book Chatbot API",
    description="Backend API for the integrated RAG chatbot system",
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
)


# Request validation middleware
@app.middleware("http")
async def validate_request_middleware(request: Request, call_next):
    """
    Middleware to validate incoming requests.

    Validates query length and content for /chat endpoint.
    """
    # Only validate for /chat endpoint
    if request.url.path == "/chat" and request.method == "POST":
        try:
            # Parse request body
            body = await request.json()

            # Validate query field exists
            if "query" not in body:
                error = ErrorRecord.validation_error(
                    "Missing required field 'query'",
                    {"field": "query"}
                )
                return JSONResponse(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    content=error.to_api_response()
                )

            query_text = body.get("query", "")

            # Validate query length
            is_valid, error_msg = validate_query_length(
                query_text,
                max_length=settings.max_query_length
            )

            if not is_valid:
                error = ErrorRecord.validation_error(
                    error_msg,
                    {"query_length": len(query_text), "max_length": settings.max_query_length}
                )
                return JSONResponse(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    content=error.to_api_response()
                )

            # Reconstruct request with validated data
            request._body = await request.body()

        except Exception as e:
            logger.error(f"Validation middleware error: {e}")
            error = ErrorRecord.validation_error(
                "Invalid request format",
                {"error": str(e)}
            )
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=error.to_api_response()
            )

    response = await call_next(request)
    return response

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """
    Application startup tasks.

    Validates configuration and logs startup info.
    """
    logger.info("=" * 60)
    logger.info("Starting RAG Book Chatbot API")
    logger.info(f"Version: {__version__}")
    logger.info(f"Environment: {settings.environment}")
    logger.info("=" * 60)

    try:
        # Validate configuration
        settings.validate()
        logger.info("✓ Configuration validated")

        # Log key settings (without secrets)
        logger.info(f"Qdrant Collection: {settings.qdrant_collection_name}")
        logger.info(f"Similarity Threshold: {settings.similarity_threshold}")
        logger.info(f"Top K Results: {settings.top_k_results}")
        logger.info(f"Max Query Length: {settings.max_query_length}")

    except ValueError as e:
        logger.error(f"❌ Configuration validation failed: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown tasks.

    Cleanup resources and log shutdown info.
    """
    logger.info("Shutting down RAG Book Chatbot API")


@app.get("/health")
async def health_check():
    """
    Health check endpoint.

    Returns:
        dict: Application health status
    """
    return {
        "status": "healthy",
        "version": __version__,
        "environment": settings.environment,
    }


@app.get("/")
async def root():
    """
    Root endpoint with API information.

    Returns:
        dict: API metadata
    """
    return {
        "name": "RAG Book Chatbot API",
        "version": __version__,
        "docs": "/docs",
        "health": "/health",
    }


@app.post("/chat", response_model=Response, status_code=status.HTTP_200_OK)
async def chat(query: Query):
    """
    Chat endpoint for book questions.

    Processes user queries using RAG to provide grounded responses with citations.

    Args:
        query: User query object containing the question

    Returns:
        Response: Chatbot response with answer and citations

    Raises:
        HTTPException: If vector DB fails, embedding fails, or other errors occur
    """
    try:
        logger.info(f"Received chat request: {query.query[:100]}...")

        # Process query through RAG agent
        response = await rag_agent.query_chatbot(query)

        logger.info(f"Chat request completed successfully")
        return response

    except ConnectionError as e:
        # Vector database connection error
        logger.error(f"Vector database error: {e}")
        error = ErrorRecord.database_error(
            "Failed to connect to vector database. Please try again.",
            {"error": str(e)}
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=error.to_api_response()
        )

    except ValueError as e:
        # Embedding generation error or validation error
        logger.error(f"Embedding error: {e}")
        error = ErrorRecord(
            error_type="embedding_error",
            message="Failed to generate embeddings. Please try again.",
            details={"error": str(e)}
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error.to_api_response()
        )

    except Exception as e:
        # General error
        logger.error(f"Unexpected error in chat endpoint: {e}")
        import traceback
        logger.error(traceback.format_exc())

        error = ErrorRecord(
            error_type="internal_error",
            message="An unexpected error occurred. Please try again.",
            details={"error": str(e)}
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error.to_api_response()
        )
