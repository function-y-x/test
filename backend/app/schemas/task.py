from typing import Optional
from datetime import datetime, date
from pydantic import BaseModel, Field, ConfigDict

class TaskCreate(BaseModel):
    text: str = Field(..., description="任务文本内容")
    task_date: Optional[date] = Field(None, description="任务日期，默认为今天")

class TaskUpdate(BaseModel):
    text: Optional[str] = None
    completed: Optional[bool] = None

class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    text: str
    completed: bool
    task_date: date
    created_at: datetime
    updated_at: datetime

