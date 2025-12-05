"""
检查压力处方功能配置
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("=" * 60)
print("压力处方功能配置检查")
print("=" * 60)
print()

# 1. 检查 .env 文件
print("1. 检查 .env 文件...")
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    print(f"   [OK] .env 文件存在: {env_path}")
else:
    print(f"   [ERROR] .env 文件不存在！")
    print(f"   请在 backend 目录创建 .env 文件")
    print()

# 2. 检查配置
print("\n2. 检查配置...")
try:
    from app.core.config import settings
    
    if settings.DEEPSEEK_API_KEY:
        print(f"   [OK] DEEPSEEK_API_KEY 已配置")
        print(f"        Key 开头: {settings.DEEPSEEK_API_KEY[:10]}...")
    else:
        print(f"   [ERROR] DEEPSEEK_API_KEY 未配置！")
        print(f"   请在 .env 文件中添加: DEEPSEEK_API_KEY=sk-your-key")
    
    if settings.DEEPSEEK_BASE_URL:
        print(f"   [OK] DEEPSEEK_BASE_URL: {settings.DEEPSEEK_BASE_URL}")
    else:
        print(f"   [WARNING] DEEPSEEK_BASE_URL 未配置，使用默认值")
        
except Exception as e:
    print(f"   [ERROR] 加载配置失败: {e}")

# 3. 检查依赖
print("\n3. 检查依赖...")
try:
    import httpx
    print(f"   [OK] httpx 已安装 (版本: {httpx.__version__})")
except ImportError:
    print(f"   [ERROR] httpx 未安装！")
    print(f"   请运行: pip install httpx")

try:
    from app.services.stress_analysis import analyze_stress_sources
    print(f"   [OK] stress_analysis 模块可导入")
except Exception as e:
    print(f"   [ERROR] 导入 stress_analysis 失败: {e}")

try:
    from app.routers.stress_prescription import router
    print(f"   [OK] stress_prescription 路由可导入")
except Exception as e:
    print(f"   [ERROR] 导入 stress_prescription 失败: {e}")

# 4. 测试压力分析算法
print("\n4. 测试压力分析算法...")
try:
    import asyncio
    from app.services.stress_analysis import analyze_stress_sources
    
    async def test():
        result = await analyze_stress_sources(
            ddl_score=60.0,
            sleep_hours=6.5,
            days_until_exam=120,
            recent_mood_stress=5
        )
        return result
    
    result = asyncio.run(test())
    print(f"   [OK] 压力分析算法正常")
    print(f"        总体压力: {result['total_score']:.1f}/100")
    print(f"        主要压力源数量: {len(result['main_sources'])}")
    
except Exception as e:
    print(f"   [ERROR] 压力分析测试失败: {e}")

print("\n" + "=" * 60)
print("检查完成！")
print("=" * 60)
print()

# 5. 给出建议
print("💡 下一步:")
if not env_path.exists():
    print("   1. 在 backend 目录创建 .env 文件")
    print("   2. 参考 DeepSeek配置说明.md")
else:
    print("   1. 确保 .env 中有正确的 DEEPSEEK_API_KEY")
    print("   2. 重启后端: python run_server.py")
    print("   3. 在前端点击'一键生成压力处方'测试")
print()

