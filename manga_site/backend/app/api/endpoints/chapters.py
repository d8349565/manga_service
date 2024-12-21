from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import json
from app.db.session import get_db
from app.models.chapter import Chapter
from app.models.user import User
from app.core.deps import get_current_user, get_current_active_user
from app.utils.image_handler import ImageHandler
import shutil
import os
from app.models.comic import Comic

router = APIRouter()


@router.get("/{comic_id}/chapters")
async def get_chapters(comic_id: int, db: Session = Depends(get_db)):
    # 只查询需要的字段,避免加载整个对象
    chapters = db.query(
        Chapter.chapter_number,
        Chapter.comic_id, 
        Chapter.id,
        Chapter.title
    ).filter(
        Chapter.comic_id == comic_id
    ).all()
    
    # 直接返回查询结果,不需要额外处理
    return [
        {
            "chapter_number": chapter[0],
            "comic_id": chapter[1], 
            "id": chapter[2],
            "title": chapter[3]
        }
        for chapter in chapters
    ]


@router.post("/{comic_id}/chapters")
async def create_chapter(
    comic_id: int,
    chapter_number: int,
    title: str,
    images: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    image_handler = ImageHandler()
    image_paths = []

    for image in images:
        file_location = f"uploads/chapters/{comic_id}/{chapter_number}/{image.filename}"
        saved_path = await image_handler.save_image(image, file_location, optimize=True)
        image_paths.append(saved_path)

    chapter = Chapter(
        comic_id=comic_id,
        chapter_number=chapter_number,
        title=title,
        images=image_paths,
    )
    db.add(chapter)
    db.commit()
    db.refresh(chapter)
    return chapter


@router.get("/{chapter_id}")
async def get_chapter(
    chapter_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    获取章节详情
    """
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="章节不存在")

    # 获取漫画信息
    comic = db.query(Comic).filter(Comic.id == chapter.comic_id).first()

    return {
        "id": chapter.id,
        "comic_id": chapter.comic_id,
        "comic_title": comic.title,
        "chapter_number": chapter.chapter_number,
        "title": chapter.title,
        "images": chapter.images_list,
    }


@router.get("/{chapter_id}/navigation")
async def get_chapter_navigation(
    chapter_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    获取章节导航信息（上一章/下一章）
    """
    current_chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not current_chapter:
        raise HTTPException(status_code=404, detail="章节不存在")

    # 获取上一章和下一章
    prev_chapter = (
        db.query(Chapter)
        .filter(
            Chapter.comic_id == current_chapter.comic_id,
            Chapter.chapter_number < current_chapter.chapter_number,
        )
        .order_by(Chapter.chapter_number.desc())
        .first()
    )

    next_chapter = (
        db.query(Chapter)
        .filter(
            Chapter.comic_id == current_chapter.comic_id,
            Chapter.chapter_number > current_chapter.chapter_number,
        )
        .order_by(Chapter.chapter_number.asc())
        .first()
    )

    return {
        "prev_chapter": prev_chapter.id if prev_chapter else None,
        "next_chapter": next_chapter.id if next_chapter else None,
    }
