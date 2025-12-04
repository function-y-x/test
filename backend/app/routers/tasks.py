from typing import List
from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select
from app.models.sqlite_user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut
from app.services.sqlite_auth import get_current_active_user
from app.db.sqlite_database import get_database
from app.models.task import TaskEntry

router = APIRouter()

@router.post("/", response_model=TaskOut)
async def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_database)
):
    """创建新任务"""
    try:
        task_date = task.task_date or date.today()
        
        db_task = TaskEntry(
            user_id=current_user.id,
            text=task.text,
            task_date=task_date,
            completed=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(db_task)
        await db.commit()
        await db.refresh(db_task)
        
        return TaskOut(
            id=db_task.id,
            user_id=db_task.user_id,
            text=db_task.text,
            completed=db_task.completed,
            task_date=db_task.task_date,
            created_at=db_task.created_at,
            updated_at=db_task.updated_at
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"任务创建失败: {str(e)}")

@router.get("/today", response_model=List[TaskOut])
async def get_today_tasks(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_database)
):
    """获取今天的任务"""
    try:
        today = date.today()
        
        # 查询今天的任务
        result = await db.execute(
            select(TaskEntry).where(
                and_(
                    TaskEntry.user_id == current_user.id,
                    TaskEntry.task_date == today
                )
            )
        )
        tasks = result.scalars().all()
        
        return [
            TaskOut(
                id=task.id,
                user_id=task.user_id,
                text=task.text,
                completed=task.completed,
                task_date=task.task_date,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
            for task in tasks
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取任务失败: {str(e)}")

@router.put("/{task_id}", response_model=TaskOut)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_database)
):
    """更新任务"""
    try:
        # 查找任务
        result = await db.execute(
            select(TaskEntry).where(
                and_(
                    TaskEntry.id == task_id,
                    TaskEntry.user_id == current_user.id
                )
            )
        )
        db_task = result.scalar_one_or_none()
        
        if not db_task:
            raise HTTPException(status_code=404, detail="任务未找到")
        
        # 更新任务字段
        if task_update.text is not None:
            db_task.text = task_update.text
        if task_update.completed is not None:
            db_task.completed = task_update.completed
        
        db_task.updated_at = datetime.utcnow()
        
        await db.commit()
        await db.refresh(db_task)
        
        return TaskOut(
            id=db_task.id,
            user_id=db_task.user_id,
            text=db_task.text,
            completed=db_task.completed,
            task_date=db_task.task_date,
            created_at=db_task.created_at,
            updated_at=db_task.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"任务更新失败: {str(e)}")

@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_database)
):
    """删除任务 - 暂时未实现"""
    raise HTTPException(status_code=501, detail="删除功能暂未实现")