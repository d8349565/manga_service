from typing import Any, Dict, Optional
from pydantic_settings import BaseSettings
import secrets

class Settings(BaseSettings):
    PROJECT_NAME: str = "Manga Reader"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    ALGORITHM: str = "HS256"
    
    # MySQL配置
    MYSQL_SERVER: str = "192.168.110.73"
    MYSQL_USER: str = "comic"
    MYSQL_PASSWORD: str = "YyzK2jPEaTKKAhjs"
    MYSQL_DB: str = "comic"
    MYSQL_PORT: str = "3306"
    
    # 构建MySQL连接URL
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
            f"@{self.MYSQL_SERVER}:{self.MYSQL_PORT}/{self.MYSQL_DB}"
        )
    
    ADMIN_REGISTER_KEY: str = "d8349565"  # 用于注册管理员的密钥
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 