from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Comic(Base):
    __tablename__ = "comics"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    author = Column(String(100))
    description = Column(Text)
    cover_image = Column(String(500))

    chapters = relationship("Chapter", back_populates="comic", cascade="all, delete-orphan") 