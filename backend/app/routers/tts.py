from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from typing import Optional
import logging
from ..services.tts_service_real import tts_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tts", tags=["TTS"])

class TTSRequest(BaseModel):
    text: str
    voice: Optional[str] = "Cherry"
    language_type: Optional[str] = "Chinese"

@router.post("/convert")
async def text_to_speech(request: TTSRequest):
    """
    将文本转换为语音
    """
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        # 限制文本长度，避免请求过大
        if len(request.text) > 1000:
            raise HTTPException(status_code=400, detail="Text too long (max 1000 characters)")
        
        logger.info(f"TTS request: voice={request.voice}, text length={len(request.text)}")
        
        # 调用TTS服务
        audio_data = await tts_service.text_to_speech(
            text=request.text,
            voice=request.voice,
            language_type=request.language_type
        )
        
        # 返回音频数据
        return Response(
            content=audio_data,
            media_type="audio/mpeg",  # 支持MP3格式
            headers={
                "Content-Disposition": "attachment; filename=speech.mp3",
                "Content-Length": str(len(audio_data))
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"TTS conversion error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/voices")
async def get_voices():
    """
    获取可用的声音列表
    """
    try:
        voices = await tts_service.get_available_voices()
        return {"voices": voices}
    except Exception as e:
        logger.error(f"Error getting voices: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get voice list")