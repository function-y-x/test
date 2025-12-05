from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sqlite_user import User
from app.services.sqlite_auth import authenticate_user, create_access_token, get_current_active_user, register_new_user
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.core.config import settings
from app.db.sqlite_database import get_database

router = APIRouter()

@router.post("/register", response_model=Token)
async def register(user_create: UserCreate, db: AsyncSession = Depends(get_database)):
    user = await register_new_user(user_create, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    # 注册成功后自动生成token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    # 构造用户输出数据
    user_out = {
        "id": str(user.id),
        "email": user.email,
        "username": user.username,
        "exam_date": user.exam_date,
        "selected_subjects": user.get_selected_subjects(),
        "ai_companion_style": user.ai_companion_style,
        "created_at": user.created_at
    }
    
    return {"access_token": access_token, "token_type": "bearer", "user": user_out}

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_database)
):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    # 构造用户输出数据
    user_out = {
        "id": str(user.id),
        "email": user.email,
        "username": user.username,
        "exam_date": user.exam_date,
        "selected_subjects": user.get_selected_subjects(),
        "ai_companion_style": user.ai_companion_style,
        "created_at": user.created_at
    }
    
    return {"access_token": access_token, "token_type": "bearer", "user": user_out}

@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    user_out = UserOut(
        id=str(current_user.id),
        email=current_user.email,
        username=current_user.username,
        exam_date=current_user.exam_date,
        selected_subjects=current_user.get_selected_subjects(),
        ai_companion_style=current_user.ai_companion_style,
        created_at=current_user.created_at
    )
    return user_out

@router.put("/me", response_model=UserOut)
async def update_users_me(
    user_update: UserUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_database)
):
    """更新当前用户信息"""
    try:
        # 更新用户信息
        if user_update.exam_date is not None:
            current_user.exam_date = user_update.exam_date
        if user_update.selected_subjects is not None:
            current_user.set_selected_subjects(user_update.selected_subjects)
        if user_update.ai_companion_style is not None:
            current_user.ai_companion_style = user_update.ai_companion_style
        
        await db.commit()
        await db.refresh(current_user)
        
        # 返回更新后的用户信息
        user_out = UserOut(
            id=str(current_user.id),
            email=current_user.email,
            username=current_user.username,
            exam_date=current_user.exam_date,
            selected_subjects=current_user.get_selected_subjects(),
            ai_companion_style=current_user.ai_companion_style,
            created_at=current_user.created_at
        )
        return user_out
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新用户信息失败: {str(e)}"
        )