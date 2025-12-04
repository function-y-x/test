from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from app.models.user import UserInDB
from app.schemas.ai import AIAnalysisResultOut, AIChatRequest, AIChatResponse
from app.services.auth import get_current_active_user
from app.services.ai import analyze_mood_with_ai, get_ai_chat_response

router = APIRouter()

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

