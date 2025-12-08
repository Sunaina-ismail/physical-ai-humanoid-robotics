"""
Embedding Service

Generates vector embeddings using Gemini text-embedding-004 via OpenAI SDK.
"""

from typing import List

from openai import OpenAI

from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class EmbeddingService:
    """
    Service for generating text embeddings using Gemini text-embedding-004.

    Uses OpenAI SDK with custom base_url to access Gemini embeddings API.
    """

    def __init__(self):
        """Initialize embedding service with Gemini configuration."""
        self.client = OpenAI(
            api_key=settings.gemini_api_key,
            base_url=settings.gemini_base_url
        )
        self.model_name = "text-embedding-004"
        self.embedding_dim = 768

        logger.info(
            f"Initialized EmbeddingService with model={self.model_name}, "
            f"dim={self.embedding_dim}"
        )

    def generate_document_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for document/content text.

        Args:
            text: The document text to embed

        Returns:
            List[float]: 768-dimensional embedding vector

        Raises:
            Exception: If embedding generation fails
        """
        try:
            response = self.client.embeddings.create(
                input=text,
                model=self.model_name
            )

            embedding = response.data[0].embedding

            # Validate dimension
            if len(embedding) != self.embedding_dim:
                raise ValueError(
                    f"Expected {self.embedding_dim}-dim embedding, "
                    f"got {len(embedding)}-dim"
                )

            logger.debug(f"Generated document embedding for text ({len(text)} chars)")
            return embedding

        except Exception as e:
            logger.error(f"Failed to generate document embedding: {e}")
            raise

    def generate_query_embedding(self, query: str) -> List[float]:
        """
        Generate embedding for user query.

        Args:
            query: The user query text to embed

        Returns:
            List[float]: 768-dimensional embedding vector

        Raises:
            Exception: If embedding generation fails
        """
        try:
            response = self.client.embeddings.create(
                input=query,
                model=self.model_name
            )

            embedding = response.data[0].embedding

            # Validate dimension
            if len(embedding) != self.embedding_dim:
                raise ValueError(
                    f"Expected {self.embedding_dim}-dim embedding, "
                    f"got {len(embedding)}-dim"
                )

            logger.debug(f"Generated query embedding for query ({len(query)} chars)")
            return embedding

        except Exception as e:
            logger.error(f"Failed to generate query embedding: {e}")
            raise

    def generate_batch_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batch.

        Args:
            texts: List of text strings to embed

        Returns:
            List[List[float]]: List of 768-dimensional embedding vectors

        Raises:
            Exception: If batch embedding generation fails
        """
        try:
            response = self.client.embeddings.create(
                input=texts,
                model=self.model_name
            )

            embeddings = [item.embedding for item in response.data]

            # Validate all dimensions
            for i, embedding in enumerate(embeddings):
                if len(embedding) != self.embedding_dim:
                    raise ValueError(
                        f"Expected {self.embedding_dim}-dim embedding at index {i}, "
                        f"got {len(embedding)}-dim"
                    )

            logger.info(f"Generated {len(embeddings)} embeddings in batch")
            return embeddings

        except Exception as e:
            logger.error(f"Failed to generate batch embeddings: {e}")
            raise