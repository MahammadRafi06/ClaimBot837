"""Configuration management for the application."""

import os
from dataclasses import dataclass
from typing import Dict, Set

@dataclass
class Config:
    """Application configuration."""
    
    # Flask settings
    UPLOAD_FOLDER: str = './data'
    ALLOWED_EXTENSIONS: Set[str] = {'pdf'}
    HOST: str = '0.0.0.0'
    PORT: int = 5000
    DEBUG: bool = True
    
    # LLM settings
    OPENAI_MODEL: str = "gpt-4"
    MAX_RETRIES: int = 3
    TEMPERATURE: float = 0.1
    
    # Agent settings
    MAX_CODERS: int = 1
    MAX_ITERATIONS: int = 3
    
    # Database settings
    DB_HOST: str = os.getenv('DB_HOST', 'localhost')
    DB_PORT: int = int(os.getenv('DB_PORT', '3306'))
    DB_NAME: str = os.getenv('DB_NAME', 'claims')
    DB_USER: str = os.getenv('DB_USER', 'root')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD', '')
    
    # Logging
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    @classmethod
    def from_env(cls) -> 'Config':
        """Create config from environment variables."""
        return cls(
            UPLOAD_FOLDER=os.getenv('UPLOAD_FOLDER', cls.UPLOAD_FOLDER),
            HOST=os.getenv('HOST', cls.HOST),
            PORT=int(os.getenv('PORT', cls.PORT)),
            DEBUG=bool(os.getenv('DEBUG', cls.DEBUG)),
            MAX_CODERS=int(os.getenv('MAX_CODERS', cls.MAX_CODERS)),
            MAX_ITERATIONS=int(os.getenv('MAX_ITERATIONS', cls.MAX_ITERATIONS))
        ) 