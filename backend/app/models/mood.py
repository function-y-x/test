from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.sqlite_database import Base

class MoodEntry(Base):
    __tablename__ = "mood_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mood = Column(String(50), nullable=False)  # 心情状态：happy, calm, anxious 等
    stress_level = Column(Integer, nullable=False)  # 压力等级 1-10
    notes = Column(Text, nullable=True)  # 可选的备注
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    user = relationship("User", back_populates="mood_entries")

