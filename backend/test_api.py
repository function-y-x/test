"""
API测试脚本
用于测试需要认证的API端点
"""

import requests
import json

# 配置
BASE_URL = "http://localhost:8000/api/v1"
EMAIL = "3099473107@qq.com"  # 修改为您的邮箱
PASSWORD = "Cyx20041120"     # 修改为您的密码

def login():
    """登录并获取token"""
    print("🔐 正在登录...")
    
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={
            "username": EMAIL,
            "password": PASSWORD
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        token = data.get("access_token")
        print(f"✅ 登录成功！")
        print(f"📝 Token: {token[:50]}...")
        return token
    else:
        print(f"❌ 登录失败: {response.status_code}")
        print(f"错误信息: {response.text}")
        return None

def test_weekly_scores(token):
    """测试weekly-scores端点"""
    print("\n📊 测试 /moods/weekly-scores 端点...")
    
    response = requests.get(
        f"{BASE_URL}/moods/weekly-scores",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ 请求成功！")
        print(f"\n返回数据:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        if data.get('success'):
            scores = data.get('data', [])
            print(f"\n📈 近7天心情得分:")
            for item in scores:
                print(f"  {item['weekday']} ({item['date']}): {item['score']} 分 ({item['count']}条记录)")
    else:
        print(f"❌ 请求失败: {response.status_code}")
        print(f"错误信息: {response.text}")

def test_weekly_stats(token):
    """测试weekly-stats端点"""
    print("\n📊 测试 /moods/weekly-stats 端点...")
    
    response = requests.get(
        f"{BASE_URL}/moods/weekly-stats",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ 请求成功！")
        print(f"\n返回数据:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(f"❌ 请求失败: {response.status_code}")
        print(f"错误信息: {response.text}")

def main():
    print("=" * 60)
    print("🧪 API 测试工具")
    print("=" * 60)
    
    # 1. 登录
    token = login()
    
    if not token:
        print("\n❌ 无法获取token，测试终止")
        return
    
    # 2. 测试API
    test_weekly_scores(token)
    test_weekly_stats(token)
    
    print("\n" + "=" * 60)
    print("✅ 测试完成！")
    print("=" * 60)

if __name__ == "__main__":
    # 检查是否安装了requests
    try:
        import requests
    except ImportError:
        print("❌ 请先安装 requests 库:")
        print("pip install requests")
        exit(1)
    
    main()

