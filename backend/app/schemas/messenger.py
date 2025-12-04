from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class MessengerCreate(BaseModel):
    message_type: str
    content: str
    sender: str

class MessengerOut(MessengerCreate):
    id: str
    user_id: str
    ai_analysis: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True

