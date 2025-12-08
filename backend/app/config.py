"""
Configuration Management

Loads and validates environment variables using python-dotenv.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    """Application configuration settings loaded from environment variables."""

    # Gemini API Configuration
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_base_url: str = os.getenv(
        "GEMINI_BASE_URL",
        "https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    # Qdrant Vector Database Configuration
    qdrant_url: str = os.getenv("QDRANT_URL", "")
    qdrant_api_key: str = os.getenv("QDRANT_API_KEY", "")
    qdrant_collection_name: str = os.getenv("QDRANT_COLLECTION_NAME", "chatkit-bot")

    # Application Settings
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    max_query_length: int = int(os.getenv("MAX_QUERY_LENGTH", "2000"))
    similarity_threshold: float = float(os.getenv("SIMILARITY_THRESHOLD", "0.7"))
    top_k_results: int = int(os.getenv("TOP_K_RESULTS", "5"))

    # Optional Settings
    environment: str = os.getenv("ENVIRONMENT", "development")

    def validate(self) -> None:
        """
        Validate required configuration values.

        Raises:
            ValueError: If required configuration is missing
        """
        if not self.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable is required. "
                "Please set it in your .env file."
            )

        if not self.qdrant_url:
            raise ValueError(
                "QDRANT_URL environment variable is required. "
                "Please set it in your .env file."
            )

        # QDRANT_API_KEY is required for cloud instances, but not for localhost
        if not self.qdrant_api_key and "localhost" not in self.qdrant_url and "127.0.0.1" not in self.qdrant_url:
            raise ValueError(
                "QDRANT_API_KEY environment variable is required for cloud instances. "
                "Please set it in your .env file."
            )

        # Validate numeric ranges
        if self.max_query_length < 1 or self.max_query_length > 10000:
            raise ValueError(
                f"MAX_QUERY_LENGTH must be between 1 and 10000, got {self.max_query_length}"
            )

        if self.similarity_threshold < 0.0 or self.similarity_threshold > 1.0:
            raise ValueError(
                f"SIMILARITY_THRESHOLD must be between 0.0 and 1.0, got {self.similarity_threshold}"
            )

        if self.top_k_results < 1 or self.top_k_results > 20:
            raise ValueError(
                f"TOP_K_RESULTS must be between 1 and 20, got {self.top_k_results}"
            )


# Global settings instance
settings = Settings()