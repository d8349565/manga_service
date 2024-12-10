from app.db.base import Base, engine
from app.models.comic import Comic
from app.models.chapter import Chapter
from app.models.user import User
import os

def migrate_database():
    # 删除旧的数据库文件
    if os.path.exists("manga.db"):
        os.remove("manga.db")
        print("已删除旧数据库")

    # 使用SQLAlchemy创建所有表
    Base.metadata.create_all(bind=engine)
    print("数据库表创建成功")

if __name__ == "__main__":
    migrate_database() 