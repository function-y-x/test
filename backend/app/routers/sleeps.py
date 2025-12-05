from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, and_
from app.models.sqlite_user import User
from app.schemas.sleep import SleepCreate, SleepOut
from app.services.sqlite_auth import get_current_active_user
from app.db.sqlite_database import get_database, AsyncSessionLocal
from app.models.sleep import SleepEntry
from datetime import datetime, timedelta

router = APIRouter()

def get_sleep_period_bounds():
    """
    获取当前睡眠记录周期的起止时间
    从当天0点到第二天0点为一个周期
    """
    now = datetime.utcnow()
    
    # 获取今天的0点作为周期开始
    period_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    # 获取明天的0点作为周期结束
    period_end = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    # 睡眠日期是昨天
    sleep_date = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    
    return period_start, period_end, sleep_date

@router.post("/", response_model=SleepOut)
async def create_sleep_entry(
    sleep: SleepCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_database)
):
    """
    创建睡眠记录
    一天只能创建一次（从当天0点到第二天0点）
    """
    period_start, period_end, sleep_date = get_sleep_period_bounds()
    
    # 检查当前周期内是否已经有记录
    result = await db.execute(
        select(SleepEntry)
        .where(
            and_(
                SleepEntry.user_id == current_user.id,
                SleepEntry.created_at >= period_start,
                SleepEntry.created_at < period_end
            )
        )
    )
    existing_entry = result.scalar_one_or_none()
    
    if existing_entry:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="今天已经记录过睡眠时长了，明天再来吧！"
        )
    
    # 创建睡眠记录
    sleep_entry = SleepEntry(
        user_id=current_user.id,
        sleep_hours=sleep.sleep_hours,
        sleep_date=sleep_date,
        created_at=datetime.utcnow()
    )
    
    db.add(sleep_entry)
    await db.commit()
    await db.refresh(sleep_entry)
    
    return SleepOut.from_orm(sleep_entry)

@router.get("/today", response_model=SleepOut)
async def get_today_sleep_entry(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_database)
):
    """
    获取今天的睡眠记录（当天0点到第二天0点的周期内）
    """
    period_start, period_end, sleep_date = get_sleep_period_bounds()
    
    result = await db.execute(
        select(SleepEntry)
        .where(
            and_(
                SleepEntry.user_id == current_user.id,
                SleepEntry.created_at >= period_start,
                SleepEntry.created_at < period_end
            )
        )
    )
    sleep_entry = result.scalar_one_or_none()
    
    if not sleep_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="今天还没有记录睡眠时长"
        )
    
    return SleepOut.from_orm(sleep_entry)

@router.get("/weekly-data")
async def get_weekly_sleep_data(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    获取近7天的睡眠时长数据
    返回格式：[{date: "2025-01-01", sleep_hours: 7.5, weekday: "周一"}, ...]
    如果某天没有数据，默认显示7小时
    """
    try:
        one_week_ago = datetime.utcnow() - timedelta(days=7)
        
        async with AsyncSessionLocal() as db:
            # 查询近7天的睡眠记录
            result = await db.execute(
                select(SleepEntry)
                .where(
                    SleepEntry.user_id == current_user.id,
                    SleepEntry.sleep_date >= one_week_ago
                )
                .order_by(SleepEntry.sleep_date)
            )
            sleep_entries = result.scalars().all()
            
            # 按日期组织数据
            sleep_data = {}
            for entry in sleep_entries:
                date_key = entry.sleep_date.date()
                sleep_data[date_key] = entry.sleep_hours
            
            # 生成近7天的数据
            weekly_data = []
            weekday_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
            
            for i in range(6, -1, -1):
                date = (datetime.utcnow() - timedelta(days=i)).date()
                weekday = weekday_names[date.weekday()]
                
                # 如果没有数据，默认显示7小时
                sleep_hours = sleep_data.get(date, 7.0)
                
                weekly_data.append({
                    'date': str(date),
                    'weekday': weekday,
                    'sleep_hours': sleep_hours,
                    'has_data': date in sleep_data
                })
            
            return {
                'success': True,
                'data': weekly_data
            }
            
    except Exception as e:
        print(f"❌ 获取睡眠数据失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'success': False,
            'data': [],
            'error': str(e)
        }

@router.get("/", response_model=List[SleepOut])
async def get_user_sleep_entries(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_database)
):
    """
    获取用户的所有睡眠记录，按时间倒序
    """
    result = await db.execute(
        select(SleepEntry)
        .where(SleepEntry.user_id == current_user.id)
        .order_by(desc(SleepEntry.created_at))
    )
    sleep_entries = result.scalars().all()
    return [SleepOut.from_orm(entry) for entry in sleep_entries]

