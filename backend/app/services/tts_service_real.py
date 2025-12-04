import os
import logging
import tempfile
import io
from typing import Optional
from gtts import gTTS

logger = logging.getLogger(__name__)

class TTSService:
    def __init__(self):
        try:
            self.api_key = os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                logger.warning("OPENAI_API_KEY environment variable is missing, using offline TTS")
            logger.info("Real TTS Service initialized successfully")
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
            
            if not text.strip():
                raise ValueError("Text cannot be empty")
            
            # 使用 gTTS (Google Text-to-Speech) 进行真实的文本转语音
            tts = gTTS(
                text=text,
                lang='zh',  # 中文
                slow=False  # 正常语速
            )
            
            # 使用内存缓冲区而不是临时文件
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            audio_data = audio_buffer.read()
            audio_buffer.close()
            
            logger.info("Generated real TTS audio with %d bytes for text: %s", len(audio_data), text[:30])
            return audio_data
                
        except Exception as e:
            logger.error("TTS error: %s", str(e))
            # 如果gTTS失败，返回到本地TTS方案
            return await self._fallback_local_tts(text)
    
    async def _fallback_local_tts(self, text: str) -> bytes:
        """备用的本地TTS方案"""
        try:
            import pyttsx3
            
            logger.info("Using fallback local TTS for text: %s", text[:30])
            
            # 初始化pyttsx3引擎
            engine = pyttsx3.init()
            
            # 设置语音属性
            voices = engine.getProperty('voices')
            
            # 尝试选择中文女性声音
            for voice in voices:
                if 'chinese' in voice.name.lower() or 'mandarin' in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
                elif 'female' in voice.name.lower() or 'woman' in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
            
            # 设置语速和音量
            engine.setProperty('rate', 150)  # 语速
            engine.setProperty('volume', 0.9)  # 音量
            
            # 使用独特的临时文件名避免冲突
            import uuid
            temp_filename = f"tts_{uuid.uuid4().hex}.wav"
            temp_path = os.path.join(tempfile.gettempdir(), temp_filename)
            
            try:
                engine.save_to_file(text, temp_path)
                engine.runAndWait()
                
                # 等待文件写入完成
                import time
                time.sleep(0.5)
                
                # 读取文件内容
                if os.path.exists(temp_path):
                    with open(temp_path, 'rb') as audio_file:
                        audio_data = audio_file.read()
                    
                    # 尝试删除临时文件
                    try:
                        os.unlink(temp_path)
                    except:
                        pass  # 忽略删除错误
                    
                    logger.info("Generated fallback TTS audio with %d bytes", len(audio_data))
                    return audio_data
                else:
                    raise FileNotFoundError("TTS output file not created")
            
            finally:
                # 确保引擎被正确关闭
                try:
                    engine.stop()
                except:
                    pass
            
        except Exception as e:
            logger.error("Fallback TTS also failed: %s", str(e))
            # 最后的备用方案：生成提示音
            return self._generate_error_tone()
    
    def _generate_error_tone(self) -> bytes:
        """生成错误提示音"""
        import struct
        import io
        import math
        
        logger.warning("Generating error tone as final fallback")
        
        sample_rate = 22050
        duration = 0.5  # 0.5秒
        samples = int(sample_rate * duration)
        
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
        
        # 生成双音调提示（表示TTS错误）
        for i in range(samples):
            t = i / sample_rate
            if i < samples // 2:
                freq = 800  # 高音调
            else:
                freq = 400  # 低音调
            
            amplitude = 8000 * (1 - t / duration)  # 渐弱
            sample_value = int(amplitude * math.sin(2 * math.pi * freq * t))
            wav_buffer.write(struct.pack('<h', sample_value))
        
        return wav_buffer.getvalue()
    
    async def get_available_voices(self) -> list:
        """
        获取可用的声音列表
        """
        return [
            {"name": "Google-Chinese", "gender": "female", "description": "Google中文女性声音"},
            {"name": "Local-TTS", "gender": "female", "description": "本地TTS引擎"},
            {"name": "Fallback", "gender": "neutral", "description": "备用提示音"}
        ]

# 全局TTS服务实例
tts_service = TTSService()