"""
Qdrant Vector Verification Script

Checks if the rag-textbook collection exists and contains vectors.

Usage:
    python scripts/check_qdrant_vectors.py
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import settings
from app.services.vector_store import VectorStoreService
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


def check_qdrant_vectors() -> None:
    """
    Verify Qdrant collection exists and contains vectors.

    Reports:
    - Collection existence
    - Vector count
    - Sample point data (if available)
    """
    logger.info("=" * 60)
    logger.info("Checking Qdrant Vector Store Status")
    logger.info(f"Collection: {settings.qdrant_collection_name}")
    logger.info("=" * 60)

    try:
        # Validate configuration
        logger.info("Validating configuration...")
        settings.validate()
        logger.info("✓ Configuration valid")

        # Initialize vector store
        logger.info("Connecting to Qdrant...")
        vector_store = VectorStoreService()

        # Check if collection exists
        exists = vector_store.collection_exists()

        if not exists:
            logger.warning("=" * 60)
            logger.warning(f"❌ Collection '{settings.qdrant_collection_name}' does NOT exist")
            logger.warning("=" * 60)
            logger.warning("")
            logger.warning("Next steps:")
            logger.warning("1. Run setup script to create collection:")
            logger.warning("   python scripts/setup_qdrant.py")
            logger.warning("")
            logger.warning("2. Ingest book content (after implementing ingestion):")
            logger.warning("   python scripts/ingest.py --source ../frontend/docs")
            logger.warning("")
            sys.exit(0)

        logger.info(f"✓ Collection '{settings.qdrant_collection_name}' exists")

        # Get collection info
        logger.info("Retrieving collection information...")
        info = vector_store.get_collection_info()

        # Display results
        logger.info("=" * 60)
        logger.info("📊 Collection Status")
        logger.info("=" * 60)
        logger.info(f"Name:          {info['name']}")
        logger.info(f"Status:        {info['status']}")
        logger.info(f"Points:        {info['points_count']}")
        logger.info("=" * 60)

        # Check if vectors are present
        if info['points_count'] == 0:
            logger.warning("")
            logger.warning("⚠️  Collection is EMPTY - no vectors stored yet")
            logger.warning("")
            logger.warning("Next steps:")
            logger.warning("1. Implement and run ingestion script:")
            logger.warning("   python scripts/ingest.py --source ../frontend/docs")
            logger.warning("")
            logger.warning("The collection is ready but needs content to be ingested.")
            logger.warning("")
        else:
            logger.info("")
            logger.info(f"✅ Collection contains {info['points_count']} vectors")
            logger.info("   Vector store is ready for RAG queries!")
            logger.info("")

            # Try to get a sample point
            try:
                logger.info("Fetching sample point...")
                results = vector_store.client.scroll(
                    collection_name=settings.qdrant_collection_name,
                    limit=1,
                    with_payload=True,
                    with_vectors=False,
                )

                if results[0]:
                    sample = results[0][0]
                    logger.info("Sample point payload:")
                    logger.info(f"  ID: {sample.id}")
                    logger.info(f"  Payload keys: {list(sample.payload.keys())}")
                    if 'chapter_number' in sample.payload:
                        logger.info(f"  Chapter: {sample.payload.get('chapter_number')}")
                    if 'section_title' in sample.payload:
                        logger.info(f"  Section: {sample.payload.get('section_title')}")
                    if 'text' in sample.payload:
                        text_preview = sample.payload['text'][:100]
                        logger.info(f"  Text preview: {text_preview}...")

            except Exception as e:
                logger.warning(f"Could not fetch sample point: {e}")

        logger.info("=" * 60)

    except ValueError as e:
        logger.error(f"❌ Configuration error: {e}")
        logger.error("Please check your .env file and ensure all required variables are set.")
        sys.exit(1)

    except Exception as e:
        logger.error(f"❌ Verification failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    check_qdrant_vectors()
