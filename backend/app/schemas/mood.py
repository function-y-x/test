from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class MoodCreate(BaseModel):
    mood: str = Field(..., description="心情状态：happy, calm, anxious, stressed, sad, excited, tired, focused")
    stress_level: int = Field(..., ge=1, le=10, description="压力等级 1-10")
    notes: Optional[str] = Field(None, description="可选的备注")

class MoodOut(BaseModel):
    id: int
    user_id: int
    mood: str
    stress_level: int
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

