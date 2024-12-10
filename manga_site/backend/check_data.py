from app.db.session import SessionLocal
from app.models.chapter import Chapter
from app.models.comic import Comic
import json

def check_data():
    db = SessionLocal()
    try:
        # 检查章节数据
        chapter = db.query(Chapter).first()
        if chapter:
            print("\n章节信息：")
            print(f"ID: {chapter.id}")
            print(f"标题: {chapter.title}")
            print(f"原始 images 数据: {chapter.images}")  # 查看原始 JSON 字符串
            print("\n解析后的图片列表:")
            try:
                images = chapter.images_list
                for i, url in enumerate(images):
                    print(f"图片 {i+1}: {url}")
            except Exception as e:
                print(f"解析图片列表出错: {str(e)}")
        else:
            print("数据库中没有章节数据")
    finally:
        db.close()

if __name__ == "__main__":
    check_data() 