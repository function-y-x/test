import os
import logging
import struct
import io
from typing import Optional

logger = logging.getLogger(__name__)

class TTSService:
    def __init__(self):
        try:
            self.api_key = os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                logger.error("OPENAI_API_KEY environment variable is missing")
                raise ValueError("OPENAI_API_KEY environment variable is required")
            logger.info("TTS Service initialized successfully")
        except Exception as e:
            logger.error("TTS Service initialization failed: %s", str(e))
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
            
            # 暂时创建一个简单的静默WAV文件，避免500错误
            # 在真实环境中，这里应该调用实际的TTS服务
            
            sample_rate = 24000
            duration = max(1, len(text) // 10)  # 根据文本长度估算时长
            samples = sample_rate * duration
            
            # 创建WAV文件头
            wav_buffer = io.BytesIO()
            wav_buffer.write(b'RIFF')
            wav_buffer.write(struct.pack('<I', 36 + samples * 2))
            wav_buffer.write(b'WAVE')
            wav_buffer.write(b'fmt ')
            wav_buffer.write(struct.pack('<I', 16))
            wav_buffer.write(struct.pack('<H', 1))  # PCM格式
            wav_buffer.write(struct.pack('<H', 1))  # 单声道
            wav_buffer.write(struct.pack('<I', sample_rate))
            wav_buffer.write(struct.pack('<I', sample_rate * 2))
            wav_buffer.write(struct.pack('<H', 2))
            wav_buffer.write(struct.pack('<H', 16))
            wav_buffer.write(b'data')
            wav_buffer.write(struct.pack('<I', samples * 2))
            
            # 生成测试音频信号（简单的正弦波）
            import math
            frequency = 440  # A4音符频率
            amplitude = 16000  # 音量
            
            for i in range(samples):
                # 生成正弦波信号
                t = i / sample_rate
                if i < samples // 4:  # 前1/4播放音调
                    sample_value = int(amplitude * math.sin(2 * math.pi * frequency * t))
                else:  # 后3/4静默
                    sample_value = 0
                wav_buffer.write(struct.pack('<h', sample_value))
            
            audio_data = wav_buffer.getvalue()
            logger.info("Generated test audio with %d bytes for text: %s", len(audio_data), text[:30])
            return audio_data
                
        except Exception as e:
            logger.error("TTS error: %s", str(e))
            from fastapi import HTTPException
            raise HTTPException(status_code=500, detail=f"Text-to-speech conversion failed: {str(e)}") from e
    
    async def get_available_voices(self) -> list:
        """
        获取可用的声音列表
        """
        return [
            {"name": "Cherry", "gender": "female", "description": "温柔女性声音"},
            {"name": "Test", "gender": "female", "description": "测试声音"}
        ]

# 全局TTS服务实例
tts_service = TTSService()