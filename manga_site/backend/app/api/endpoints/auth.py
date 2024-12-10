from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User, UserRole
from app.core import security
from app.core.config import settings
from app.core.deps import get_current_active_user
from typing import Any
from pydantic import BaseModel

router = APIRouter()

# 添加请求模型
class UserCreate(BaseModel):
    username: str
    password: str

class AdminCreate(UserCreate):
    admin_key: str

@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
) -> Any:
    """
    注册新用户
    """
    existing_user = db.query(User).filter(User.email == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="该用户名已被注册"
        )
    
    new_user = User(
        email=user.username,
        hashed_password=security.get_password_hash(user.password),
        role=UserRole.USER,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    
    return {"msg": "用户注册成功"}

@router.post("/register/admin")
def register_admin(
    admin: AdminCreate,
    db: Session = Depends(get_db)
) -> Any:
    """
    注册管理员账号
    """
    if admin.admin_key != settings.ADMIN_REGISTER_KEY:
        raise HTTPException(
            status_code=400,
            detail="管理员注册密钥错误"
        )
        
    existing_user = db.query(User).filter(User.email == admin.username).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="该用户名已被注册"
        )
    
    new_user = User(
        email=admin.username,
        hashed_password=security.get_password_hash(admin.password),
        role=UserRole.ADMIN,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    
    return {"msg": "管理员注册成功"}

@router.post("/login")
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    用户登录
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=400,
            detail="用户名或密码错误"
        )
    if not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="用户名或密码错误"
        )
    
    return {
        "access_token": security.create_access_token(user.id),
        "token_type": "bearer"
    }

@router.get("/me")
async def read_users_me(
    current_user: User = Depends(get_current_active_user)
):
    """
    获取当前登录用户信息
    """
    return {
        "email": current_user.email,
        "role": current_user.role,
        "is_active": current_user.is_active
    } 