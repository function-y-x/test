from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.services.ai import generate_emergency_guidance, generate_scenario_simulation
from typing import Optional

router = APIRouter(prefix="/emotional-aid", tags=["Emotional Aid"])


class EmergencyRequest(BaseModel):
    emotion_state: str  # 情绪状态：焦虑、愤怒、悲伤等
    intensity: float  # 强度 0-10


class ScenarioRequest(BaseModel):
    scenario_type: str  # 场景类型：exam、interview、study
    user_concerns: str  # 用户担忧


class BreathingExerciseRequest(BaseModel):
    duration: Optional[int] = 180  # 默认3分钟
    style: Optional[str] = "478"  # 4-7-8呼吸法


@router.post("/emergency-guidance")
async def get_emergency_guidance(request: EmergencyRequest):
    """获取90秒情绪急救指导"""
    try:
        guidance = await generate_emergency_guidance(
            emotion_state=request.emotion_state,
            intensity=request.intensity
        )
        return {
            "success": True,
            "data": guidance
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成急救指导失败: {str(e)}")


@router.post("/scenario-simulation")
async def get_scenario_simulation(request: ScenarioRequest):
    """获取场景模拟指导"""
    try:
        simulation = await generate_scenario_simulation(
            scenario_type=request.scenario_type,
            user_concerns=request.user_concerns
        )
        return {
            "success": True,
            "data": simulation
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成场景模拟失败: {str(e)}")


@router.post("/breathing-exercise")
async def get_breathing_exercise(request: BreathingExerciseRequest):
    """获取呼吸练习配置"""
    try:
        if request.style == "478":
            pattern = {
                "inhale": 4,
                "hold": 7, 
                "exhale": 8,
                "cycles": request.duration // 19  # 每个周期约19秒
            }
        elif request.style == "box":
            pattern = {
                "inhale": 4,
                "hold": 4,
                "exhale": 4,
                "hold2": 4,
                "cycles": request.duration // 16  # 每个周期16秒
            }
        else:
            pattern = {
                "inhale": 4,
                "hold": 4,
                "exhale": 6,
                "cycles": request.duration // 14  # 每个周期14秒
            }
        
        return {
            "success": True,
            "data": {
                "pattern": pattern,
                "duration": request.duration,
                "guidance_text": "跟随引导，专注于呼吸。吸气时感受腹部缓慢上升，呼气时让身体完全放松。",
                "background_music": "nature_sounds"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成呼吸练习失败: {str(e)}")


@router.get("/micro-review")
async def get_micro_review():
    """获取微回顾练习"""
    try:
        prompts = [
            "回想今天最让你感到满足的一个小瞬间",
            "想一想今天你为哪件事感到骄傲",
            "回忆今天遇到的一个善意举动",
            "思考今天学到的一个新知识或技能",
            "回想今天克服的一个小困难",
            "想想今天感受到的一次温暖"
        ]
        
        import random
        selected_prompt = random.choice(prompts)
        
        return {
            "success": True,
            "data": {
                "prompt": selected_prompt,
                "guidance": "花1-2分钟静静思考这个问题，让积极的记忆在心中展开。",
                "duration": 120,
                "background": "soft_light"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成微回顾失败: {str(e)}")
