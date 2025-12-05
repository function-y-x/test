from datetime import datetime
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field, ConfigDict

class AIAnalysisResult(BaseModel):
    stress_index: float
    mood_radar: str
    explanation: str
    intervention_suggestion: Optional[str] = None

class AIConversation(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )
    
    id: Optional[str] = Field(alias="_id")
    user_id: str
    messages: List[Dict[str, Any]] # [{'role': 'user', 'content': 'hello'}, {'role': 'ai', 'content': 'hi'}]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

