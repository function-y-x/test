import asyncio
import sys
import os
import time

# 添加项目路径
sys.path.append('e:/pythondownload/pythonProject1/kaoyan-mindcoach/backend')

# 设置环境变量
os.environ['OPENAI_API_KEY'] = 'sk-ac5ae6e934f54368b1a0339a79ec24cf'
os.environ['OPENAI_API_BASE'] = 'https://dashscope.aliyuncs.com/compatible-mode/v1'

from openai import OpenAI

async def test_openai_connection():
    print("🔧 OpenAI连接测试开始...")
    
    # 创建客户端
    client = OpenAI(
        api_key=os.environ['OPENAI_API_KEY'],
        base_url=os.environ['OPENAI_API_BASE']
    )
    
    print(f"✅ 客户端创建成功")
    print(f"✅ API Key: {os.environ['OPENAI_API_KEY'][:10]}...")
    print(f"✅ Base URL: {os.environ['OPENAI_API_BASE']}")
    
    try:
        print("🚀 开始测试简单API调用...")
        start_time = time.time()
        
        response = client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {"role": "system", "content": "你是一个测试助手，请简短回复。"},
                {"role": "user", "content": "请回复：测试成功"}
            ],
            max_tokens=20,
            timeout=1000
        )
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        print(f"🎉 API调用成功! 耗时: {elapsed:.2f}秒")
        print(f"🎉 模型响应: {response.choices[0].message.content}")
        print(f"🎉 使用token: {response.usage.total_tokens if hasattr(response, 'usage') else '未知'}")
        
        return True
        
    except Exception as e:
        print(f"❌ API调用失败: {type(e).__name__}: {str(e)}")
        
        # 详细错误分析
        error_str = str(e).lower()
        if "timeout" in error_str:
            print("⏰ 错误类型: 超时 - 网络或服务器响应慢")
        elif "401" in error_str or "unauthorized" in error_str:
            print("🔐 错误类型: 认证失败 - API Key可能无效")
        elif "403" in error_str or "forbidden" in error_str:
            print("🚫 错误类型: 权限不足 - API Key可能没有权限")
        elif "404" in error_str:
            print("🔍 错误类型: 资源未找到 - API地址或模型可能错误")
        elif "429" in error_str:
            print("⚡ 错误类型: 请求过于频繁 - 需要降低请求频率")
        elif "500" in error_str:
            print("🔧 错误类型: 服务器内部错误 - API服务器问题")
        else:
            print("❓ 错误类型: 未知错误")
            
        return False

async def test_ai_services():
    print("\n" + "="*50)
    print("🧠 AI服务集成测试")
    print("="*50)
    
    # 先测试基础连接
    connection_ok = await test_openai_connection()
    
    if not connection_ok:
        print("❌ 基础连接失败，跳过AI服务测试")
        return
    
    print("\n🔥 测试AI服务功能...")
    
    # 导入AI服务
    from app.services.ai import generate_emergency_guidance, generate_scenario_simulation
    
    # 测试情绪急救
    print("\n🚨 测试情绪急救...")
    try:
        result = await generate_emergency_guidance("焦虑", 7.5)
        print(f"✅ 情绪急救测试完成")
    except Exception as e:
        print(f"❌ 情绪急救测试失败: {e}")
    
    # 测试场景模拟 
    print("\n🎭 测试场景模拟...")
    try:
        result = await generate_scenario_simulation("exam", "担心考试发挥失常")
        print(f"✅ 场景模拟测试完成")
    except Exception as e:
        print(f"❌ 场景模拟测试失败: {e}")

if __name__ == "__main__":
    asyncio.run(test_ai_services())