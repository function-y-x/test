from openai import OpenAI
from app.core.config import settings
from app.schemas.ai import AIAnalysisResultOut, AIChatMessage
from app.db.database import get_database
from app.models.ai import AIConversation
from typing import List

# 创建OpenAI客户端
client = None
if settings.OPENAI_API_KEY:
    client = OpenAI(
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL
    )
    print("OpenAI客户端初始化成功，使用阿里云DashScope API")
else:
    print("Warning: OpenAI API key is not set. AI functionalities will be mocked.")

async def analyze_mood_with_ai(text: str) -> AIAnalysisResultOut:
    if not settings.OPENAI_API_KEY or not client:
        print("OpenAI API key not set. Returning mock AI analysis.")
        return AIAnalysisResultOut(
            stress_index=0.5,
            mood_radar="情绪平稳，略有波动",
            explanation="根据您的描述，情绪处于中等水平，建议保持观察。",
            intervention_suggestion="可以尝试进行一次冥想。"
        )
    try:
        response = client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {"role": "system", "content": "你是一个心理健康助手，擅长分析用户情绪并提供建议。"},
                {"role": "user", "content": f"请分析以下文本的情绪，并给出压力指数（0-1之间）、情绪雷达描述、解释和干预建议：\n\n{text}"
                }
            ],
            temperature=0.7,
            max_tokens=200
        )
        ai_response_content = response.choices[0].message.content

        # Attempt to parse the AI response into the desired format
        # This is a simplified parsing, a more robust solution might use regex or more structured prompts
        stress_index = 0.5
        mood_radar = "情绪分析结果"
        explanation = ai_response_content
        intervention_suggestion = ""

        # Example of simple parsing (can be improved)
        if "压力指数:" in ai_response_content:
            try:
                stress_index = float(ai_response_content.split("压力指数:")[1].split("\n")[0].strip())
            except ValueError:
                pass
        if "情绪雷达:" in ai_response_content:
            mood_radar = ai_response_content.split("情绪雷达:")[1].split("\n")[0].strip()
        if "解释:" in ai_response_content:
            explanation = ai_response_content.split("解释:")[1].split("\n")[0].strip()
        if "干预建议:" in ai_response_content:
            intervention_suggestion = ai_response_content.split("干预建议:")[1].split("\n")[0].strip()

        return AIAnalysisResultOut(
            stress_index=stress_index,
            mood_radar=mood_radar,
            explanation=explanation,
            intervention_suggestion=intervention_suggestion
        )
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return AIAnalysisResultOut(
            stress_index=0.5,
            mood_radar="情绪分析暂时不可用",
            explanation="AI服务暂时不可用，请稍后再试。",
            intervention_suggestion="建议进行深呼吸练习。"
        )

async def generate_emergency_guidance(emotion_state: str, intensity: float) -> dict:
    """生成90秒情绪急救指导"""
    if not settings.OPENAI_API_KEY or not client:
        return {
            "voice_script": "请深呼吸，吸气4秒，保持4秒，呼气6秒。重复这个过程，让自己平静下来。",
            "visual_prompt": "一片宁静的森林，阳光透过树叶洒下斑驳的光影",
            "music_type": "nature_sounds",
            "duration": 90
        }
    
    try:
        print(f"🔥 [DEBUG] 开始调用AI生成急救指导...")
        print(f"🔥 [DEBUG] 情绪状态: {emotion_state}, 强度: {intensity}")
        print(f"🔥 [DEBUG] 使用模型: qwen-plus")
        print(f"🔥 [DEBUG] API Base URL: {settings.OPENAI_BASE_URL}")
        print(f"🔥 [DEBUG] API Key前4位: {settings.OPENAI_API_KEY[:4]}****")
        
        # 使用结构化prompt要求AI返回JSON格式
        response = client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {
                    "role": "system", 
                    "content": "你是专业的心理危机干预师。请严格按照JSON格式回复，包含voice_script(语音引导词)、visual_prompt(视觉场景描述)、music_type(音乐类型)三个字段。音乐类型只能从nature_sounds、relaxing_piano、meditation_bell中选择。"
                },
                {
                    "role": "user", 
                    "content": f"为{emotion_state}情绪(强度{intensity}/10)设计90秒急救方案。请回复JSON格式：{{\"voice_script\": \"温和具体的呼吸和放松引导词\", \"visual_prompt\": \"平静自然场景描述\", \"music_type\": \"适合的音乐类型\"}}"
                }
            ],
            temperature=0.7,
            max_tokens=400,
            timeout=30  # 设置30秒超时
        )
        
        print(f"🎉 [DEBUG] AI调用成功! 响应状态: {response}")
        print(f"🎉 [DEBUG] 响应内容长度: {len(response.choices[0].message.content)}")
        print(f"🎉 [DEBUG] 响应原文: {response.choices[0].message.content}")
        
        # 计算token使用量
        if hasattr(response, 'usage'):
            print(f"🎉 [DEBUG] Token使用量: {response.usage}")
        
        # 计算请求耗时
        import time
        start_time = time.time()
        print(f"🎉 [DEBUG] 处理响应开始时间: {start_time}")
        
        content = response.choices[0].message.content.strip()
        print(f"🔍 [DEBUG] AI回复原文: {content}")  # 调试日志
        print(f"🔍 [DEBUG] 开始解析JSON响应...")
        
        # 尝试解析JSON响应
        import json
        import re
        
        try:
            # 如果响应包含markdown代码块，提取JSON部分
            json_match = re.search(r'```(?:json)?\s*({[^}]*})\s*```', content, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                print(f"🔍 [DEBUG] 从markdown代码块提取JSON: {json_str}")
            else:
                # 查找第一个完整的JSON对象
                json_match = re.search(r'{[^{}]*"voice_script"[^{}]*}', content, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                    print(f"🔍 [DEBUG] 使用正则提取JSON: {json_str}")
                else:
                    json_str = content
                    print(f"🔍 [DEBUG] 直接使用完整内容作为JSON: {json_str}")
            
            ai_data = json.loads(json_str)
            print(f"✅ [DEBUG] JSON解析成功: {ai_data}")
            
            # 验证和规范化数据
            voice_script = ai_data.get("voice_script", "请深呼吸，让身心放松。专注于当下，感受每一次呼吸带来的平静。")
            visual_prompt = ai_data.get("visual_prompt", "一片宁静的海滩，海浪轻柔地拍打着岸边")
            music_type = ai_data.get("music_type", "relaxing_piano")
            
            print(f"✅ [DEBUG] 提取字段 - 语音脚本长度: {len(voice_script)}")
            print(f"✅ [DEBUG] 提取字段 - 视觉提示长度: {len(visual_prompt)}")
            print(f"✅ [DEBUG] 提取字段 - 音乐类型: {music_type}")
            
            # 确保音乐类型在允许范围内
            valid_music_types = ["nature_sounds", "relaxing_piano", "meditation_bell"]
            if music_type not in valid_music_types:
                print(f"⚠️  [DEBUG] 音乐类型不在范围内，使用默认: {music_type} -> nature_sounds")
                music_type = "nature_sounds"
            
            result = {
                "voice_script": voice_script,
                "visual_prompt": visual_prompt,
                "music_type": music_type,
                "duration": 90
            }
            
            print(f"🎉 [DEBUG] 最终返回结果: {result}")
            return result
            
        except (json.JSONDecodeError, KeyError) as e:
            print(f"❌ [DEBUG] JSON解析失败: {e}，尝试文本解析")
            print(f"❌ [DEBUG] 失败的JSON字符串: {json_str}")
            
            # 备选：文本解析
            lines = content.split('\n')
            voice_script = "请深呼吸，让身心放松。专注于当下这一刻，感受每一次呼吸带来的平静。"
            visual_prompt = "一片宁静的森林，阳光透过树叶洒下温暖的光芒"
            music_type = "nature_sounds"
            
            print(f"🔄 [DEBUG] 开始文本解析，共{len(lines)}行")
            
            for i, line in enumerate(lines):
                line = line.strip()
                print(f"🔄 [DEBUG] 解析第{i+1}行: {line}")
                if "语音" in line or "voice" in line.lower():
                    if ":" in line:
                        voice_script = line.split(":", 1)[1].strip().strip('"').strip("'")
                        print(f"✅ [DEBUG] 找到语音脚本: {voice_script}")
                elif "视觉" in line or "visual" in line.lower():
                    if ":" in line:
                        visual_prompt = line.split(":", 1)[1].strip().strip('"').strip("'")
                        print(f"✅ [DEBUG] 找到视觉提示: {visual_prompt}")
                elif "音乐" in line or "music" in line.lower():
                    if ":" in line:
                        music_candidate = line.split(":", 1)[1].strip().strip('"').strip("'")
                        if music_candidate in ["nature_sounds", "relaxing_piano", "meditation_bell"]:
                            music_type = music_candidate
                            print(f"✅ [DEBUG] 找到音乐类型: {music_type}")
            
            result = {
                "voice_script": voice_script,
                "visual_prompt": visual_prompt,
                "music_type": music_type,
                "duration": 90
            }
            
            print(f"🔄 [DEBUG] 文本解析结果: {result}")
            return result
        
    except Exception as e:
        print(f"💥 [DEBUG] AI调用发生异常: {type(e).__name__}: {str(e)}")
        print(f"💥 [DEBUG] 异常详情: {repr(e)}")
        
        # 检查是否是超时错误
        if "timeout" in str(e).lower() or "timed out" in str(e).lower():
            print(f"⏰ [DEBUG] 确认为超时错误，可能原因:")
            print(f"   1. 网络连接问题")
            print(f"   2. API服务器响应慢")
            print(f"   3. 请求参数过大")
            print(f"   4. API配置问题")
        
        # 检查是否是认证错误
        if "auth" in str(e).lower() or "401" in str(e) or "403" in str(e):
            print(f"🔐 [DEBUG] 可能的认证问题:")
            print(f"   API Key: {settings.OPENAI_API_KEY[:10]}...")
            print(f"   Base URL: {settings.OPENAI_BASE_URL}")
        
        print(f"Error generating emergency guidance: {e}")
        return {
            "voice_script": "请深呼吸，吸气4秒，保持4秒，呼气6秒。重复这个过程，让自己平静下来。",
            "visual_prompt": "一片宁静的森林，阳光透过树叶洒下斑驳的光影",
            "music_type": "nature_sounds",
            "duration": 90
        }

async def generate_scenario_simulation(scenario_type: str, user_concerns: str) -> dict:
    """生成场景模拟指导"""
    if not settings.OPENAI_API_KEY or not client:
        scenarios = {
            "exam": {
                "preparation_steps": ["深呼吸3次", "回顾知识要点", "积极心理暗示"],
                "mindset_guidance": "你已经充分准备，相信自己的能力",
                "visualization_script": "想象自己在考场上冷静答题的场景",
                "duration": 300
            },
            "interview": {
                "preparation_steps": ["整理着装", "练习自我介绍", "模拟问答"],
                "mindset_guidance": "展现真实的自己，面试官也希望找到合适的人",
                "visualization_script": "想象自己自信地与面试官交流",
                "duration": 300
            },
            "study": {
                "preparation_steps": ["清理桌面", "设定学习目标", "准备学习材料"],
                "mindset_guidance": "每一分钟的努力都在为梦想添砖加瓦",
                "visualization_script": "想象自己专注学习，逐步掌握知识的满足感",
                "duration": 180
            }
        }
        return scenarios.get(scenario_type, scenarios["study"])
    
    try:
        print(f"🎭 [DEBUG] 开始调用AI生成场景模拟...")
        print(f"🎭 [DEBUG] 场景类型: {scenario_type}, 用户担忧: {user_concerns}")
        print(f"🎭 [DEBUG] 使用模型: qwen-plus")
        
        response = client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {"role": "system", "content": "你是专业的心理教练，擅长帮助学生快速进入最佳状态。请提供具体的准备步骤、心态调整和可视化引导。"},
                {"role": "user", "content": f"场景类型：{scenario_type}，用户担忧：{user_concerns}。请设计进入状态的方案，包含：1)具体准备步骤 2)心态调整指导 3)可视化引导脚本"}
            ],
            temperature=0.7,
            max_tokens=400,
            timeout=30
        )
        
        print(f"🎉 [DEBUG] 场景模拟AI调用成功!")
        print(f"🎉 [DEBUG] 响应内容: {response.choices[0].message.content}")
        
        content = response.choices[0].message.content
        
        # 简单解析响应内容
        preparation_steps = []
        mindset_guidance = content
        visualization_script = "想象成功完成任务的场景"
        
        # 尝试从响应中提取结构化信息
        lines = content.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if '准备' in line or '步骤' in line:
                current_section = 'preparation'
            elif '心态' in line or '指导' in line:
                current_section = 'mindset'
            elif '可视化' in line or '想象' in line:
                current_section = 'visualization'
            elif line and current_section == 'preparation' and ('1.' in line or '2.' in line or '3.' in line or '-' in line):
                # 提取准备步骤
                step = line.replace('1.', '').replace('2.', '').replace('3.', '').replace('-', '').strip()
                if step:
                    preparation_steps.append(step)
        
        if not preparation_steps:
            preparation_steps = ["准备第一步", "准备第二步", "准备第三步"]
        
        result = {
            "preparation_steps": preparation_steps[:3],  # 最多3个步骤
            "mindset_guidance": mindset_guidance,
            "visualization_script": visualization_script,
            "duration": 300
        }
        
        print(f"🎭 [DEBUG] 场景模拟最终结果: {result}")
        return result
        
    except Exception as e:
        print(f"💥 [DEBUG] 场景模拟AI调用异常: {type(e).__name__}: {str(e)}")
        print(f"💥 [DEBUG] 异常详情: {repr(e)}")
        
        # 检查错误类型
        if "timeout" in str(e).lower():
            print(f"⏰ [DEBUG] 场景模拟超时错误")
        
        print(f"Error generating scenario simulation: {e}")
        return {
            "preparation_steps": ["深呼吸调整", "明确目标", "积极暗示"],
            "mindset_guidance": "相信自己的能力，一步步来",
            "visualization_script": "想象自己成功完成目标的场景",
            "duration": 300
        }

async def get_ai_chat_response(messages: List[AIChatMessage], user_id: str) -> str:
    if not settings.OPENAI_API_KEY or not client:
        print("OpenAI API key not set. Returning mock AI chat response.")
        return "抱歉，AI服务暂时不可用，请设置OpenAI API密钥。"

    db = get_database()
    # Load previous conversation history for context
    conversation_history = []
    # In a real app, you might limit the history or summarize it
    async for conv_msg in db["ai_conversations"].find({"user_id": user_id}).sort("created_at", -1).limit(5):
        conversation_history.extend(conv_msg["messages"])

    full_messages = [
        {"role": "system", "content": "你是一个考研心理健康助手，专注于提供情感支持和学习建议。"}
    ]
    # Add historical messages, ensuring they are in the correct format
    for msg in conversation_history:
        full_messages.append({"role": msg["role"], "content": msg["content"]})
    # Add current messages
    for msg in messages:
        full_messages.append({"role": msg.role, "content": msg.content})

    try:
        response = client.chat.completions.create(
            model="qwen-plus",
            messages=full_messages,
            temperature=0.7,
            max_tokens=500
        )
        ai_response_content = response.choices[0].message.content

        # Save current interaction to conversation history
        new_conversation = AIConversation(
            user_id=user_id,
            messages=[msg.dict() for msg in messages] + [{
                "role": "assistant",
                "content": ai_response_content
            }]
        )
        await db["ai_conversations"].insert_one(new_conversation.dict(by_alias=True, exclude_unset=True))

        return ai_response_content
    except Exception as e:
        print(f"Error calling OpenAI API for chat: {e}")
        return "抱歉，AI服务暂时不可用，请稍后再试。"

