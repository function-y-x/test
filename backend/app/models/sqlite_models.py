from sqlalchemy import Column, String, Integer, DateTime, JSON, Text
from sqlalchemy.sql import func
from app.db.sqlite_database import Base

class PaintingEntryORM(Base):
    __tablename__ = "painting_entries"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    image_data_url = Column(Text, nullable=False)  # 使用Text存储长的base64字符串
    ai_analysis = Column(JSON, nullable=True)  # 存储AI分析结果的JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    painting_time_seconds = Column(Integer, default=0)
    submitted_at = Column(DateTime(timezone=True))