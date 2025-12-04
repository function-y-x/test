from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.sqlite_database import connect_to_sqlite, close_sqlite_connection, create_tables
from app.routers import sqlite_auth as auth, users, moods, tasks, ai, errors, reports, paintings, messengers, emotional_aid

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:8081", "http://localhost:8082", "http://localhost:3000"],  # 添加8082端口
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # 创建数据库表
    await create_tables()
    await connect_to_sqlite()

@app.on_event("shutdown")
async def shutdown_event():
    await close_sqlite_connection()

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(moods.router, prefix="/api/v1/moods", tags=["moods"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks"])
app.include_router(ai.router, prefix="/api/v1/ai", tags=["ai"])
app.include_router(errors.router, prefix="/api/v1/errors", tags=["errors"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["reports"])
app.include_router(paintings.router, prefix="/api/v1/paintings", tags=["paintings"])
app.include_router(messengers.router, prefix="/api/v1/messengers", tags=["messengers"])
app.include_router(emotional_aid.router, prefix="/api/v1", tags=["emotional-aid"])

@app.get("/", tags=["root"])
async def read_root():
    return {"message": "Welcome to KaoYan MindCoach API"}

