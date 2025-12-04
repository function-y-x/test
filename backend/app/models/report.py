from datetime import datetime
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field

class WeeklyReport(BaseModel):
    id: Optional[str] = Field(alias="_id")
    user_id: str
    start_date: datetime
    end_date: datetime
    mood_trend_data: List[Dict[str, Any]]
    efficiency_mood_scatter_data: List[Dict[str, Any]]
    insights: List[str]
    suggestions: List[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

