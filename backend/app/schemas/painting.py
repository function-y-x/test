from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class PaintingCreate(BaseModel):
    image_data_url: str

class PaintingOut(PaintingCreate):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    user_id: str
    ai_analysis: Optional[Dict[str, Any]] = None
    created_at: datetime

