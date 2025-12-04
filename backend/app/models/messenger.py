from datetime import datetime
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field

class MessengerEntry(BaseModel):
    id: Optional[str] = Field(alias="_id")
    user_id: str
    message_type: str # e.g., text, image, audio
    content: str # text content, or URL/base64 for image/audio
    sender: str # user or ai
    ai_analysis: Optional[Dict[str, Any]] = None # e.g., emotional analysis of user message
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

