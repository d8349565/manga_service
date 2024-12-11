from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.db.session import get_db
from app.models.comic import Comic
from app.models.chapter import Chapter
from app.models.user import User
from app.models.reading_progress import ReadingProgress
from app.core.deps import get_current_user

router = APIRouter()

@router.get("/comics/{comic_id}/read/{chapter_id}")
async def get_chapter_content(
    comic_id: int,
    chapter_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 获取漫画和章节信息
    chapter = db.query(Chapter).filter(
        Chapter.id == chapter_id,
        Chapter.comic_id == comic_id
    ).first()
    
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    # 更新阅读进度
    progress = db.query(ReadingProgress).filter(
        ReadingProgress.user_id == current_user.id,
        ReadingProgress.comic_id == comic_id
    ).first()
    
    if progress:
        progress.chapter_id = chapter_id
        progress.last_read_at = datetime.utcnow()
    else:
        progress = ReadingProgress(
            user_id=current_user.id,
            comic_id=comic_id,
            chapter_id=chapter_id
        )
        db.add(progress)
    
    db.commit()
    
    # 获取前后章节信息
    prev_chapter = db.query(Chapter).filter(
        Chapter.comic_id == comic_id,
        Chapter.chapter_number < chapter.chapter_number
    ).order_by(Chapter.chapter_number.desc()).first()
    
    next_chapter = db.query(Chapter).filter(
        Chapter.comic_id == comic_id,
        Chapter.chapter_number > chapter.chapter_number
    ).order_by(Chapter.chapter_number.asc()).first()
    
    return {
        "chapter": chapter,
        "images": chapter.images,
        "navigation": {
            "prev_chapter": prev_chapter.id if prev_chapter else None,
            "next_chapter": next_chapter.id if next_chapter else None,
        }
    }

@router.get("/comics/{comic_id}/progress")
async def get_reading_progress(
    comic_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    progress = db.query(ReadingProgress).filter(
        ReadingProgress.user_id == current_user.id,
        ReadingProgress.comic_id == comic_id
    ).first()
    
    return {
        "current_chapter": progress.chapter_id if progress else None,
        "last_read_at": progress.last_read_at if progress else None
    } 

@router.get("/history")
async def get_reading_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 20
):
    """
    获取用户的阅读历史
    """
    history = (
        db.query(ReadingProgress, Comic, Chapter)
        .join(Comic, ReadingProgress.comic_id == Comic.id)
        .join(Chapter, ReadingProgress.chapter_id == Chapter.id)
        .filter(ReadingProgress.user_id == current_user.id)
        .order_by(ReadingProgress.last_read_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    return [{
        "comic_id": item.ReadingProgress.comic_id,
        "comic_title": item.Comic.title,
        "comic_cover": item.Comic.cover_image,
        "chapter_id": item.ReadingProgress.chapter_id,
        "chapter_title": item.Chapter.title,
        "chapter_number": item.Chapter.chapter_number,
        "last_read_at": item.ReadingProgress.last_read_at
    } for item in history] 