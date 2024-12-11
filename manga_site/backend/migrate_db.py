from app.db.base import Base, engine
from app.models.comic import Comic
from app.models.chapter import Chapter
from app.models.user import User
from app.models.reading_progress import ReadingProgress
from sqlalchemy import text, inspect
import os

def migrate_reading_progress():
    # 连接到数据库
    with engine.connect() as connection:
        try:
            # 检查reading_progress表是否存在
            inspector = inspect(engine)
            if 'reading_progress' in inspector.get_table_names():
                # 删除reading_progress表
                connection.execute(text("DROP TABLE reading_progress"))
                print("已删除reading_progress表")
            
            # 重新创建reading_progress表
            ReadingProgress.__table__.create(engine)
            print("成功创建reading_progress表")
            
        except Exception as e:
            print(f"迁移出错: {str(e)}")
            raise

if __name__ == "__main__":
    migrate_reading_progress() 