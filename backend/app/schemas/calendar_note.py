from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field

class CalendarNoteBase(BaseModel):
    """日历备注基础模型"""
    note_date: date
    note_text: Optional[str] = None
    color: str = '#ffffff'
    progress: int = 0  # DDL进度 (0-100)
    ddl_date: Optional[date] = None  # DDL截止日期

class CalendarNoteCreate(CalendarNoteBase):
    """创建日历备注"""
    pass

class CalendarNoteUpdate(BaseModel):
    """更新日历备注"""
    note_text: Optional[str] = None
    color: Optional[str] = None
    progress: Optional[int] = None  # DDL进度 (0-100)
    ddl_date: Optional[date] = None  # DDL截止日期

class CalendarNoteOut(CalendarNoteBase):
    """返回的日历备注"""
    id: int
    user_id: int
    stress_score: int = 0  # 紧张分数 (0-100)
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        orm_mode = True

