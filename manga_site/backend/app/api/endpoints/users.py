from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.user import User, UserRole
from app.core.deps import check_admin
from app.core import security
from pydantic import BaseModel

router = APIRouter()

class UserResponse(BaseModel):
    id: int
    email: str
    role: UserRole
    is_active: bool

class UserCreate(BaseModel):
    email: str
    password: str
    role: UserRole = UserRole.USER
    is_active: bool = True

@router.get("", response_model=List[UserResponse])
async def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(check_admin)
):
    """获取所有用户列表"""
    users = db.query(User).all()
    return users

@router.post("")
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_admin)
):
    """创建新用户"""
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="该用户名已被注册"
        )
    
    new_user = User(
        email=user.email,
        hashed_password=security.get_password_hash(user.password),
        role=user.role,
        is_active=user.is_active
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "用户创建成功", "id": new_user.id}

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_admin)
):
    """删除用户"""
    if user_id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="不能删除当前登录的用户"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="用户不存在"
        )
    
    db.delete(user)
    db.commit()
    return {"msg": "用户删除成功"} 