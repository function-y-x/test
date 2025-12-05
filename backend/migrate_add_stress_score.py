"""
数据库迁移脚本：添加 DDL 紧张分数相关字段

功能：
  为 calendar_notes 表添加以下字段：
    - ddl_date (DATE)      : DDL 截止日期
    - stress_score (INTEGER): 紧张分数 (0-100)

运行方式：
  python backend/migrate_add_stress_score.py

适用场景：
  - 从旧版本升级到新版本
  - 已有数据库需要添加新字段
  - 从其他开发者处获取代码后需要更新数据库

注意：
  - 新用户（全新数据库）不需要运行此脚本
  - 建议先备份数据库文件
  - 确保后端服务已停止
"""

import sqlite3
import sys
from pathlib import Path
from datetime import datetime

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def migrate_database():
    """执行数据库迁移"""
    # 尝试多个可能的数据库位置
    possible_paths = [
        project_root / "kaoyan_mindcoach.db",
        project_root / "backend" / "kaoyan_mindcoach.db"
    ]
    
    db_path = None
    for path in possible_paths:
        if path.exists():
            db_path = path
            break
    
    if db_path is None:
        print("未找到数据库文件，尝试过以下位置：")
        for path in possible_paths:
            print(f"  - {path}")
        print("\n如果这是首次运行，请先启动后端服务创建数据库")
        return False
    
    print(f"连接到数据库: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 检查是否已经存在这些字段
        cursor.execute("PRAGMA table_info(calendar_notes)")
        columns = [row[1] for row in cursor.fetchall()]
        
        print(f"当前 calendar_notes 表的字段: {columns}")
        
        # 添加 ddl_date 字段
        if 'ddl_date' not in columns:
            print("添加 ddl_date 字段...")
            cursor.execute("""
                ALTER TABLE calendar_notes 
                ADD COLUMN ddl_date DATE
            """)
            print("✓ ddl_date 字段添加成功")
        else:
            print("✓ ddl_date 字段已存在")
        
        # 添加 stress_score 字段
        if 'stress_score' not in columns:
            print("添加 stress_score 字段...")
            cursor.execute("""
                ALTER TABLE calendar_notes 
                ADD COLUMN stress_score INTEGER NOT NULL DEFAULT 0
            """)
            print("✓ stress_score 字段添加成功")
        else:
            print("✓ stress_score 字段已存在")
        
        # 提交更改
        conn.commit()
        print("\n数据库迁移成功完成！")
        print("\n新增字段说明:")
        print("- ddl_date: DDL截止日期（可选）")
        print("- stress_score: 紧张分数（0-100，自动计算）")
        
        return True
        
    except sqlite3.Error as e:
        print(f"数据库迁移失败: {e}")
        conn.rollback()
        return False
        
    finally:
        cursor.close()
        conn.close()

def verify_migration():
    """验证迁移是否成功"""
    # 尝试多个可能的数据库位置
    possible_paths = [
        project_root / "kaoyan_mindcoach.db",
        project_root / "backend" / "kaoyan_mindcoach.db"
    ]
    
    db_path = None
    for path in possible_paths:
        if path.exists():
            db_path = path
            break
    
    if db_path is None:
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("PRAGMA table_info(calendar_notes)")
        columns = {row[1]: row[2] for row in cursor.fetchall()}
        
        print("\n验证迁移结果...")
        print("calendar_notes 表结构:")
        for col_name, col_type in columns.items():
            print(f"  - {col_name}: {col_type}")
        
        # 检查必需字段
        required_fields = ['ddl_date', 'stress_score']
        missing_fields = [f for f in required_fields if f not in columns]
        
        if missing_fields:
            print(f"\n⚠ 警告：缺少字段 {missing_fields}")
            return False
        else:
            print("\n✓ 所有必需字段都存在")
            return True
            
    finally:
        cursor.close()
        conn.close()

def print_usage_info():
    """打印使用说明"""
    print()
    print("=" * 70)
    print("  数据库迁移 - DDL 紧张分数功能")
    print("=" * 70)
    print()
    print("此脚本将为 calendar_notes 表添加以下字段：")
    print("  • ddl_date      (DATE)    - DDL 截止日期")
    print("  • stress_score  (INTEGER) - 紧张分数 (0-100)")
    print()
    print("重要提示：")
    print("  ✓ 新用户（全新数据库）不需要运行此脚本")
    print("  ✓ 建议先备份数据库文件")
    print("  ✓ 确保后端服务已停止")
    print()
    print("=" * 70)
    print()

def create_backup():
    """创建数据库备份"""
    possible_paths = [
        project_root / "kaoyan_mindcoach.db",
        project_root / "backend" / "kaoyan_mindcoach.db"
    ]
    
    for db_path in possible_paths:
        if db_path.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = db_path.parent / f"{db_path.stem}_backup_{timestamp}{db_path.suffix}"
            
            try:
                import shutil
                shutil.copy2(db_path, backup_path)
                print(f"✓ 已创建备份: {backup_path.name}")
                return True
            except Exception as e:
                print(f"⚠ 备份失败: {e}")
                return False
    
    return False

if __name__ == "__main__":
    print_usage_info()
    
    # 询问是否继续
    response = input("是否继续迁移？(y/n): ").strip().lower()
    if response not in ['y', 'yes', '是']:
        print("已取消迁移。")
        sys.exit(0)
    
    print()
    print("开始迁移...")
    print()
    
    # 创建备份
    print("正在创建数据库备份...")
    create_backup()
    print()
    
    # 执行迁移
    success = migrate_database()
    
    if success:
        print()
        if verify_migration():
            print()
            print("=" * 70)
            print("✓ 迁移成功完成！")
            print()
            print("下一步：")
            print("  1. 启动后端服务: cd backend && python run_server.py")
            print("  2. 访问 http://localhost:8000/docs 验证 API")
            print("  3. 登录系统测试紧张分数功能")
            print("=" * 70)
        else:
            print()
            print("=" * 70)
            print("⚠ 迁移可能未完全成功，请检查上述信息。")
            print("=" * 70)
            sys.exit(1)
    else:
        print()
        print("=" * 70)
        print("✗ 迁移失败！")
        print()
        print("可能的原因：")
        print("  1. 数据库文件不存在（需要先启动一次后端）")
        print("  2. 数据库被占用（请关闭后端服务）")
        print("  3. 权限不足")
        print()
        print("解决方案：")
        print("  • 查看上述错误信息")
        print("  • 阅读 README-部署说明.md")
        print("  • 查看 backend/数据库迁移说明.txt")
        print("=" * 70)
        sys.exit(1)
