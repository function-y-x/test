from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class MessengerCreate(BaseModel):
    message_type: str = Field(description="消息类型: text, audio, image, mixed")
    text_content: Optional[str] = None
    audio_data: Optional[str] = None  # base64 encoded audio
    image_data: Optional[str] = None  # base64 encoded image
    anonymous_mode: bool = False

class MessengerOut(BaseModel):
    id: int
    user_id: str
    message_type: str
    text_content: Optional[str] = None
    audio_path: Optional[str] = None
    image_path: Optional[str] = None
    sender: str
    emotion_report: Optional[Dict[str, Any]] = None
    risk_level: Optional[str] = None
    ai_reply_text: Optional[str] = None
    ai_reply_video_path: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class EmotionAnalysisResponse(BaseModel):
    message_id: int
    emotion_report: Dict[str, Any]
    risk_level: str
    ai_reply: Dict[str, Any]
    video_url: Optional[str] = None

class MessageHistoryResponse(BaseModel):
    messages: List[MessengerOut]
    total_count: int
    emotion_timeline: List[Dict[str, Any]]

