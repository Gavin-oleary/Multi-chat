"""
Utility helper functions used throughout the application.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
import re


def truncate_string(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate a string to a maximum length, adding a suffix if truncated.
    
    Args:
        text: The text to truncate
        max_length: Maximum length of the result
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a string to be safe for use as a filename.
    
    Args:
        filename: The filename to sanitize
        
    Returns:
        Sanitized filename
    """
    # Remove any character that isn't alphanumeric, dash, underscore, or dot
    sanitized = re.sub(r'[^\w\s\-\.]', '', filename)
    # Replace spaces with underscores
    sanitized = sanitized.replace(' ', '_')
    # Remove consecutive underscores or dashes
    sanitized = re.sub(r'[-_]+', '_', sanitized)
    return sanitized


def format_timestamp(dt: datetime, format_string: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format a datetime object as a string.
    
    Args:
        dt: The datetime to format
        format_string: The format string to use
        
    Returns:
        Formatted datetime string
    """
    return dt.strftime(format_string)


def calculate_token_estimate(text: str) -> int:
    """
    Rough estimate of token count for text.
    This is a simplified version - actual tokenization varies by model.
    
    Args:
        text: The text to estimate tokens for
        
    Returns:
        Estimated token count
    """
    # Rough estimate: ~4 characters per token on average
    return len(text) // 4


def extract_code_blocks(text: str) -> List[Dict[str, str]]:
    """
    Extract code blocks from markdown-formatted text.
    
    Args:
        text: Text containing markdown code blocks
        
    Returns:
        List of dicts with 'language' and 'code' keys
    """
    pattern = r'```(\w+)?\n(.*?)```'
    matches = re.finditer(pattern, text, re.DOTALL)
    
    code_blocks = []
    for match in matches:
        language = match.group(1) or "plaintext"
        code = match.group(2).strip()
        code_blocks.append({
            "language": language,
            "code": code
        })
    
    return code_blocks


def merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge two dictionaries, with dict2 values taking precedence.
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary
        
    Returns:
        Merged dictionary
    """
    result = dict1.copy()
    result.update(dict2)
    return result


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Split a list into chunks of specified size.
    
    Args:
        lst: List to chunk
        chunk_size: Size of each chunk
        
    Returns:
        List of chunks
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def is_valid_email(email: str) -> bool:
    """
    Simple email validation.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if email appears valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def safe_get(dictionary: Dict, *keys: str, default: Any = None) -> Any:
    """
    Safely get a nested value from a dictionary.
    
    Args:
        dictionary: The dictionary to get value from
        *keys: Sequence of keys to traverse
        default: Default value if key path doesn't exist
        
    Returns:
        The value at the key path, or default if not found
    """
    value = dictionary
    for key in keys:
        if isinstance(value, dict):
            value = value.get(key)
            if value is None:
                return default
        else:
            return default
    return value


def format_file_size(size_bytes: int) -> str:
    """
    Format a file size in bytes to a human-readable string.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"