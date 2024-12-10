from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class ReadingProgress(Base):
    __tablename__ = "reading_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    comic_id = Column(Integer, ForeignKey("comics.id"))
    chapter_id = Column(Integer, ForeignKey("chapters.id"))
    last_read_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", backref="reading_progress")
    comic = relationship("Comic", backref="reading_progress")
    chapter = relationship("Chapter", backref="reading_progress") 