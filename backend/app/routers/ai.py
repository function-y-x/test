from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from app.models.user import UserInDB
from app.schemas.ai import AIAnalysisResultOut, AIChatRequest, AIChatResponse
from app.services.auth import get_current_active_user
from app.services.ai import analyze_mood_with_ai, get_ai_chat_response, generate_emergency_guidance, generate_scenario_simulation
from pydantic import BaseModel

router = APIRouter()

class EmergencyGuidanceRequest(BaseModel):
    emotion_state: str
    intensity: float

class ScenarioSimulationRequest(BaseModel):
    scenario_type: str  # "exam", "interview", "study"
    user_concerns: str

@router.post("/analyze-mood", response_model=AIAnalysisResultOut)
async def analyze_mood(
    text: str,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    # This is a placeholder. In a real app, you'd send text to OpenAI for analysis.
    # For now, a mock response.
    result = await analyze_mood_with_ai(text)
    return result

@router.post("/chat", response_model=AIChatResponse)
async def chat_with_ai(
    chat_request: AIChatRequest,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    response_text = await get_ai_chat_response(chat_request.messages, str(current_user.id))
    return AIChatResponse(response=response_text)

@router.post("/emergency-guidance")
async def create_emergency_guidance(
    request: EmergencyGuidanceRequest,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    """生成90秒情绪急救指导"""
    guidance = await generate_emergency_guidance(request.emotion_state, request.intensity)
    return guidance

@router.post("/scenario-simulation")
async def create_scenario_simulation(
    request: ScenarioSimulationRequest,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    """生成场景模拟指导"""
    simulation = await generate_scenario_simulation(request.scenario_type, request.user_concerns)
    return simulation

