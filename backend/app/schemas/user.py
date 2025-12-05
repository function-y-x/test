from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

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
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    exam_date: Optional[datetime] = None
    selected_subjects: Optional[List[str]] = []
    ai_companion_style: Optional[str] = None
    created_at: datetime

