from datetime import datetime, date
from typing import Optional
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.db.sqlite_database import Base

class TaskEntry(Base):
    __tablename__ = "task_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    text = Column(String(500), nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
    task_date = Column(Date, nullable=False)  # 任务归属的日期
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联到用户
    user = relationship("User", back_populates="task_entries")

