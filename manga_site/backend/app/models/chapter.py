from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import json

class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)
    comic_id = Column(Integer, ForeignKey("comics.id"))
    chapter_number = Column(Integer)
    title = Column(String(255))
    images = Column(Text)

    comic = relationship("Comic", back_populates="chapters")

    @property
    def images_list(self):
        """将JSON字符串转换为列表"""
        try:
            return json.loads(self.images) if self.images else []
        except:
            return []