from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    exam_date: Optional[datetime] = None
    selected_subjects: Optional[List[str]] = None
    ai_companion_style: Optional[str] = None

class UserOut(UserBase):
    id: str
    exam_date: Optional[datetime] = None
    selected_subjects: Optional[List[str]] = []
    ai_companion_style: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

