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

class EmergencyGuidanceRequest(BaseModel):
    emotion_type: str
    intensity: int
    context: Optional[str] = ""

class EmergencyGuidanceResponse(BaseModel):
    voice_guidance: str
    visualization: str
    music_suggestion: str
    steps: List[str]
    duration: int

class ScenarioSimulationRequest(BaseModel):
    scenario_type: str
    user_context: Optional[str] = ""

class ScenarioSimulationResponse(BaseModel):
    preparation_steps: List[str]
    mindset_guidance: str
    visualization_script: str
    confidence_boosters: List[str]
    practical_tips: List[str]

