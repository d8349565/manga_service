from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.comic import Comic
from app.models.chapter import Chapter
from pydantic import BaseModel
from app.core.deps import check_admin, get_current_active_user
from app.models.user import User

router = APIRouter()

class ComicCreate(BaseModel):
    title: str
    author: str
    description: str
    cover_url: str
    chapter_images: List[str]

@router.post("")
async def create_comic(
    *,
    db: Session = Depends(get_db),
    comic_data: ComicCreate,
    current_user: User = Depends(check_admin)
):
    """
    创建新漫画
    """
    try:
        # 创建漫画记录
        comic = Comic(
            title=comic_data.title,
            author=comic_data.author,
            description=comic_data.description,
            cover_image=comic_data.cover_url  # 直接使用图片URL
        )
        db.add(comic)
        db.commit()
        db.refresh(comic)
        
        # 创建第一章
        chapter = Chapter(
            comic_id=comic.id,
            chapter_number=1,
            title="第一话",
            images=comic_data.chapter_images  # 存储图片URL列表
        )
        db.add(chapter)
        db.commit()
        
        return {"id": comic.id, "message": "漫画创建成功"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"创建漫画失败: {str(e)}"
        )

@router.get("")
async def get_comics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100
):
    """
    获取漫画列表
    """
    comics = db.query(Comic).offset(skip).limit(limit).all()
    return comics 

@router.delete("/{comic_id}")
async def delete_comic(
    comic_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_admin)
):
    """
    删除漫画及其所有章节
    """
    try:
        # 首先删除所有相关章节
        db.query(Chapter).filter(Chapter.comic_id == comic_id).delete()
        
        # 然后删除漫画
        comic = db.query(Comic).filter(Comic.id == comic_id).first()
        if not comic:
            raise HTTPException(status_code=404, detail="漫画不存在")
        
        db.delete(comic)
        db.commit()
        
        return {"message": "漫画删除成功"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"删除漫画失败: {str(e)}"
        )

@router.get("/{comic_id}")
async def get_comic(
    comic_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取漫画详情
    """
    comic = db.query(Comic).filter(Comic.id == comic_id).first()
    if not comic:
        raise HTTPException(status_code=404, detail="漫画不存在")
    return comic

@router.get("/{comic_id}/chapters")
async def get_comic_chapters(
    comic_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取漫画的所有章节
    """
    # 优化查询，只获取需要的字段
    chapters = db.query(
        Chapter.chapter_number,
        Chapter.comic_id, 
        Chapter.id,
        Chapter.title
    ).filter(
        Chapter.comic_id == comic_id
    ).order_by(Chapter.chapter_number).all()
    
    return [
        {
            "chapter_number": chapter[0],
            "comic_id": chapter[1], 
            "id": chapter[2],
            "title": chapter[3]
        }
        for chapter in chapters
    ]