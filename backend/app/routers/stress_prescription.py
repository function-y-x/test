"""
压力处方生成 API
"""

from typing import Annotated
from datetime import date, datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from app.models.sqlite_user import User
from app.models.calendar_note import CalendarNote
from app.models.sleep import SleepEntry
from app.models.mood import MoodEntry
from app.services.sqlite_auth import get_current_active_user
from app.db.sqlite_database import get_database
from app.services.stress_analysis import analyze_stress_sources, generate_stress_prescription_stream

router = APIRouter()


@router.post("/generate")
async def generate_prescription(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_database)
):
    """
    生成压力处方（流式输出）
    
    分析四个压力来源：
    1. DDL 任务压力
    2. 睡眠不足压力
    3. 考研倒计时焦虑
    4. 心理情绪压力
    """
    try:
        # 1. 获取 DDL 平均紧张分数（最近 7 天有任务的）
        today = date.today()
        result = await db.execute(
            select(func.avg(CalendarNote.stress_score))
            .where(
                and_(
                    CalendarNote.user_id == current_user.id,
                    CalendarNote.stress_score > 0,
                    CalendarNote.note_date >= today
                )
            )
        )
        avg_ddl_score = result.scalar() or 0
        
        # 2. 获取最近的睡眠时长
        result = await db.execute(
            select(SleepEntry)
            .where(SleepEntry.user_id == current_user.id)
            .order_by(SleepEntry.created_at.desc())
            .limit(1)
        )
        sleep_entry = result.scalar_one_or_none()
        sleep_hours = sleep_entry.sleep_hours if sleep_entry else None
        
        # 3. 计算距离考研天数
        if current_user.exam_date:
            days_until_exam = (current_user.exam_date.date() - today).days
        else:
            days_until_exam = 365  # 默认一年
        
        # 4. 获取最近的情绪压力等级
        result = await db.execute(
            select(MoodEntry)
            .where(MoodEntry.user_id == current_user.id)
            .order_by(MoodEntry.created_at.desc())
            .limit(1)
        )
        mood_entry = result.scalar_one_or_none()
        recent_mood_stress = mood_entry.stress_level if mood_entry else None
        
        # 5. 分析压力来源
        stress_analysis = await analyze_stress_sources(
            ddl_score=avg_ddl_score,
            sleep_hours=sleep_hours,
            days_until_exam=days_until_exam,
            recent_mood_stress=recent_mood_stress
        )
        
        # 6. 使用 DeepSeek 生成压力处方（流式）
        async def stream_generator():
            # 先发送压力分析数据
            import json
            analysis_data = {
                'type': 'analysis',
                'data': {
                    'total_score': stress_analysis['total_score'],
                    'main_sources': stress_analysis['main_sources'],
                    'ddl_score': avg_ddl_score,
                    'sleep_hours': sleep_hours,
                    'days_until_exam': days_until_exam,
                    'mood_stress': recent_mood_stress
                }
            }
            yield f"data: {json.dumps(analysis_data, ensure_ascii=False)}\n\n"
            
            # 然后流式输出 AI 生成的处方
            async for chunk in generate_stress_prescription_stream(
                stress_analysis,
                user_info={'username': current_user.username}
            ):
                prescription_data = {
                    'type': 'prescription',
                    'content': chunk
                }
                yield f"data: {json.dumps(prescription_data, ensure_ascii=False)}\n\n"
            
            # 发送结束标记
            yield "data: [DONE]\n\n"
        
        return StreamingResponse(
            stream_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成压力处方失败: {str(e)}")
