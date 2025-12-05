from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.sqlite_database import Base

class SleepEntry(Base):
    __tablename__ = "sleep_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    sleep_hours = Column(Float, nullable=False)  # 睡眠时长（小时）
    sleep_date = Column(DateTime, nullable=False)  # 睡眠日期（前一天的日期）
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    user = relationship("User", back_populates="sleep_entries")

