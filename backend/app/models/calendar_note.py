from datetime import datetime, date
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.db.sqlite_database import Base

class CalendarNote(Base):
    """学习日历备注模型"""
    __tablename__ = "calendar_notes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    note_date = Column(Date, nullable=False, index=True)  # 备注的日期
    note_text = Column(Text, nullable=True)  # 备注内容
    color = Column(String(20), nullable=False, default='#ffffff')  # 日历颜色标记
    progress = Column(Integer, nullable=False, default=0)  # DDL进度 (0-100)
    ddl_date = Column(Date, nullable=True)  # DDL截止日期
    stress_score = Column(Integer, nullable=False, default=0)  # 紧张分数 (0-100)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联到用户
    user = relationship("User", back_populates="calendar_notes")

