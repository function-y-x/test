"""
压力分析服务
使用 DeepSeek AI 分析用户的压力来源并提供建议
"""

from typing import Dict, List, Optional, Any
from datetime import date, datetime
import httpx
from app.core.config import settings


async def analyze_stress_sources(
    ddl_score: float,
    sleep_hours: Optional[float],
    days_until_exam: int,
    recent_mood_stress: Optional[int]
) -> Dict[str, Any]:
    """
    分析压力来源
    
    参数:
        ddl_score: DDL 平均紧张分数 (0-100)
        sleep_hours: 昨日睡眠时长
        days_until_exam: 距离考研天数
        recent_mood_stress: 最近情绪压力等级 (1-10)
    
    返回:
        压力分析结果
    """
    # 1. 计算各个压力源的得分
    stress_sources = []
    
    # DDL 压力（权重：40%）
    if ddl_score > 0:
        ddl_stress_level = ddl_score  # 直接使用 DDL 分数
        stress_sources.append({
            'source': 'ddl',
            'name': 'DDL任务压力',
            'score': ddl_stress_level,
            'weight': 0.4
        })
    
    # 睡眠不足压力（权重：25%）
    if sleep_hours is not None:
        # 理想睡眠 7-8 小时
        if sleep_hours < 6:
            sleep_stress_level = (6 - sleep_hours) / 6 * 100  # 睡眠越少，压力越大
        elif sleep_hours > 9:
            sleep_stress_level = (sleep_hours - 9) / 3 * 50  # 睡太多也有问题
        else:
            sleep_stress_level = 0
        
        stress_sources.append({
            'source': 'sleep',
            'name': '睡眠质量压力',
            'score': min(100, sleep_stress_level),
            'weight': 0.25
        })
    
    # 考研倒计时焦虑（权重：20%）
    if days_until_exam <= 365:  # 一年内
        if days_until_exam <= 30:
            exam_anxiety = 90  # 最后一个月，焦虑很高
        elif days_until_exam <= 90:
            exam_anxiety = 70  # 最后三个月，焦虑较高
        elif days_until_exam <= 180:
            exam_anxiety = 50  # 半年内，中等焦虑
        else:
            exam_anxiety = 30  # 半年以上，焦虑较低
        
        stress_sources.append({
            'source': 'exam',
            'name': '考研倒计时焦虑',
            'score': exam_anxiety,
            'weight': 0.2
        })
    
    # 心理压力（权重：15%）
    if recent_mood_stress is not None:
        # 情绪压力等级 1-10 转换为 0-100
        mood_stress_level = (recent_mood_stress - 1) / 9 * 100
        stress_sources.append({
            'source': 'mood',
            'name': '心理情绪压力',
            'score': mood_stress_level,
            'weight': 0.15
        })
    
    # 2. 计算加权总分
    if not stress_sources:
        return {
            'total_score': 0,
            'main_sources': [],
            'analysis': '暂无压力数据',
            'suggestions': []
        }
    
    # 按分数排序，选择最高的 1-2 个
    stress_sources.sort(key=lambda x: x['score'], reverse=True)
    
    # 选择主要压力源（分数 > 30 的，最多 2 个）
    main_sources = []
    for source in stress_sources[:2]:
        if source['score'] > 30:
            main_sources.append(source)
    
    # 如果没有明显压力源，选择分数最高的一个
    if not main_sources and stress_sources:
        main_sources = [stress_sources[0]]
    
    return {
        'total_score': sum(s['score'] * s['weight'] for s in stress_sources),
        'main_sources': main_sources,
        'all_sources': stress_sources
    }


async def generate_stress_prescription_with_deepseek(
    stress_analysis: Dict,
    user_info: Optional[Dict] = None
) -> str:
    """
    使用 DeepSeek 生成压力处方
    
    参数:
        stress_analysis: 压力分析结果
        user_info: 用户信息（可选）
    
    返回:
        AI 生成的压力处方建议（流式）
    """
    if not settings.DEEPSEEK_API_KEY:
        return "DeepSeek API key 未配置，无法生成压力处方。"
    
    # 构建 prompt
    main_sources = stress_analysis.get('main_sources', [])
    total_score = stress_analysis.get('total_score', 0)
    
    if not main_sources:
        prompt = "用户目前压力较小，状态良好。请给出鼓励和保持建议。"
    else:
        source_desc = "、".join([s['name'] for s in main_sources])
        source_details = "\n".join([
            f"- {s['name']}: {s['score']:.1f}分"
            for s in main_sources
        ])
        
        prompt = f"""你是一位专业的考研心理辅导师。请根据以下压力分析数据，为学生生成一份简洁实用的压力处方。

【压力分析】
总体压力指数: {total_score:.1f}/100
主要压力来源: {source_desc}

详细数据:
{source_details}

【要求】
1. 简洁明了，控制在 200-300 字
2. 针对主要压力源给出具体可行的建议
3. 包含以下部分：
   - 压力诊断（1-2句话）
   - 具体建议（2-3条，带序号）
   - 鼓励的话（1句）
4. 语气温和、专业、鼓励
5. 避免说教，注重实用性

请生成压力处方："""
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{settings.DEEPSEEK_BASE_URL}/v1/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {
                            "role": "system",
                            "content": "你是一位专业、温和的考研心理辅导师，擅长分析学生压力并提供实用建议。"
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 500,
                    "stream": False
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"DeepSeek API 调用失败: {response.status_code}"
                
    except Exception as e:
        print(f"DeepSeek API 错误: {e}")
        return f"生成压力处方失败: {str(e)}"


async def generate_stress_prescription_stream(
    stress_analysis: Dict,
    user_info: Optional[Dict] = None
):
    """
    使用 DeepSeek 生成压力处方（流式输出）
    
    参数:
        stress_analysis: 压力分析结果
        user_info: 用户信息（可选）
    
    Yields:
        AI 生成的文本片段
    """
    if not settings.DEEPSEEK_API_KEY:
        yield "DeepSeek API key 未配置，无法生成压力处方。"
        return
    
    # 构建 prompt
    main_sources = stress_analysis.get('main_sources', [])
    total_score = stress_analysis.get('total_score', 0)
    
    if not main_sources:
        prompt = "用户目前压力较小，状态良好。请给出鼓励和保持建议。"
    else:
        source_desc = "、".join([s['name'] for s in main_sources])
        source_details = "\n".join([
            f"- {s['name']}: {s['score']:.1f}分"
            for s in main_sources
        ])
        
        prompt = f"""你是一位专业的考研心理辅导师。请根据以下压力分析数据，为学生生成一份简洁实用的压力处方。

【压力分析】
总体压力指数: {total_score:.1f}/100
主要压力来源: {source_desc}

详细数据:
{source_details}

【要求】
1. 简洁明了，控制在 200-300 字
2. 针对主要压力源给出具体可行的建议
3. 包含以下部分：
   - 压力诊断（1-2句话）
   - 具体建议（2-3条，带序号）
   - 鼓励的话（1句）
4. 语气温和、专业、鼓励
5. 避免说教，注重实用性

请生成压力处方："""
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream(
                "POST",
                f"{settings.DEEPSEEK_BASE_URL}/v1/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {
                            "role": "system",
                            "content": "你是一位专业、温和的考研心理辅导师，擅长分析学生压力并提供实用建议。"
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 500,
                    "stream": True
                }
            ) as response:
                if response.status_code != 200:
                    yield f"DeepSeek API 调用失败: {response.status_code}"
                    return
                
                import json
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:]  # 移除 "data: " 前缀
                        if data_str.strip() == "[DONE]":
                            break
                        try:
                            data = json.loads(data_str)
                            if 'choices' in data and len(data['choices']) > 0:
                                delta = data['choices'][0].get('delta', {})
                                content = delta.get('content', '')
                                if content:
                                    yield content
                        except json.JSONDecodeError:
                            continue
                            
    except Exception as e:
        print(f"DeepSeek API 流式错误: {e}")
        yield f"\n\n生成压力处方时出错: {str(e)}"
