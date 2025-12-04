from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field, ConfigDict

class PaintingEntry(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )
    
    id: Optional[str] = Field(alias="_id")
    user_id: str
    image_data_url: str # Base64 encoded image
    ai_analysis: Optional[Dict[str, Any]] = None # {stress_index: 0.5, mood_radar: "..."}
    created_at: datetime = Field(default_factory=datetime.utcnow)

