"""
Input Validation Utilities

Validation functions for query inputs and data integrity.
"""

from typing import Optional, Tuple


def validate_query_length(query: str, max_length: int = 2000) -> Tuple[bool, Optional[str]]:
    """
    Validate query length constraints.

    Args:
        query: The user query string
        max_length: Maximum allowed length (default: 2000)

    Returns:
        Tuple[bool, Optional[str]]: (is_valid, error_message)
            - (True, None) if valid
            - (False, error_message) if invalid
    """
    if not query:
        return False, "Query cannot be empty"

    if not query.strip():
        return False, "Query cannot be whitespace-only"

    if len(query) > max_length:
        return False, f"Query exceeds maximum length of {max_length} characters (got {len(query)})"

    return True, None


def validate_selected_text(selected_text: Optional[str], max_length: int = 5000) -> Tuple[bool, Optional[str]]:
    """
    Validate selected text constraints.

    Args:
        selected_text: Optional text selected from the book
        max_length: Maximum allowed length (default: 5000)

    Returns:
        Tuple[bool, Optional[str]]: (is_valid, error_message)
            - (True, None) if valid or None
            - (False, error_message) if invalid
    """
    # None is valid (optional field)
    if selected_text is None:
        return True, None

    if not selected_text.strip():
        return False, "Selected text cannot be whitespace-only (omit field instead)"

    if len(selected_text) > max_length:
        return False, f"Selected text exceeds maximum length of {max_length} characters (got {len(selected_text)})"

    return True, None


def validate_not_empty(value: str, field_name: str = "Field") -> Tuple[bool, Optional[str]]:
    """
    Validate that a string field is not empty or whitespace-only.

    Args:
        value: The string value to validate
        field_name: Name of the field for error messages

    Returns:
        Tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    if not value:
        return False, f"{field_name} cannot be empty"

    if not value.strip():
        return False, f"{field_name} cannot be whitespace-only"

    return True, None


def validate_chapter_number(chapter_number: int, min_chapter: int = 1) -> Tuple[bool, Optional[str]]:
    """
    Validate chapter number is positive integer.

    Args:
        chapter_number: The chapter number to validate
        min_chapter: Minimum valid chapter number (default: 1)

    Returns:
        Tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    if not isinstance(chapter_number, int):
        return False, f"Chapter number must be an integer, got {type(chapter_number).__name__}"

    if chapter_number < min_chapter:
        return False, f"Chapter number must be at least {min_chapter}, got {chapter_number}"

    return True, None


def validate_similarity_threshold(threshold: float) -> Tuple[bool, Optional[str]]:
    """
    Validate similarity threshold is in valid range [0.0, 1.0].

    Args:
        threshold: The similarity threshold value

    Returns:
        Tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    if not isinstance(threshold, (int, float)):
        return False, f"Similarity threshold must be a number, got {type(threshold).__name__}"

    if threshold < 0.0 or threshold > 1.0:
        return False, f"Similarity threshold must be between 0.0 and 1.0, got {threshold}"

    return True, None
