"""
Vector Store Service

Qdrant vector database operations for semantic search.
"""

from typing import Dict, List, Optional

from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, PointStruct, VectorParams

from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class VectorStoreService:
    """
    Service for managing vector storage and retrieval using Qdrant.

    Handles collection creation, indexing, search, and CRUD operations.
    """

    def __init__(self):
        """Initialize Qdrant client connection."""
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )
        self.collection_name = settings.qdrant_collection_name
        self.vector_size = 768
        self.distance_metric = Distance.COSINE

        logger.info(
            f"Initialized VectorStoreService for collection={self.collection_name}"
        )

    def create_collection(self) -> None:
        """
        Create Qdrant collection with proper configuration.

        Creates collection with 768-dim vectors and COSINE distance.
        Idempotent - recreates if already exists.

        Raises:
            Exception: If collection creation fails
        """
        try:
            # Delete existing collection if present
            if self.collection_exists():
                logger.warning(
                    f"Collection '{self.collection_name}' already exists, recreating..."
                )
                self.client.delete_collection(collection_name=self.collection_name)

            # Create new collection
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=self.distance_metric
                ),
            )

            logger.info(
                f"Created collection '{self.collection_name}' "
                f"(size={self.vector_size}, distance={self.distance_metric})"
            )

        except Exception as e:
            logger.error(f"Failed to create collection: {e}")
            raise

    def create_payload_index(self, field_name: str, field_type: str = "keyword") -> None:
        """
        Create payload index for efficient filtering.

        Args:
            field_name: Field name to index (e.g., "chapter_number", "section_title")
            field_type: Field type ("keyword", "integer", "float", etc.)

        Raises:
            Exception: If index creation fails
        """
        try:
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name=field_name,
                field_schema=field_type,
            )

            logger.info(
                f"Created payload index for '{field_name}' (type={field_type})"
            )

        except Exception as e:
            logger.error(f"Failed to create payload index for '{field_name}': {e}")
            raise

    def collection_exists(self) -> bool:
        """
        Check if collection exists.

        Returns:
            bool: True if collection exists, False otherwise
        """
        try:
            collections = self.client.get_collections().collections
            return any(c.name == self.collection_name for c in collections)
        except Exception as e:
            logger.error(f"Failed to check collection existence: {e}")
            return False

    def upsert_points(
        self,
        points: List[PointStruct],
        wait: bool = True
    ) -> None:
        """
        Insert or update points in the collection.

        Args:
            points: List of PointStruct objects to upsert
            wait: Whether to wait for operation completion (default: True)

        Raises:
            Exception: If upsert operation fails
        """
        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points,
                wait=wait,
            )

            logger.info(f"Upserted {len(points)} points (wait={wait})")

        except Exception as e:
            logger.error(f"Failed to upsert points: {e}")
            raise

    def search(
        self,
        query_vector: List[float],
        limit: int = 5,
        score_threshold: Optional[float] = None,
        filter_conditions: Optional[Dict] = None,
    ) -> List[models.ScoredPoint]:
        """
        Search for similar vectors in the collection.

        Args:
            query_vector: Query embedding vector (768-dim)
            limit: Maximum number of results (default: 5)
            score_threshold: Minimum similarity score (default: None)
            filter_conditions: Optional Qdrant filter dict (default: None)

        Returns:
            List[ScoredPoint]: Search results with scores and payloads

        Raises:
            Exception: If search operation fails
        """
        try:
            response = self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                limit=limit,
                score_threshold=score_threshold,
                query_filter=filter_conditions,
            )

            # Extract points from the response object
            results = response.points if hasattr(response, 'points') else response

            # Ensure results is a list-like object
            if hasattr(results, '__len__'):
                result_count = len(results)
            elif hasattr(response, 'points_count'):
                result_count = response.points_count
            else:
                # Fallback: convert to list and count
                results = list(results) if not isinstance(results, list) else results
                result_count = len(results)

            logger.debug(
                f"Search returned {result_count} results "
                f"(limit={limit}, threshold={score_threshold})"
            )

            return results

        except Exception as e:
            logger.error(f"Failed to search vectors: {e}")
            raise

    def delete_by_filter(self, filter_conditions: Dict, wait: bool = True) -> int:
        """
        Delete points matching filter conditions.

        Args:
            filter_conditions: Qdrant filter dict
            wait: Whether to wait for operation completion (default: True)

        Returns:
            int: Number of points deleted (0 if unavailable)

        Raises:
            Exception: If delete operation fails
        """
        try:
            # Count points before deletion (for logging)
            count_before = self.count_points(filter_conditions)

            self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.FilterSelector(
                    filter=models.Filter(**filter_conditions)
                ),
                wait=wait,
            )

            logger.info(
                f"Deleted points matching filter (before_count={count_before}, wait={wait})"
            )

            return count_before

        except Exception as e:
            logger.error(f"Failed to delete points: {e}")
            raise

    def count_points(self, filter_conditions: Optional[Dict] = None) -> int:
        """
        Count points in collection matching filter.

        Args:
            filter_conditions: Optional Qdrant filter dict (default: None for all points)

        Returns:
            int: Number of points matching filter

        Raises:
            Exception: If count operation fails
        """
        try:
            if filter_conditions:
                result = self.client.count(
                    collection_name=self.collection_name,
                    count_filter=models.Filter(**filter_conditions),
                )
            else:
                result = self.client.count(collection_name=self.collection_name)

            count = result.count
            logger.debug(f"Point count: {count}")
            return count

        except Exception as e:
            logger.error(f"Failed to count points: {e}")
            raise

    def search_book_content(
        self,
        query_vector: List[float],
        top_k: Optional[int] = None,
        score_threshold: Optional[float] = None,
        chapter_filter: Optional[int] = None,
    ) -> List[Dict]:
        """
        Search for book content using query embedding.

        Args:
            query_vector: Query embedding vector (768-dim)
            top_k: Number of results (default: from settings)
            score_threshold: Minimum similarity (default: from settings)
            chapter_filter: Optional chapter number to filter by

        Returns:
            List[Dict]: Search results with text, metadata, and similarity scores
        """
        from app.config import settings

        # Use settings defaults if not provided
        if top_k is None:
            top_k = settings.top_k_results
        if score_threshold is None:
            score_threshold = settings.similarity_threshold

        # Build filter conditions
        filter_conditions = None
        if chapter_filter:
            filter_conditions = {
                "must": [{"key": "chapter_number", "match": {"value": chapter_filter}}]
            }

        try:
            # Perform vector search
            results = self.search(
                query_vector=query_vector,
                limit=top_k,
                score_threshold=score_threshold,
                filter_conditions=filter_conditions,
            )

            # Format results for RAG agent
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "text": result.payload.get("text", ""),
                    "chapter_number": result.payload.get("chapter_number"),
                    "chapter_title": result.payload.get("chapter_title", ""),
                    "section_title": result.payload.get("section_title", ""),
                    "similarity_score": result.score,
                    "metadata": {
                        k: v for k, v in result.payload.items()
                        if k not in ["text", "chapter_number", "chapter_title", "section_title"]
                    }
                })

            logger.info(
                f"Book search returned {len(formatted_results)} results "
                f"(threshold={score_threshold})"
            )

            return formatted_results

        except Exception as e:
            logger.error(f"Failed to search book content: {e}")
            raise

    def get_collection_info(self) -> dict:
        """
        Get collection metadata and statistics.

        Returns:
            dict: Collection information

        Raises:
            Exception: If retrieval fails
        """
        try:
            info = self.client.get_collection(collection_name=self.collection_name)
            return {
                "name": self.collection_name,
                "points_count": info.points_count,
                "status": info.status,
            }
        except Exception as e:
            logger.error(f"Failed to get collection info: {e}")
            raise