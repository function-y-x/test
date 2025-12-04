import openai
from app.core.config import settings
from app.schemas.ai import AIAnalysisResultOut, AIChatMessage
from app.db.database import get_database
from app.models.ai import AIConversation
from typing import List

# Ensure OpenAI API key is set before use
if settings.OPENAI_API_KEY:
    openai.api_key = settings.OPENAI_API_KEY
else:
    print("Warning: OpenAI API key is not set. AI functionalities will be mocked.")

async def analyze_mood_with_ai(text: str) -> AIAnalysisResultOut:
    if not settings.OPENAI_API_KEY:
        print("OpenAI API key not set. Returning mock AI analysis.")
        return AIAnalysisResultOut(
            stress_index=0.5,
            mood_radar="情绪平稳，略有波动",
            explanation="根据您的描述，情绪处于中等水平，建议保持观察。",
            intervention_suggestion="可以尝试进行一次冥想。"
        )
    try:
        response = openai.chat.completions.create(
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
        print(f"Error calling OpenAI API for mood analysis: {e}")
        return AIAnalysisResultOut(
            stress_index=0.5,
            mood_radar="API调用失败，返回默认情绪分析",
            explanation="抱歉，AI服务暂时不可用，请稍后再试。",
            intervention_suggestion=""
        )

async def get_ai_chat_response(messages: List[AIChatMessage], user_id: str) -> str:
    if not settings.OPENAI_API_KEY:
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
        response = openai.chat.completions.create(
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

