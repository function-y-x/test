from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class PaintingCreate(BaseModel):
    image_data_url: str

class PaintingOut(PaintingCreate):
    id: str
    user_id: str
    ai_analysis: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True

