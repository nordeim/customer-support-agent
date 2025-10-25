# backend/app/core/config.py
from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Application settings
    app_name: str = "Customer Support Agent"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Database settings
    database_url: str = "sqlite:///./customer_support.db"
    
    # Agent Framework settings
    agent_framework_endpoint: Optional[str] = None
    agent_framework_api_key: Optional[str] = None
    
    # Vector store settings
    chroma_persist_directory: str = "./chroma_db"
    embedding_model_name: str = "google/embeddinggemma-300m"
    
    # Security settings
    secret_key: str = "change-me-in-production"
    session_timeout: int = 3600  # 1 hour
    
    # Logging settings
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"

settings = Settings()
