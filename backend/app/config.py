from pydantic_settings import BaseSettings
from typing import List
import json


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # Cache
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # API Keys
    ANTHROPIC_API_KEY: str
    OPENAI_API_KEY: str
    GOOGLE_API_KEY: str
    XAI_API_KEY: str
    PERPLEXITY_API_KEY: str
    
    # Application
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Multi-Model Chat Client"
    
    # CORS
    CORS_ORIGINS: str = '["http://localhost:5173", "http://localhost:3000"]'
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from JSON string to list"""
        return json.loads(self.CORS_ORIGINS)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields not defined in the model


settings = Settings()