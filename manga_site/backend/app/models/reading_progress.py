from sqlalchemy import Column, Integer, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class ReadingProgress(Base):
    __tablename__ = "reading_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    comic_id = Column(Integer, ForeignKey("comics.id"))
    chapter_id = Column(Integer, ForeignKey("chapters.id"))
    last_read_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", backref="reading_progress")
    comic = relationship("Comic", backref="reading_progress")
    chapter = relationship("Chapter", backref="reading_progress")

    # 添加复合索引以提高查询效率
    __table_args__ = (
        Index('idx_user_comic', user_id, comic_id),
    ) 