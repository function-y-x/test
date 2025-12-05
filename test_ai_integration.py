import asyncio
import sys
import os

# 添加项目路径
sys.path.append('e:/pythondownload/pythonProject1/kaoyan-mindcoach/backend')

# 设置环境变量
os.environ['OPENAI_API_KEY'] = 'sk-ac5ae6e934f54368b1a0339a79ec24cf'
os.environ['OPENAI_API_BASE'] = 'https://dashscope.aliyuncs.com/compatible-mode/v1'

from app.services.ai import generate_emergency_guidance, generate_scenario_simulation
from app.core.config import settings

async def test_ai_functions():
    print("🔧 测试AI配置:")
    print(f"✅ API Key存在: {bool(settings.OPENAI_API_KEY)}")
    print(f"✅ Base URL: {settings.OPENAI_BASE_URL}")
    print()
    
    print("🚨 测试情绪急救功能:")
    try:
        guidance = await generate_emergency_guidance("焦虑", 7.5)
        print("✅ 情绪急救API调用成功!")
        print(f"语音脚本: {guidance['voice_script'][:50]}...")
        print(f"视觉提示: {guidance['visual_prompt'][:50]}...")
        print(f"音乐类型: {guidance['music_type']}")
        print(f"持续时间: {guidance['duration']}秒")
        print()
    except Exception as e:
        print(f"❌ 情绪急救API调用失败: {str(e)}")
        print()
    
    print("🎭 测试场景模拟功能:")
    try:
        simulation = await generate_scenario_simulation("exam", "担心考试发挥失常")
        print("✅ 场景模拟API调用成功!")
        print(f"准备步骤: {simulation.get('preparation_steps', ['未获取'])}")
        print(f"心态指导: {simulation['mindset_guidance'][:50]}...")
        print(f"可视化脚本: {simulation['visualization_script'][:50]}...")
        print()
    except Exception as e:
        print(f"❌ 场景模拟API调用失败: {str(e)}")
        print()

if __name__ == "__main__":
    asyncio.run(test_ai_functions())