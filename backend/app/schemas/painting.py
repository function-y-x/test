from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class PaintingCreate(BaseModel):
    image_data_url: str
    painting_time_seconds: int = 0

class PaintingOut(PaintingCreate):
    id: str
    user_id: str
    ai_analysis: Optional[Dict[str, Any]] = None
    created_at: datetime
    submitted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

