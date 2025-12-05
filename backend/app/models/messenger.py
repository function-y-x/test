from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel, Field

Base = declarative_base()

class MessengerEntry(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    message_type = Column(String)  # text, audio, image, mixed
    text_content = Column(Text, nullable=True)
    audio_path = Column(String, nullable=True)
    image_path = Column(String, nullable=True)
    sender = Column(String)  # user or ai
    emotion_report = Column(JSON, nullable=True)  # AI情绪分析报告
    risk_level = Column(String, nullable=True)  # green, yellow, red
    ai_reply_text = Column(Text, nullable=True)
    ai_reply_video_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class EmotionReport(BaseModel):
    stress_index: int = Field(ge=0, le=100, description="压力指数0-100")
    main_emotions: List[str] = Field(description="主要情绪，如焦虑、疲惫等")
    possible_causes: List[str] = Field(description="可能原因")
    explanation: str = Field(description="分析解释")
    risk_keywords: List[str] = Field(default=[], description="风险关键词")

class AIReply(BaseModel):
    empathy_text: str = Field(description="共情回复")
    cognitive_guidance: str = Field(description="认知行为引导")
    practical_tips: List[str] = Field(description="实用减压技巧")
    follow_up_tasks: List[str] = Field(description="跟进微任务")
    resource_links: List[str] = Field(default=[], description="资源链接")

