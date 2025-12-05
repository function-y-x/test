from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.sqlite_database import Base
import json

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    exam_date = Column(DateTime, nullable=True)
    selected_subjects = Column(Text, nullable=True)  # JSON字符串存储列表
    ai_companion_style = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    is_active = Column(Boolean, default=True)

    # 关系
    mood_entries = relationship("MoodEntry", back_populates="user")
    task_entries = relationship("TaskEntry", back_populates="user")
    calendar_notes = relationship("CalendarNote", back_populates="user")
    sleep_entries = relationship("SleepEntry", back_populates="user")

    def get_selected_subjects(self):
        """获取选择的科目列表"""
        if self.selected_subjects:
            return json.loads(self.selected_subjects)
        return []

    def set_selected_subjects(self, subjects):
        """设置选择的科目列表"""
        if subjects:
            self.selected_subjects = json.dumps(subjects)
        else:
            self.selected_subjects = None