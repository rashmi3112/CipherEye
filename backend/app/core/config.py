from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    """
    Centralized configuration management for the application.
    Loads settings from environment variables or a .env file.
    """
    # API Keys
    gemini_api_key: str
    
    # Environment config
    environment: str = "development"
    log_level: str = "INFO"
    
    # MCP Servers (Optional)
    mcp_search_url: Optional[str] = None
    mcp_ocr_url: Optional[str] = None
    
    # PII Configuration
    enable_pii_detection: bool = True
    
    # Mock LLM (Optional fallback)
    mock_llm: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

# Global settings instance
settings = Settings()
