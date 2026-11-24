from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "GenStudio AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Database
    # Default to local SQLite for instant zero-dependency running; supports PostgreSQL via DATABASE_URL
    DATABASE_URL: str = Field(
        default=f"sqlite:///{BASE_DIR / 'genstudio.db'}",
        description="Database connection string (PostgreSQL or SQLite)"
    )
    
    # Redis / Celery
    REDIS_URL: Optional[str] = "redis://localhost:6379/0"
    USE_REDIS_QUEUE: bool = False
    
    # Security
    JWT_SECRET: str = "genstudio_super_secret_jwt_key_2026_academic_eval_secure_change_in_prod"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 24 hours
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]
    
    # Storage
    MEDIA_STORAGE_DIR: str = str(BASE_DIR / "storage" / "media")
    MAX_UPLOAD_SIZE_BYTES: int = 25 * 1024 * 1024  # 25 MB
    ALLOWED_IMAGE_TYPES: List[str] = ["image/jpeg", "image/png", "image/webp"]
    ALLOWED_VIDEO_TYPES: List[str] = ["video/mp4", "video/webm"]
    
    # AI Providers
    # Provider Operating Mode: "live" (real inference only), "test" (deterministic fixtures for automated test suites), or "offline-preview" (labeled synthetic demo mode)
    PROVIDER_MODE: str = Field(
        default="live",
        description="Provider operating mode: 'live', 'test', or 'offline-preview'"
    )
    HF_API_TOKEN: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    COMFYUI_BASE_URL: Optional[str] = "http://127.0.0.1:8188"
    
    # Public Base URL
    PUBLIC_APP_URL: str = "http://localhost:3000"
    BACKEND_URL: str = "http://localhost:8000"
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
