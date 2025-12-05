import os
import json
import base64
import asyncio
from typing import Dict, Any, List, Optional
from openai import AsyncOpenAI
from app.models.messenger import EmotionReport, AIReply
from app.core.config import settings

class MessengerAIService:
    def __init__(self):
        # 延迟初始化客户端，避免启动时错误
        self.client = None
        self.model_name = "qwen3-omni-flash"  # 使用指定的模型
        
    def _get_client(self):
        """延迟初始化 OpenAI 客户端"""
        if self.client is None:
            try:
                # 尝试使用最小参数集合初始化
                self.client = AsyncOpenAI(
                    api_key=os.getenv("OPENAI_API_KEY", "sk-ac5ae6e934f54368b1a0339a79ec24cf"),
                    base_url=os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
                )
            except Exception as e:
                # 如果还是失败，使用默认设置
                print(f"OpenAI 客户端初始化失败: {e}")
                print("使用默认API设置...")
                self.client = AsyncOpenAI(
                    api_key=os.getenv("OPENAI_API_KEY", "sk-ac5ae6e934f54368b1a0339a79ec24cf")
                )
        return self.client
        
    async def analyze_emotion(self, text_content: str, audio_features: Optional[Dict] = None, 
                            image_analysis: Optional[Dict] = None) -> EmotionReport:
        """多模态情绪分析"""
        try:
            # 构建分析提示
            analysis_prompt = self._build_emotion_analysis_prompt(text_content, audio_features, image_analysis)
            
            # 构建消息，支持多模态
            messages = [
                {"role": "system", "content": "你是一位专业的心理健康AI助手，专门帮助考研学生进行情绪分析。请基于用户输入进行专业的情绪评估。"},
                {"role": "user", "content": [{"type": "text", "text": analysis_prompt}]}
            ]
            
            # 如果有图像，添加图像信息
            if image_analysis and image_analysis.get("image_url"):
                messages[1]["content"].append({
                    "type": "image_url", 
                    "image_url": {"url": image_analysis["image_url"]}
                })
            
            # 如果 modalities 参数不支持，可以先注释掉进行测试
            response = await self._get_client().chat.completions.create(
                model=self.model_name,
                messages=messages,
                # modalities=["text", "audio"] if audio_features else ["text"],
                # audio={"voice": "Chelsie", "format": "wav"} if audio_features else None,
                temperature=0.7,
                max_tokens=1000,
                stream=True
                # stream_options={"include_usage": True}
            )
            
            # 解析流式响应
            analysis_text = ""
            async for chunk in response:
                if chunk.choices[0].delta.content:
                    analysis_text += chunk.choices[0].delta.content
            
            return self._parse_emotion_analysis(analysis_text, text_content)
            
        except Exception as e:
            print(f"情绪分析失败: {e}")
            return self._get_default_emotion_report()
    
    def _build_emotion_analysis_prompt(self, text: str, audio_features: Optional[Dict], 
                                     image_analysis: Optional[Dict]) -> str:
        """构建情绪分析提示"""
        prompt = f"""请分析以下考研学生的情绪状态：

文本内容：{text}
"""
        
        if audio_features:
            prompt += f"""
语音特征：
- 语速：{audio_features.get('speed', '正常')}
- 音调：{audio_features.get('pitch', '中等')}
- 音量：{audio_features.get('volume', '中等')}
"""
        
        if image_analysis:
            prompt += f"""
图像分析：{image_analysis.get('description', '无特殊内容')}
"""
        
        prompt += """
请从以下维度分析：
1. 压力指数（0-100分）
2. 主要情绪（如：焦虑、疲惫、兴奋、沮丧等）
3. 可能原因分析
4. 风险评估（绿色=正常，黄色=需关注，红色=高风险）
5. 简短解释

请以JSON格式回复，包含：stress_index, main_emotions, possible_causes, risk_level, explanation, risk_keywords
"""
        return prompt
    
    def _parse_emotion_analysis(self, analysis_text: str, original_text: str) -> EmotionReport:
        """解析AI情绪分析结果"""
        try:
            # 尝试提取JSON部分
            start = analysis_text.find('{')
            end = analysis_text.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = analysis_text[start:end]
                analysis_data = json.loads(json_str)
            else:
                # 如果无法解析JSON，使用默认分析
                analysis_data = self._analyze_text_keywords(original_text)
            
            return EmotionReport(
                stress_index=analysis_data.get('stress_index', 50),
                main_emotions=analysis_data.get('main_emotions', ['未知']),
                possible_causes=analysis_data.get('possible_causes', ['需要更多信息']),
                explanation=analysis_data.get('explanation', '基于文本内容的初步分析'),
                risk_keywords=analysis_data.get('risk_keywords', [])
            )
        except Exception as e:
            print(f"解析情绪分析失败: {e}")
            return self._get_default_emotion_report()
    
    def _analyze_text_keywords(self, text: str) -> Dict[str, Any]:
        """基于关键词的简单情绪分析"""
        stress_keywords = ['压力', '焦虑', '紧张', '失眠', '疲惫', '崩溃', '痛苦']
        positive_keywords = ['开心', '高兴', '兴奋', '满意', '进步', '成功']
        negative_keywords = ['沮丧', '失望', '难过', '痛苦', '绝望', '无助']
        risk_keywords = ['自杀', '死', '结束', '放弃一切', '没意思', '活着没意义']
        
        stress_score = sum(10 for word in stress_keywords if word in text)
        positive_score = sum(5 for word in positive_keywords if word in text)
        negative_score = sum(10 for word in negative_keywords if word in text)
        risk_score = sum(30 for word in risk_keywords if word in text)
        
        stress_index = min(100, max(0, 30 + stress_score + negative_score - positive_score))
        
        main_emotions = []
        if any(word in text for word in stress_keywords):
            main_emotions.append('压力')
        if any(word in text for word in negative_keywords):
            main_emotions.append('消极情绪')
        if any(word in text for word in positive_keywords):
            main_emotions.append('积极情绪')
        if not main_emotions:
            main_emotions = ['中性情绪']
        
        risk_level = 'red' if risk_score > 0 else ('yellow' if stress_index > 70 else 'green')
        found_risk_keywords = [word for word in risk_keywords if word in text]
        
        return {
            'stress_index': stress_index,
            'main_emotions': main_emotions,
            'possible_causes': ['学习压力', '考试焦虑'] if stress_score > 0 else ['情绪正常'],
            'risk_level': risk_level,
            'explanation': f'基于关键词分析，检测到压力指数为{stress_index}',
            'risk_keywords': found_risk_keywords
        }
    
    async def generate_ai_reply(self, emotion_report: EmotionReport, user_message: str) -> AIReply:
        """生成AI回复"""
        try:
            reply_prompt = f"""用户消息：{user_message}

情绪分析结果：
- 压力指数：{emotion_report.stress_index}
- 主要情绪：{', '.join(emotion_report.main_emotions)}
- 风险等级：{emotion_report.risk_level}

请作为一位温暖、专业的心理健康助手，为这位考研学生提供回复。回复应包含：
1. 共情表达（理解和认同用户感受）
2. 认知行为引导（帮助重新看待问题）
3. 实用建议（2-3个具体的减压或学习技巧）
4. 跟进任务（简单易行的小任务）

请以JSON格式回复，包含：empathy_text, cognitive_guidance, practical_tips, follow_up_tasks, resource_links
"""
            
            response = await self._get_client().chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "你是一位专业、温暖的心理健康AI助手，专门为考研学生提供情感支持和学习指导。"},
                    {"role": "user", "content": reply_prompt}
                ],
                # modalities=["text"],
                temperature=0.8,
                max_tokens=1500,
                stream=True
                # stream_options={"include_usage": True}
            )
            
            # 解析流式响应
            reply_text = ""
            async for chunk in response:
                if chunk.choices[0].delta.content:
                    reply_text += chunk.choices[0].delta.content
            return self._parse_ai_reply(reply_text, emotion_report)
            
        except Exception as e:
            print(f"生成AI回复失败: {e}")
            return self._get_default_ai_reply(emotion_report)
    
    def _parse_ai_reply(self, reply_text: str, emotion_report: EmotionReport) -> AIReply:
        """解析AI回复"""
        try:
            start = reply_text.find('{')
            end = reply_text.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = reply_text[start:end]
                reply_data = json.loads(json_str)
            else:
                # 如果无法解析JSON，使用默认回复
                reply_data = self._generate_default_reply_data(emotion_report)
            
            return AIReply(
                empathy_text=reply_data.get('empathy_text', '我理解你现在的感受。'),
                cognitive_guidance=reply_data.get('cognitive_guidance', '让我们换个角度来看待这个问题。'),
                practical_tips=reply_data.get('practical_tips', ['深呼吸练习', '适当休息']),
                follow_up_tasks=reply_data.get('follow_up_tasks', ['今天给自己10分钟放松时间']),
                resource_links=reply_data.get('resource_links', [])
            )
        except Exception as e:
            print(f"解析AI回复失败: {e}")
            return self._get_default_ai_reply(emotion_report)
    
    def _generate_default_reply_data(self, emotion_report: EmotionReport) -> Dict[str, Any]:
        """生成默认回复数据"""
        if emotion_report.stress_index > 70:
            return {
                'empathy_text': '我能感受到你现在承受着很大的压力，这种感觉真的很不容易。',
                'cognitive_guidance': '高压状态下的焦虑是正常的反应，但我们可以通过一些方法来缓解它。',
                'practical_tips': ['进行5分钟深呼吸', '听一首放松的音乐', '做简单的伸展运动'],
                'follow_up_tasks': ['今晚早睡30分钟', '明天安排一个小奖励给自己'],
                'resource_links': []
            }
        else:
            return {
                'empathy_text': '感谢你与我分享你的想法，我很高兴能陪伴你。',
                'cognitive_guidance': '保持现在的状态很棒，继续前进的同时也要关注自己的感受。',
                'practical_tips': ['保持规律作息', '适度运动', '与朋友交流'],
                'follow_up_tasks': ['制定明天的小目标', '记录一件开心的事'],
                'resource_links': []
            }
    
    def _get_default_emotion_report(self) -> EmotionReport:
        """获取默认情绪报告"""
        return EmotionReport(
            stress_index=50,
            main_emotions=['需要更多信息'],
            possible_causes=['暂时无法分析'],
            explanation='暂时无法进行详细分析，请提供更多信息',
            risk_keywords=[]
        )
    
    def _get_default_ai_reply(self, emotion_report: EmotionReport) -> AIReply:
        """获取默认AI回复"""
        return AIReply(
            empathy_text='谢谢你与我分享，我会认真倾听你的每一句话。',
            cognitive_guidance='每个人在学习路上都会遇到挑战，重要的是我们如何面对它们。',
            practical_tips=['保持规律作息', '适当休息', '与他人交流'],
            follow_up_tasks=['今天给自己一个微笑'],
            resource_links=[]
        )
    
    async def generate_video_reply(self, ai_reply: AIReply) -> Optional[str]:
        """生成视频回复（暂时返回文本，实际应用中可集成SadTalker）"""
        # 这里应该集成SadTalker生成视频
        # 现在暂时返回文本内容
        full_reply = f"{ai_reply.empathy_text}\n\n{ai_reply.cognitive_guidance}\n\n实用建议：\n"
        for tip in ai_reply.practical_tips:
            full_reply += f"• {tip}\n"
        
        if ai_reply.follow_up_tasks:
            full_reply += f"\n跟进任务：\n"
            for task in ai_reply.follow_up_tasks:
                full_reply += f"• {task}\n"
        
        return full_reply

# 全局AI服务实例
messenger_ai_service = MessengerAIService()