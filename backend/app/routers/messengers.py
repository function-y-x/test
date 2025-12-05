import os
import base64
import asyncio
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.models.user import UserInDB
from app.models.messenger import MessengerEntry, EmotionReport, AIReply
from app.schemas.messenger import MessengerCreate, MessengerOut, EmotionAnalysisResponse, MessageHistoryResponse
from app.services.auth import get_current_active_user
from app.db.sqlite_database import get_database
from app.services.messenger_ai import messenger_ai_service
from app.services.crisis_intervention import crisis_intervention_service
import json
from datetime import datetime

router = APIRouter()

@router.post("/send-message", response_model=EmotionAnalysisResponse)
async def send_message(
    message_type: str = Form(...),
    text_content: str = Form(None),
    anonymous_mode: bool = Form(False),
    audio_file: UploadFile = File(None),
    image_file: UploadFile = File(None),
    current_user: Annotated[UserInDB, Depends(get_current_active_user)] = None,
    db: AsyncSession = Depends(get_database)
):
    """发送多模态消息并获取AI分析回复"""
    try:
        # 处理匿名模式
        user_id = "anonymous" if anonymous_mode else str(current_user.id)
        
        # 保存上传的文件
        audio_path = None
        image_path = None
        
        if audio_file:
            audio_path = await save_uploaded_file(audio_file, "audio")
        
        if image_file:
            image_path = await save_uploaded_file(image_file, "image")
        
        # 创建消息记录
        message_entry = MessengerEntry(
            user_id=user_id,
            message_type=message_type,
            text_content=text_content,
            audio_path=audio_path,
            image_path=image_path,
            sender="user",
            created_at=datetime.utcnow()
        )
        
        db.add(message_entry)
        await db.flush()  # 获取ID
        
        # AI情绪分析
        audio_features = None
        image_analysis = None
        
        if audio_path:
            # 这里应该分析音频特征（语速、音调等）
            audio_features = {"speed": "正常", "pitch": "中等", "volume": "中等"}
        
        if image_path:
            # 这里应该分析图像内容
            image_analysis = {"description": "用户上传的图片"}
        
        emotion_report = await messenger_ai_service.analyze_emotion(
            text_content or "", audio_features, image_analysis
        )
        
        # 危机评估
        risk_level = crisis_intervention_service.assess_risk_level(
            text_content or "", emotion_report.dict()
        )
        
        # 获取危机干预资源
        crisis_resources = crisis_intervention_service.get_crisis_resources(risk_level)
        
        # 生成AI回复（包含危机干预信息）
        ai_reply = await messenger_ai_service.generate_ai_reply(emotion_report, text_content or "")
        
        # 如果是高风险，添加立即响应
        if risk_level == "red":
            immediate_response = crisis_intervention_service.get_immediate_response(risk_level)
            ai_reply.empathy_text = immediate_response + "\n\n" + ai_reply.empathy_text
            ai_reply.resource_links.extend([
                resource["name"] + ": " + resource["phone"] 
                for resource in crisis_resources["resources"]["hotlines"]
            ])
        elif risk_level == "yellow":
            ai_reply.resource_links.extend([
                resource["name"] 
                for resource in crisis_resources["resources"]["online_resources"]
            ])
        
        # 生成视频回复
        video_content = await messenger_ai_service.generate_video_reply(ai_reply)
        
        # 更新消息记录
        message_entry.emotion_report = emotion_report.dict()
        message_entry.risk_level = risk_level
        message_entry.ai_reply_text = video_content
        
        # 创建AI回复消息
        ai_message = MessengerEntry(
            user_id=user_id,
            message_type="text",
            text_content=video_content,
            sender="ai",
            created_at=datetime.utcnow()
        )
        
        db.add(ai_message)
        await db.commit()
        
        return EmotionAnalysisResponse(
            message_id=message_entry.id,
            emotion_report=emotion_report.dict(),
            risk_level=risk_level,
            ai_reply=ai_reply.dict(),
            video_url=None,  # 暂时返回None，实际应用中返回视频URL
            crisis_resources=crisis_resources if risk_level in ["red", "yellow"] else None
        )
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"处理消息失败: {str(e)}")

@router.get("/history", response_model=MessageHistoryResponse)
async def get_message_history(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_database),
    limit: int = 50,
    offset: int = 0
):
    """获取用户消息历史"""
    try:
        # 查询用户消息
        stmt = select(MessengerEntry).where(
            MessengerEntry.user_id == str(current_user.id)
        ).order_by(MessengerEntry.created_at.desc()).limit(limit).offset(offset)
        
        result = await db.execute(stmt)
        messages = result.scalars().all()
        
        # 查询总数
        count_stmt = select(MessengerEntry).where(MessengerEntry.user_id == str(current_user.id))
        count_result = await db.execute(count_stmt)
        total_count = len(count_result.scalars().all())
        
        # 生成情绪时间线
        emotion_timeline = []
        for msg in messages:
            if msg.emotion_report and msg.sender == "user":
                emotion_timeline.append({
                    "date": msg.created_at.isoformat(),
                    "stress_index": msg.emotion_report.get("stress_index", 0),
                    "main_emotions": msg.emotion_report.get("main_emotions", []),
                    "risk_level": msg.risk_level
                })
        
        return MessageHistoryResponse(
            messages=[MessengerOut.from_orm(msg) for msg in messages],
            total_count=total_count,
            emotion_timeline=emotion_timeline
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取历史消息失败: {str(e)}")

@router.get("/message/{message_id}", response_model=MessengerOut)
async def get_message_by_id(
    message_id: int,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_database)
):
    """根据ID获取消息详情"""
    try:
        stmt = select(MessengerEntry).where(
            and_(
                MessengerEntry.id == message_id,
                MessengerEntry.user_id == str(current_user.id)
            )
        )
        result = await db.execute(stmt)
        message = result.scalar_one_or_none()
        
        if not message:
            raise HTTPException(status_code=404, detail="消息不存在")
        
        return MessengerOut.from_orm(message)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取消息失败: {str(e)}")

@router.delete("/message/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(
    message_id: int,
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_database)
):
    """删除消息"""
    try:
        stmt = select(MessengerEntry).where(
            and_(
                MessengerEntry.id == message_id,
                MessengerEntry.user_id == str(current_user.id)
            )
        )
        result = await db.execute(stmt)
        message = result.scalar_one_or_none()
        
        if not message:
            raise HTTPException(status_code=404, detail="消息不存在")
        
        await db.delete(message)
        await db.commit()
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"删除消息失败: {str(e)}")

@router.get("/emotion-stats")
async def get_emotion_statistics(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    db: AsyncSession = Depends(get_database),
    days: int = 30
):
    """获取情绪统计数据"""
    try:
        # 查询最近的用户消息
        stmt = select(MessengerEntry).where(
            and_(
                MessengerEntry.user_id == str(current_user.id),
                MessengerEntry.sender == "user",
                MessengerEntry.emotion_report.isnot(None)
            )
        ).order_by(MessengerEntry.created_at.desc()).limit(days)
        
        result = await db.execute(stmt)
        messages = result.scalars().all()
        
        if not messages:
            return {"message": "暂无情绪数据"}
        
        # 统计数据
        stress_levels = []
        emotion_counts = {}
        risk_levels = {"green": 0, "yellow": 0, "red": 0}
        
        for msg in messages:
            report = msg.emotion_report
            if report:
                stress_levels.append(report.get("stress_index", 0))
                
                for emotion in report.get("main_emotions", []):
                    emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
                
                risk_level = msg.risk_level or "green"
                risk_levels[risk_level] += 1
        
        avg_stress = sum(stress_levels) / len(stress_levels) if stress_levels else 0
        
        return {
            "average_stress_index": round(avg_stress, 2),
            "stress_trend": stress_levels[-7:] if len(stress_levels) >= 7 else stress_levels,
            "emotion_distribution": emotion_counts,
            "risk_distribution": risk_levels,
            "total_messages": len(messages)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计数据失败: {str(e)}")

async def save_uploaded_file(file: UploadFile, file_type: str) -> str:
    """保存上传的文件"""
    try:
        # 创建上传目录
        upload_dir = f"uploads/{file_type}"
        os.makedirs(upload_dir, exist_ok=True)
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(upload_dir, filename)
        
        # 保存文件
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        return file_path
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件保存失败: {str(e)}")

def determine_risk_level(emotion_report: EmotionReport) -> str:
    """确定风险等级"""
    if emotion_report.risk_keywords:
        return "red"
    elif emotion_report.stress_index > 70:
        return "yellow"
    else:
        return "green"

