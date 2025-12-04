from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class AIAnalysisResultOut(BaseModel):
    stress_index: float
    mood_radar: str
    explanation: str
    intervention_suggestion: Optional[str] = None

class AIChatMessage(BaseModel):
    role: str
    content: str

class AIChatRequest(BaseModel):
    messages: List[AIChatMessage]

class AIChatResponse(BaseModel):
    response: str
    conversation_id: Optional[str] = None

