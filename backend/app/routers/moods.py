from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models.sqlite_user import User
from app.schemas.mood import MoodCreate, MoodOut
from app.services.sqlite_auth import get_current_active_user
from app.db.sqlite_database import get_database
from app.models.mood import MoodEntry
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=MoodOut)
async def create_mood_entry(
    mood: MoodCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_database)
):
    # 创建情绪记录
    mood_data = mood.dict()
    mood_data['user_id'] = current_user.id
    mood_data['created_at'] = datetime.utcnow()
    
    mood_entry = MoodEntry(**mood_data)
    db.add(mood_entry)
    await db.commit()
    await db.refresh(mood_entry)
    
    return MoodOut.from_orm(mood_entry)

@router.get("/", response_model=List[MoodOut])
async def get_user_moods(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_database)
):
    # 获取用户的所有情绪记录，按时间倒序
    result = await db.execute(
        select(MoodEntry)
        .where(MoodEntry.user_id == current_user.id)
        .order_by(desc(MoodEntry.created_at))
    )
    moods = result.scalars().all()
    return [MoodOut.from_orm(mood) for mood in moods]

@router.get("/latest", response_model=MoodOut)
async def get_latest_mood(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_database)
):
    # 获取用户最新的情绪记录
    result = await db.execute(
        select(MoodEntry)
        .where(MoodEntry.user_id == current_user.id)
        .order_by(desc(MoodEntry.created_at))
        .limit(1)
    )
    mood = result.scalar_one_or_none()
    
    if not mood:
        raise HTTPException(status_code=404, detail="No mood entries found")
    
    return MoodOut.from_orm(mood)

@router.get("/{mood_id}", response_model=MoodOut)
async def get_mood_by_id(
    mood_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_database)
):
    result = await db.execute(
        select(MoodEntry)
        .where(MoodEntry.id == mood_id, MoodEntry.user_id == current_user.id)
    )
    mood = result.scalar_one_or_none()
    
    if not mood:
        raise HTTPException(status_code=404, detail="Mood entry not found")
    
    return MoodOut.from_orm(mood)

@router.delete("/{mood_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mood(
    mood_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_database)
):
    result = await db.execute(
        select(MoodEntry)
        .where(MoodEntry.id == mood_id, MoodEntry.user_id == current_user.id)
    )
    mood = result.scalar_one_or_none()
    
    if not mood:
        raise HTTPException(status_code=404, detail="Mood entry not found")
    
    await db.delete(mood)
    await db.commit()
    return

