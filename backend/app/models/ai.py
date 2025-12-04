from datetime import datetime
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field

class AIAnalysisResult(BaseModel):
    stress_index: float
    mood_radar: str
    explanation: str
    intervention_suggestion: Optional[str] = None

class AIConversation(BaseModel):
    id: Optional[str] = Field(alias="_id")
    user_id: str
    messages: List[Dict[str, Any]] # [{'role': 'user', 'content': 'hello'}, {'role': 'ai', 'content': 'hi'}]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

