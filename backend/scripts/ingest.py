"""
Book Content Ingestion Script

Reads markdown files from frontend/docs, chunks content, generates embeddings,
and uploads to Qdrant vector database.

Usage:
    python scripts/ingest.py --source ../frontend/docs
    python scripts/ingest.py --source ../frontend/docs --chapter 5
    python scripts/ingest.py --source ../frontend/docs --reingest
"""

import argparse
import sys
import time
from pathlib import Path
from typing import List, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from qdrant_client.http.models import PointStruct

from app.config import settings
from app.models import BookChapter, ContentSegment, IngestionLog
from app.services.chunking import chunking_service
from app.services.embeddings import EmbeddingService
from app.services.vector_store import VectorStoreService
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Ingest book content into Qdrant vector database"
    )

    parser.add_argument(
        "--source",
        type=str,
        required=True,
        help="Path to directory containing markdown chapter files"
    )

    parser.add_argument(
        "--chapter",
        type=int,
        default=None,
        help="Specific chapter number to ingest (optional, default: all)"
    )

    parser.add_argument(
        "--reingest",
        action="store_true",
        help="Re-ingest and replace existing vectors for chapter(s)"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate ingestion without uploading to Qdrant"
    )

    return parser.parse_args()


def discover_chapters(source_dir: Path) -> List[Path]:
    """
    Discover all markdown chapter files in source directory.

    Args:
        source_dir: Directory containing chapter files

    Returns:
        List[Path]: Sorted list of markdown file paths
    """
    if not source_dir.exists():
        raise ValueError(f"Source directory does not exist: {source_dir}")

    if not source_dir.is_dir():
        raise ValueError(f"Source path is not a directory: {source_dir}")

    # Find all .md and .mdx files
    md_files = sorted(source_dir.glob("**/*.md"))
    mdx_files = sorted(source_dir.glob("**/*.mdx"))
    all_files = sorted(md_files + mdx_files)

    if not all_files:
        logger.warning(f"No markdown files found in {source_dir}")

    logger.info(f"Discovered {len(all_files)} markdown files (.md: {len(md_files)}, .mdx: {len(mdx_files)})")
    return all_files


def extract_chapter_number(file_path: Path) -> Optional[int]:
    """
    Extract chapter number from filename.

    Patterns supported:
    - chapter-1.md -> 1
    - 01-introduction.md -> 1
    - week-1/lesson.md -> 1

    Args:
        file_path: Path to markdown file

    Returns:
        Optional[int]: Chapter number or None if not found
    """
    import re

    # Try to find number in filename
    filename = file_path.stem
    match = re.search(r'(\d+)', filename)

    if match:
        return int(match.group(1))

    # Try parent directory name
    parent = file_path.parent.name
    match = re.search(r'(\d+)', parent)

    if match:
        return int(match.group(1))

    return None


def load_chapter(file_path: Path, chapter_number: int) -> BookChapter:
    """
    Load chapter content from markdown file.

    Args:
        file_path: Path to markdown file
        chapter_number: Chapter number

    Returns:
        BookChapter: Loaded chapter object

    Raises:
        ValueError: If file is empty or invalid
    """
    if not file_path.exists():
        raise ValueError(f"Chapter file does not exist: {file_path}")

    content = file_path.read_text(encoding="utf-8")

    if not content.strip():
        raise ValueError(f"Chapter file is empty: {file_path}")

    # Extract title from first heading or filename
    title = file_path.stem.replace("-", " ").replace("_", " ").title()

    import re
    heading_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if heading_match:
        title = heading_match.group(1).strip()

    word_count = len(content.split())

    chapter = BookChapter(
        chapter_number=chapter_number,
        title=title,
        file_path=file_path.absolute(),
        raw_content=content,
        word_count=word_count,
        metadata={
            "filename": file_path.name,
            "relative_path": str(file_path.relative_to(file_path.parent.parent))
        }
    )

    logger.info(f"Loaded chapter {chapter_number}: {title} ({word_count} words)")
    return chapter


def ingest_chapter(
    chapter: BookChapter,
    embedding_service: EmbeddingService,
    vector_store: VectorStoreService,
    reingest: bool = False,
    dry_run: bool = False
) -> IngestionLog:
    """
    Ingest a single chapter into Qdrant.

    Args:
        chapter: BookChapter object to ingest
        embedding_service: Embedding service instance
        vector_store: Vector store service instance
        reingest: Whether to delete existing vectors first
        dry_run: Simulate without uploading

    Returns:
        IngestionLog: Log entry for this operation
    """
    start_time = time.time()
    vectors_deleted = 0

    try:
        logger.info(f"Processing chapter {chapter.chapter_number}: {chapter.title}")

        # Delete existing vectors if reingest
        if reingest and not dry_run:
            logger.info(f"Deleting existing vectors for chapter {chapter.chapter_number}")
            vectors_deleted = vector_store.delete_by_filter({
                "must": [{"key": "chapter_number", "match": {"value": chapter.chapter_number}}]
            })
            logger.info(f"Deleted {vectors_deleted} existing vectors")

        # Chunk the chapter
        logger.info("Chunking chapter content...")
        segments = chunking_service.chunk_chapter(
            content=chapter.raw_content,
            chapter_number=chapter.chapter_number,
            chapter_metadata={
                "chapter_title": chapter.title,
                **chapter.metadata
            }
        )

        if not segments:
            raise ValueError("Chunking produced no segments")

        logger.info(f"Created {len(segments)} segments")

        # Generate embeddings in batch
        logger.info("Generating embeddings...")
        texts = [seg.text for seg in segments]
        embeddings = embedding_service.generate_batch_embeddings(texts)

        # Attach embeddings to segments
        for segment, embedding in zip(segments, embeddings):
            segment.embedding = embedding

        # Convert to Qdrant points
        logger.info("Preparing Qdrant points...")
        points = []
        for i, segment in enumerate(segments):
            # Generate unique integer ID to comply with Qdrant requirements
            # Using a combination of chapter number and segment index
            point_id = (chapter.chapter_number * 10000) + i
            point = PointStruct(
                id=point_id,
                vector=segment.embedding,
                payload={
                    "text": segment.text,
                    "chapter_number": segment.chapter_number,
                    "section_title": segment.section_title,
                    "order": segment.order,
                    "word_count": segment.word_count,
                    **segment.metadata
                }
            )
            points.append(point)

        # Upload to Qdrant
        if not dry_run:
            logger.info(f"Uploading {len(points)} points to Qdrant...")
            vector_store.upsert_points(points, wait=True)
            logger.info("✓ Upload complete")
        else:
            logger.info(f"[DRY RUN] Would upload {len(points)} points")

        # Create success log
        duration = time.time() - start_time
        log_entry = IngestionLog(
            operation="re_ingest" if reingest else "initial_ingest",
            chapter_number=chapter.chapter_number,
            chapter_title=chapter.title,
            segments_processed=len(segments),
            vectors_deleted=vectors_deleted,
            status="success",
            duration_seconds=duration
        )

        logger.info(f"✓ Chapter {chapter.chapter_number} ingested successfully ({duration:.2f}s)")
        return log_entry

    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"Failed to ingest chapter {chapter.chapter_number}: {e}")

        log_entry = IngestionLog(
            operation="re_ingest" if reingest else "initial_ingest",
            chapter_number=chapter.chapter_number,
            chapter_title=chapter.title,
            segments_processed=0,
            vectors_deleted=vectors_deleted,
            status="failure",
            error_message=str(e),
            duration_seconds=duration
        )

        return log_entry


def main():
    """Main ingestion workflow."""
    args = parse_arguments()

    logger.info("=" * 60)
    logger.info("Book Content Ingestion")
    logger.info("=" * 60)
    logger.info(f"Source: {args.source}")
    logger.info(f"Chapter filter: {args.chapter or 'all'}")
    logger.info(f"Reingest mode: {args.reingest}")
    logger.info(f"Dry run: {args.dry_run}")
    logger.info("=" * 60)

    try:
        # Validate configuration
        settings.validate()

        # Initialize services
        embedding_service = EmbeddingService()
        vector_store = VectorStoreService()

        # Verify collection exists
        if not vector_store.collection_exists():
            logger.error("Qdrant collection does not exist. Run setup_qdrant.py first.")
            sys.exit(1)

        # Discover chapter files
        source_dir = Path(args.source).resolve()
        chapter_files = discover_chapters(source_dir)

        if not chapter_files:
            logger.error("No markdown files found to ingest")
            sys.exit(1)

        # Process each chapter
        logs = []
        for file_path in chapter_files:
            # Extract chapter number
            chapter_number = extract_chapter_number(file_path)
            if chapter_number is None:
                logger.warning(f"Skipping file (no chapter number): {file_path.name}")
                continue

            # Filter by chapter if specified
            if args.chapter and chapter_number != args.chapter:
                continue

            try:
                # Load chapter
                chapter = load_chapter(file_path, chapter_number)

                # Ingest chapter
                log_entry = ingest_chapter(
                    chapter=chapter,
                    embedding_service=embedding_service,
                    vector_store=vector_store,
                    reingest=args.reingest,
                    dry_run=args.dry_run
                )

                logs.append(log_entry)

            except Exception as e:
                logger.error(f"Error processing {file_path.name}: {e}")
                continue

        # Summary
        logger.info("=" * 60)
        logger.info("Ingestion Summary")
        logger.info("=" * 60)

        success_count = sum(1 for log in logs if log.status == "success")
        failure_count = sum(1 for log in logs if log.status == "failure")
        total_segments = sum(log.segments_processed for log in logs)
        total_deleted = sum(log.vectors_deleted for log in logs)

        logger.info(f"Chapters processed: {len(logs)}")
        logger.info(f"  Success: {success_count}")
        logger.info(f"  Failure: {failure_count}")
        logger.info(f"Segments created: {total_segments}")
        logger.info(f"Vectors deleted: {total_deleted}")
        logger.info("=" * 60)

        if failure_count > 0:
            logger.warning("Some chapters failed to ingest. Check logs above.")
            sys.exit(1)
        else:
            logger.info("✅ All chapters ingested successfully!")

    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()