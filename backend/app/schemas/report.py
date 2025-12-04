from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class ReportCreate(BaseModel):
    start_date: datetime
    end_date: datetime
    mood_trend_data: List[Dict[str, Any]]
    efficiency_mood_scatter_data: List[Dict[str, Any]]
    insights: List[str]
    suggestions: List[str]

class ReportOut(ReportCreate):
    id: str
    user_id: str
    created_at: datetime

    class Config:
        from_attributes = True

