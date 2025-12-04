from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from app.models.sqlite_user import User
from app.schemas.mood import MoodCreate, MoodOut
from app.services.sqlite_auth import get_current_active_user
from app.db.sqlite_database import get_database, AsyncSessionLocal
from app.models.mood import MoodEntry
from datetime import datetime, timedelta

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

@router.get("/weekly-scores")
async def get_weekly_mood_scores(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    获取近7天的心情得分（简化版）
    返回格式：[{date: "周一", score: 7.5}, ...]
    """
    try:
        one_week_ago = datetime.utcnow() - timedelta(days=7)
        
        async with AsyncSessionLocal() as db:
            # 查询近7天的情绪记录
            result = await db.execute(
                select(MoodEntry)
                .where(
                    MoodEntry.user_id == current_user.id,
                    MoodEntry.created_at >= one_week_ago
                )
                .order_by(MoodEntry.created_at)
            )
            moods = result.scalars().all()
            
            # 按日期分组
            daily_scores = {}
            for mood in moods:
                date_key = mood.created_at.date()
                if date_key not in daily_scores:
                    daily_scores[date_key] = []
                daily_scores[date_key].append(mood.stress_level)
            
            # 生成结果
            scores = []
            weekday_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
            
            for i in range(6, -1, -1):
                date = (datetime.utcnow() - timedelta(days=i)).date()
                weekday = weekday_names[date.weekday()]
                
                if date in daily_scores:
                    avg_score = sum(daily_scores[date]) / len(daily_scores[date])
                    count = len(daily_scores[date])
                else:
                    avg_score = 5.0
                    count = 0
                
                scores.append({
                    'date': str(date),
                    'weekday': weekday,
                    'score': round(avg_score, 1),
                    'count': count
                })
            
            return {
                'success': True,
                'data': scores
            }
            
    except Exception as e:
        print(f"❌ 获取心情得分失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'success': False,
            'data': [],
            'error': str(e)
        }


@router.get("/weekly-stats")
async def get_weekly_mood_stats(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    获取近一周的情绪统计数据
    返回每天的平均压力等级，用于压力雷达图表
    """
    try:
        # 计算一周前的日期
        one_week_ago = datetime.utcnow() - timedelta(days=7)
        
        # 手动创建数据库会话
        async with AsyncSessionLocal() as db:
            # 获取近一周的所有情绪记录
            result = await db.execute(
                select(MoodEntry)
                .where(
                    MoodEntry.user_id == current_user.id,
                    MoodEntry.created_at >= one_week_ago
                )
                .order_by(MoodEntry.created_at)
            )
            moods = result.scalars().all()
        
            # 按日期分组统计
            daily_stats = {}
            for mood in moods:
                # 获取日期（不包含时间）
                date_key = mood.created_at.date()
                
                if date_key not in daily_stats:
                    daily_stats[date_key] = {
                        'stress_levels': [],
                        'moods': []
                    }
                
                daily_stats[date_key]['stress_levels'].append(mood.stress_level)
                daily_stats[date_key]['moods'].append(mood.mood)
            
            # 生成近7天的数据（即使某天没有记录也要显示）
            weekly_data = []
            for i in range(6, -1, -1):  # 从6天前到今天
                date = (datetime.utcnow() - timedelta(days=i)).date()
                
                if date in daily_stats:
                    # 计算当天的平均压力等级
                    avg_stress = sum(daily_stats[date]['stress_levels']) / len(daily_stats[date]['stress_levels'])
                    most_common_mood = max(set(daily_stats[date]['moods']), key=daily_stats[date]['moods'].count)
                else:
                    # 如果当天没有记录，使用默认值
                    avg_stress = 5
                    most_common_mood = 'calm'
                
                # 格式化日期为星期几
                weekday_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
                weekday = weekday_names[date.weekday()]
                
                weekly_data.append({
                    'date': str(date),
                    'weekday': weekday,
                    'avg_stress_level': round(avg_stress, 2),
                    'mood': most_common_mood,
                    'record_count': len(daily_stats.get(date, {}).get('stress_levels', []))
                })
            
            return {
                'weekly_data': weekly_data,
                'total_records': len(moods)
            }
    except Exception as e:
        print(f"❌ 获取周情绪数据时出错: {str(e)}")
        print(f"错误类型: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        
        # 返回空数据而不是抛出异常
        return {
            'weekly_data': [],
            'total_records': 0,
            'error': str(e)
        }


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

