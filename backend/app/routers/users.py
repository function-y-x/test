from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.sqlite_user import User
from app.schemas.user import UserUpdate, UserOut
from app.services.sqlite_auth import get_current_active_user
from app.db.sqlite_database import get_database

router = APIRouter()

@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    """获取当前用户信息"""
    return UserOut(
        id=str(current_user.id),
        email=current_user.email,
        username=current_user.username,
        exam_date=current_user.exam_date,
        selected_subjects=current_user.get_selected_subjects(),
        ai_companion_style=current_user.ai_companion_style,
        created_at=current_user.created_at
    )

@router.put("/me", response_model=UserOut)
async def update_users_me(
    user_update: UserUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_database)
):
    """更新当前用户信息"""
    # 更新用户信息
    if user_update.exam_date is not None:
        current_user.exam_date = user_update.exam_date
    
    if user_update.selected_subjects is not None:
        current_user.set_selected_subjects(user_update.selected_subjects)
    
    if user_update.ai_companion_style is not None:
        current_user.ai_companion_style = user_update.ai_companion_style
    
    # 提交更改
    await db.commit()
    await db.refresh(current_user)
    
    return UserOut(
        id=str(current_user.id),
        email=current_user.email,
        username=current_user.username,
        exam_date=current_user.exam_date,
        selected_subjects=current_user.get_selected_subjects(),
        ai_companion_style=current_user.ai_companion_style,
        created_at=current_user.created_at
    )

