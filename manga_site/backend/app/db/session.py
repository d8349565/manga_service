from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # 添加连接池健康检查
    pool_size=5,         # 连接池大小
    max_overflow=10,     # 最大溢出连接数
    pool_recycle=3600,   # 连接回收时间(秒)
    # MySQL特定配置
    pool_timeout=30,     # 连接超时时间
    max_identifier_length=64  # MySQL标识符最大长度
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 