from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field

class PaintingEntry(BaseModel):
    id: Optional[str] = Field(alias="_id")
    user_id: str
    image_data_url: str # Base64 encoded image
    ai_analysis: Optional[Dict[str, Any]] = None # {stress_index: 0.5, mood_radar: "..."}
    created_at: datetime = Field(default_factory=datetime.utcnow)
    painting_time_seconds: int = 0  # 绘画时长（秒）
    submitted_at: Optional[datetime] = None  # 提交分析的时间

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

