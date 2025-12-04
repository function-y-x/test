from typing import Annotated, List
from datetime import date, datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.models.sqlite_user import User
from app.models.calendar_note import CalendarNote
from app.schemas.calendar_note import CalendarNoteCreate, CalendarNoteUpdate, CalendarNoteOut
from app.services.sqlite_auth import get_current_active_user
from app.db.sqlite_database import get_database

router = APIRouter()


def calculate_stress_score(ddl_date: date | None, current_date: date, progress: int) -> int:
    """
    计算DDL紧张分数
    
    算法考虑两个因素：
    1. 时间紧迫度：当前日期离DDL截止日期越近，紧张程度越高
    2. 进度紧迫度：当前进度越低，紧张程度越高
    
    参数:
        ddl_date: DDL截止日期
        current_date: 当前日期
        progress: 当前进度 (0-100)
    
    返回:
        紧张分数 (0-100)，其中：
        - 0 表示一点不紧张或已完成
        - 100 表示时间紧迫且进度缓慢
    """
    # 如果没有设置DDL或者进度已完成，紧张分数为0
    if ddl_date is None or progress >= 100:
        return 0
    
    # 计算剩余天数
    days_remaining = (ddl_date - current_date).days
    
    # 如果DDL已过期且未完成，紧张分数为100
    if days_remaining < 0:
        return 100
    
    # 时间紧张度：假设30天以上为充裕，0天为最紧张
    # 使用非线性曲线，让最后几天的紧张度上升更快
    if days_remaining >= 30:
        time_stress = 0
    else:
        # 使用平方曲线，让紧张度在最后几天快速上升
        time_stress = ((30 - days_remaining) / 30) ** 1.5 * 100
    
    # 进度紧张度：进度越低，紧张度越高
    progress_stress = 100 - progress
    
    # 综合紧张度计算
    # 当时间很紧迫时（最后7天），时间因素权重更大
    if days_remaining <= 7:
        # 最后7天：时间权重70%，进度权重30%
        stress_score = time_stress * 0.7 + progress_stress * 0.3
    else:
        # 正常情况：时间权重50%，进度权重50%
        stress_score = time_stress * 0.5 + progress_stress * 0.5
    
    # 确保分数在0-100范围内
    return min(100, max(0, int(stress_score)))

@router.post("/", response_model=CalendarNoteOut, status_code=status.HTTP_201_CREATED)
async def create_calendar_note(
    note: CalendarNoteCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_database)
):
    """创建或更新日历备注"""
    try:
        # 计算紧张分数
        current_date = date.today()
        stress_score = calculate_stress_score(note.ddl_date, current_date, note.progress)
        
        # 检查该日期是否已存在备注
        result = await db.execute(
            select(CalendarNote).where(
                and_(
                    CalendarNote.user_id == current_user.id,
                    CalendarNote.note_date == note.note_date
                )
            )
        )
        existing_note = result.scalar_one_or_none()
        
        if existing_note:
            # 如果已存在，更新它
            existing_note.note_text = note.note_text
            existing_note.color = note.color
            existing_note.progress = note.progress
            existing_note.ddl_date = note.ddl_date
            existing_note.stress_score = stress_score
            existing_note.updated_at = datetime.utcnow()
            await db.commit()
            await db.refresh(existing_note)
            return CalendarNoteOut.from_orm(existing_note)
        else:
            # 否则创建新的
            db_note = CalendarNote(
                user_id=current_user.id,
                note_date=note.note_date,
                note_text=note.note_text,
                color=note.color,
                progress=note.progress,
                ddl_date=note.ddl_date,
                stress_score=stress_score,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(db_note)
            await db.commit()
            await db.refresh(db_note)
            return CalendarNoteOut.from_orm(db_note)
            
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"创建日历备注失败: {str(e)}")

@router.get("/", response_model=List[CalendarNoteOut])
async def get_all_calendar_notes(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_database)
):
    """获取用户的所有日历备注"""
    result = await db.execute(
        select(CalendarNote)
        .where(CalendarNote.user_id == current_user.id)
        .order_by(CalendarNote.note_date)
    )
    notes = result.scalars().all()
    return [CalendarNoteOut.from_orm(note) for note in notes]

@router.get("/date/{note_date}", response_model=CalendarNoteOut)
async def get_calendar_note_by_date(
    note_date: date,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_database)
):
    """获取指定日期的日历备注"""
    result = await db.execute(
        select(CalendarNote).where(
            and_(
                CalendarNote.user_id == current_user.id,
                CalendarNote.note_date == note_date
            )
        )
    )
    note = result.scalar_one_or_none()
    
    if not note:
        raise HTTPException(status_code=404, detail="该日期没有备注")
    
    return CalendarNoteOut.from_orm(note)

@router.put("/{note_id}", response_model=CalendarNoteOut)
async def update_calendar_note(
    note_id: int,
    note_update: CalendarNoteUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_database)
):
    """更新日历备注"""
    result = await db.execute(
        select(CalendarNote).where(
            and_(
                CalendarNote.id == note_id,
                CalendarNote.user_id == current_user.id
            )
        )
    )
    note = result.scalar_one_or_none()
    
    if not note:
        raise HTTPException(status_code=404, detail="备注不存在")
    
    # 更新字段
    if note_update.note_text is not None:
        note.note_text = note_update.note_text
    if note_update.color is not None:
        note.color = note_update.color
    if note_update.progress is not None:
        note.progress = note_update.progress
    if note_update.ddl_date is not None:
        note.ddl_date = note_update.ddl_date
    
    # 重新计算紧张分数
    current_date = date.today()
    note.stress_score = calculate_stress_score(note.ddl_date, current_date, note.progress)
    
    note.updated_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(note)
    
    return CalendarNoteOut.from_orm(note)

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_calendar_note(
    note_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_database)
):
    """删除日历备注"""
    result = await db.execute(
        select(CalendarNote).where(
            and_(
                CalendarNote.id == note_id,
                CalendarNote.user_id == current_user.id
            )
        )
    )
    note = result.scalar_one_or_none()
    
    if not note:
        raise HTTPException(status_code=404, detail="备注不存在")
    
    await db.delete(note)
    await db.commit()
    
    return

@router.delete("/date/{note_date}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_calendar_note_by_date(
    note_date: date,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_database)
):
    """删除指定日期的日历备注"""
    result = await db.execute(
        select(CalendarNote).where(
            and_(
                CalendarNote.user_id == current_user.id,
                CalendarNote.note_date == note_date
            )
        )
    )
    note = result.scalar_one_or_none()
    
    if not note:
        raise HTTPException(status_code=404, detail="该日期没有备注")
    
    await db.delete(note)
    await db.commit()
    
    return


@router.get("/stress-scores/range", response_model=dict)
async def get_stress_scores_by_range(
    start_date: date,
    end_date: date,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_database)
):
    """
    获取指定日期范围内的紧张分数
    
    返回格式: {
        "2024-01-01": 50,
        "2024-01-02": 0,
        "2024-01-03": 75,
        ...
    }
    """
    # 获取日期范围内的所有备注
    result = await db.execute(
        select(CalendarNote).where(
            and_(
                CalendarNote.user_id == current_user.id,
                CalendarNote.note_date >= start_date,
                CalendarNote.note_date <= end_date
            )
        )
    )
    notes = result.scalars().all()
    
    # 重新计算所有紧张分数（以防过了一天，分数需要更新）
    current_date = date.today()
    stress_scores = {}
    
    for note in notes:
        # 重新计算紧张分数
        new_stress_score = calculate_stress_score(note.ddl_date, current_date, note.progress)
        
        # 如果分数发生变化，更新数据库
        if new_stress_score != note.stress_score:
            note.stress_score = new_stress_score
            note.updated_at = datetime.utcnow()
        
        stress_scores[str(note.note_date)] = note.stress_score
    
    # 提交更新
    await db.commit()
    
    return stress_scores


@router.post("/recalculate-all-stress", status_code=status.HTTP_200_OK)
async def recalculate_all_stress_scores(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_database)
):
    """
    重新计算用户所有日历备注的紧张分数
    这个接口可以在每天定时调用，或者在用户打开日历时调用
    """
    try:
        # 获取用户的所有日历备注
        result = await db.execute(
            select(CalendarNote).where(CalendarNote.user_id == current_user.id)
        )
        notes = result.scalars().all()
        
        current_date = date.today()
        updated_count = 0
        
        for note in notes:
            # 重新计算紧张分数
            new_stress_score = calculate_stress_score(note.ddl_date, current_date, note.progress)
            
            # 如果分数发生变化，更新
            if new_stress_score != note.stress_score:
                note.stress_score = new_stress_score
                note.updated_at = datetime.utcnow()
                updated_count += 1
        
        await db.commit()
        
        return {
            "message": f"成功重新计算 {updated_count} 条日历备注的紧张分数",
            "updated_count": updated_count,
            "total_count": len(notes)
        }
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"重新计算紧张分数失败: {str(e)}")

