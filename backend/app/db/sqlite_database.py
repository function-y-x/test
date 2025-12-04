import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

# SQLite数据库URL
DATABASE_URL = "sqlite+aiosqlite:///./kaoyan_mindcoach.db"

# 创建异步引擎
engine = create_async_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

Base = declarative_base()

async def connect_to_sqlite():
    print("SQLite connection ready!")

async def close_sqlite_connection():
    await engine.dispose()
    print("Disconnected from SQLite!")

async def get_database():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def create_tables():
    """创建所有表"""
    # 只导入SQLAlchemy模型以确保表被创建
    try:
        from app.models.sqlite_user import User
        from app.models.messenger import MessengerEntry  
        from app.models.mood import MoodEntry
        from app.models.task import TaskEntry
        # 注意：以下是 Pydantic 模型，不是 SQLAlchemy 模型，所以不需要导入
        # - app.models.painting.PaintingEntry
        # - app.models.report.WeeklyReport  
        # - app.models.error.ErrorEntry
        print("成功导入所有SQLAlchemy模型")
    except ImportError as e:
        print(f"导入模型时出错: {e}")
        # 即使导入失败，也要创建基础表结构
        pass
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)