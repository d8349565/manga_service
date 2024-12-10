import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base_class import Base
from app.db.session import SessionLocal
from app.models.comic import Comic
from app.models.chapter import Chapter
from app.core.config import settings
import json
from collections import defaultdict

def import_from_mysql():
    # MySQL连接配置
    mysql_config = {
        'host': '192.168.110.93',
        'user': 'comic',
        'password': '@Ld1133111131',
        'database': 'comic'  # 替换为您的数据库名
    }

    # 连接MySQL
    mysql_conn = mysql.connector.connect(**mysql_config)
    mysql_cursor = mysql_conn.cursor(dictionary=True)

    # 使用SQLite会话
    db = SessionLocal()

    try:
        # 先获取所有漫画信息
        print("开始导入漫画信息...")
        mysql_cursor.execute("""
            SELECT DISTINCT Comic_name, Comic_cover 
            FROM pic 
            WHERE Comic_name IS NOT NULL 
            AND Comic_cover IS NOT NULL
        """)
        comics = mysql_cursor.fetchall()
        
        comic_id_map = {}
        for comic in comics:
            if not comic['Comic_name']:
                continue
                
            existing_comic = db.query(Comic).filter(Comic.title == comic['Comic_name']).first()
            if not existing_comic:
                new_comic = Comic(
                    title=comic['Comic_name'],
                    cover_image=comic['Comic_cover'],
                    author='未知',
                    description='暂无描述'
                )
                db.add(new_comic)
                db.flush()
                comic_id_map[comic['Comic_name']] = new_comic.id
                print(f"添加漫画: {comic['Comic_name']}")

        db.commit()
        print(f"成功导入 {len(comic_id_map)} 部漫画")

        # 获取每部漫画的章节信息
        print("\n开始导入章节信息...")
        for comic_name in comic_id_map.keys():
            # 获取这部漫画的所有章节
            mysql_cursor.execute("""
                SELECT DISTINCT Chapter_title 
                FROM pic 
                WHERE Comic_name = %s 
                AND Chapter_title IS NOT NULL
                ORDER BY Chapter_title
            """, (comic_name,))
            
            chapters = mysql_cursor.fetchall()
            comic_id = comic_id_map[comic_name]
            chapter_number = 1
            
            for chapter in chapters:
                chapter_title = chapter['Chapter_title']
                
                # 获取该章节的所有图片URL，按name字段排序
                mysql_cursor.execute("""
                    SELECT target_url, name 
                    FROM pic 
                    WHERE Comic_name = %s 
                    AND Chapter_title = %s 
                    AND target_url IS NOT NULL 
                    AND target_url != ''
                    ORDER BY name
                """, (comic_name, chapter_title))
                
                chapter_images = mysql_cursor.fetchall()
                
                if chapter_images:  # 只添加有图片的章节
                    # 提取排序后的URL列表
                    image_urls = [img['target_url'] for img in chapter_images if img['target_url']]
                    
                    if image_urls:  # 确保有有效的URL
                        existing_chapter = db.query(Chapter).filter(
                            Chapter.comic_id == comic_id,
                            Chapter.title == chapter_title
                        ).first()
                        
                        if not existing_chapter:
                            new_chapter = Chapter(
                                comic_id=comic_id,
                                chapter_number=chapter_number,
                                title=chapter_title,
                                images=json.dumps(image_urls)  # 存储排序后的URL列表
                            )
                            db.add(new_chapter)
                            print(f"添加章节: {comic_name} - {chapter_title} (图片数: {len(image_urls)})")
                            chapter_number += 1
            
            db.commit()
            print(f"完成漫画 {comic_name} 的导入，共 {chapter_number-1} 章")

        print("\n数据导入完成！")

    except Exception as e:
        print(f"导入出错: {str(e)}")
        db.rollback()
        raise
    finally:
        mysql_cursor.close()
        mysql_conn.close()
        db.close()

if __name__ == "__main__":
    import_from_mysql() 