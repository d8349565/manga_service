from typing import Any, Dict, Optional
from pydantic_settings import BaseSettings
import secrets

class Settings(BaseSettings):
    PROJECT_NAME: str = "Manga Reader"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    ALGORITHM: str = "HS256"
    
    # Database
    DATABASE_URL: str = "sqlite:///./manga.db"
    
    ADMIN_REGISTER_KEY: str = "your-secret-admin-key"  # 用于注册管理员的密钥
    
    class Config:
        case_sensitive = True

settings = Settings() 