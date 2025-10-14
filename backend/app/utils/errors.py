"""
Standardized error handling utilities
"""

from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from app.constants import ERROR_MESSAGES
import logging

logger = logging.getLogger(__name__)


class APIError(HTTPException):
    """Standardized API error with consistent format"""
    
    def __init__(
        self,
        error_key: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        **kwargs
    ):
        """
        Create a standardized API error.
        
        Args:
            error_key: Key from ERROR_MESSAGES constant
            status_code: HTTP status code
            **kwargs: Parameters to format the error message
        """
        # Get error message template
        message_template = ERROR_MESSAGES.get(
            error_key, 
            ERROR_MESSAGES["api_error"]
        )
        
        # Format message with provided parameters
        try:
            message = message_template.format(**kwargs)
        except KeyError:
            # Fallback if formatting fails
            message = message_template
            logger.error(f"Failed to format error message: {error_key} with {kwargs}")
        
        # Create detail object
        detail = {
            "error": error_key,
            "message": message,
            "details": kwargs if kwargs else None
        }
        
        super().__init__(status_code=status_code, detail=detail)


def create_error_response(
    error_key: str,
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    **kwargs
) -> Dict[str, Any]:
    """
    Create a standardized error response dictionary.
    
    Args:
        error_key: Key from ERROR_MESSAGES constant
        status_code: HTTP status code (for logging)
        **kwargs: Parameters to format the error message
        
    Returns:
        Dictionary with error details
    """
    message_template = ERROR_MESSAGES.get(
        error_key,
        ERROR_MESSAGES["api_error"]
    )
    
    try:
        message = message_template.format(**kwargs)
    except KeyError:
        message = message_template
        logger.error(f"Failed to format error message: {error_key} with {kwargs}")
    
    return {
        "error": error_key,
        "message": message,
        "status_code": status_code,
        "details": kwargs if kwargs else None
    }


# Common error responses
def invalid_request_error(**kwargs):
    """Invalid request format error"""
    return APIError("invalid_request", status.HTTP_400_BAD_REQUEST, **kwargs)


def model_unavailable_error(model: str):
    """Model temporarily unavailable error"""
    return APIError("model_unavailable", status.HTTP_503_SERVICE_UNAVAILABLE, model=model)


def rate_limit_error():
    """Rate limit exceeded error"""
    return APIError("rate_limit", status.HTTP_429_TOO_MANY_REQUESTS)


def database_error():
    """Database error"""
    return APIError("database_error", status.HTTP_500_INTERNAL_SERVER_ERROR)


def conversation_not_found_error():
    """Conversation not found error"""
    return APIError("conversation_not_found", status.HTTP_404_NOT_FOUND)


def empty_prompt_error():
    """Empty prompt error"""
    return APIError("empty_prompt", status.HTTP_400_BAD_REQUEST)


def prompt_too_long_error(tokens: int, max_tokens: int):
    """Prompt too long error"""
    return APIError(
        "prompt_too_long", 
        status.HTTP_400_BAD_REQUEST,
        tokens=tokens,
        max_tokens=max_tokens
    )
