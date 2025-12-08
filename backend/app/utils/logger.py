"""
Structured Logging Configuration

Provides logging with secret masking to prevent credential leakage.
"""

import logging
import re
from typing import Optional

from app.config import settings


class SecretMaskingFormatter(logging.Formatter):
    """
    Custom formatter that masks sensitive data in log messages.

    Prevents API keys, tokens, and other secrets from appearing in logs.
    """

    # Patterns to detect and mask sensitive data
    SECRET_PATTERNS = [
        (re.compile(r'(api_key|apikey|API_KEY)(["\']?\s*[:=]\s*["\']?)([^\s&"\']+)'), r'\1\2***REDACTED***'),
        (re.compile(r'(token|TOKEN)(["\']?\s*[:=]\s*["\']?)([^\s&"\']+)'), r'\1\2***REDACTED***'),
        (re.compile(r'(password|PASSWORD|pwd)(["\']?\s*[:=]\s*["\']?)([^\s&"\']+)'), r'\1\2***REDACTED***'),
        (re.compile(r'(secret|SECRET)(["\']?\s*[:=]\s*["\']?)([^\s&"\']+)'), r'\1\2***REDACTED***'),
        (re.compile(r'Bearer\s+[A-Za-z0-9\-._~+/]+=*'), r'Bearer ***REDACTED***'),
    ]

    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record and mask any sensitive data.

        Args:
            record: The log record to format

        Returns:
            str: Formatted log message with secrets masked
        """
        message = super().format(record)

        # Apply all secret masking patterns
        for pattern, replacement in self.SECRET_PATTERNS:
            message = pattern.sub(replacement, message)

        return message


def setup_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Configure and return a logger with secret masking.

    Args:
        name: Logger name (defaults to root logger)

    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)

    # Avoid duplicate handlers if logger already configured
    if logger.handlers:
        return logger

    # Set log level from configuration
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
    logger.setLevel(log_level)

    # Console handler with secret masking
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    # Format: timestamp - logger_name - level - message
    formatter = SecretMaskingFormatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    # Prevent propagation to root logger to avoid duplicate logs
    logger.propagate = False

    return logger


# Default application logger
app_logger = setup_logger("rag_chatbot")
