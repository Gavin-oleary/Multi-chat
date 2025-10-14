"""
Structured logging configuration
"""

import logging
import logging.config
import json
from datetime import datetime
from typing import Any, Dict
import sys


class StructuredFormatter(logging.Formatter):
    """Custom formatter that outputs structured JSON logs"""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields if present
        if hasattr(record, "extra_fields"):
            log_data.update(record.extra_fields)
        
        return json.dumps(log_data)


def setup_logging(level: str = "INFO", json_logs: bool = True):
    """
    Configure structured logging for the application.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_logs: Whether to output JSON formatted logs
    """
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "structured": {
                "()": StructuredFormatter
            },
            "simple": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": level,
                "formatter": "structured" if json_logs else "simple",
                "stream": sys.stdout
            }
        },
        "root": {
            "level": level,
            "handlers": ["console"]
        },
        "loggers": {
            # Silence noisy libraries
            "httpx": {"level": "WARNING"},
            "anthropic": {"level": "WARNING"},
            "openai": {"level": "WARNING"},
            "google": {"level": "WARNING"},
            # App loggers
            "app": {"level": level},
            "uvicorn.access": {"level": "INFO"}
        }
    }
    
    logging.config.dictConfig(config)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with structured logging support.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


class LoggerAdapter(logging.LoggerAdapter):
    """
    Logger adapter that adds extra fields to all log messages.
    Useful for adding request IDs, user IDs, etc.
    """
    
    def process(self, msg: str, kwargs: Dict[str, Any]) -> tuple:
        """Add extra fields to log record"""
        extra = kwargs.get("extra", {})
        extra["extra_fields"] = self.extra
        kwargs["extra"] = extra
        return msg, kwargs


def create_logger(name: str, **extra_fields) -> LoggerAdapter:
    """
    Create a logger with extra fields that will be included in all messages.
    
    Args:
        name: Logger name
        **extra_fields: Fields to include in all log messages
        
    Returns:
        LoggerAdapter instance
    """
    logger = get_logger(name)
    return LoggerAdapter(logger, extra_fields)
