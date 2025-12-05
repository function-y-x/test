from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict

class UserInDB(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )
    
    id: Optional[str] = Field(alias="_id")
    username: str
    email: str
    hashed_password: str
    exam_date: Optional[datetime] = None
    selected_subjects: Optional[List[str]] = []
    ai_companion_style: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

