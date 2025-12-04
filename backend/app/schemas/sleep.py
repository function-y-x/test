from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SleepCreate(BaseModel):
    sleep_hours: float  # 睡眠时长（小时）

class SleepOut(BaseModel):
    id: int
    user_id: int
    sleep_hours: float
    sleep_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True
        orm_mode = True

