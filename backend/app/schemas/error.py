from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class ErrorCreate(BaseModel):
    description: str
    image_url: Optional[str] = None

class ErrorUpdate(BaseModel):
    description: Optional[str] = None
    image_url: Optional[str] = None
    ai_analysis: Optional[Dict[str, Any]] = None

class ErrorOut(ErrorCreate):
    id: str
    user_id: str
    ai_analysis: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

