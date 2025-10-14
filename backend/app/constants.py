"""
Application-wide constants
"""

# Model identifiers
CLAUDE_MODEL = "claude-sonnet-4-5-20250929"
OPENAI_MODEL = "gpt-4o"
GEMINI_MODEL = "gemini-2.5-flash"
GROK_MODEL = "grok-4-fast-reasoning"
PERPLEXITY_MODEL = "sonar"

# Model display names
MODEL_DISPLAY_NAMES = {
    "claude": "Claude",
    "chatgpt": "ChatGPT",
    "gemini": "Gemini",
    "grok": "Grok",
    "perplexity": "Perplexity"
}

# Model token limits
MODEL_TOKEN_LIMITS = {
    "claude": 100000,      # Claude 3 models
    "chatgpt": 4096,       # GPT-3.5/4
    "gemini": 32768,       # Gemini Pro
    "grok": 8192,          # Grok (estimated)
    "perplexity": 4096,    # Perplexity (estimated)
}

# API endpoints
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
GROK_API_URL = "https://api.x.ai/v1/chat/completions"
PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"

# Error messages
ERROR_MESSAGES = {
    "invalid_request": "Invalid request format",
    "model_unavailable": "{model} is temporarily unavailable",
    "rate_limit": "Rate limit exceeded. Please try again later",
    "api_error": "API error: {error}",
    "network_error": "Network error. Please check your connection",
    "timeout": "Request timed out. Please try again",
    "invalid_model": "Invalid model: {model}",
    "empty_prompt": "Prompt cannot be empty",
    "prompt_too_long": "Prompt too long: approximately {tokens} tokens (maximum {max_tokens} tokens allowed)",
    "conversation_not_found": "Conversation not found",
    "database_error": "Database error occurred",
    "circuit_breaker_open": "{provider} is temporarily unavailable due to repeated failures"
}

# Response timeouts (seconds)
DEFAULT_TIMEOUT = 30
STREAMING_TIMEOUT = 120

# Cache settings
CACHE_TTL_HOURS = 24
CACHE_KEY_PREFIX = "chat_response"

# Database settings
DB_POOL_SIZE = 20
DB_MAX_OVERFLOW = 10
DB_POOL_RECYCLE = 3600  # 1 hour

# Conversation settings
MAX_CONVERSATION_HISTORY = 20  # Maximum messages to load for context
MAX_PROMPT_LENGTH = 10000  # Maximum characters in a prompt
MIN_PROMPT_LENGTH = 1      # Minimum characters in a prompt
