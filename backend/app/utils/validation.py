"""
Input validation and sanitization utilities.
"""

import re
from typing import Any, Optional
import bleach
from app.constants import MODEL_TOKEN_LIMITS


def sanitize_string(text: str, max_length: int = 1000) -> str:
    """Sanitize and truncate string"""
    cleaned = bleach.clean(text, strip=True)
    return cleaned[:max_length]


def sanitize_html(html: str, allowed_tags: Optional[list] = None) -> str:
    """
    Sanitize HTML content to prevent XSS attacks.
    
    Args:
        html: HTML string to sanitize
        allowed_tags: List of allowed HTML tags
        
    Returns:
        Sanitized HTML string
    """
    if allowed_tags is None:
        allowed_tags = ['b', 'i', 'u', 'em', 'strong', 'p', 'br']
    
    return bleach.clean(
        html,
        tags=allowed_tags,
        attributes={},
        strip=True
    )


def validate_sql_identifier(identifier: str) -> bool:
    """
    Validate that a string is a safe SQL identifier (table/column name).
    
    Args:
        identifier: The identifier to validate
        
    Returns:
        True if valid, False otherwise
    """
    # SQL identifiers should only contain alphanumeric characters and underscores
    # and should not start with a number
    pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
    return bool(re.match(pattern, identifier))


def escape_sql_like(value: str) -> str:
    """
    Escape special characters in SQL LIKE patterns.
    
    Args:
        value: The value to escape
        
    Returns:
        Escaped string safe for use in LIKE queries
    """
    # Escape special LIKE characters
    value = value.replace('\\', '\\\\')
    value = value.replace('%', '\\%')
    value = value.replace('_', '\\_')
    value = value.replace('[', '\\[')
    return value


def validate_integer_id(value: Any) -> int:
    """
    Validate and convert a value to a positive integer ID.
    
    Args:
        value: The value to validate
        
    Returns:
        Valid integer ID
        
    Raises:
        ValueError: If value is not a valid positive integer
    """
    try:
        int_value = int(value)
        if int_value <= 0:
            raise ValueError("ID must be a positive integer")
        return int_value
    except (TypeError, ValueError) as e:
        raise ValueError(f"Invalid ID: {value}") from e


def estimate_token_count(text: str, chars_per_token: float = 4.0) -> int:
    """
    Estimate the number of tokens in a text string.
    
    This is a rough approximation. For more accurate counts,
    use the specific tokenizer for each model.
    
    Args:
        text: The text to count tokens for
        chars_per_token: Average characters per token (default 4.0)
        
    Returns:
        Estimated token count
    """
    return int(len(text) / chars_per_token)


def validate_prompt_length(prompt: str, min_len: int = 1, max_len: int = 10000) -> bool:
    """Validate prompt length"""
    return min_len <= len(prompt.strip()) <= max_len


def get_model_token_limit(model: str) -> int:
    """
    Get the token limit for a specific model.
    
    Args:
        model: The model name
        
    Returns:
        Token limit for the model
    """
    return MODEL_TOKEN_LIMITS.get(model.lower(), 4096)  # Default to 4096
