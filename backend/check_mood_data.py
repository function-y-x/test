"""
检查和添加测试情绪数据的脚本
用于排查压力雷达"暂无数据"的问题
"""

import asyncio
import sys
from datetime import datetime, timedelta
from sqlalchemy import select
from app.db.sqlite_database import AsyncSessionLocal, engine, Base
from app.models.mood import MoodEntry
from app.models.sqlite_user import User

async def check_mood_data():
    """检查数据库中的情绪记录"""
    async with AsyncSessionLocal() as session:
        # 检查用户
        result = await session.execute(select(User))
        users = result.scalars().all()
        
        print("=" * 60)
        print("📊 数据库情绪记录检查")
        print("=" * 60)
        print(f"\n✅ 用户总数: {len(users)}")
        
        if not users:
            print("❌ 错误：数据库中没有用户！请先注册账号。")
            return
        
        for user in users:
            print(f"\n👤 用户: {user.username} ({user.email})")
            
            # 查询该用户的所有情绪记录
            result = await session.execute(
                select(MoodEntry)
                .where(MoodEntry.user_id == user.id)
                .order_by(MoodEntry.created_at.desc())
            )
            moods = result.scalars().all()
            
            print(f"   情绪记录总数: {len(moods)}")
            
            # 查询近7天的记录
            one_week_ago = datetime.utcnow() - timedelta(days=7)
            result = await session.execute(
                select(MoodEntry)
                .where(
                    MoodEntry.user_id == user.id,
                    MoodEntry.created_at >= one_week_ago
                )
                .order_by(MoodEntry.created_at.desc())
            )
            recent_moods = result.scalars().all()
            
            print(f"   近7天记录数: {len(recent_moods)}")
            
            if recent_moods:
                print("\n   📅 近7天的情绪记录:")
                for mood in recent_moods:
                    print(f"      - {mood.created_at.strftime('%Y-%m-%d %H:%M')} | "
                          f"心情: {mood.mood} | 压力: {mood.stress_level}/10")
            else:
                print("   ⚠️  近7天没有情绪记录")
        
        print("\n" + "=" * 60)

async def add_test_data():
    """为当前用户添加测试数据"""
    async with AsyncSessionLocal() as session:
        # 获取第一个用户
        result = await session.execute(select(User))
        user = result.scalar_one_or_none()
        
        if not user:
            print("❌ 错误：数据库中没有用户！请先注册账号。")
            return
        
        print(f"\n🔄 为用户 {user.username} 添加测试数据...\n")
        
        # 添加近7天的测试数据
        test_moods = [
            {'days_ago': 6, 'mood': 'anxious', 'stress': 8},
            {'days_ago': 5, 'mood': 'stressed', 'stress': 7},
            {'days_ago': 4, 'mood': 'tired', 'stress': 6},
            {'days_ago': 3, 'mood': 'calm', 'stress': 4},
            {'days_ago': 2, 'mood': 'happy', 'stress': 3},
            {'days_ago': 1, 'mood': 'excited', 'stress': 2},
            {'days_ago': 0, 'mood': 'calm', 'stress': 4},
        ]
        
        for item in test_moods:
            created_time = datetime.utcnow() - timedelta(days=item['days_ago'])
            mood_entry = MoodEntry(
                user_id=user.id,
                mood=item['mood'],
                stress_level=item['stress'],
                notes=f"测试数据 - {item['days_ago']}天前",
                created_at=created_time
            )
            session.add(mood_entry)
            print(f"✅ 添加: {created_time.strftime('%Y-%m-%d')} | {item['mood']} | 压力{item['stress']}")
        
        await session.commit()
        print("\n✅ 测试数据添加完成！")
        print("💡 现在可以刷新压力雷达页面查看效果了。\n")

async def main():
    print("\n" + "=" * 60)
    print("🔧 情绪数据检查工具")
    print("=" * 60)
    print("\n选项:")
    print("1. 检查现有数据")
    print("2. 添加测试数据（近7天）")
    print("3. 检查并添加（推荐）")
    print("\n" + "=" * 60)
    
    choice = input("\n请选择操作 (1/2/3): ").strip()
    
    if choice == '1':
        await check_mood_data()
    elif choice == '2':
        await add_test_data()
        await check_mood_data()
    elif choice == '3':
        await check_mood_data()
        print("\n" + "=" * 60)
        add = input("\n是否添加测试数据？(y/n): ").strip().lower()
        if add == 'y':
            await add_test_data()
    else:
        print("❌ 无效选项")

if __name__ == "__main__":
    asyncio.run(main())

