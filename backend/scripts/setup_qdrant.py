"""
Qdrant Collection Setup Script

Creates and configures the book_content collection with proper schema.

Usage:
    python scripts/setup_qdrant.py
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import settings
from app.services.vector_store import VectorStoreService
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


def setup_qdrant_collection() -> None:
    """
    Create and configure Qdrant collection for book content.

    Steps:
    1. Validate configuration
    2. Create collection with 768-dim vectors and COSINE distance
    3. Create payload indexes for chapter_number and section_title
    4. Verify collection is ready
    """
    logger.info("Starting Qdrant collection setup...")

    try:
        # Validate configuration
        logger.info("Validating configuration...")
        settings.validate()
        logger.info("Configuration valid")

        # Initialize vector store service
        logger.info("Connecting to Qdrant...")
        vector_store = VectorStoreService()

        # Create collection
        logger.info(
            f"Creating collection '{settings.qdrant_collection_name}' "
            f"(768-dim, COSINE distance)..."
        )
        vector_store.create_collection()
        logger.info("Collection created")

        # Create payload indexes for efficient filtering
        logger.info("Creating payload indexes...")

        # Index for chapter_number (integer field)
        vector_store.create_payload_index(
            field_name="chapter_number",
            field_type="integer"
        )
        logger.info("Created index for 'chapter_number'")

        # Index for section_title (keyword field)
        vector_store.create_payload_index(
            field_name="section_title",
            field_type="keyword"
        )
        logger.info("Created index for 'section_title'")

        # Verify collection
        logger.info("Verifying collection...")
        info = vector_store.get_collection_info()
        logger.info(f"Collection verified: {info}")

        logger.info("=" * 60)
        logger.info("Qdrant collection setup complete!")
        logger.info(f"   Collection: {info['name']}")
        logger.info(f"   Status: {info['status']}")
        logger.info(f"   Points: {info['points_count']}")
        logger.info("=" * 60)

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        logger.error("Please check your .env file and ensure all required variables are set.")
        sys.exit(1)

    except Exception as e:
        logger.error(f"Setup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    setup_qdrant_collection()