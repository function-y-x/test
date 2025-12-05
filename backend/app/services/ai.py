import os
import asyncio
import httpx
import random
from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Dict, Any

# 确保.env文件存在且正确加载
print(f"当前工作目录: {os.getcwd()}")
env_path = os.path.join(os.getcwd(), '.env')
print(f".env文件路径: {env_path}, 是否存在: {os.path.exists(env_path)}")

# 首先加载环境变量
load_dotenv(override=True)  # 使用override=True确保强制重新加载

# 打印环境变量加载状态
print("环境变量加载状态:")
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_api_base = os.getenv("OPENAI_API_BASE")
print(f"OPENAI_API_KEY是否存在: {'是' if openai_api_key else '否'}")
print(f"OPENAI_API_KEY长度: {len(openai_api_key) if openai_api_key else 0}")
print(f"OPENAI_API_BASE是否存在: {'是' if openai_api_base else '否'}")
print(f"OPENAI_API_BASE值: {openai_api_base or '未设置，将使用默认值'}")

# 然后再导入settings，确保环境变量已加载
from app.core.config import settings
from app.schemas.ai import AIAnalysisResultOut, AIChatMessage
from app.db.database import get_database
from app.models.ai import AIConversation

# 初始化客户端 - 完全复制test.py的初始化方式
client = None
try:
    # 直接从os获取环境变量，与test.py完全一致
    api_key = openai_api_key
    api_base = openai_api_base or "https://dashscope.aliyuncs.com/compatible-mode/v1"
    
    print(f"初始化客户端 - API Key前10位: {api_key[:10]}..." if api_key else "API Key未设置")
    print(f"使用的端点: {api_base}")
    
    # 创建自定义HTTP客户端，与test.py完全一致
    http_client = httpx.Client(timeout=120.0)  # 增加超时时间以避免网络问题
    client = OpenAI(
        api_key=api_key,
        base_url=api_base,
        http_client=http_client,
    )
    print("OpenAI客户端初始化成功")
except Exception as e:
    print(f"OpenAI客户端初始化失败: {e}")
    import traceback
    traceback.print_exc()
    client = None

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
        # 使用客户端实例调用API，适应SDK 1.3.5版本
        response = client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {"role": "system", "content": "你是一个心理健康助手，擅长分析用户情绪并提供建议。"},
                {"role": "user", "content": f"请分析以下文本的情绪，并给出压力指数（0-1之间）、情绪雷达描述、解释和干预建议：\n\n{text}"}
        
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
        # 使用客户端实例调用API，适应SDK 1.3.5版本
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

async def analyze_painting_with_qwen_vl(image_data_url: str, painting_mode: str, theme: str = None, local_analysis: Dict[str, Any] = None) -> Dict[str, Any]:
    """使用qwen-vl多模态大模型分析绘画内容 - 简化版分析，只获取画面内容描述"""

    print("调用函数: analyze_painting_with_qwen_vl")
    global client
    
    print(f"开始分析绘画 - 模式: {painting_mode}, 主题: {theme}")
    print(f"图像数据格式检查: {image_data_url[:50]}...")
    print(f"客户端状态: {'已初始化' if client else '未初始化'}")
    print(f"本地分析数据: {local_analysis}")
    
    # 再次检查并尝试重新初始化客户端（如果之前失败）
    if client is None:
        print("尝试重新初始化客户端...")
        try:
            api_key = os.getenv("OPENAI_API_KEY")
            api_base = os.getenv("OPENAI_API_BASE", "https://dashscope.aliyuncs.com/compatible-mode/v1")
            http_client = httpx.Client(timeout=120.0)  # 增加HTTP客户端超时时间到120秒
            client = OpenAI(
                api_key=api_key,
                base_url=api_base,
                http_client=http_client,
            )
            print("客户端重新初始化成功")
        except Exception as re_init_error:
            print(f"客户端重新初始化失败: {re_init_error}")
    
    # 如果客户端仍然未初始化，返回详细的错误信息
    if client is None:
        print("客户端仍然未初始化，返回模拟分析结果")
        error_result = {
            "content_description": "系统错误: AI客户端未初始化",
            "analysis_result": "",
            "is_real_analysis": False,
            "error_type": "CLIENT_NOT_INITIALIZED",
            "error_message": "无法初始化AI客户端，请检查环境变量配置和网络连接"
        }
        print(f"返回错误结果: {error_result}")
        return error_result

    print("客户端正常")
    
    try:
        # 根据不同绘画模式生成个性化提示词
        mode_specific_instructions = ""
        if painting_mode == "house_tree_person":
            mode_specific_instructions = "这是一幅房树人测试画作，请特别关注：房屋的结构、门窗状态（开放/封闭）、树木的类型和特征、人物的姿态和表情。房树人测试中，房屋通常代表自我意识，树木代表成长历程，人物代表自我形象。"
        elif painting_mode == "theme_painting":
            mode_specific_instructions = f"这是一幅以'{theme}'为主题的创作画作，请特别关注：用户如何诠释和表达这个主题、主题元素的呈现方式、情感与主题的关联。主题创作能反映用户的思维方式和对特定概念的理解。"
        else:  # free_drawing
            mode_specific_instructions = "这是一幅自由创作画作，请特别关注：用户选择表达的核心元素、自发的表达方式、没有约束下展现的潜意识内容。自由创作能真实反映用户当前的情绪状态和内心世界。"
        
        # 修改后的提示词，按照要求分析多维度内容并整合成一段描述
        prompt = f"""请对这幅画作进行专业分析，并将结果整合成一段完整的描述。

绘画模式: {painting_mode}
绘画主题: {theme if theme else '自由创作'}

{mode_specific_instructions}

请按照以下维度进行分析：
1. 符号与内容识别：详细识别画中内容及其特征
2. 色彩情感分析：分析冷色调/暖色调比例、主色饱和度与明度
3. 笔触动力学分析：分析线条的流畅性、力度、是否断续、涂改痕迹
4. 构图与空间分析：分析图像重心、空间利用情况
5. 结合你的专业知识，分析用户展现出什么心理状态，对于考研有什么针对性建议

请将以上五个维度的分析，每一个点形成一个自然段，首字缩进两格，使用自然流畅的语言，全文不超过250字。


"""

        print(f"准备调用API - 模型: qwen-vl-plus, 多维度分析提示词已准备")

        # 简化API调用参数
        response = client.chat.completions.create(
            model="qwen-vl-plus",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_data_url}}
                    ]
                }
            ],
            max_tokens=500,  # 减少token数量，只需描述画面内容
            temperature=0.3  # 降低温度使输出更确定
        )

        # 验证响应格式 - 添加更全面的安全检查
        ai_response_content = ""
        if response and hasattr(response, 'choices') and response.choices and len(response.choices) > 0 and hasattr(response.choices[0], 'message') and response.choices[0].message and hasattr(response.choices[0].message, 'content'):
            ai_response_content = response.choices[0].message.content or ""
            print(f"API调用成功，响应长度: {len(ai_response_content)} 字符")
        else:
            print("API响应格式异常，无法获取content")
            # 创建默认数据，避免后续处理出错
            ai_response_content = ""

        # 处理响应内容 - 使用API返回的内容作为整合后的多维度分析描述
        content_description = ai_response_content.strip() if ai_response_content else "未能进行完整分析"
        analysis_result = "多维度心理分析已完成"
        
        print(f"设置内容描述: {content_description[:100]}...")
        
        # 创建获取额外数据的提示词，确保简洁明了
        data_extraction_prompt = "请基于这幅画作，提取以下具体数据并严格按照指定格式返回：\n\n"
        data_extraction_prompt += "1. 情绪雷达数据：焦虑程度(1-10)、压力水平(1-10)、积极情绪(1-10)、创造力(1-10)、专注度(1-10)、情绪稳定性(1-10)\n"
        data_extraction_prompt += "2. 色彩情感分析：冷色调比例(%)、暖色调比例(%)、色彩多样性(丰富/适中/单调)、情绪倾向描述\n"
        data_extraction_prompt += "3. 笔触动力学：线条特征、力度水平、连贯性、情绪稳定性\n"
        data_extraction_prompt += "4. 构图空间：密度描述、空间利用率(%)、中心位置、元素排列方式\n\n"
        data_extraction_prompt += "请以JSON格式返回，不要添加任何其他文字！格式如下：\n"
        data_extraction_prompt += '{"mood_radar":{"焦虑程度":5,"压力水平":5,"积极情绪":5,"创造力":5,"专注度":5,"情绪稳定性":5},"color_analysis":{"emotion_tendency":"描述","cool_color_ratio":"50%","warm_color_ratio":"50%","color_diversity":"适中"},"brush_analysis":{"stroke_characteristics":"流畅稳定","pressure_level":"适中","stroke_consistency":"连贯","emotional_stability":"较高"},"composition_analysis":{"密度":"适中","空间利用率":"50%","中心位置":"居中","元素排列方式":"有序"}}'
        
        # 调用API获取数据
        data_response = None
        try:
            data_response = client.chat.completions.create(
                model="qwen-vl-plus",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": data_extraction_prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_data_url
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500,
                temperature=0.2  # 降低温度以确保一致性
            )
        except Exception as data_api_error:
            print(f"获取额外数据API调用异常: {data_api_error}")
        
        # 解析或使用默认数据
        mood_radar_data = {
            "焦虑程度": 5,
            "压力水平": 5,
            "积极情绪": 5,
            "创造力": 5,
            "专注度": 5,
            "情绪稳定性": 5
        }
        
        color_emotion_data = {
            "emotion_tendency": "情绪平衡",
            "cool_color_ratio": "50%",
            "warm_color_ratio": "50%",
            "color_diversity": "适中"
        }
        
        brush_dynamics_data = {
            "stroke_characteristics": "流畅稳定",
            "pressure_level": "适中",
            "stroke_consistency": "连贯",
            "emotional_stability": "较高"
        }
        
        composition_data = {
            "密度": "适中，心理状态平衡",
            "空间利用率": "50%",
            "中心位置": "居中",
            "元素排列方式": "有序"
        }
        
        # 尝试解析AI返回的JSON数据
        if data_response and hasattr(data_response, 'choices') and data_response.choices and len(data_response.choices) > 0 and hasattr(data_response.choices[0], 'message') and data_response.choices[0].message and hasattr(data_response.choices[0].message, 'content'):
            data_content = data_response.choices[0].message.content.strip()
            print(f"额外数据响应: {data_content[:100]}...")
            
            # 尝试提取JSON部分
            try:
                # 提取花括号之间的内容
                start_idx = data_content.find('{')
                end_idx = data_content.rfind('}')
                if start_idx != -1 and end_idx != -1:
                    json_str = data_content[start_idx:end_idx+1]
                    import json
                    ai_data = json.loads(json_str)
                    
                    # 更新数据
                    if 'mood_radar' in ai_data:
                        mood_radar_data = ai_data['mood_radar']
                    if 'color_analysis' in ai_data:
                        color_emotion_data = ai_data['color_analysis']
                    if 'brush_analysis' in ai_data:
                        brush_dynamics_data = ai_data['brush_analysis']
                    if 'composition_analysis' in ai_data:
                        composition_data = ai_data['composition_analysis']
            except Exception as json_error:
                print(f"JSON解析异常: {json_error}")
        
        print(f"最终情绪雷达数据: {mood_radar_data}")
        print(f"最终色彩分析数据: {color_emotion_data}")

        # 返回真实的API响应，并添加明确的标记
        return {
            "content_description": content_description,  # 这是个性化心理画像栏要显示的内容
            "analysis_result": analysis_result,
            "is_real_analysis": True,
            "error_type": None,
            "analysis_dimensions": ["色彩情感", "笔触动力学", "构图空间", "符号内容", "心理画像", "针对性建议"],
            "mood_radar_data": mood_radar_data,
            # 三个小模块的数据（模拟数据）
            "color_emotion_analysis": {
                "description": "色彩情感分析",
                "data": color_emotion_data
            },
            "brush_dynamics_analysis": {
                "description": "笔触动力学分析",
                "data": brush_dynamics_data
            },
            "composition_analysis": {
                "description": "构图与空间分析",
                "data": composition_data
            }
        }
    except Exception as e:
        print(f"API调用异常: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # 返回明确的错误信息，包含异常类型，同时提供默认的情绪雷达图数据
        error_result = {
            "content_description": "API调用失败",
            "analysis_result": "",
            "is_real_analysis": False,
            "error_type": type(e).__name__,
            "error_message": str(e),
            "mood_radar_data": {
                "焦虑程度": 5,
                "压力水平": 5,
                "积极情绪": 5,
                "创造力": 5,
                "专注度": 5,
                "情绪稳定性": 5
            },
            "color_emotion_analysis": {
                "description": "色彩情感分析",
                "data": {
                    "emotion_tendency": "温暖积极，充满活力",
                    "cool_color_ratio": "30%",
                    "warm_color_ratio": "70%",
                    "color_diversity": "适中"
                }
            },
            "brush_dynamics_analysis": {
                "description": "笔触动力学分析",
                "data": {
                    "stroke_characteristics": "流畅稳定",
                    "pressure_level": "适中",
                    "stroke_consistency": "连贯",
                    "emotional_stability": "较高"
                }
            },
            "composition_analysis": {
                "description": "构图与空间分析",
                "data": {
                    "密度": "低，思维开阔或情绪平静",
                    "空间利用率": "5%",
                    "中心位置": "居中",
                    "元素排列方式": "有序"
                }
            }
        }
        print(f"返回API错误结果: {error_result}")
        return error_result


async def generate_mindfulness_guidance(painting_analysis: Dict[str, Any]) -> Dict[str, Any]:
    """
    根据用户画作分析生成个性化正念绘画引导文本
    
    Args:
        painting_analysis: 包含用户画作分析结果的字典
        
    Returns:
        包含引导文本的字典
    """
    print("调用函数: generate_mindfulness_guidance")
    print(f"分析数据: {painting_analysis}")
    
    # 再次检查并尝试重新初始化客户端（如果之前失败）
    global client
    if client is None:
        print("尝试重新初始化客户端...")
        try:
            api_key = os.getenv("OPENAI_API_KEY")
            api_base = os.getenv("OPENAI_API_BASE", "https://dashscope.aliyuncs.com/compatible-mode/v1")
            http_client = httpx.Client(timeout=120.0)  # 增加HTTP客户端超时时间到120秒
            client = OpenAI(
                api_key=api_key,
                base_url=api_base,
                http_client=http_client,
            )
            print("客户端重新初始化成功")
        except Exception as re_init_error:
            print(f"客户端重新初始化失败: {re_init_error}")
    
    # 如果客户端仍然未初始化，返回模拟引导
    if client is None:
        print("客户端未初始化，返回模拟引导文本")
        return {
            "guidance_text": "现在，请闭上眼睛，想象一股平静的蓝色能量从笔尖流出，慢慢填满整个画布。感受你的呼吸，让每一次呼吸都成为画笔的一次移动。不要担心画得如何，只关注当下的感受和体验。让你的手自由地表达内心的情感，不需要思考太多，跟随直觉去创作。",
            "is_real_guidance": False,
            "guidance_type": "mindfulness"
        }
    
    try:
        # 获取分析结果中的关键信息
        mood_description = painting_analysis.get("content_description", "")
        mood_radar_data = painting_analysis.get("mood_radar_data", {})
        color_analysis = painting_analysis.get("color_emotion_analysis", {})
        brush_analysis = painting_analysis.get("brush_dynamics_analysis", {})
        composition_analysis = painting_analysis.get("composition_analysis", {})
        
        # 构建提示词
        prompt = f"""
        请基于以下用户画作分析结果，生成一段个性化的正念绘画引导文本。
        这段引导应该帮助用户在下一次绘画中获得更好的情绪体验和自我表达。
        
        用户画作分析结果：
        - 心理画像：{mood_description}
        - 情绪雷达数据：{mood_radar_data}
        - 色彩情感分析：{color_analysis.get('data', {})}
        - 笔触动力学分析：{brush_analysis.get('data', {})}
        - 构图与空间分析：{composition_analysis.get('data', {})}
        
        请创作一段约200字的引导文本，语言要温和、鼓励性强，包含冥想元素。
        引导应该包括：
        1. 简短的呼吸引导
        2. 意象可视化建议（如颜色、形状、能量等）
        3. 绘画动作的指导
        4. 心态调整的建议
        
        请直接返回引导文本，不要添加任何其他说明。
        """
        
        print(f"发送引导生成请求到AI模型")
        
        # 调用AI模型生成引导文本
        response = client.chat.completions.create(
            model="qwen-vl-plus",
            messages=[
                {"role": "system", "content": "你是一位专业的艺术心理治疗师，擅长通过引导性语言帮助用户进行正念绘画和情绪表达。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        # 解析响应
        guidance_text = response.choices[0].message.content.strip()
        print(f"生成的引导文本: {guidance_text}")
        
        return {
            "guidance_text": guidance_text,
            "is_real_guidance": True,
            "guidance_type": "mindfulness"
        }
        
    except Exception as e:
        print(f"生成引导文本异常: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # 返回默认引导文本
        default_guidance = "现在，请闭上眼睛，想象一股平静的蓝色能量从笔尖流出，慢慢填满整个画布。感受你的呼吸，让每一次呼吸都成为画笔的一次移动。不要担心画得如何，只关注当下的感受和体验。让你的手自由地表达内心的情感，不需要思考太多，跟随直觉去创作。"
        
        return {
            "guidance_text": default_guidance,
            "is_real_guidance": False,
            "guidance_type": "mindfulness",
            "error": str(e)
        }


async def generate_healing_story(analysis_result: Dict[str, Any], image_data_url: str = None) -> str:
    """
    根据用户画作分析结果生成疗愈小故事
    图片URL是可选的，主要基于分析数据生成
    
    Args:
        analysis_result: 画作的AI分析结果
        image_data_url: 可选，画作的base64数据URL
        
    Returns:
        疗愈小故事文本
    """
    print("调用函数: generate_healing_story")
    print(f"分析数据摘要: {analysis_result.get('content_description', '')[:100]}...")
    
    # 再次检查并尝试重新初始化客户端（如果之前失败）
    global client
    if client is None:
        print("尝试重新初始化客户端...")
        try:
            api_key = os.getenv("OPENAI_API_KEY")
            api_base = os.getenv("OPENAI_API_BASE", "https://dashscope.aliyuncs.com/compatible-mode/v1")
            http_client = httpx.Client(timeout=120.0)  # 增加HTTP客户端超时时间到120秒
            client = OpenAI(
                api_key=api_key,
                base_url=api_base,
                http_client=http_client,
            )
            print("客户端重新初始化成功")
        except Exception as re_init_error:
            print(f"客户端重新初始化失败: {re_init_error}")
    
    # 如果客户端未初始化，返回默认故事
    if client is None:
        print("客户端未初始化，返回默认疗愈故事")
        return "在一片绿意盎然的森林中，你发现了一面神奇的镜子。当你望向镜中，看到的不仅是自己，还有无数可能。每一片落叶都代表一个过去的烦恼，每一道阳光都预示着新的希望。深呼吸，感受大自然的治愈力量，你会发现，内心的平静一直都在那里，等待你去发现。"


async def generate_mind_mirror(image_data_url: str) -> Dict[str, Any]:
    """
    生成心灵镜像：根据用户的画作，生成一幅保持核心元素但色彩更明媚、构图更和谐的"积极版本"
    
    Args:
        image_data_url: 用户画作的base64数据URL
        
    Returns:
        包含积极版本画作描述和引导语的字典
    """
    
    print("调用函数: generate_mind_mirror")
    print(f"图像数据格式检查: {image_data_url[:50]}...")
    
    # 再次检查并尝试重新初始化客户端（如果之前失败）
    global client
    if client is None:
        print("尝试重新初始化客户端...")
        try:
            api_key = os.getenv("OPENAI_API_KEY")
            api_base = os.getenv("OPENAI_API_BASE", "https://dashscope.aliyuncs.com/compatible-mode/v1")
            http_client = httpx.Client(timeout=120.0)  # 增加HTTP客户端超时时间到120秒
            client = OpenAI(
                api_key=api_key,
                base_url=api_base,
                http_client=http_client,
            )
            print("客户端重新初始化成功")
        except Exception as re_init_error:
            print(f"客户端重新初始化失败: {re_init_error}")
    
    # 如果客户端仍然未初始化，返回模拟结果
    if client is None:
        print("客户端未初始化，返回模拟心灵镜像结果")
        return {
            "positive_image_description": "这是一幅充满希望的画面，阳光透过云层洒在大地上，色彩明亮温暖，构图和谐平衡。",
            "guidance_text": "看，如果给这里加一缕阳光，是不是感觉充满了希望？",
            "is_real_mirror": False,
            "error_type": "CLIENT_NOT_INITIALIZED"
        }
    
    try:
        # 构建提示词，让AI分析原图并给出积极版本的描述
        prompt = f"""
        请分析这幅画作，然后生成一幅保持核心元素但色彩更明媚、构图更和谐的"积极版本"描述。
        
        具体要求：
        1. 首先识别画作的核心元素和主题
        2. 然后描述一个积极版本的画面，特点包括：
           - 色彩更加明亮、温暖、积极
           - 构图更加平衡和谐
           - 保持原有的核心元素和主题
           - 加入一些积极的元素（如阳光、明亮的色彩等）
        3. 最后提供一句简短的引导语，格式类似："看，如果给这里加一缕阳光，是不是感觉充满了希望？"
        
        请以JSON格式返回，包含以下字段：
        - positive_image_description: 积极版本画面的详细描述
        - guidance_text: 一句简短的引导语
        """
        
        print(f"发送心灵镜像生成请求到AI模型")
        
        # 调用AI模型生成心灵镜像描述
        response = client.chat.completions.create(
            model="qwen-vl-plus",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_data_url}}
                    ]
                }
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        # 解析响应
        ai_response_content = response.choices[0].message.content.strip()
        print(f"AI响应: {ai_response_content}")
        
        # 尝试提取JSON部分
        try:
            # 提取花括号之间的内容
            start_idx = ai_response_content.find('{')
            end_idx = ai_response_content.rfind('}')
            if start_idx != -1 and end_idx != -1:
                json_str = ai_response_content[start_idx:end_idx+1]
                import json
                result_data = json.loads(json_str)
                
                # 确保返回的字典包含必要字段
                if 'positive_image_description' in result_data and 'guidance_text' in result_data:
                    return {
                        "positive_image_description": result_data['positive_image_description'],
                        "guidance_text": result_data['guidance_text'],
                        "is_real_mirror": True,
                        "error_type": None
                    }
                else:
                    # 如果JSON格式不完整，使用默认值
                    return {
                        "positive_image_description": "这是一幅充满阳光和希望的画面，色彩明亮温暖，构图和谐平衡。",
                        "guidance_text": "看，如果给这里加一缕阳光，是不是感觉充满了希望？",
                        "is_real_mirror": True,
                        "error_type": None
                    }
            else:
                # 如果没有找到有效的JSON，使用默认值
                return {
                    "positive_image_description": "这是一幅充满阳光和希望的画面，色彩明亮温暖，构图和谐平衡。",
                    "guidance_text": "看，如果给这里加一缕阳光，是不是感觉充满了希望？",
                    "is_real_mirror": True,
                    "error_type": None
                }
        except Exception as json_error:
            print(f"JSON解析异常: {json_error}")
            # JSON解析失败，返回默认值
            return {
                "positive_image_description": "这是一幅充满阳光和希望的画面，色彩明亮温暖，构图和谐平衡。",
                "guidance_text": "看，如果给这里加一缕阳光，是不是感觉充满了希望？",
                "is_real_mirror": True,
                "error_type": None
            }
            
    except Exception as e:
        print(f"生成心灵镜像异常: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # 返回默认结果
        return {
            "positive_image_description": "这是一幅充满阳光和希望的画面，色彩明亮温暖，构图和谐平衡。",
            "guidance_text": "看，如果给这里加一缕阳光，是不是感觉充满了希望？",
            "is_real_mirror": False,
            "error_type": type(e).__name__
        }
    
    try:
        # 获取分析结果中的关键信息
        mood_description = analysis_result.get("content_description", "")
        mood_radar_data = analysis_result.get("mood_radar_data", {})
        color_analysis = analysis_result.get("color_emotion_analysis", {})
        brush_analysis = analysis_result.get("brush_dynamics_analysis", {})
        composition_analysis = analysis_result.get("composition_analysis", {})
        
        # 构建提示词，主要基于分析数据
        prompt = f"""
        请基于用户画作的详细分析结果，创作一个简短的疗愈小故事。
        
        画作分析信息：
        - 心理画像：{mood_description}
        - 情绪雷达数据：{mood_radar_data}
        - 色彩情感分析：{color_analysis.get('data', {})}
        - 笔触动力学分析：{brush_analysis.get('data', {})}
        - 构图与空间分析：{composition_analysis.get('data', {})}
        
        创作要求：
        1. 故事长度控制在200字以内
        2. 包含积极的隐喻和象征
        3. 语言温暖、治愈、富有画面感
        4. 帮助用户换一个视角看待问题
        5. 故事要有明确的积极寓意和希望感
        6. 不要直接提及考研或学习压力，而是通过隐喻来表达
        
        请直接返回故事内容，不要添加任何其他说明。
        """
        
        print(f"发送疗愈故事生成请求到AI模型")
        
        # 构建消息数组
        messages = [
            {"role": "system", "content": "你是一位专业的艺术心理治疗师，擅长通过富有寓意的小故事帮助用户获得心理疗愈。"}
        ]
        
        # 根据是否有图片URL构建不同的消息内容
        if image_data_url:
            # 如果有图片，使用多模态消息
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_data_url}}
                ]
            })
        else:
            # 没有图片时，只使用文本提示
            messages.append({
                "role": "user",
                "content": prompt
            })
        
        # 调用AI模型生成疗愈故事
        response = client.chat.completions.create(
            model="qwen-vl-plus",
            messages=messages,
            temperature=0.7,
            max_tokens=300  # 限制token数，确保故事简短
        )
        
        # 解析响应
        story = response.choices[0].message.content.strip()
        print(f"生成的疗愈故事: {story}")
        
        # 确保故事不超过200字
        if len(story) > 200:
            story = story[:197] + "..."
        
        return story
        
    except Exception as e:
        print(f"生成疗愈故事异常: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # 返回默认疗愈故事
        return "在一片绿意盎然的森林中，你发现了一面神奇的镜子。当你望向镜中，看到的不仅是自己，还有无数可能。每一片落叶都代表一个过去的烦恼，每一道阳光都预示着新的希望。深呼吸，感受大自然的治愈力量，你会发现，内心的平静一直都在那里，等待你去发现。"

