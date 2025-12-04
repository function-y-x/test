import os
import dashscope
import base64
import io
from typing import Generator, Optional
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

class TTSService:
    def __init__(self):
        try:
            # 使用新加坡区域的API
            dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'
            self.api_key = os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                logger.error("OPENAI_API_KEY environment variable is missing")
                raise ValueError("OPENAI_API_KEY environment variable is required")
            logger.info("TTS Service initialized successfully")
        except Exception as e:
            logger.error(f"TTS Service initialization failed: {e}")
            raise
    
    async def text_to_speech(
        self, 
        text: str, 
        voice: str = "Cherry", 
        language_type: str = "Chinese"
    ) -> bytes:
        """
        将文本转换为语音
        
        Args:
            text: 要转换的文本
            voice: 声音类型 (Cherry为女性声音)
            language_type: 语言类型
            
        Returns:
            音频数据的字节流
        """
        try:
            logger.info("Converting text to speech: %s...", text[:50])
            
            # 设置API密钥
            dashscope.api_key = self.api_key
            
            # 使用Dashscope的语音合成API
            from dashscope.audio.tts import SpeechSynthesizer
            
            result = SpeechSynthesizer.call(
                model='sambert-zhichu-v1',
                text=text,
                sample_rate=24000,
                format='wav'
            )
            
            if result.get_audio_data() is not None:
                audio_data = result.get_audio_data()
                logger.info("Generated audio with %d bytes", len(audio_data))
                return audio_data
            else:
                error_msg = f"TTS API failed: {result.get_response()}"
                logger.error(error_msg)
                raise HTTPException(status_code=500, detail=error_msg)
                
        except Exception as e:
            logger.error("TTS error: %s", str(e))
            raise HTTPException(status_code=500, detail=f"Text-to-speech conversion failed: {str(e)}") from e
    
    async def get_available_voices(self) -> list:
        """
        获取可用的声音列表
        """
        # Qwen-TTS支持的声音类型
        return [
            {"name": "Cherry", "gender": "female", "description": "温柔女性声音"},
            {"name": "Longying", "gender": "female", "description": "专业女性声音"},
            {"name": "Longwan", "gender": "male", "description": "温和男性声音"},
            {"name": "Longxiang", "gender": "male", "description": "专业男性声音"}
        ]

# 全局TTS服务实例
tts_service = TTSService()